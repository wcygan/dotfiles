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
    }


def run_bootstrap(
    command_bin: Path,
    tmp_path: Path,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(BOOTSTRAP), *args],
        cwd=REPO_ROOT,
        env=bootstrap_environment(command_bin, tmp_path),
        text=True,
        capture_output=True,
        check=False,
    )


def test_existing_nix_executes_locked_doctor(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", 'printf "%s\\n" "$@" > "$BOOTSTRAP_CAPTURE"')

    result = run_bootstrap(command_bin, tmp_path)

    assert result.returncode == 0
    captured = (tmp_path / "capture").read_text().splitlines()
    assert captured == [
        "--extra-experimental-features",
        "nix-command flakes",
        "develop",
        ".#default",
        "--command",
        "uv",
        "run",
        "--locked",
        "python",
        "-m",
        "dotfiles_setup",
        "doctor",
    ]


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


def test_migration_phase_rejects_mutating_commands(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", "exit 0")

    result = run_bootstrap(command_bin, tmp_path, "install")

    assert result.returncode == 2
    assert "Only the doctor command" in result.stderr
