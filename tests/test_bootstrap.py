from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPO_ROOT / "bootstrap.sh"


def write_executable(path: Path, contents: str) -> None:
    path.write_text(f"#!/bin/sh\nset -eu\n{contents}")
    path.chmod(0o755)


@pytest.fixture
def command_bin(tmp_path: Path) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    return bin_dir


def bootstrap_environment(command_bin: Path, tmp_path: Path) -> dict[str, str]:
    return {
        **os.environ,
        "HOME": str(tmp_path / "home"),
        "PATH": f"{command_bin}:/usr/bin:/bin",
        "BOOTSTRAP_CAPTURE": str(tmp_path / "capture"),
        "DOTFILES_BOOTSTRAP_SKIP_PROFILE": "1",
        "VIRTUAL_ENV": str(tmp_path / "active-virtual-environment"),
    }


def run_bootstrap(
    command_bin: Path,
    tmp_path: Path,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(BOOTSTRAP), *args],
        cwd=tmp_path,
        env=bootstrap_environment(command_bin, tmp_path),
        text=True,
        capture_output=True,
        check=False,
    )


def test_existing_nix_executes_locked_install(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", 'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"')

    result = run_bootstrap(command_bin, tmp_path)

    assert result.returncode == 0
    captured = (tmp_path / "capture").read_text().splitlines()
    assert captured == [
        "--extra-experimental-features",
        "nix-command flakes",
        "develop",
        "--no-write-lock-file",
        ".#default",
        "--command",
        "uv",
        "run",
        "--locked",
        "python",
        "-m",
        "dotfiles_setup",
        "install",
    ]


def test_locked_flake_failure_stops_before_python(command_bin: Path, tmp_path: Path) -> None:
    write_executable(
        command_bin / "nix",
        'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"; '
        'printf "committed lock cannot satisfy flake\\n" >&2; exit 1',
    )

    result = run_bootstrap(command_bin, tmp_path)

    assert result.returncode == 1
    assert "committed lock cannot satisfy flake" in result.stderr
    captured = (tmp_path / "capture").read_text().splitlines()
    assert "--no-write-lock-file" in captured


def test_macos_missing_nix_opens_package_installer(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "uname", 'printf "Darwin\\n"')
    write_executable(command_bin / "open", 'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"')

    result = run_bootstrap(command_bin, tmp_path)

    assert result.returncode == 2
    assert (tmp_path / "capture").read_text().strip() == (
        "https://install.determinate.systems/determinate-pkg/stable/Universal"
    )
    assert "rerun ./bootstrap.sh" in result.stdout


def test_linux_missing_nix_requires_explicit_consent(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "uname", 'printf "Linux\\n"')

    result = run_bootstrap(command_bin, tmp_path, "--install-nix")

    assert result.returncode == 2
    assert "--install-nix --yes" in result.stdout


def test_linux_installer_requires_nix_to_become_available(
    command_bin: Path, tmp_path: Path
) -> None:
    write_executable(command_bin / "uname", 'printf "Linux\\n"')
    write_executable(command_bin / "curl", "printf 'exit 0\\n'")

    result = run_bootstrap(command_bin, tmp_path, "--install-nix", "--yes")

    assert result.returncode == 1
    assert "nix is not available" in result.stderr


def test_unsupported_operating_system_is_rejected(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "uname", 'printf "FreeBSD\\n"')

    result = run_bootstrap(command_bin, tmp_path)

    assert result.returncode == 2
    assert "Unsupported operating system: FreeBSD" in result.stderr


def test_commands_are_forwarded_without_shell_dispatch(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", 'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"')

    result = run_bootstrap(command_bin, tmp_path, "unknown-command")

    assert result.returncode == 0
    captured = (tmp_path / "capture").read_text().splitlines()
    assert captured[-1] == "unknown-command"


def test_command_options_are_forwarded_to_python(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", 'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"')

    result = run_bootstrap(command_bin, tmp_path, "uninstall", "--yes")

    assert result.returncode == 0
    captured = (tmp_path / "capture").read_text().splitlines()
    assert captured[-2:] == ["uninstall", "--yes"]


def test_leading_bootstrap_options_are_not_forwarded(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", 'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"')

    result = run_bootstrap(command_bin, tmp_path, "--install-nix", "--yes", "verify")

    assert result.returncode == 0
    captured = (tmp_path / "capture").read_text().splitlines()
    assert captured[-1] == "verify"
    assert "--install-nix" not in captured
    assert "--yes" not in captured


def test_double_dash_forwards_remaining_arguments(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", 'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"')

    result = run_bootstrap(command_bin, tmp_path, "--", "--install-nix", "--yes")

    assert result.returncode == 0
    captured = (tmp_path / "capture").read_text().splitlines()
    assert captured[-2:] == ["--install-nix", "--yes"]


def test_python_cli_runs_from_repo_without_virtual_environment(
    command_bin: Path, tmp_path: Path
) -> None:
    write_executable(
        command_bin / "nix",
        'printf "cwd=%s\\nvirtual_env=%s\\n" "$PWD" "${VIRTUAL_ENV-unset}" '
        '> "$BOOTSTRAP_CAPTURE"',
    )

    result = run_bootstrap(command_bin, tmp_path, "verify")

    assert result.returncode == 0
    assert (tmp_path / "capture").read_text().splitlines() == [
        f"cwd={REPO_ROOT}",
        "virtual_env=unset",
    ]
