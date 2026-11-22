"""Interrupt link setup before every durable step and require a clean recovery."""

from __future__ import annotations

import os
import re
import stat
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from dotfiles_setup import links as links_module
from dotfiles_setup import mutations as mutations_module
from dotfiles_setup.destinations import DestinationState, classify
from dotfiles_setup.links import Link, link_config
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.paths import UserPathContext
from dotfiles_setup.recovery import run_recovery

REPO_ROOT = Path(__file__).resolve().parents[1]
SYSTEM = os.uname().sysname
Snapshot = dict[str, tuple[str, int, str | bytes | None]]
# Recovery never deletes what setup created: it leaves it under one of these names.
QUARANTINE_NAME = re.compile(r"\..+\.dotfiles(-result)?\.[0-9a-f]{32}")


class _Crash(BaseException):
    """Stand in for process death: ``except Exception`` rollback must not run."""


class _StepCounter:
    """Count durable steps and crash before the chosen one."""

    def __init__(self, crash_before: int | None) -> None:
        self.crash_before = crash_before
        self.names: list[str] = []

    def wrap(self, name: str, step: Callable[..., Any]) -> Callable[..., Any]:
        def counted(*args: Any, **kwargs: Any) -> Any:
            if len(self.names) == self.crash_before:
                raise _Crash(f"before step {self.crash_before}: {name}")
            self.names.append(name)
            return step(*args, **kwargs)

        return counted


def _environment(root: Path) -> dict[str, str]:
    return {"HOME": str(root / "home"), "XDG_STATE_HOME": str(root / "state")}


def _inventory(values: dict[str, str]) -> tuple[Link, ...]:
    context = UserPathContext.from_environment(values, system=SYSTEM)
    return links_module.managed_links(
        REPO_ROOT,
        home=context.home,
        config_home=context.config_home,
        codex_home=context.codex_home,
        system=context.platform,
    )


def _seed_home(root: Path, values: dict[str, str]) -> None:
    """Give link setup one destination of each kind it must preserve."""

    home = root / "home"
    home.mkdir(parents=True)
    (home / ".npmrc").write_text("registry=https://example.invalid\n")
    inventory = _inventory(values)
    directory, stale, regular, _absent = (link.destination for link in inventory)
    directory.mkdir(parents=True)
    (directory / "user-file").write_text("user directory content\n")
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.symlink_to(root / "elsewhere")
    regular.parent.mkdir(parents=True, exist_ok=True)
    regular.write_text("user file content\n")


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


def _interrupted_link(
    values: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
    crash_before: int | None,
) -> tuple[list[str], bool]:
    """Run link setup, crashing before one step; return the steps run and whether it crashed."""

    counter = _StepCounter(crash_before)
    journal = OperationJournal("link", REPO_ROOT, environ=values)
    real_open = os.open

    def creating_open(path: Any, flags: int, *args: Any, **kwargs: Any) -> int:
        if flags & os.O_CREAT:
            return counter.wrap("create file", real_open)(path, flags, *args, **kwargs)
        return real_open(path, flags, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(journal, "_write", counter.wrap("journal write", journal._write))
        for name in ("_rename_no_replace", "_create_symlink"):
            patch.setattr(
                mutations_module,
                name,
                counter.wrap(name.strip("_"), getattr(mutations_module, name)),
            )
        patch.setattr(os, "mkdir", counter.wrap("mkdir", os.mkdir))
        patch.setattr(os, "open", creating_open)
        try:
            journal.transition("applying")
            link_config(
                REPO_ROOT,
                environ=values,
                system=SYSTEM,
                journal=journal,
                output=lambda _: None,
            )
        except _Crash:
            return counter.names, True
    return counter.names, False


def test_recovery_restores_home_after_a_crash_before_every_link_step(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Every managed link takes the same steps, so one link per prior kind keeps the
    # sweep fast. Recovery reads the same trimmed inventory as its allowlist.
    full_inventory = links_module.managed_links
    monkeypatch.setattr(
        links_module,
        "managed_links",
        lambda *args, **kwargs: full_inventory(*args, **kwargs)[:4],
    )
    baseline_root = tmp_path / "baseline"
    baseline_values = _environment(baseline_root)
    _seed_home(baseline_root, baseline_values)
    steps, crashed = _interrupted_link(baseline_values, monkeypatch, None)
    assert not crashed
    assert {"journal write", "rename_no_replace", "create_symlink", "mkdir", "create file"} <= set(
        steps
    )

    # Index len(steps) crashes nothing: every step ran but completion was never recorded.
    for index in range(len(steps) + 1):
        label = f"crash before step {index} ({steps[index] if index < len(steps) else 'end'})"
        root = tmp_path / str(index)
        values = _environment(root)
        _seed_home(root, values)
        home = root / "home"
        before = _snapshot(home)

        ran, crashed = _interrupted_link(values, monkeypatch, index)
        assert ran == steps[:index], label
        assert crashed == (index < len(steps)), label

        assert run_recovery(environ=values, apply=True, yes=True, output=lambda _: None) == 0, label
        after = _snapshot(home)
        assert {key: after.get(key) for key in before} == before, label
        unexpected = [
            key
            for key in after.keys() - before.keys()
            if not any(QUARANTINE_NAME.fullmatch(part) for part in Path(key).parts)
        ]
        assert not unexpected, label

        link_config(REPO_ROOT, environ=values, system=SYSTEM, output=lambda _: None)
        for link in _inventory(values):
            state = classify(link.destination, link.source).state
            assert state is DestinationState.CORRECT, f"{label}: {link.destination}"
