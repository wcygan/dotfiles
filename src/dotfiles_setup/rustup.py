"""Install and resolve rust-analyzer from the repository-pinned toolchain."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tomllib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

Command = Sequence[str]
CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
CommandLocator = Callable[[str], str | None]

_EXACT_TOOLCHAIN = re.compile(r"^[1-9][0-9]*\.[0-9]+\.[0-9]+$")


class RustupError(RuntimeError):
    """Raised when the pinned Rust toolchain cannot be prepared or inspected."""


@dataclass(frozen=True)
class RustToolchain:
    channel: str
    profile: str
    components: tuple[str, ...]


@dataclass(frozen=True)
class RustupResult:
    toolchain: str
    binary: Path

    def __str__(self) -> str:
        return f"Rust {self.toolchain} rust-analyzer at {self.binary}"


def load_rust_toolchain(repo_root: Path) -> RustToolchain:
    """Read and validate the exact repository-owned Rust toolchain contract."""

    path = repo_root.resolve() / "rust-toolchain.toml"
    try:
        with path.open("rb") as file:
            payload = tomllib.load(file)
    except FileNotFoundError as error:
        raise RustupError(f"missing Rust toolchain configuration: {path}") from error
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise RustupError(f"cannot read Rust toolchain configuration {path}: {error}") from error

    toolchain = payload.get("toolchain")
    if not isinstance(toolchain, dict):
        raise RustupError(f"{path} must contain a [toolchain] table")
    channel = toolchain.get("channel")
    profile = toolchain.get("profile")
    components = toolchain.get("components")
    if not isinstance(channel, str) or _EXACT_TOOLCHAIN.fullmatch(channel) is None:
        raise RustupError(f"{path} must pin an exact numeric Rust channel")
    if profile not in {"minimal", "default", "complete"}:
        raise RustupError(f"{path} contains an unsupported Rust profile")
    if not isinstance(components, list) or not all(
        isinstance(component, str) for component in components
    ):
        raise RustupError(f"{path} must declare Rust components as strings")
    if "rust-analyzer" not in components:
        raise RustupError(f"{path} must include the rust-analyzer component")
    return RustToolchain(channel, profile, tuple(components))


def setup_rustup(
    repo_root: Path,
    *,
    run: CommandRunner = subprocess.run,
    which: CommandLocator = shutil.which,
    environment: Mapping[str, str] | None = None,
) -> RustupResult:
    """Install the exact pinned toolchain without changing the global default."""

    rustup = which("rustup")
    if rustup is None:
        raise RustupError("rustup is not available in PATH; run ./bootstrap.sh profile first")
    selected = load_rust_toolchain(repo_root)
    command_environment = _command_environment(environment)
    install = (
        rustup,
        "toolchain",
        "install",
        selected.channel,
        "--profile",
        selected.profile,
        "--component",
        "rust-analyzer",
        "--no-self-update",
    )
    _require_success(_run(run, install, command_environment), install)
    binary = resolve_rust_analyzer(Path(rustup), selected, run=run, environment=command_environment)
    return RustupResult(selected.channel, binary)


def resolve_rust_analyzer(
    rustup: Path,
    toolchain: RustToolchain,
    *,
    run: CommandRunner = subprocess.run,
    environment: Mapping[str, str] | None = None,
) -> Path:
    """Resolve rust-analyzer through an explicit toolchain, never a global default."""

    command = (
        str(rustup),
        "which",
        "--toolchain",
        toolchain.channel,
        "rust-analyzer",
    )
    result = _require_success(_run(run, command, _command_environment(environment)), command)
    value = result.stdout.strip()
    if not value:
        raise RustupError(
            f"rustup returned no rust-analyzer path for toolchain {toolchain.channel}; "
            "rerun when the Rust distribution cache or network is available"
        )
    path = Path(value)
    if not path.is_file() or not os.access(path, os.X_OK):
        raise RustupError(
            f"rustup resolved rust-analyzer for {toolchain.channel} to unusable path {path}; "
            "rerun ./bootstrap.sh rustup"
        )
    return path


def _command_environment(environment: Mapping[str, str] | None) -> dict[str, str]:
    values = dict(os.environ if environment is None else environment)
    values.pop("RUSTUP_TOOLCHAIN", None)
    return values


def _run(
    run: CommandRunner,
    command: Command,
    environment: Mapping[str, str],
) -> subprocess.CompletedProcess[str]:
    try:
        return run(list(command), capture_output=True, check=False, env=environment, text=True)
    except OSError as error:
        raise RustupError(
            f"{' '.join(command)} could not start: {error}; "
            "rerun when the Rust distribution cache or network is available"
        ) from error


def _require_success(
    result: subprocess.CompletedProcess[str], command: Command
) -> subprocess.CompletedProcess[str]:
    if result.returncode == 0:
        return result
    details = result.stderr.strip() or result.stdout.strip() or "no diagnostic output"
    raise RustupError(
        f"{' '.join(command)} failed: {details}; "
        "rerun when the Rust distribution cache or network is available"
    )
