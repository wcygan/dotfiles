from __future__ import annotations

import os
import shutil
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
    inherited = {
        name: value
        for name, value in os.environ.items()
        if name != "DOTFILES_BOOTSTRAP_DEV_CACHE"
    }
    return {
        **inherited,
        "HOME": str(tmp_path / "home"),
        "XDG_CACHE_HOME": str(tmp_path / "cache"),
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


# Stands in for Nix: `print-dev-env` writes a small environment and its profile,
# and every call is logged so tests can see which Nix commands ran.
CACHING_NIX = """
printf '%s\\n' "$*" >> "$NIX_LOG"
case " $* " in
  *" print-dev-env "*)
    previous=""
    for argument in "$@"; do
      if [ "$previous" = --profile ]; then : > "$argument"; fi
      previous=$argument
    done
    printf "BASH='%s'\\nexport TMPDIR=''\\nexport FROM_DEV_ENV=yes\\n" "$DEV_BASH"
    ;;
esac
"""
RECORDING_UV = """
{
  printf '%s\\n' "$@"
  printf 'dev=%s\\ntmp=%s\\n' "${FROM_DEV_ENV-}" "${TMPDIR-}"
} > "$BOOTSTRAP_CAPTURE"
"""


@pytest.fixture
def checkout(command_bin: Path, tmp_path: Path) -> Path:
    """A throwaway checkout whose flake files a test may change."""

    root = tmp_path / "checkout"
    root.mkdir()
    shutil.copy2(BOOTSTRAP, root / "bootstrap.sh")
    (root / "flake.nix").write_text("first flake\n")
    (root / "flake.lock").write_text("first lock\n")
    write_executable(command_bin / "nix", CACHING_NIX)
    write_executable(command_bin / "uv", RECORDING_UV)
    return root


def run_checkout(
    checkout: Path,
    command_bin: Path,
    tmp_path: Path,
    *,
    arguments: tuple[str, ...] = ("verify",),
    **overrides: str,
) -> list[str]:
    """Run the checkout's bootstrap and return the Nix commands run so far."""

    bash = shutil.which("bash")
    assert bash is not None
    environment = {
        **bootstrap_environment(command_bin, tmp_path),
        "NIX_LOG": str(tmp_path / "nix-log"),
        "DEV_BASH": bash,
        "TMPDIR": str(tmp_path),
        **overrides,
    }
    result = subprocess.run(
        [str(checkout / "bootstrap.sh"), *arguments],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return (tmp_path / "nix-log").read_text().splitlines()


def test_dev_environment_is_built_once_and_reused(
    checkout: Path, command_bin: Path, tmp_path: Path
) -> None:
    first = run_checkout(checkout, command_bin, tmp_path)
    second = run_checkout(checkout, command_bin, tmp_path)

    assert len(first) == 1
    assert " print-dev-env --no-write-lock-file --profile " in first[0]
    assert second == first
    assert (tmp_path / "capture").read_text().splitlines() == [
        "run",
        "--locked",
        "python",
        "-m",
        "dotfiles_setup",
        "verify",
        "dev=yes",
        f"tmp={tmp_path}",
    ]


@pytest.mark.parametrize("changed", ("flake.nix", "flake.lock"))
def test_changed_flake_input_rebuilds_the_dev_environment(
    checkout: Path, command_bin: Path, tmp_path: Path, changed: str
) -> None:
    run_checkout(checkout, command_bin, tmp_path)
    (checkout / changed).write_text("second\n")

    assert len(run_checkout(checkout, command_bin, tmp_path)) == 2
    assert len(list((tmp_path / "cache" / "dotfiles" / "dev-env").iterdir())) == 1


def test_collected_dev_environment_is_rebuilt(
    checkout: Path, command_bin: Path, tmp_path: Path
) -> None:
    run_checkout(checkout, command_bin, tmp_path)
    (profile,) = (tmp_path / "cache" / "dotfiles" / "dev-env").glob("*/profile")
    profile.unlink()

    assert len(run_checkout(checkout, command_bin, tmp_path)) == 2


def test_dev_environment_cache_can_be_turned_off(
    checkout: Path, command_bin: Path, tmp_path: Path
) -> None:
    (log,) = run_checkout(checkout, command_bin, tmp_path, DOTFILES_BOOTSTRAP_DEV_CACHE="0")

    assert " develop --no-write-lock-file .#default --command uv run --locked " in log
    assert not (tmp_path / "cache").exists()


def test_unusable_dev_environment_falls_back_to_nix_develop(
    checkout: Path, command_bin: Path, tmp_path: Path
) -> None:
    log = run_checkout(checkout, command_bin, tmp_path, DEV_BASH="/nonexistent/bash")

    assert [line.split()[3] for line in log] == ["print-dev-env", "develop"]


def test_run_executes_a_command_in_the_dev_environment(
    checkout: Path, command_bin: Path, tmp_path: Path
) -> None:
    (log,) = run_checkout(
        checkout, command_bin, tmp_path, arguments=("--run", "uv", "lock", "--check")
    )

    assert " print-dev-env " in log
    assert (tmp_path / "capture").read_text().splitlines()[:3] == ["lock", "--check", "dev=yes"]


def test_run_falls_back_to_nix_develop(
    checkout: Path, command_bin: Path, tmp_path: Path
) -> None:
    (log,) = run_checkout(
        checkout,
        command_bin,
        tmp_path,
        arguments=("--run", "uv", "lock", "--check"),
        DOTFILES_BOOTSTRAP_DEV_CACHE="0",
    )

    assert log.endswith(" develop --no-write-lock-file .#default --command uv lock --check")


def test_run_without_a_command_is_rejected(command_bin: Path, tmp_path: Path) -> None:
    write_executable(command_bin / "nix", "exit 0")

    result = run_bootstrap(command_bin, tmp_path, "--run")

    assert result.returncode == 2
    assert "--run needs a command." in result.stderr
