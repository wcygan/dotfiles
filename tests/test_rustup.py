from __future__ import annotations

import subprocess
from collections.abc import Mapping, Sequence

import pytest

from dotfiles_setup import cli
from dotfiles_setup.rustup import RustupError, setup_rustup


class FakeRunner:
    def __init__(
        self, responses: Mapping[tuple[str, ...], subprocess.CompletedProcess[str]]
    ) -> None:
        self.responses = responses
        self.calls: list[tuple[list[str], dict[str, str]]] = []

    def __call__(
        self,
        command: Sequence[str],
        *,
        capture_output: bool,
        check: bool,
        env: Mapping[str, str],
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        assert capture_output is True
        assert check is False
        assert text is True
        self.calls.append((list(command), dict(env)))
        return self.responses[tuple(command)]


def completed(
    command: Sequence[str], *, stdout: str = "", stderr: str = "", returncode: int = 0
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


def test_existing_default_adds_component_and_returns_resolved_path() -> None:
    runner = FakeRunner(
        {
            ("rustup", "default"): completed(
                ("rustup", "default"), stdout="nightly-2026-08-01-aarch64-apple-darwin (default)\n"
            ),
            (
                "rustup",
                "component",
                "add",
                "rust-analyzer",
                "--toolchain",
                "nightly-2026-08-01-aarch64-apple-darwin",
            ): completed(("rustup", "component", "add")),
            ("rustup", "which", "rust-analyzer"): completed(
                ("rustup", "which", "rust-analyzer"),
                stdout="/toolchains/nightly/bin/rust-analyzer\n",
            ),
        }
    )

    result = setup_rustup(
        run=runner,
        which=lambda _: "/nix/store/rustup",
        environment={"PATH": "/bin"},
    )

    assert result.as_posix() == "/toolchains/nightly/bin/rust-analyzer"
    assert [command for command, _ in runner.calls] == [
        ["rustup", "default"],
        [
            "rustup",
            "component",
            "add",
            "rust-analyzer",
            "--toolchain",
            "nightly-2026-08-01-aarch64-apple-darwin",
        ],
        ["rustup", "which", "rust-analyzer"],
    ]
    assert runner.calls[0][1] == {"PATH": "/bin"}
    assert runner.calls[2][1] == {
        "PATH": "/bin",
        "RUSTUP_TOOLCHAIN": "nightly-2026-08-01-aarch64-apple-darwin",
    }


def test_missing_default_bootstraps_stable_before_resolving() -> None:
    runner = FakeRunner(
        {
            ("rustup", "default"): completed(
                ("rustup", "default"), returncode=1, stderr="no default"
            ),
            (
                "rustup",
                "toolchain",
                "install",
                "stable",
                "--profile",
                "default",
                "--component",
                "rust-analyzer",
            ): completed(("rustup", "toolchain", "install")),
            ("rustup", "default", "stable"): completed(("rustup", "default", "stable")),
            ("rustup", "which", "rust-analyzer"): completed(
                ("rustup", "which", "rust-analyzer"),
                stdout="/toolchains/stable/bin/rust-analyzer\n",
            ),
        }
    )

    result = setup_rustup(run=runner, which=lambda _: "/usr/bin/rustup", environment={})

    assert result.as_posix() == "/toolchains/stable/bin/rust-analyzer"
    assert [command for command, _ in runner.calls] == [
        ["rustup", "default"],
        [
            "rustup",
            "toolchain",
            "install",
            "stable",
            "--profile",
            "default",
            "--component",
            "rust-analyzer",
        ],
        ["rustup", "default", "stable"],
        ["rustup", "which", "rust-analyzer"],
    ]
    assert runner.calls[-1][1] == {"RUSTUP_TOOLCHAIN": "stable"}


def test_empty_default_output_bootstraps_stable() -> None:
    runner = FakeRunner(
        {
            ("rustup", "default"): completed(("rustup", "default"), stdout="  \n"),
            (
                "rustup",
                "toolchain",
                "install",
                "stable",
                "--profile",
                "default",
                "--component",
                "rust-analyzer",
            ): completed(("rustup", "toolchain", "install")),
            ("rustup", "default", "stable"): completed(("rustup", "default", "stable")),
            ("rustup", "which", "rust-analyzer"): completed(
                ("rustup", "which", "rust-analyzer"), stdout="/stable/rust-analyzer"
            ),
        }
    )

    setup_rustup(run=runner, which=lambda _: "/usr/bin/rustup", environment={})

    assert runner.calls[1][0][:4] == ["rustup", "toolchain", "install", "stable"]


def test_missing_rustup_fails_before_running_a_command() -> None:
    runner = FakeRunner({})

    with pytest.raises(RustupError, match="rustup is not available in PATH"):
        setup_rustup(run=runner, which=lambda _: None, environment={})

    assert runner.calls == []


def test_component_failure_includes_rustup_diagnostic() -> None:
    runner = FakeRunner(
        {
            ("rustup", "default"): completed(("rustup", "default"), stdout="stable (default)"),
            ("rustup", "component", "add", "rust-analyzer", "--toolchain", "stable"): completed(
                ("rustup", "component", "add"), returncode=1, stderr="component unavailable"
            ),
        }
    )

    with pytest.raises(RustupError, match="component unavailable"):
        setup_rustup(run=runner, which=lambda _: "/usr/bin/rustup", environment={})


def test_empty_rust_analyzer_path_fails_clearly() -> None:
    runner = FakeRunner(
        {
            ("rustup", "default"): completed(("rustup", "default"), stdout="stable"),
            ("rustup", "component", "add", "rust-analyzer", "--toolchain", "stable"): completed(
                ("rustup", "component", "add")
            ),
            ("rustup", "which", "rust-analyzer"): completed(("rustup", "which", "rust-analyzer")),
        }
    )

    with pytest.raises(RustupError, match="did not return a path"):
        setup_rustup(run=runner, which=lambda _: "/usr/bin/rustup", environment={})


def test_rust_analyzer_lookup_failure_includes_rustup_diagnostic() -> None:
    runner = FakeRunner(
        {
            ("rustup", "default"): completed(("rustup", "default"), stdout="stable"),
            ("rustup", "component", "add", "rust-analyzer", "--toolchain", "stable"): completed(
                ("rustup", "component", "add")
            ),
            ("rustup", "which", "rust-analyzer"): completed(
                ("rustup", "which", "rust-analyzer"),
                returncode=1,
                stderr="rust-analyzer is unavailable",
            ),
        }
    )

    with pytest.raises(RustupError, match="rust-analyzer is unavailable"):
        setup_rustup(run=runner, which=lambda _: "/usr/bin/rustup", environment={})


def test_rustup_cli_reports_resolved_path(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "setup_rustup", lambda: "/toolchains/stable/rust-analyzer")

    assert cli.main(["rustup"]) == 0
    assert "/toolchains/stable/rust-analyzer" in capsys.readouterr().out


def test_rustup_cli_reports_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail() -> None:
        raise RustupError("component unavailable")

    monkeypatch.setattr(cli, "setup_rustup", fail)

    assert cli.main(["rustup"]) == 1
    assert "component unavailable" in capsys.readouterr().out
