"""Interrupt setup commands before every durable step and require a clean recovery."""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from dotfiles_setup import links as links_module
from dotfiles_setup import mutations as mutations_module
from dotfiles_setup import nightly_health, nightly_schedule
from dotfiles_setup.cleanup import cleanup_links
from dotfiles_setup.destinations import DestinationState, classify
from dotfiles_setup.installer import run_mutation
from dotfiles_setup.links import Link, link_config
from dotfiles_setup.manifest import ManifestRepository, OperationJournal
from dotfiles_setup.paths import UserPathContext
from dotfiles_setup.recovery import run_recovery
from dotfiles_setup.shell_handoff import configure_shell_handoff

REPO_ROOT = Path(__file__).resolve().parents[1]
SYSTEM = os.uname().sysname
Environment = dict[str, str]
Snapshot = dict[str, tuple[str, int, str | bytes | None]]
Operation = Callable[[Environment, OperationJournal], None]
# Recovery never deletes what setup created: it leaves it under one of these names.
QUARANTINE_NAME = re.compile(r"\..+\.dotfiles(-result)?\.[0-9a-f]{32}")
_RANDOM_ID = re.compile(r"[0-9a-f]{32}")


class _Crash(BaseException):
    """Stand in for process death: ``except Exception`` rollback must not run."""


class _StepCounter:
    """Count durable steps and crash before the chosen one."""

    def __init__(self, crash_before: int | None) -> None:
        self.crash_before = crash_before
        self.names: list[str] = []
        self._inside_step = False

    def wrap(self, name: str, step: Callable[..., Any]) -> Callable[..., Any]:
        def counted(*args: Any, **kwargs: Any) -> Any:
            # A manifest write creates its own temporary file. Nothing durable happens
            # between the two, so the inner step is not a separate crash point.
            if self._inside_step:
                return step(*args, **kwargs)
            if len(self.names) == self.crash_before:
                raise _Crash(f"before step {self.crash_before}: {name}")
            self.names.append(name)
            self._inside_step = True
            try:
                return step(*args, **kwargs)
            finally:
                self._inside_step = False

        return counted


def _environment(root: Path) -> Environment:
    return {
        "HOME": str(root / "home"),
        "XDG_STATE_HOME": str(root / "state"),
        "XDG_CACHE_HOME": str(root / "cache"),
    }


def _inventory(values: Environment) -> tuple[Link, ...]:
    context = UserPathContext.from_environment(values, system=SYSTEM)
    return links_module.managed_links(
        REPO_ROOT,
        home=context.home,
        config_home=context.config_home,
        codex_home=context.codex_home,
        system=context.platform,
    )


def _snapshot(home: Path) -> Snapshot:
    """Record the kind, mode, and link target or content of every path under home."""

    snapshot: Snapshot = {}
    for path in sorted(home.rglob("*")):
        metadata = path.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        key = str(path.relative_to(home))
        if stat.S_ISLNK(metadata.st_mode):
            snapshot[key] = ("symlink", 0, os.readlink(path))
        elif stat.S_ISDIR(metadata.st_mode):
            snapshot[key] = ("directory", mode, None)
        else:
            snapshot[key] = ("file", mode, path.read_bytes())
    return snapshot


def _recovered_shape(root: Path, extras: list[str]) -> tuple[object, ...]:
    """Describe what recovery left behind, ignoring random names and the test root.

    The home directory is otherwise identical to the seed. What is left for a
    later command to meet is the quarantined extras, each journal's state (the
    only journal field a new command reads before it starts), and any other
    state file in full. Journal entries are deliberately left out.
    """

    def described(path: Path) -> str:
        text = path.read_text()
        state = json.loads(text).get("state") if path.suffix == ".json" else None
        return state or text.replace(str(root), "")

    state_files = sorted(
        (_RANDOM_ID.sub("*", str(path.relative_to(root))), described(path))
        for path in (root / "state").rglob("*")
        if path.is_file()
    )
    return (tuple(_RANDOM_ID.sub("*", extra) for extra in extras), tuple(state_files))


def _run(
    command: str,
    repository: Path,
    operation: Operation,
    values: Environment,
    monkeypatch: pytest.MonkeyPatch,
    crash_before: int | None,
) -> tuple[list[str], bool]:
    """Run one command, crashing before one step; return the steps run and whether it crashed."""

    counter = _StepCounter(crash_before)
    real_open = os.open
    counted_open = counter.wrap("create file", real_open)
    real_write = ManifestRepository.write
    real_read = ManifestRepository.read
    created: set[Path] = set()
    latest: dict[Path, tuple[ManifestRepository, str]] = {}

    def creating_open(path: Any, flags: int, *args: Any, **kwargs: Any) -> int:
        opener = counted_open if flags & os.O_CREAT else real_open
        return opener(path, flags, *args, **kwargs)

    def write(manifests: ManifestRepository, path: Path, value: dict[str, Any]) -> None:
        # Every write replaces the whole manifest, so a crash leaves only the latest one
        # on disk. A run that will crash keeps that one in memory and writes it once at
        # the crash, instead of rewriting the file at every checkpoint on the way there.
        if crash_before is None or path not in created:
            created.add(path)
            real_write(manifests, path, value)
        else:
            latest[path] = (manifests, json.dumps(value))

    def read(manifests: ManifestRepository, path: Path) -> dict[str, Any]:
        assert path not in latest, f"{path} was read back before the crash"
        return real_read(manifests, path)

    crashed = False
    with monkeypatch.context() as patch:
        patch.setattr(ManifestRepository, "write", counter.wrap("journal write", write))
        patch.setattr(ManifestRepository, "read", read)
        for name in ("_rename_no_replace", "_create_symlink"):
            patch.setattr(
                mutations_module,
                name,
                counter.wrap(name.strip("_"), getattr(mutations_module, name)),
            )
        patch.setattr(os, "mkdir", counter.wrap("mkdir", os.mkdir))
        patch.setattr(os, "open", creating_open)
        try:
            exit_code = run_mutation(
                command,
                repository,
                lambda journal: operation(values, journal),
                environ=values,
                output=lambda _: None,
            )
        except _Crash:
            crashed = True
    for path, (manifests, value) in latest.items():
        real_write(manifests, path, json.loads(value))
    assert crashed or exit_code == 0
    return counter.names, crashed


def _sweep(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    seed: Callable[[Path, Environment], None],
    operation: Operation,
    verify: Callable[[Environment], None],
    *,
    repository: Callable[[Path], Path] = lambda _root: REPO_ROOT,
) -> list[str]:
    """Crash before every durable step of a command; return the names of its steps.

    After each crash, recovery must put every seeded path back unchanged, leave
    nothing behind except quarantine names, and let the command succeed.
    """

    def run(root: Path, crash_before: int | None) -> tuple[list[str], bool]:
        return _run(
            command, repository(root), operation, _environment(root), monkeypatch, crash_before
        )

    baseline_root = tmp_path / "baseline"
    seed(baseline_root, _environment(baseline_root))
    steps, crashed = run(baseline_root, None)
    assert not crashed
    verify(_environment(baseline_root))

    rerun_shapes: set[tuple[object, ...]] = set()
    for index, name in enumerate(steps):
        label = f"crash before step {index} ({name})"
        root = tmp_path / str(index)
        values = _environment(root)
        seed(root, values)
        home = root / "home"
        before = _snapshot(home)

        ran, crashed = run(root, index)
        assert ran == steps[:index], label
        assert crashed, label

        journal = root / "state/dotfiles/current.json"
        committed = journal.exists() and json.loads(journal.read_text())["state"] == "completed"
        assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0, label
        if committed:
            # Only the write of the completed-journal copy follows the commit point,
            # so the finished result stands and recovery has nothing to undo.
            assert index == len(steps) - 1, label
            verify(values)
            continue
        after = _snapshot(home)
        assert {key: after.get(key) for key in before} == before, label
        extras = sorted(after.keys() - before.keys())
        unexpected = [
            key
            for key in extras
            if not any(QUARANTINE_NAME.fullmatch(part) for part in Path(key).parts)
        ]
        assert not unexpected, label

        # The command reads nothing but the home directory and the journals, so one
        # rerun per distinct recovered shape covers every crash point with that shape.
        shape = _recovered_shape(root, extras)
        if shape not in rerun_shapes:
            rerun_shapes.add(shape)
            _ran, crashed = run(root, None)
            assert not crashed, label
            verify(values)
    return steps


def _seed_link_home(root: Path, values: Environment) -> None:
    """Give link setup one destination of each kind it must preserve."""

    home = root / "home"
    home.mkdir(parents=True)
    (home / ".npmrc").write_text("registry=https://example.invalid\n")
    directory, stale, regular, _absent = (link.destination for link in _inventory(values))
    directory.mkdir(parents=True)
    (directory / "user-file").write_text("user directory content\n")
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.symlink_to(root / "elsewhere")
    regular.parent.mkdir(parents=True, exist_ok=True)
    regular.write_text("user file content\n")


@pytest.fixture
def four_links(monkeypatch: pytest.MonkeyPatch) -> None:
    """Trim the inventory: every managed link takes the same steps.

    Recovery reads the same trimmed inventory as its allowlist.
    """

    full_inventory = links_module.managed_links
    monkeypatch.setattr(
        links_module,
        "managed_links",
        lambda *args, **kwargs: full_inventory(*args, **kwargs)[:4],
    )


@pytest.mark.usefixtures("four_links")
def test_recovery_restores_home_after_a_crash_before_every_link_step(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def link(values: Environment, journal: OperationJournal) -> None:
        link_config(
            REPO_ROOT, environ=values, system=SYSTEM, journal=journal, output=lambda _: None
        )

    def linked(values: Environment) -> None:
        for link in _inventory(values):
            assert classify(link.destination, link.source).state is DestinationState.CORRECT

    steps = _sweep(tmp_path, monkeypatch, "link", _seed_link_home, link, linked)

    assert set(steps) == {
        "journal write",
        "rename_no_replace",
        "create_symlink",
        "mkdir",
        "create file",
    }


def _seed_linked_home(root: Path, values: Environment) -> None:
    """Give uninstall two managed links to remove and local state it must keep."""

    home = root / "home"
    in_directory, in_home, unmanaged, local = _inventory(values)
    in_directory.destination.parent.mkdir(parents=True)
    in_directory.destination.symlink_to(in_directory.source)
    in_home.destination.symlink_to(in_home.source)
    unmanaged.destination.symlink_to(root / "elsewhere")
    local.destination.mkdir()
    (local.destination / "user-file").write_text("user directory content\n")
    (home / ".tmux.conf.backup.1").write_text("earlier backup\n")


@pytest.mark.usefixtures("four_links")
def test_recovery_restores_home_after_a_crash_before_every_uninstall_step(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def uninstall(values: Environment, journal: OperationJournal) -> None:
        cleanup_links(
            REPO_ROOT, environ=values, system=SYSTEM, journal=journal, output=lambda _: None
        )

    def uninstalled(values: Environment) -> None:
        in_directory, in_home, unmanaged, local = _inventory(values)
        assert not in_directory.destination.is_symlink()
        assert not in_home.destination.is_symlink()
        assert unmanaged.destination.is_symlink()
        assert (local.destination / "user-file").is_file()

    steps = _sweep(tmp_path, monkeypatch, "uninstall", _seed_linked_home, uninstall, uninstalled)

    assert {"journal write", "rename_no_replace"} <= set(steps)


_STALE_BASH_PROFILE = """\
export EDITOR=vi
# Added by dotfiles Python shell-handoff setup (DOTFILES:BASH_PROFILE_SOURCE_BASHRC)
. ~/.old-bashrc
"""


def _seed_shell_home(root: Path, _values: Environment) -> None:
    """Give shell handoff one shell file of each kind it must preserve."""

    home = root / "home"
    (home / "shell").mkdir(parents=True)
    (home / ".bashrc").write_text("alias ll='ls -l'\n")
    (home / ".bashrc").chmod(0o600)
    (home / ".bash_profile").write_text(_STALE_BASH_PROFILE)
    (home / "shell/zshenv").write_text("export LANG=C\n")
    (home / ".zshenv").symlink_to("shell/zshenv")


def test_recovery_restores_home_after_a_crash_before_every_shell_handoff_step(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def hand_off(values: Environment, journal: OperationJournal | None) -> tuple[Path, ...]:
        return configure_shell_handoff(
            home=Path(values["HOME"]), shell="/bin/bash", journal=journal
        ).updated_files

    def handed_off(values: Environment) -> None:
        home = Path(values["HOME"])
        assert hand_off(values, None) == ()
        assert (home / ".bashrc").read_text().startswith("alias ll='ls -l'\n")
        assert ". ~/.old-bashrc" not in (home / ".bash_profile").read_text()
        assert "DOTFILES:EXEC_FISH" in (home / ".zshrc").read_text()
        assert (home / ".zshenv").is_symlink()

    steps = _sweep(tmp_path, monkeypatch, "shell-handoff", _seed_shell_home, hand_off, handed_off)

    assert {"journal write", "rename_no_replace", "create file"} <= set(steps)


def _schedule_files(values: Environment) -> dict[Path, bytes]:
    context = UserPathContext.from_environment(values)
    return nightly_schedule.schedule_contents(context.home / "repo", context, enabled=True)


def _seed_scheduled_home(root: Path, values: Environment) -> None:
    """Give the nightly schedule an older scheduler file to replace."""

    home = root / "home"
    (home / ".nix-profile/bin").mkdir(parents=True)
    (home / ".nix-profile/bin/python3").write_text("#!/bin/sh\n")
    (home / "repo").mkdir()
    (home / "repo/flake.lock").write_text("{}\n")
    older = next(iter(_schedule_files(values)))
    older.parent.mkdir(parents=True)
    older.write_text("older schedule\n")


def test_recovery_restores_home_after_a_crash_before_every_nightly_schedule_step(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Stand in for launchd and systemd: this sweep covers only the files on disk.
    monkeypatch.setattr(subprocess, "run", lambda args, **_: subprocess.CompletedProcess(args, 0))
    monkeypatch.setattr(nightly_health, "probe_scheduler", lambda _repo, _context: "token")
    monkeypatch.setattr(nightly_schedule, "fingerprint", lambda _repo, _ignored: "source")

    def schedule(values: Environment, journal: OperationJournal) -> None:
        nightly_schedule.configure(
            Path(values["HOME"]) / "repo", journal, enabled=True, environ=values
        )

    def scheduled(values: Environment) -> None:
        for path, contents in _schedule_files(values).items():
            assert path.read_bytes() == contents
        state = json.loads(
            Path(values["XDG_STATE_HOME"], "dotfiles/nightly/schedule.json").read_text()
        )
        assert state["enabled"] is True

    steps = _sweep(
        tmp_path,
        monkeypatch,
        "nightly-schedule",
        _seed_scheduled_home,
        schedule,
        scheduled,
        repository=lambda root: root / "home/repo",
    )

    assert {"journal write", "rename_no_replace", "create file"} <= set(steps)
