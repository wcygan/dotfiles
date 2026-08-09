from __future__ import annotations

import threading
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.installer import run_install


def test_profile_completes_before_parallel_setup() -> None:
    events: list[str] = []
    setup_barrier = threading.Barrier(2)

    def profile() -> str:
        events.append("profile")
        return "ready"

    def operation(name: str) -> None:
        assert events[0] == "profile"
        assert not any(event.endswith("-finished") for event in events)
        events.append(f"{name}-started")
        setup_barrier.wait(timeout=2)
        events.append(f"{name}-finished")

    exit_code = run_install(
        profile=profile,
        links=lambda: operation("links"),
        rustup=lambda: operation("rustup"),
        verify=lambda: 0,
        output=lambda _: None,
    )

    assert exit_code == 0
    assert events[0] == "profile"
    assert set(events[1:3]) == {"links-started", "rustup-started"}


def test_parallel_failures_are_collected_and_handoff_is_skipped() -> None:
    events: list[str] = []
    output: list[str] = []

    def fail_links() -> None:
        events.append("links")
        raise RuntimeError("link failure")

    def rustup() -> Path:
        events.append("rustup")
        return Path("/rust-analyzer")

    exit_code = run_install(
        profile=lambda: "ready",
        links=fail_links,
        rustup=rustup,
        shell_handoff=lambda: events.append("handoff"),
        verify=lambda: events.append("verify") or 0,
        output=output.append,
    )

    assert exit_code == 1
    assert "rustup" in events
    assert "handoff" not in events
    assert events[-1] == "verify"
    assert any(line == "[FAIL] links: link failure" for line in output)
    assert any("[PASS] rustup" in line for line in output)


def test_profile_failure_skips_setup_but_still_verifies() -> None:
    events: list[str] = []
    output: list[str] = []

    def fail_profile() -> None:
        raise RuntimeError("profile locked")

    exit_code = run_install(
        profile=fail_profile,
        links=lambda: events.append("links"),
        rustup=lambda: events.append("rustup"),
        verify=lambda: events.append("verify") or 0,
        shell_handoff=lambda: events.append("handoff"),
        output=output.append,
    )

    assert exit_code == 1
    assert events == ["verify"]
    assert "[SKIP] links: profile failed" in output
    assert "[SKIP] rustup: profile failed" in output
    assert "[SKIP] shell-handoff: profile failed" in output


def test_successful_setup_runs_opt_in_handoff_before_verify() -> None:
    events: list[str] = []

    exit_code = run_install(
        profile=lambda: None,
        links=lambda: None,
        rustup=lambda: None,
        shell_handoff=lambda: events.append("handoff"),
        verify=lambda: events.append("verify") or 0,
        output=lambda _: None,
    )

    assert exit_code == 0
    assert events == ["handoff", "verify"]


def test_install_cli_wires_optional_shell_handoff(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def install(**kwargs: object) -> int:
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(cli, "run_install", install)

    assert cli.main(["install", "--shell-handoff"]) == 0
    assert callable(captured["profile"])
    assert callable(captured["links"])
    assert callable(captured["rustup"])
    assert callable(captured["verify"])
    assert callable(captured["shell_handoff"])
