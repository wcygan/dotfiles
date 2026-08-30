"""Strict post-installation verification for repository-managed state."""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.links import managed_links
from dotfiles_setup.nix_profile import (
    NixProfileError,
    ProfileElement,
    list_profile_elements,
    select_current_checkout_profile,
)
from dotfiles_setup.paths import UserPathContext
from dotfiles_setup.rustup import RustupError, load_rust_toolchain, resolve_rust_analyzer

ProfileLoader = Callable[[], tuple[ProfileElement, ...]]
CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
Output = Callable[[str], None]

REQUIRED_PROFILE_BINARIES = (
    "python3",
    "uv",
    "fish",
    "direnv",
    "starship",
    "rustup",
    "git",
    "rg",
    "nvim",
)


@dataclass(frozen=True)
class VerificationResult:
    """One required installation postcondition."""

    name: str
    passed: bool
    message: str


def _observed_profiles(elements: tuple[ProfileElement, ...]) -> str:
    if not elements:
        return "none"
    return ", ".join(
        f"{element.name} -> {element.original_url or '(unknown source)'}" for element in elements
    )


def _profile_results(
    repo_root: Path,
    elements: tuple[ProfileElement, ...],
    required_binaries: Iterable[str],
    command_runner: CommandRunner,
    environment: Mapping[str, str],
) -> list[VerificationResult]:
    required = tuple(required_binaries)
    element = select_current_checkout_profile(elements, repo_root, active_only=True)
    if element is None:
        observed = _observed_profiles(elements)
        remediation = "run ./bootstrap.sh profile from this checkout"
        return [
            VerificationResult(
                "nix-profile",
                False,
                f"no active profile element comes from {repo_root.resolve()}; "
                f"observed: {observed}; {remediation}",
            ),
            VerificationResult(
                "profile-binaries",
                False,
                f"cannot verify installed binaries without this checkout's profile; {remediation}",
            ),
            VerificationResult(
                "python-runtime",
                False,
                f"cannot verify Python 3.13 without this checkout's profile; {remediation}",
            ),
        ]

    identity = VerificationResult(
        "nix-profile",
        True,
        f"profile element {element.name!r} comes from {element.original_url or '(unknown source)'}",
    )
    resolved_binaries = {command: element.executable(command) for command in required}
    missing = [command for command, path in resolved_binaries.items() if path is None]
    if missing:
        binaries = VerificationResult(
            "profile-binaries",
            False,
            f"profile element {element.name!r} is missing required binaries: "
            f"{', '.join(missing)}; run ./bootstrap.sh profile",
        )
    elif not element.store_paths:
        binaries = VerificationResult(
            "profile-binaries",
            False,
            f"profile element {element.name!r} reported no store paths; run ./bootstrap.sh profile",
        )
    else:
        binaries = VerificationResult(
            "profile-binaries",
            True,
            f"profile element {element.name!r} provides {', '.join(required)} "
            f"from {', '.join(str(path) for path in element.store_paths)}",
        )
    python = resolved_binaries.get("python3")
    if python is None:
        python_result = VerificationResult(
            "python-runtime",
            False,
            f"profile element {element.name!r} does not provide Python 3.13",
        )
    else:
        try:
            completed = command_runner(
                [str(python), "--version"],
                check=False,
                text=True,
                capture_output=True,
                env=environment,
            )
            version = (completed.stdout or completed.stderr).strip()
        except OSError as error:
            completed = None
            version = str(error)
        if completed is None or completed.returncode != 0 or not version.startswith("Python 3.13."):
            python_result = VerificationResult(
                "python-runtime",
                False,
                f"profile Python at {python} is not Python 3.13 "
                f"(observed: {version or 'no output'}); run ./bootstrap.sh profile",
            )
        else:
            python_result = VerificationResult(
                "python-runtime", True, f"profile Python is {version} at {python}"
            )
    return [identity, binaries, python_result]


def _link_result(source: Path, destination: Path) -> VerificationResult:
    name = f"link:{destination}"
    if not destination.is_symlink():
        if destination.exists():
            state = "unmanaged destination exists and is not a symlink"
        else:
            state = "managed destination is absent"
        return VerificationResult(name, False, f"{destination}: {state}; run ./bootstrap.sh link")

    try:
        target = destination.resolve(strict=False)
        target_exists = destination.exists()
    except (OSError, RuntimeError) as error:
        return VerificationResult(
            name,
            False,
            f"{destination}: broken symlink cannot be resolved ({error}); run ./bootstrap.sh link",
        )
    if not target_exists:
        return VerificationResult(
            name,
            False,
            f"{destination}: broken symlink resolves to {target}; run ./bootstrap.sh link",
        )
    try:
        expected = source.resolve()
    except (OSError, RuntimeError) as error:
        return VerificationResult(
            name,
            False,
            f"{destination}: repository source {source} cannot be resolved ({error})",
        )
    if target != expected:
        return VerificationResult(
            name,
            False,
            f"{destination}: stale symlink resolves to {target}, expected {expected}; "
            "run ./bootstrap.sh link",
        )
    return VerificationResult(name, True, f"{destination} resolves to {expected}")


def _codex_config_result(codex_home: Path) -> VerificationResult:
    destination = codex_home / "config.toml"
    if destination.is_symlink():
        return VerificationResult(
            "codex-config",
            False,
            f"{destination} is a symlink; run ./bootstrap.sh link to migrate it to a local file",
        )
    if not destination.exists():
        return VerificationResult(
            "codex-config",
            False,
            f"{destination} is missing; run ./bootstrap.sh link",
        )
    if not destination.is_file():
        return VerificationResult(
            "codex-config",
            False,
            f"{destination} is not a regular local file; move it aside and run ./bootstrap.sh link",
        )
    return VerificationResult("codex-config", True, f"{destination} is a regular local file")


def _rust_analyzer_result(
    repo_root: Path,
    elements: tuple[ProfileElement, ...],
    command_runner: CommandRunner,
    environment: Mapping[str, str],
) -> VerificationResult:
    element = select_current_checkout_profile(elements, repo_root, active_only=True)
    if element is None:
        return VerificationResult(
            "rust-analyzer",
            False,
            "cannot verify pinned rust-analyzer without this checkout's active profile",
        )
    rustup = element.executable("rustup")
    if rustup is None:
        return VerificationResult(
            "rust-analyzer",
            False,
            f"profile element {element.name!r} does not provide rustup",
        )
    try:
        selected = load_rust_toolchain(repo_root)
        binary = resolve_rust_analyzer(
            rustup,
            selected,
            run=command_runner,
            environment=environment,
        )
    except RustupError as error:
        return VerificationResult("rust-analyzer", False, str(error))
    return VerificationResult(
        "rust-analyzer",
        True,
        f"rust-analyzer for pinned Rust {selected.channel} resolves to {binary}",
    )


def verify_installation(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    profile_loader: ProfileLoader | None = None,
    required_binaries: Iterable[str] = REQUIRED_PROFILE_BINARIES,
    command_runner: CommandRunner = subprocess.run,
) -> list[VerificationResult]:
    """Evaluate every required postcondition without mutating user state."""

    values = os.environ if environ is None else environ
    context = UserPathContext.from_environment(values, system=system)

    try:
        elements = (
            list_profile_elements(environment=values)
            if profile_loader is None
            else profile_loader()
        )
        profile_results = _profile_results(
            repo_root,
            elements,
            required_binaries,
            command_runner,
            values,
        )
        rust_result = _rust_analyzer_result(
            repo_root,
            elements,
            command_runner,
            values,
        )
    except (NixProfileError, OSError) as error:
        profile_results = [
            VerificationResult(
                "nix-profile",
                False,
                f"could not inspect the user profile: {error}; run ./bootstrap.sh profile",
            ),
            VerificationResult(
                "profile-binaries",
                False,
                "cannot verify installed binaries because the user profile could not be inspected",
            ),
            VerificationResult(
                "python-runtime",
                False,
                "cannot verify Python 3.13 because the user profile could not be inspected",
            ),
        ]
        rust_result = VerificationResult(
            "rust-analyzer",
            False,
            "cannot verify pinned rust-analyzer because the user profile could not be inspected",
        )

    link_results = [
        _link_result(link.source, link.destination)
        for link in managed_links(
            repo_root,
            home=context.home,
            config_home=context.config_home,
            codex_home=context.codex_home,
            system=context.platform,
        )
    ]
    return [
        *profile_results,
        rust_result,
        *link_results,
        _codex_config_result(context.codex_home),
    ]


def run_verify(
    repo_root: Path,
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    results: Iterable[VerificationResult] | None = None,
    output: Output = print,
) -> int:
    """Print strict results and fail if any postcondition is missing."""

    evaluated = (
        list(results)
        if results is not None
        else verify_installation(repo_root, environ=environ, system=system)
    )
    for result in evaluated:
        marker = "PASS" if result.passed else "FAIL"
        output(f"[{marker}] {result.message}")
    return 1 if any(not result.passed for result in evaluated) else 0
