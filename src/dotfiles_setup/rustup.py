"""Ensure the selected Rust toolchain provides rust-analyzer."""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

Command = Sequence[str]
CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
CommandLocator = Callable[[str], str | None]


class RustupError(RuntimeError):
    """Raised when rustup cannot prepare or locate rust-analyzer."""


def setup_rustup(
    *,
    run: CommandRunner = subprocess.run,
    which: CommandLocator = shutil.which,
    environment: Mapping[str, str] | None = None,
) -> Path:
    """Install rust-analyzer for the default toolchain and return its path.

    Rustup owns the idempotency of the install and component commands.  The
    injectable dependencies keep this operation independent of the process
    environment for callers and tests.
    """
    if which("rustup") is None:
        raise RustupError("rustup is not available in PATH; install it before running setup")

    command_environment = dict(os.environ if environment is None else environment)
    default_result = _run(run, ("rustup", "default"), command_environment)
    toolchain = _default_toolchain(default_result)

    if toolchain is None:
        toolchain = "stable"
        _require_success(
            _run(
                run,
                (
                    "rustup",
                    "toolchain",
                    "install",
                    toolchain,
                    "--profile",
                    "default",
                    "--component",
                    "rust-analyzer",
                ),
                command_environment,
            ),
            ("rustup", "toolchain", "install", toolchain),
        )
        _require_success(
            _run(run, ("rustup", "default", toolchain), command_environment),
            ("rustup", "default", toolchain),
        )
    else:
        _require_success(
            _run(
                run,
                ("rustup", "component", "add", "rust-analyzer", "--toolchain", toolchain),
                command_environment,
            ),
            ("rustup", "component", "add", "rust-analyzer", "--toolchain", toolchain),
        )

    resolved_environment = {**command_environment, "RUSTUP_TOOLCHAIN": toolchain}
    resolved = _require_success(
        _run(run, ("rustup", "which", "rust-analyzer"), resolved_environment),
        ("rustup", "which", "rust-analyzer"),
    )
    path = resolved.stdout.strip()
    if not path:
        raise RustupError("rustup did not return a path for rust-analyzer")
    return Path(path)


def _run(
    run: CommandRunner,
    command: Command,
    environment: Mapping[str, str],
) -> subprocess.CompletedProcess[str]:
    return run(list(command), capture_output=True, check=False, env=environment, text=True)


def _default_toolchain(result: subprocess.CompletedProcess[str]) -> str | None:
    if result.returncode != 0:
        return None

    tokens = result.stdout.split()
    return tokens[0] if tokens else None


def _require_success(
    result: subprocess.CompletedProcess[str], command: Command
) -> subprocess.CompletedProcess[str]:
    if result.returncode == 0:
        return result

    details = result.stderr.strip() or result.stdout.strip() or "no diagnostic output"
    raise RustupError(f"{' '.join(command)} failed: {details}")
