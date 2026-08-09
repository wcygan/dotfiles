from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.installer import run_install


def test_profile_completes_before_serial_setup() -> None:
    events: list[str] = []

    def profile() -> str:
        events.append("profile")
        return "ready"

    def operation(name: str) -> None:
        assert events[0] == "profile"
        events.append(name)

    exit_code = run_install(
        profile=profile,
        links=lambda: operation("links"),
        rustup=lambda: operation("rustup"),
        verify=lambda: 0,
        output=lambda _: None,
    )

    assert exit_code == 0
    assert events == ["profile", "links", "rustup"]


def test_link_failure_stops_later_mutations_and_handoff_is_skipped() -> None:
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
    assert "rustup" not in events
    assert "handoff" not in events
    assert events[-1] == "verify"
    assert any(line == "[FAIL] links: link failure" for line in output)
    assert "[SKIP] rustup: links failed" in output


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


def test_install_cli_wires_optional_shell_handoff(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)

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
