from __future__ import annotations

import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

Runner = Callable[..., subprocess.CompletedProcess[str]]


class NixProfileError(RuntimeError):
    """Raised when the user Nix profile cannot be inspected or updated."""


@dataclass(frozen=True)
class ProfileElement:
    """Identity and outputs reported for one user-profile element."""

    name: str
    original_url: str | None
    store_paths: tuple[Path, ...]
    active: bool

    @property
    def original_path(self) -> Path | None:
        return _original_path(self.original_url)


def _nix_command(*args: str) -> list[str]:
    return [
        "nix",
        "--extra-experimental-features",
        "nix-command flakes",
        *args,
    ]


def _run(runner: Runner, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    try:
        return runner(args, check=True, text=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", None) or str(error)
        raise NixProfileError(f"Nix profile command failed: {detail.strip()}") from error


def _profile_elements(payload: str) -> Mapping[str, Mapping[str, Any]]:
    try:
        parsed = json.loads(payload)
        elements = parsed["elements"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise NixProfileError("nix profile list returned invalid JSON") from error

    if not isinstance(elements, dict):
        raise NixProfileError("nix profile list returned invalid elements")
    return elements


def _original_path(original_url: object) -> Path | None:
    if not isinstance(original_url, str):
        return None
    normalized = original_url.removeprefix("git+")
    parsed = urlparse(normalized)
    if parsed.scheme not in {"file", "path"}:
        return None
    return Path(unquote(parsed.path)).resolve()


def find_profile_element(
    elements: Mapping[str, Mapping[str, Any]],
    repo_root: Path,
) -> str | None:
    resolved_root = repo_root.resolve()
    for name, details in elements.items():
        if _original_path(details.get("originalUrl")) == resolved_root:
            return name
    return None


def list_profile_elements(
    *,
    runner: Runner = subprocess.run,
) -> tuple[ProfileElement, ...]:
    """Return the user profile inventory with source and output identity intact."""

    result = _run(runner, _nix_command("profile", "list", "--json"))
    elements = _profile_elements(result.stdout)
    inventory: list[ProfileElement] = []
    for name, details in elements.items():
        if not isinstance(name, str) or not isinstance(details, Mapping):
            raise NixProfileError("nix profile list returned an invalid element")
        active = details.get("active")
        if not isinstance(active, bool):
            raise NixProfileError(f"nix profile element {name!r} has invalid active state")
        original_url = details.get("originalUrl")
        raw_store_paths = details.get("storePaths")
        if not isinstance(raw_store_paths, list) or not all(
            isinstance(path, str) and Path(path).is_absolute() for path in raw_store_paths
        ):
            raise NixProfileError(f"nix profile element {name!r} has invalid store paths")
        store_paths = tuple(Path(path) for path in raw_store_paths)
        inventory.append(
            ProfileElement(
                name=name,
                original_url=original_url if isinstance(original_url, str) else None,
                store_paths=store_paths,
                active=active,
            )
        )
    return tuple(inventory)


def ensure_profile(
    repo_root: Path,
    *,
    runner: Runner = subprocess.run,
) -> str:
    list_result = _run(runner, _nix_command("profile", "list", "--json"))
    elements = _profile_elements(list_result.stdout)
    element_name = find_profile_element(elements, repo_root)

    if element_name is not None:
        _run(
            runner,
            _nix_command("profile", "upgrade", element_name, "--no-write-lock-file"),
        )
        return f"Upgraded Nix profile element: {element_name}"

    flake_reference = f"{repo_root.resolve()}#default"
    _run(
        runner,
        _nix_command(
            "profile",
            "add",
            flake_reference,
            "--priority",
            "5",
            "--no-write-lock-file",
        ),
    )
    return f"Added Nix profile from: {flake_reference}"
