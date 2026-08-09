from __future__ import annotations

import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from dotfiles_setup import cli
from dotfiles_setup.rustup import (
    RustToolchain,
    RustupError,
    RustupResult,
    load_rust_toolchain,
    resolve_rust_analyzer,
    setup_rustup,
)


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


def write_toolchain(
    repo: Path,
    *,
    channel: str = "1.97.1",
    components: str = '["rust-analyzer"]',
) -> None:
    (repo / "rust-toolchain.toml").write_text(
        f'[toolchain]\nchannel = "{channel}"\nprofile = "default"\ncomponents = {components}\n'
    )


def executable(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\nexit 0\n")
    path.chmod(0o755)
    return path


def test_repository_toolchain_is_exact_and_includes_rust_analyzer() -> None:
    selected = load_rust_toolchain(Path.cwd())

    assert selected == RustToolchain("1.97.1", "default", ("rust-analyzer",))


@pytest.mark.parametrize("channel", ["stable", "1.97", "nightly-2026-08-01"])
def test_toolchain_rejects_moving_or_partial_channels(tmp_path: Path, channel: str) -> None:
    write_toolchain(tmp_path, channel=channel)

    with pytest.raises(RustupError, match="exact numeric"):
        load_rust_toolchain(tmp_path)


def test_toolchain_requires_rust_analyzer_component(tmp_path: Path) -> None:
    write_toolchain(tmp_path, components='["rustfmt"]')

    with pytest.raises(RustupError, match="rust-analyzer"):
        load_rust_toolchain(tmp_path)


def test_setup_installs_and_resolves_only_the_pinned_toolchain(tmp_path: Path) -> None:
    write_toolchain(tmp_path)
    analyzer = executable(tmp_path / "toolchains" / "1.97.1" / "bin" / "rust-analyzer")
    rustup = "/nix/store/profile/bin/rustup"
    install = (
        rustup,
        "toolchain",
        "install",
        "1.97.1",
        "--profile",
        "default",
        "--component",
        "rust-analyzer",
        "--no-self-update",
    )
    lookup = (rustup, "which", "--toolchain", "1.97.1", "rust-analyzer")
    runner = FakeRunner(
        {
            install: completed(install),
            lookup: completed(lookup, stdout=f"{analyzer}\n"),
        }
    )

    result = setup_rustup(
        tmp_path,
        run=runner,
        which=lambda _: rustup,
        environment={"PATH": "/bin", "RUSTUP_TOOLCHAIN": "nightly"},
    )

    assert result == RustupResult("1.97.1", analyzer)
    assert [command for command, _ in runner.calls] == [list(install), list(lookup)]
    assert all("default" not in command[:3] for command, _ in runner.calls)
    assert all("RUSTUP_TOOLCHAIN" not in environment for _, environment in runner.calls)


def test_missing_rustup_fails_before_running_a_command(tmp_path: Path) -> None:
    write_toolchain(tmp_path)
    runner = FakeRunner({})

    with pytest.raises(RustupError, match="rustup is not available"):
        setup_rustup(tmp_path, run=runner, which=lambda _: None, environment={})

    assert runner.calls == []


def test_install_failure_has_actionable_offline_guidance(tmp_path: Path) -> None:
    write_toolchain(tmp_path)
    rustup = "/usr/bin/rustup"
    install = (
        rustup,
        "toolchain",
        "install",
        "1.97.1",
        "--profile",
        "default",
        "--component",
        "rust-analyzer",
        "--no-self-update",
    )
    runner = FakeRunner({install: completed(install, returncode=1, stderr="download unavailable")})

    with pytest.raises(RustupError, match="cache or network"):
        setup_rustup(tmp_path, run=runner, which=lambda _: rustup, environment={})


def test_explicit_lookup_rejects_an_unusable_path(tmp_path: Path) -> None:
    rustup = tmp_path / "rustup"
    lookup = (str(rustup), "which", "--toolchain", "1.97.1", "rust-analyzer")
    runner = FakeRunner(
        {lookup: completed(lookup, stdout=f"{tmp_path / 'missing-rust-analyzer'}\n")}
    )

    with pytest.raises(RustupError, match="unusable path"):
        resolve_rust_analyzer(
            rustup,
            RustToolchain("1.97.1", "default", ("rust-analyzer",)),
            run=runner,
            environment={},
        )


def test_production_rustup_code_never_invokes_global_default() -> None:
    source = (Path.cwd() / "src/dotfiles_setup/rustup.py").read_text()

    assert '"rustup", "default"' not in source
    assert '"default", toolchain' not in source


def test_rustup_cli_reports_toolchain_and_path(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(
        cli,
        "setup_rustup",
        lambda _: RustupResult("1.97.1", Path("/toolchains/1.97.1/rust-analyzer")),
    )

    assert cli.main(["rustup"]) == 0
    output = capsys.readouterr().out
    assert "1.97.1" in output
    assert "/toolchains/1.97.1/rust-analyzer" in output


def test_rustup_cli_reports_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)

    def fail(_: Path) -> RustupResult:
        raise RustupError("component unavailable")

    monkeypatch.setattr(cli, "setup_rustup", fail)

    assert cli.main(["rustup"]) == 1
    assert "component unavailable" in capsys.readouterr().out
