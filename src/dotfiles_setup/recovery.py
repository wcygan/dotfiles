"""Safe inspection and application of interrupted link recovery."""

from __future__ import annotations

import hashlib
import os
import stat
import uuid
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from dotfiles_setup import links as link_inventory
from dotfiles_setup.errors import RecoveryError
from dotfiles_setup.manifest import _atomic_json, read_manifest, state_directory

Output = Callable[[str], None]


def _matches_link(path: Path, target: str) -> bool:
    try:
        return path.is_symlink() and os.readlink(path) == target
    except OSError:
        return False


def _restore_symlink(path: Path, target: str) -> None:
    temporary: Path | None = None
    for _ in range(20):
        candidate = path.parent / f".{path.name}.recover.{uuid.uuid4().hex}"
        try:
            os.symlink(target, candidate)
            temporary = candidate
            break
        except FileExistsError:
            continue
    if temporary is None:
        raise RecoveryError(f"cannot allocate a temporary recovery link for {path}")
    temporary_identity = temporary.lstat()
    try:
        os.replace(temporary, path)
    except OSError:
        try:
            metadata = temporary.lstat()
            if (
                metadata.st_dev == temporary_identity.st_dev
                and metadata.st_ino == temporary_identity.st_ino
            ):
                temporary.unlink()
        except OSError:
            pass
        raise


def _pending_manifest(environ: Mapping[str, str] | None) -> tuple[Path, dict[str, Any]] | None:
    directory = state_directory(environ)
    recovery = directory / "recovery-needed.json"
    active = directory / "current.json"
    if recovery.exists():
        value = read_manifest(recovery)
        if value["state"] == "recovery-needed":
            return recovery, value
    if active.exists():
        value = read_manifest(active)
        if value["state"] in {"applying", "recovery-needed"}:
            return active, value
    return None


def _allowed_links(manifest: dict[str, Any], environ: Mapping[str, str] | None) -> dict[Path, Path]:
    values = os.environ if environ is None else environ
    repository_value = manifest.get("repository_root")
    if not isinstance(repository_value, str):
        raise RecoveryError("recovery manifest has no valid repository root")
    repository_root = Path(repository_value).expanduser().resolve()
    home = link_inventory.resolve_home(values)
    config_home = link_inventory.resolve_config_home(home, values)
    codex_home = link_inventory.resolve_codex_home(home, values)
    inventory = link_inventory.managed_links(
        repository_root,
        home=home,
        config_home=config_home,
        codex_home=codex_home,
        system=os.uname().sysname,
    )
    return {link.destination: link.source for link in inventory}


def _recorded_path(value: str, label: str) -> Path:
    path = Path(value)
    normalized = Path(os.path.normpath(value))
    if not path.is_absolute() or path != normalized:
        raise RecoveryError(f"recovery manifest has a non-normalized {label}: {value}")
    return path


def _validate_entries(
    manifest: dict[str, Any],
    entries: list[Any],
    environ: Mapping[str, str] | None,
) -> None:
    allowed = _allowed_links(manifest, environ)
    values = os.environ if environ is None else environ
    home = link_inventory.resolve_home(values)
    codex_home = link_inventory.resolve_codex_home(home, values)
    shell_destinations = {
        home / ".bashrc",
        home / ".bash_profile",
        home / ".zshrc",
        home / ".zshenv",
    }
    for raw in entries:
        if not isinstance(raw, dict):
            raise RecoveryError("recovery manifest contains an invalid entry")
        destination_value = raw.get("destination")
        source_value = raw.get("source")
        if not isinstance(destination_value, str) or not isinstance(source_value, str):
            raise RecoveryError("recovery manifest entry has invalid paths")
        destination = _recorded_path(destination_value, "destination")
        if raw.get("entry_type") == "file":
            visible_value = raw.get("visible_destination")
            visible = (
                _recorded_path(visible_value, "visible destination")
                if isinstance(visible_value, str)
                else None
            )
            valid_scope = False
            if source_value == "shell-handoff":
                valid_scope = (
                    manifest.get("command") in {"shell-handoff", "install"}
                    and visible in shell_destinations
                    and destination.resolve(strict=False).is_relative_to(home.resolve())
                )
            elif source_value == "npmrc":
                valid_scope = (
                    manifest.get("command") in {"link", "install"}
                    and visible == home / ".npmrc"
                    and destination.resolve(strict=False).is_relative_to(home.resolve())
                )
            elif source_value == "codex-template":
                valid_scope = (
                    manifest.get("command") in {"link", "install"}
                    and visible == codex_home / "config.toml"
                    and destination == visible
                )
            if (
                not valid_scope
                or raw.get("prior_kind") not in {"absent", "file", "symlink"}
                or raw.get("result_kind") != "file"
            ):
                raise RecoveryError(
                    f"file recovery destination is outside the managed scope: {destination}"
                )
            assert visible is not None
            if source_value == "codex-template" and visible.is_symlink():
                if raw.get("prior_kind") != "symlink" or os.readlink(visible) != raw.get(
                    "prior_target"
                ):
                    raise RecoveryError(
                        f"Codex config symlink changed after interruption: {visible}"
                    )
            elif visible.is_symlink():
                if visible.resolve(strict=False) != destination:
                    raise RecoveryError(f"shell file symlink changed after interruption: {visible}")
            elif visible != destination:
                raise RecoveryError(f"shell file destination changed after interruption: {visible}")
            _validate_file_backup(raw, destination)
            continue
        expected_source = allowed.get(destination)
        source = _recorded_path(source_value, "source")
        if expected_source is None or source != expected_source:
            raise RecoveryError(
                f"recovery destination is outside the managed inventory: {destination}"
            )
        if raw.get("prior_kind") not in {"absent", "symlink", "file", "directory"}:
            raise RecoveryError(f"invalid prior state for recovery destination {destination}")
        if raw.get("result_kind") not in {"symlink", "absent"}:
            raise RecoveryError(f"invalid result state for recovery destination {destination}")
        backup_value = raw.get("backup")
        if backup_value is None:
            continue
        if not isinstance(backup_value, str):
            raise RecoveryError(f"invalid backup path for recovery destination {destination}")
        backup = _recorded_path(backup_value, "backup")
        if backup.parent != destination.parent or not backup.name.startswith(
            f"{destination.name}.backup."
        ):
            raise RecoveryError(f"backup is outside the expected destination directory: {backup}")
        if backup.exists() or backup.is_symlink():
            metadata = backup.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                raise RecoveryError(f"recovery backup must not be a symlink: {backup}")
            if metadata.st_dev != raw.get("prior_device") or metadata.st_ino != raw.get(
                "prior_inode"
            ):
                raise RecoveryError(f"recovery backup identity changed: {backup}")


def _file_hash(path: Path) -> str | None:
    try:
        if not path.is_file() or path.is_symlink():
            return None
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _validate_file_backup(raw: dict[str, Any], destination: Path) -> None:
    backup_value = raw.get("backup")
    if backup_value is None:
        return
    if not isinstance(backup_value, str):
        raise RecoveryError(f"invalid backup path for shell file {destination}")
    backup = _recorded_path(backup_value, "file backup")
    if backup.parent != destination.parent or not backup.name.startswith(
        f"{destination.name}.backup."
    ):
        raise RecoveryError(f"shell backup is outside the destination directory: {backup}")
    if backup.is_symlink():
        raise RecoveryError(f"file recovery backup must not be a symlink: {backup}")


def _matches_file_prior(destination: Path, raw: dict[str, Any]) -> bool:
    if raw.get("prior_kind") == "absent":
        return not (destination.exists() or destination.is_symlink())
    if raw.get("prior_kind") == "symlink":
        try:
            return destination.is_symlink() and os.readlink(destination) == raw.get("prior_target")
        except OSError:
            return False
    return _file_hash(destination) == raw.get("prior_hash")


def _matches_prior(destination: Path, raw: dict[str, Any]) -> bool:
    prior_kind = raw.get("prior_kind")
    if prior_kind == "absent":
        return not (destination.exists() or destination.is_symlink())
    if prior_kind == "symlink":
        try:
            return destination.is_symlink() and os.readlink(destination) == raw.get("prior_target")
        except OSError:
            return False
    try:
        metadata = destination.lstat()
    except OSError:
        return False
    return metadata.st_dev == raw.get("prior_device") and metadata.st_ino == raw.get("prior_inode")


def _persist_progress(
    path: Path,
    manifest: dict[str, Any],
    environ: Mapping[str, str] | None,
) -> None:
    manifest["state"] = "recovery-needed"
    _atomic_json(path, manifest)
    _atomic_json(state_directory(environ) / "recovery-needed.json", manifest)


def run_recovery(
    *,
    environ: Mapping[str, str] | None = None,
    apply: bool = False,
    yes: bool = False,
    output: Output = print,
) -> int:
    """Describe or explicitly apply recovery for the latest interrupted operation."""

    pending = _pending_manifest(environ)
    if pending is None:
        output("No interrupted dotfiles operation needs recovery.")
        return 0
    path, manifest = pending
    entries = manifest.get("entries", [])
    if not isinstance(entries, list):
        raise RecoveryError(f"invalid recovery entries in {path}")
    _validate_entries(manifest, entries, environ)
    output(f"Recovery is needed for {manifest.get('command', 'setup')} ({path}).")
    for raw in entries:
        if not isinstance(raw, dict) or not raw.get("mutation_started"):
            continue
        destination = raw.get("destination")
        backup = raw.get("backup")
        action = (
            f"restore {backup}"
            if backup
            else "restore the prior file state"
            if raw.get("entry_type") == "file"
            else "restore the prior link state"
        )
        output(f"- {destination}: {action}")
    if not any(isinstance(raw, dict) and raw.get("mutation_started") for raw in entries):
        output(
            "No reversible link entries were recorded. Inspect the command's external state; "
            "an authorized apply acknowledges the current state but does not undo it."
        )
    if manifest.get("command") in {"install", "profile"}:
        output(
            "Package changes are not reversed automatically; use `nix profile rollback` if needed."
        )
    if not apply:
        output("Dry run only. Apply with: ./bootstrap.sh recover --apply --yes")
        return 0
    if not yes:
        raise RecoveryError("recovery mutation requires both --apply and --yes")

    _persist_progress(path, manifest, environ)

    unresolved: list[str] = []
    for raw in reversed(entries):
        if not isinstance(raw, dict) or not raw.get("mutation_started") or raw.get("recovered"):
            continue
        destination = Path(str(raw["destination"]))
        if raw.get("entry_type") == "file":
            if _matches_file_prior(destination, raw):
                raw["recovered"] = True
                _persist_progress(path, manifest, environ)
                output(f"Already recovered {destination}")
                continue
            current_hash = _file_hash(destination)
            if current_hash != raw.get("result_hash"):
                unresolved.append(
                    f"{destination}: current file changed; manual intervention required"
                )
                continue
            backup_value = raw.get("backup")
            backup = Path(str(backup_value)) if backup_value else None
            try:
                if backup is not None and backup.exists():
                    if _file_hash(backup) != raw.get("prior_hash"):
                        unresolved.append(
                            f"{destination}: backup contents changed; manual intervention required"
                        )
                        continue
                    os.replace(backup, destination)
                elif raw.get("prior_kind") == "symlink" and isinstance(
                    raw.get("prior_target"), str
                ):
                    _restore_symlink(destination, str(raw["prior_target"]))
                elif raw.get("prior_kind") == "absent":
                    destination.unlink()
                else:
                    unresolved.append(
                        f"{destination}: shell backup is missing; manual intervention required"
                    )
                    continue
                raw["recovered"] = True
                _persist_progress(path, manifest, environ)
                output(f"Recovered {destination}")
            except OSError as error:
                unresolved.append(f"{destination}: {error}; manual intervention required")
            continue
        result_target = str(raw.get("result_target", ""))
        backup_value = raw.get("backup")
        backup = Path(str(backup_value)) if backup_value else None
        prior_kind = raw.get("prior_kind")
        prior_target = raw.get("prior_target")
        result_kind = raw.get("result_kind")
        if _matches_prior(destination, raw):
            raw["recovered"] = True
            _persist_progress(path, manifest, environ)
            output(f"Already recovered {destination}")
            continue
        current_expected = (
            not (destination.exists() or destination.is_symlink())
            if result_kind == "absent"
            else _matches_link(destination, result_target)
        )

        try:
            if backup is not None and backup.exists():
                if not current_expected and (destination.exists() or destination.is_symlink()):
                    unresolved.append(f"{destination}: current state changed; preserved {backup}")
                    continue
                if current_expected:
                    destination.unlink()
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(backup, destination)
            elif prior_kind == "symlink" and isinstance(prior_target, str):
                if not current_expected:
                    unresolved.append(
                        f"{destination}: current state changed; prior link not restored"
                    )
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                if result_kind == "absent":
                    os.symlink(prior_target, destination)
                else:
                    _restore_symlink(destination, prior_target)
            elif prior_kind == "absent":
                if not current_expected:
                    unresolved.append(f"{destination}: current state changed; link not removed")
                    continue
                destination.unlink()
            else:
                unresolved.append(f"{destination}: backup is missing; manual intervention required")
                continue
            raw["recovered"] = True
            _persist_progress(path, manifest, environ)
            output(f"Recovered {destination}")
        except OSError as error:
            unresolved.append(f"{destination}: {error}; manual intervention required")

    if unresolved:
        for message in unresolved:
            output(f"[FAIL] {message}")
        _persist_progress(path, manifest, environ)
        raise RecoveryError(f"recovery remains incomplete; manifest preserved at {path}")

    manifest["state"] = "completed"
    _atomic_json(state_directory(environ) / "current.json", manifest)
    _atomic_json(state_directory(environ) / "completed.json", manifest)
    recovery_path = state_directory(environ) / "recovery-needed.json"
    recovery_path.unlink(missing_ok=True)
    output("Recovery completed. Re-running recovery is safe.")
    return 0
