from __future__ import annotations

import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

Runner = Callable[..., subprocess.CompletedProcess[str]]


class NixProfileError(RuntimeError):
    """Raised when the user Nix profile cannot be inspected or updated."""


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
    if parsed.scheme != "file":
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


def ensure_profile(
    repo_root: Path,
    *,
    runner: Runner = subprocess.run,
) -> str:
    list_result = _run(runner, _nix_command("profile", "list", "--json"))
    elements = _profile_elements(list_result.stdout)
    element_name = find_profile_element(elements, repo_root)

    if element_name is not None:
        _run(runner, _nix_command("profile", "upgrade", element_name))
        return f"Upgraded Nix profile element: {element_name}"

    flake_reference = f"{repo_root.resolve()}#default"
    _run(
        runner,
        _nix_command("profile", "add", flake_reference, "--priority", "5"),
    )
    return f"Added Nix profile from: {flake_reference}"
