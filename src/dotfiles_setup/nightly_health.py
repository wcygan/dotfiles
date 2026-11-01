"""Scheduler registration checks and a harmless end-to-end installation probe."""

from __future__ import annotations

import os
import plistlib
import re
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

from dotfiles_setup.manifest import _atomic_json
from dotfiles_setup.nightly import directory, read_state
from dotfiles_setup.nightly_state import (
    SchedulerObservation,
    SchedulerPhase,
    acceptance_error,
    phase_of,
)
from dotfiles_setup.paths import UserPathContext


def acknowledge(repo: Path, token: str) -> None:
    if not re.fullmatch(r"[a-f0-9]{32}", token):
        raise ValueError("invalid scheduler probe token")
    _atomic_json(
        directory() / "last-health.json",
        {
            "repository": str(repo.resolve()),
            "token": token,
            "completed": time.time(),
        },
    )


def probe_scheduler(repo: Path, context: UserPathContext) -> str:
    from dotfiles_setup.nightly_schedule import LABEL, schedule_contents, schedule_environment

    token = uuid.uuid4().hex
    args = ["/bin/bash", str(repo.resolve() / "bootstrap.sh"), "nightly-probe", token]
    root = context.state_directory / "nightly"
    probe_label = LABEL + ".probe-" + token
    with tempfile.TemporaryDirectory(prefix="probe-", dir=root) as temporary:
        if context.platform.lower() == "darwin":
            job = plistlib.loads(
                next(iter(schedule_contents(repo, context, enabled=True).values()))
            )
            job.update(Label=probe_label, ProgramArguments=args, RunAtLoad=True)
            job.pop("StartCalendarInterval")
            path = Path(temporary) / "probe.plist"
            path.write_bytes(plistlib.dumps(job))
            service = f"gui/{os.getuid()}/{probe_label}"
            try:
                subprocess.run(
                    ["launchctl", "bootstrap", f"gui/{os.getuid()}", str(path)],
                    check=True,
                    timeout=15,
                )
                _wait_for_ack(repo, token, root)
            finally:
                subprocess.run(
                    ["launchctl", "bootout", service], capture_output=True, check=False, timeout=15
                )
        else:
            unit = "dotfiles-nightly-probe-" + token
            command = [
                "systemd-run",
                "--user",
                "--wait",
                "--collect",
                "--unit",
                unit,
                *[
                    "--setenv=" + key + "=" + value
                    for key, value in schedule_environment(context).items()
                ],
                *args,
            ]
            try:
                subprocess.run(command, check=True, timeout=30)
                _wait_for_ack(repo, token, root)
            finally:
                subprocess.run(
                    ["systemctl", "--user", "stop", unit],
                    capture_output=True,
                    check=False,
                    timeout=15,
                )
    return token


def _wait_for_ack(repo: Path, token: str, root: Path) -> None:
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        result = read_state(root / "last-health.json")
        if result.get("token") == token and result.get("repository") == str(repo.resolve()):
            return
        time.sleep(0.1)
    raise RuntimeError("scheduler probe did not reach the checkout; inspect scheduler logs")


def service_registered(context: UserPathContext) -> bool:
    """Return whether the operating system still has a live nightly timer.

    A timer that is loaded but explicitly disabled cannot fire, so it counts as
    unregistered. ``launchctl`` and ``systemctl`` failures mean no registration
    is observable; a missing tool cannot keep a timer alive.
    """
    from dotfiles_setup.nightly_schedule import LABEL

    if context.platform.lower() == "darwin":
        try:
            loaded = subprocess.run(
                ["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"],
                capture_output=True,
                timeout=10,
            )
            if loaded.returncode != 0:
                return False
            disabled = subprocess.run(
                ["launchctl", "print-disabled", f"gui/{os.getuid()}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if disabled.returncode != 0:
                return True
            return not re.search(
                r'"' + re.escape(LABEL) + r'"\s*=>\s*true', disabled.stdout
            )
        except (OSError, subprocess.SubprocessError):
            return False
    try:
        for args in (
            ["is-enabled", "dotfiles-nightly.timer"],
            ["is-active", "dotfiles-nightly.timer"],
        ):
            result = subprocess.run(
                ["systemctl", "--user", *args],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip() in {"enabled", "active"}:
                return True
        return False
    except (OSError, subprocess.SubprocessError):
        return False


def check_scheduler(repo: Path, context: UserPathContext) -> str | None:
    """Read-only acceptance: enabled configuration must be loaded and previously probed."""
    from dotfiles_setup.nightly_schedule import LABEL, schedule_contents

    root = context.state_directory / "nightly"
    state = read_state(root / "schedule.json")
    phase = phase_of(state)
    if phase is SchedulerPhase.REQUESTED:
        raise ValueError("nightly updates were requested but scheduler setup is incomplete")
    if phase is SchedulerPhase.UNKNOWN:
        raise ValueError("nightly updates are marked enabled without a completed scheduler probe")
    if phase is SchedulerPhase.UNCONFIGURED:
        if any(path.exists() for path in schedule_contents(repo, context, enabled=True)):
            raise ValueError("nightly files exist without setup state; run nightly-schedule enable")
        return None
    observation = SchedulerObservation(phase, service_registered(context))
    error = acceptance_error(observation)
    if error is not None:
        raise ValueError(error)
    if phase is SchedulerPhase.DISABLED:
        return None
    if state.get("repository") != str(repo.resolve()):
        raise ValueError("nightly scheduler belongs to a different checkout")
    for path, contents in schedule_contents(repo, context, enabled=True).items():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != contents:
            raise ValueError(f"nightly scheduler configuration differs: {path}")
    health = read_state(root / "last-health.json")
    if (
        not state.get("health_token")
        or health.get("token") != state["health_token"]
        or health.get("repository") != str(repo.resolve())
    ):
        raise ValueError("nightly scheduler has not passed its installation probe")
    if context.platform.lower() == "darwin":
        subprocess.run(
            ["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"],
            capture_output=True,
            check=True,
            timeout=10,
        )
        disabled = subprocess.check_output(
            ["launchctl", "print-disabled", f"gui/{os.getuid()}"],
            text=True,
            timeout=10,
        )
        if re.search(r'"' + re.escape(LABEL) + r'"\s*=>\s*true', disabled):
            raise ValueError("nightly LaunchAgent is disabled")
    else:
        for args, expected in [
            (["is-enabled", "dotfiles-nightly.timer"], "enabled"),
            (["is-active", "dotfiles-nightly.timer"], "active"),
        ]:
            result = subprocess.check_output(
                ["systemctl", "--user", *args], text=True, timeout=10
            ).strip()
            if result != expected:
                raise ValueError("nightly timer is not durably enabled and active")
        next_run = subprocess.check_output(
            [
                "systemctl",
                "--user",
                "show",
                "dotfiles-nightly.timer",
                "--property=NextElapseUSecRealtime",
                "--value",
            ],
            text=True,
            timeout=10,
        ).strip()
        if not next_run:
            raise ValueError("nightly timer has no next run")
    return "nightly scheduler is registered for 03:00 local and passed its installation probe"
