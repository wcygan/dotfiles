from __future__ import annotations

import contextlib
import hashlib
import json
import os
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from dotfiles_setup.paths import UserPathContext

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

    def comes_from(self, repo_root: Path) -> bool:
        """Return whether this element has the exact checkout source."""

        return self.original_path == repo_root.resolve()

    def executable(self, command: str) -> Path | None:
        """Return an executable from this element's reported store outputs."""

        return next(
            (
                candidate
                for store_path in self.store_paths
                if (candidate := store_path / "bin" / command).is_file()
                and os.access(candidate, os.X_OK)
            ),
            None,
        )


def _nix_command(*args: str) -> list[str]:
    return [
        "nix",
        "--extra-experimental-features",
        "nix-command flakes",
        *args,
    ]


def _run(
    runner: Runner,
    args: Sequence[str],
    environment: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        kwargs: dict[str, object] = {
            "check": True,
            "text": True,
            "capture_output": True,
        }
        if environment is not None:
            kwargs["env"] = environment
        return runner(args, **kwargs)
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


def select_current_checkout_profile(
    elements: Sequence[ProfileElement],
    repo_root: Path,
    *,
    active_only: bool,
) -> ProfileElement | None:
    """Select the exact checkout profile under the stated active policy."""

    return next(
        (
            element
            for element in elements
            if (not active_only or element.active) and element.comes_from(repo_root)
        ),
        None,
    )


def list_profile_elements(
    *,
    runner: Runner = subprocess.run,
    environment: Mapping[str, str] | None = None,
) -> tuple[ProfileElement, ...]:
    """Return the user profile inventory with source and output identity intact."""

    result = _run(
        runner,
        _nix_command("profile", "list", "--json"),
        environment,
    )
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


class ProfileState(StrEnum):
    """The checkout's element in the user Nix profile."""

    ABSENT = "absent"
    ACTIVE = "active"
    INACTIVE = "inactive"


class ProfileAction(StrEnum):
    """What the install must do for one profile state."""

    ADD = "add"
    UPGRADE = "upgrade"
    BLOCKED = "blocked"


PROFILE_ACTIONS: Mapping[ProfileState, ProfileAction] = {
    ProfileState.ABSENT: ProfileAction.ADD,
    ProfileState.ACTIVE: ProfileAction.UPGRADE,
    ProfileState.INACTIVE: ProfileAction.BLOCKED,
}


def profile_state(inventory: Sequence[ProfileElement], repo_root: Path) -> ProfileState:
    """Return the one state for this checkout's profile element."""

    if select_current_checkout_profile(inventory, repo_root, active_only=True) is not None:
        return ProfileState.ACTIVE
    if select_current_checkout_profile(inventory, repo_root, active_only=False) is not None:
        return ProfileState.INACTIVE
    return ProfileState.ABSENT


def _flake_fingerprint(repo_root: Path) -> str | None:
    """Identify the checkout and the two files that decide its default package.

    flake.nix reads nothing else from the checkout, so with a complete
    flake.lock these files fix the package's store path.
    """

    digest = hashlib.sha256(os.fsencode(repo_root.resolve()))
    for name in ("flake.nix", "flake.lock"):
        try:
            content = (repo_root / name).read_bytes()
        except OSError:
            return None
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def _record_path(environment: Mapping[str, str] | None) -> Path:
    return UserPathContext.from_environment(environment).state_directory / "nix-profile.json"


def _is_current(element: ProfileElement, record_path: Path, fingerprint: str | None) -> bool:
    """Return whether the last upgrade already installed these flake files.

    Every doubt answers no, which costs one ordinary upgrade.
    """

    if fingerprint is None or not element.store_paths:
        return False
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return (
        isinstance(record, dict)
        and record.get("fingerprint") == fingerprint
        and record.get("store_paths") == [str(path) for path in element.store_paths]
        and all(path.exists() for path in element.store_paths)
    )


def _record_current(
    repo_root: Path,
    record_path: Path,
    fingerprint: str | None,
    runner: Runner,
    environment: Mapping[str, str] | None,
) -> None:
    """Remember which store paths the profile holds for these flake files."""

    if fingerprint is None or _flake_fingerprint(repo_root) != fingerprint:
        return
    try:
        # An incomplete flake.lock lets Nix pick new inputs on every upgrade,
        # so the flake files would not fix the result.
        _run(
            runner,
            _nix_command(
                "flake", "metadata", "--no-update-lock-file", "--json", str(repo_root.resolve())
            ),
            environment,
        )
        inventory = list_profile_elements(runner=runner, environment=environment)
    except NixProfileError:
        return
    element = select_current_checkout_profile(inventory, repo_root, active_only=True)
    if element is None or not element.store_paths:
        return
    record = {
        "fingerprint": fingerprint,
        "store_paths": [str(path) for path in element.store_paths],
    }
    temporary = record_path.with_name(f"{record_path.name}.{os.getpid()}")
    with contextlib.suppress(OSError):
        record_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        temporary.write_text(json.dumps(record), encoding="utf-8")
        temporary.replace(record_path)


def ensure_profile(
    repo_root: Path,
    *,
    runner: Runner = subprocess.run,
    environment: Mapping[str, str] | None = None,
    skip_when_current: bool = False,
) -> str:
    """Add or upgrade this checkout's profile element.

    Install passes ``skip_when_current`` so an unchanged flake costs nothing.
    The explicit profile command always upgrades, which is how to force one.
    """

    inventory = list_profile_elements(runner=runner, environment=environment)
    state = profile_state(inventory, repo_root)
    action = PROFILE_ACTIONS[state]
    fingerprint = _flake_fingerprint(repo_root)
    record_path = _record_path(environment)

    if action is ProfileAction.UPGRADE:
        element = select_current_checkout_profile(inventory, repo_root, active_only=True)
        assert element is not None
        if skip_when_current and _is_current(element, record_path, fingerprint):
            return f"Nix profile element is current: {element.name}"
        _run(
            runner,
            _nix_command("profile", "upgrade", element.name, "--no-write-lock-file"),
            environment,
        )
        _record_current(repo_root, record_path, fingerprint, runner, environment)
        return f"Upgraded Nix profile element: {element.name}"

    if action is ProfileAction.BLOCKED:
        inactive = select_current_checkout_profile(inventory, repo_root, active_only=False)
        assert inactive is not None
        raise NixProfileError(
            f"Nix profile element {inactive.name!r} for this checkout is inactive; "
            f"remove it with `nix profile remove {inactive.name}` and rerun "
            "./bootstrap.sh profile"
        )

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
        environment,
    )
    _record_current(repo_root, record_path, fingerprint, runner, environment)
    return f"Added Nix profile from: {flake_reference}"
