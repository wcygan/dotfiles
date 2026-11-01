"""Explicit installation of per-user platform schedulers for nightly updates."""

from __future__ import annotations

import json
import os
import plistlib
import subprocess
from pathlib import Path

from dotfiles_setup.links import nightly_files
from dotfiles_setup.manifest import OperationJournal, _atomic_json
from dotfiles_setup.mutations import FileMutation, execute_mutations
from dotfiles_setup.nightly import (
    NightlyError,
    directory,
    fingerprint,
    lock_hash,
    owned_backups,
    read_state,
)
from dotfiles_setup.nightly_state import (
    SchedulerEvent,
    SchedulerPhase,
    phase_of,
    transition_state,
)
from dotfiles_setup.paths import UserPathContext

LABEL = "com.wcygan.dotfiles.nightly"


def schedule_environment(context: UserPathContext) -> dict[str, str]:
    environment = {
        "HOME": str(context.home),
        "XDG_CONFIG_HOME": str(context.config_home),
        "XDG_STATE_HOME": str(context.state_home),
        "XDG_CACHE_HOME": str(context.cache_home),
        "CODEX_HOME": str(context.codex_home),
        "PATH": (
            f"{context.home}/.nix-profile/bin:/nix/var/nix/profiles/default/bin:"
            "/usr/bin:/bin:/usr/sbin:/sbin"
        ),
    }
    bundle = context.home / ".nix-profile/etc/ssl/certs/ca-bundle.crt"
    if bundle.is_file():
        environment.update(
            SSL_CERT_FILE=str(bundle),
            NIX_SSL_CERT_FILE=str(bundle),
            SSL_CERT_DIR=str(bundle.parent),
        )
    return environment


def schedule_contents(repo: Path, context: UserPathContext, *, enabled: bool) -> dict[Path, bytes]:
    repo = repo.resolve()
    files = nightly_files(repo, context)[:-1]
    args = ["/bin/bash", str(repo / "bootstrap.sh"), "nightly-run"]
    environment = schedule_environment(context)
    if context.platform.lower() == "darwin":
        return {
            files[0]: plistlib.dumps(
                {
                    "Label": LABEL,
                    "ProgramArguments": args,
                    "StartCalendarInterval": {"Hour": 3, "Minute": 0},
                    "Disabled": not enabled,
                    "EnvironmentVariables": environment,
                    "StandardOutPath": str(context.state_directory / "nightly/scheduler.log"),
                    "StandardErrorPath": str(
                        context.state_directory / "nightly/scheduler-error.log"
                    ),
                    "ProcessType": "Background",
                }
            )
        }
    if context.platform.lower() != "linux":
        raise ValueError("nightly scheduling supports macOS and systemd Linux only")
    if any(any(char in value for char in "\n\r\0") for value in [*args, *environment.values()]):
        raise ValueError("scheduler paths cannot contain control characters")
    # systemd's ExecStart parser differs from a shell; quote each argument explicitly.
    command = " ".join(
        '"'
        + arg.replace("$", "$$").replace("%", "%%").replace("\\", "\\\\").replace('"', '\\"')
        + '"'
        for arg in args
    )
    variables = "\n".join(
        'Environment="'
        + key
        + "="
        + value.replace("%", "%%").replace("\\", "\\\\").replace('"', '\\"')
        + '"'
        for key, value in environment.items()
    )
    service = (
        "[Unit]\nDescription=Nightly verified Nix updates\n\n[Service]\nType=oneshot\n"
        f"ExecStart={command}\n{variables}\n"
        "TimeoutStartSec=1h\nKillMode=control-group\n"
    )
    timer = (
        "[Unit]\nDescription=Check for Nix updates at 03:00 local time\n\n[Timer]\n"
        "OnCalendar=*-*-* 03:00:00\nPersistent=false\nWakeSystem=false\n"
        "AccuracySec=1min\nRandomizedDelaySec=0\n\n[Install]\nWantedBy=timers.target\n"
    )
    return {files[0]: service.encode(), files[1]: timer.encode()}


def configure(repo: Path, journal: OperationJournal, *, enabled: bool, environ=None) -> None:
    context = UserPathContext.from_environment(environ)
    root = context.state_directory / "nightly"
    repo = repo.resolve()
    if not repo.is_relative_to(context.home):
        raise ValueError("nightly checkout must be inside HOME")
    if not (context.home / ".nix-profile/bin/python3").is_file():
        raise ValueError("install the Nix profile before scheduling updates")
    state = read_state(root / "schedule.json")
    phase = phase_of(state)
    if phase is not SchedulerPhase.UNCONFIGURED and state.get("repository") != str(repo):
        if phase in {
            SchedulerPhase.REQUESTED,
            SchedulerPhase.ENABLED,
            SchedulerPhase.UNKNOWN,
        }:
            raise ValueError("another checkout owns the nightly schedule; disable it there first")
        state = {}
        phase = SchedulerPhase.UNCONFIGURED
    state = dict(state)
    state["repository"] = str(repo)
    event = SchedulerEvent.REQUEST_ENABLE if enabled else SchedulerEvent.REQUEST_DISABLE
    state = transition_state(state, event)
    _atomic_json(root / "schedule.json", state)
    contents = schedule_contents(repo, context, enabled=enabled)
    execute_mutations(
        tuple(
            FileMutation(
                destination=path,
                visible_destination=path,
                source="nightly-schedule",
                contents=body,
                mode=0o644,
            )
            for path, body in contents.items()
        ),
        journal=journal,
        authority_roots=(context.home,),
    )
    if context.platform.lower() == "darwin":
        service = f"gui/{os.getuid()}/{LABEL}"
        subprocess.run(["launchctl", "bootout", service], capture_output=True, check=False)
        if enabled:
            subprocess.run(["launchctl", "enable", service], check=True)
            subprocess.run(
                ["launchctl", "bootstrap", f"gui/{os.getuid()}", str(next(iter(contents)))],
                check=True,
            )
        else:
            subprocess.run(["launchctl", "disable", service], check=True)
    else:
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        action = "enable" if enabled else "disable"
        subprocess.run(
            ["systemctl", "--user", action, "--now", "dotfiles-nightly.timer"], check=True
        )
    from dotfiles_setup.nightly_health import probe_scheduler, service_registered

    if enabled:
        health_token = probe_scheduler(repo, context)
        state = transition_state(state, SchedulerEvent.COMMIT_ENABLE, token=health_token)
    else:
        health_token = None
        if service_registered(context):
            raise NightlyError(
                "nightly updates are disabled but the scheduler is still registered; "
                "run ./bootstrap.sh nightly-schedule disable"
            )
    state.update(
        health_token=health_token,
        enabled=enabled,
        source_hash=fingerprint(repo, owned_backups(state)),
        lock_hash=lock_hash(repo),
    )
    _atomic_json(root / "schedule.json", state)
    print(
        "Nightly updates "
        + ("enabled: 03:00–04:00 local, seven-day quarantine." if enabled else "disabled.")
    )


def status() -> str:
    state = read_state(directory() / "schedule.json")
    if not state:
        return "Nightly updates are not configured."
    from dotfiles_setup.nightly_health import check_scheduler

    try:
        health = check_scheduler(Path(state["repository"]), UserPathContext.from_environment())
        healthy = health is not None
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        health, healthy = str(error), False
    return json.dumps(
        {
            "enabled": state.get("enabled", False),
            "healthy": healthy,
            "health": health,
            "repository": state.get("repository"),
            "window": "03:00–04:00 local",
            "minimum_observation_age_days": 7,
            "logs": str(directory()),
            "last_run": read_state(directory() / "last-run.json"),
        },
        indent=2,
    )
