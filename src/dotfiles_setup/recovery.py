"""Safe inspection and application of interrupted link recovery."""

from __future__ import annotations

import os
import stat
from collections.abc import Callable, Mapping
from dataclasses import replace
from pathlib import Path

from dotfiles_setup import links as link_inventory
from dotfiles_setup.errors import RecoveryError
from dotfiles_setup.manifest import ManifestRepository
from dotfiles_setup.mutations import (
    DirectoryRecoveryRecord,
    FileRecoveryRecord,
    LinkRecoveryRecord,
    MutationExecutionError,
    MutationRecordError,
    RecoveryRecord,
    decode_recovery_record,
    prepare_recovery_record,
    recover_mutation,
)
from dotfiles_setup.paths import UserPathContext

Output = Callable[[str], None]


def _allowed_links(
    manifest: dict[str, object],
    environ: Mapping[str, str] | None,
    system: str | None,
) -> dict[Path, Path]:
    values = os.environ if environ is None else environ
    repository_value = manifest.get("repository_root")
    if not isinstance(repository_value, str):
        raise RecoveryError("recovery manifest has no valid repository root")
    repository_root = Path(repository_value).expanduser().resolve()
    context = UserPathContext.from_environment(values, system=system)
    inventory = link_inventory.managed_links(
        repository_root,
        home=context.home,
        config_home=context.config_home,
        codex_home=context.codex_home,
        system=context.platform,
    )
    return {link.destination: link.source for link in inventory}


def _recorded_path(value: str, label: str) -> Path:
    path = Path(value)
    normalized = Path(os.path.normpath(value))
    if not path.is_absolute() or path != normalized:
        raise RecoveryError(f"recovery manifest has a non-normalized {label}: {value}")
    return path


def _validate_file_entry(
    manifest: dict[str, object],
    record: FileRecoveryRecord,
    destination: Path,
    *,
    home: Path,
    codex_home: Path,
    shell_destinations: set[Path],
) -> None:
    visible = _recorded_path(str(record.visible_destination), "visible destination")
    source = record.source
    valid_scope = False
    if source == "shell-handoff":
        valid_scope = (
            manifest.get("command") in {"shell-handoff", "install"}
            and visible in shell_destinations
            and destination.resolve(strict=False).is_relative_to(home.resolve())
        )
    elif source == "npmrc":
        valid_scope = (
            manifest.get("command") in {"link", "install"}
            and visible == home / ".npmrc"
            and destination.resolve(strict=False).is_relative_to(home.resolve())
        )
    elif source == "codex-template":
        valid_scope = (
            manifest.get("command") in {"link", "install"}
            and visible == codex_home / "config.toml"
            and destination == visible
        )
    if (
        not valid_scope
        or record.prior_kind not in {"absent", "file", "symlink"}
        or record.result_kind != "file"
    ):
        raise RecoveryError(
            f"file recovery destination is outside the managed scope: {destination}"
        )
    if source == "codex-template" and visible.is_symlink():
        if record.prior_kind != "symlink" or os.readlink(visible) != record.prior_target:
            raise RecoveryError(f"Codex config symlink changed after interruption: {visible}")
    elif visible.is_symlink():
        if visible.resolve(strict=False) != destination:
            raise RecoveryError(f"shell file symlink changed after interruption: {visible}")
    elif visible != destination:
        raise RecoveryError(f"shell file destination changed after interruption: {visible}")
    _validate_file_backup(record, destination)


def _validate_link_entry(
    record: LinkRecoveryRecord,
    destination: Path,
    allowed: dict[Path, Path],
) -> None:
    expected_source = allowed.get(destination)
    source = _recorded_path(str(record.source), "source")
    if expected_source is None or source != expected_source:
        raise RecoveryError(
            f"recovery destination is outside the managed inventory: {destination}"
        )
    if record.prior_kind not in {"absent", "symlink", "file", "directory"}:
        raise RecoveryError(f"invalid prior state for recovery destination {destination}")
    if record.result_kind not in {"symlink", "absent"}:
        raise RecoveryError(f"invalid result state for recovery destination {destination}")
    if record.result_kind == "symlink" and record.result_target != str(expected_source):
        raise RecoveryError(f"invalid result target for recovery destination {destination}")
    backup = record.backup
    if backup is None:
        return
    backup = _recorded_path(str(backup), "backup")
    if backup.parent != destination.parent or not backup.name.startswith(
        f"{destination.name}.backup."
    ):
        raise RecoveryError(f"backup is outside the expected destination directory: {backup}")
    if backup.exists() or backup.is_symlink():
        metadata = backup.lstat()
        if stat.S_ISLNK(metadata.st_mode) and record.prior_kind != "symlink":
            raise RecoveryError(f"recovery backup has an invalid type: {backup}")
        if metadata.st_dev != record.prior_device or metadata.st_ino != record.prior_inode:
            raise RecoveryError(f"recovery backup identity changed: {backup}")


def _validate_entries(
    manifest: dict[str, object],
    entries: list[object],
    environ: Mapping[str, str] | None,
    system: str | None,
) -> tuple[list[RecoveryRecord], list[dict[Path, tuple[int, int]]]]:
    allowed = _allowed_links(manifest, environ, system)
    values = os.environ if environ is None else environ
    context = UserPathContext.from_environment(values, system=system)
    home = context.home
    codex_home = context.codex_home
    shell_destinations = {
        home / ".bashrc",
        home / ".bash_profile",
        home / ".zshrc",
        home / ".zshenv",
    }
    directory_destinations = _allowed_directories(
        allowed,
        home=home,
        config_home=context.config_home,
        codex_home=codex_home,
        shell_destinations=shell_destinations,
    )
    records: list[RecoveryRecord] = []
    root_candidates = (home, context.config_home, codex_home)
    roots = tuple(
        root
        for root in root_candidates
        if not any(
            root != other and root.is_relative_to(other) for other in root_candidates
        )
    )
    for raw in entries:
        if not isinstance(raw, dict):
            raise RecoveryError("recovery manifest contains an invalid entry")
        try:
            record = decode_recovery_record(raw)
        except MutationRecordError as error:
            raise RecoveryError(f"invalid recovery manifest entry: {error}") from error
        destination = _recorded_path(str(record.destination), "destination")
        _validate_managed_parent(destination, roots)
        records.append(record)
    planned_missing_roots = {
        record.destination
        for record in records
        if isinstance(record, DirectoryRecoveryRecord)
        and record.authority_root_was_missing
        and record.destination in roots
    }
    planned_directories = {
        record.destination
        for record in records
        if isinstance(record, DirectoryRecoveryRecord)
        and record.mutation_started
        and not record.recovered
    }
    for record in records:
        destination = record.destination
        _validate_result_backup(
            record,
            destination,
            roots,
            planned_missing_roots,
        )
        if isinstance(record, DirectoryRecoveryRecord):
            if destination not in directory_destinations:
                raise RecoveryError(
                    f"directory recovery destination is outside managed scope: {destination}"
                )
            _validate_stage(record, destination, roots, planned_missing_roots)
        elif isinstance(record, FileRecoveryRecord):
            _validate_file_entry(
                manifest,
                record,
                destination,
                home=home,
                codex_home=codex_home,
                shell_destinations=shell_destinations,
            )
            _validate_stage(record, destination, roots, planned_missing_roots)
        else:
            _validate_link_entry(record, destination, allowed)
    parent_identities = [
        _capture_recovery_parent_identities(record, planned_directories)
        if record.mutation_started and not record.recovered
        else {}
        for record in records
    ]
    return records, parent_identities


def _capture_recovery_parent_identities(
    record: RecoveryRecord,
    planned_directories: set[Path],
) -> dict[Path, tuple[int, int]]:
    """Capture each parent identity used by one recovery operation."""

    paths = {
        record.destination,
        *(
            path
            for path in (
                record.backup,
                record.result_backup,
                getattr(record, "stage_path", None),
            )
            if path is not None
        ),
    }
    if isinstance(record, FileRecoveryRecord) and record.visible_kind is not None:
        paths.add(record.visible_destination)
    identities: dict[Path, tuple[int, int]] = {}
    for parent in {path.parent for path in paths}:
        current = parent
        missing: list[Path] = []
        while True:
            try:
                metadata = current.lstat()
                break
            except FileNotFoundError:
                missing.append(current)
                if current.parent == current:
                    raise RecoveryError(
                        f"recovery parent is unavailable: {parent}"
                    ) from None
                current = current.parent
            except OSError as error:
                raise RecoveryError(
                    f"recovery parent is unavailable: {parent}"
                ) from error
        unplanned = tuple(path for path in missing if path not in planned_directories)
        if unplanned:
            raise RecoveryError(
                f"recovery parent is unavailable: {unplanned[0]}"
            )
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise RecoveryError(f"recovery parent is unsafe: {current}")
        identities[current] = (metadata.st_dev, metadata.st_ino)
    return identities


def _allowed_directories(
    allowed_links: Mapping[Path, Path],
    *,
    home: Path,
    config_home: Path,
    codex_home: Path,
    shell_destinations: set[Path],
) -> set[Path]:
    roots = (home, config_home, codex_home)
    destinations = {
        *allowed_links,
        *shell_destinations,
        home / ".npmrc",
        home / ".local" / "bin",
        home / ".local" / "lib",
        codex_home / "config.toml",
    }
    directories: set[Path] = set()
    for destination in destinations:
        candidate = (
            destination
            if destination.suffix == "" and destination.name in {"bin", "lib"}
            else destination.parent
        )
        for root in roots:
            if candidate.is_relative_to(root):
                while candidate.is_relative_to(root):
                    directories.add(candidate)
                    if candidate == root:
                        break
                    candidate = candidate.parent
                break
    return directories


def _validate_file_backup(record: FileRecoveryRecord, destination: Path) -> None:
    backup = record.backup
    if backup is None:
        return
    backup = _recorded_path(str(backup), "file backup")
    if backup.parent != destination.parent or not backup.name.startswith(
        f"{destination.name}.backup."
    ):
        raise RecoveryError(f"shell backup is outside the destination directory: {backup}")
    if not (backup.exists() or backup.is_symlink()):
        return
    metadata = backup.lstat()
    expected_type_matches = (
        record.prior_kind == "file" and stat.S_ISREG(metadata.st_mode)
    ) or (record.prior_kind == "symlink" and stat.S_ISLNK(metadata.st_mode))
    if not expected_type_matches:
        raise RecoveryError(f"file recovery backup has an invalid type: {backup}")
    if (
        record.prior_device is not None
        and record.prior_inode is not None
        and (metadata.st_dev, metadata.st_ino)
        != (record.prior_device, record.prior_inode)
    ):
        raise RecoveryError(f"file recovery backup identity changed: {backup}")
    if (
        record.prior_kind == "file"
        and record.prior_mode is not None
        and stat.S_IMODE(metadata.st_mode) != record.prior_mode
    ):
        raise RecoveryError(f"file recovery backup mode changed: {backup}")


def _validate_result_backup(
    record: RecoveryRecord,
    destination: Path,
    roots: tuple[Path, ...],
    planned_missing_roots: set[Path],
) -> None:
    result_backup = record.result_backup
    if result_backup is None:
        return
    result_backup = _recorded_path(str(result_backup), "result quarantine")
    candidates = tuple(
        root for root in roots if destination == root or destination.is_relative_to(root)
    )
    root = max(candidates, key=lambda item: len(item.parts), default=None)
    managed_parent = (
        root is not None
        and result_backup.parent.is_relative_to(root)
        and destination.parent.is_relative_to(result_backup.parent)
    )
    root_parent = (
        root is not None
        and root in planned_missing_roots
        and result_backup.parent == root.parent
    )
    if not (managed_parent or root_parent) or not result_backup.name.startswith(
        f".{destination.name}.dotfiles-result."
    ):
        raise RecoveryError(
            f"result quarantine is outside the managed destination path: {result_backup}"
        )
    if root_parent:
        try:
            metadata = result_backup.parent.lstat()
        except OSError as error:
            raise RecoveryError(
                f"result quarantine parent is unavailable: {result_backup.parent}"
            ) from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise RecoveryError(
                f"result quarantine parent is unsafe: {result_backup.parent}"
            )
        return
    _validate_managed_parent(result_backup, roots)


def _validate_stage(
    record: FileRecoveryRecord | DirectoryRecoveryRecord,
    destination: Path,
    roots: tuple[Path, ...],
    planned_missing_roots: set[Path],
) -> None:
    stage = record.stage_path
    if stage is None:
        return
    stage = _recorded_path(str(stage), "stage path")
    if not stage.name.startswith(f".{destination.name}.dotfiles."):
        raise RecoveryError(f"stage path has an invalid name: {stage}")
    candidates = tuple(
        root for root in roots if destination == root or destination.is_relative_to(root)
    )
    root = max(candidates, key=lambda item: len(item.parts), default=None)
    if (
        root is not None
        and root in planned_missing_roots
        and stage.parent == root.parent
    ):
        try:
            metadata = stage.parent.lstat()
        except OSError as error:
            raise RecoveryError(f"stage parent is unavailable: {stage.parent}") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise RecoveryError(f"stage parent is unsafe: {stage.parent}")
        return
    _validate_managed_parent(stage, roots)


def _validate_managed_parent(destination: Path, roots: tuple[Path, ...]) -> None:
    candidates = tuple(
        root for root in roots if destination == root or destination.is_relative_to(root)
    )
    if not candidates:
        raise RecoveryError(
            f"recovery destination is outside the managed inventory path roots: {destination}"
        )
    root = max(candidates, key=lambda item: len(item.parts))
    try:
        root_metadata = root.lstat()
    except FileNotFoundError:
        try:
            parent_metadata = root.parent.lstat()
        except OSError as error:
            raise RecoveryError(f"managed path root is unavailable: {root}") from error
        if stat.S_ISLNK(parent_metadata.st_mode) or not stat.S_ISDIR(
            parent_metadata.st_mode
        ):
            raise RecoveryError(
                f"managed path root parent is unsafe: {root.parent}"
            ) from None
        return
    except OSError as error:
        raise RecoveryError(f"managed path root is unavailable: {root}") from error
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
        raise RecoveryError(f"managed path root is unsafe: {root}")
    if destination == root:
        return
    current = root
    for part in destination.parent.relative_to(root).parts:
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        except OSError as error:
            raise RecoveryError(f"cannot inspect recovery parent path: {current}") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise RecoveryError(f"recovery parent path is unsafe: {current}")


def _persist_progress(
    repository: ManifestRepository,
    path: Path,
    manifest: dict[str, object],
) -> None:
    repository.checkpoint_recovery(path, manifest)


def _report_recovery(
    path: Path,
    manifest: dict[str, object],
    entries: list[RecoveryRecord],
    output: Output,
) -> None:
    output(f"Recovery is needed for {manifest.get('command', 'setup')} ({path}).")
    for record in entries:
        if not record.mutation_started:
            continue
        destination = record.destination
        backup = record.backup
        action = (
            f"restore {backup}"
            if backup
            else "restore the prior file state"
            if isinstance(record, FileRecoveryRecord)
            else "restore the prior link state"
        )
        output(f"- {destination}: {action}")
    if not any(record.mutation_started for record in entries):
        output(
            "No reversible link entries were recorded. Inspect the command's external state; "
            "an authorized apply acknowledges the current state but does not undo it."
        )
    if manifest.get("command") in {"install", "profile"}:
        output(
            "Package changes are not reversed automatically; use `nix profile rollback` if needed."
        )
    if manifest.get("command") == "agent-skills":
        output(
            "Agent skill changes are not reversed automatically; inspect them with "
            "`./bootstrap.sh agent-skills --check` before acknowledging recovery."
        )


def _mark_recovered(
    repository: ManifestRepository,
    path: Path,
    manifest: dict[str, object],
    index: int,
    record: RecoveryRecord,
    destination: Path,
    output: Output,
    *,
    already: bool,
) -> None:
    repository.checkpoint_entry_recovery(
        path,
        manifest,
        index,
        replace(record, recovered=True),
    )
    suffix = _retained_quarantine_suffix(record)
    output(f"{'Already recovered' if already else 'Recovered'} {destination}{suffix}")


def _retained_quarantine_suffix(record: RecoveryRecord) -> str:
    """Report every recorded stage or result quarantine that still exists."""

    retained = tuple(
        path
        for path in (
            getattr(record, "stage_path", None),
            record.result_backup,
        )
        if path is not None and (path.exists() or path.is_symlink())
    )
    return f"; retained quarantine: {', '.join(map(str, retained))}" if retained else ""


def _unapplied_record_has_verified_missing_parent(
    record: RecoveryRecord,
    parent_identities: Mapping[Path, tuple[int, int]],
) -> bool:
    """Accept a prior absent state under a parent that validation found absent."""

    destination_parent = record.destination.parent
    if record.applied or record.prior_kind != "absent":
        return False
    if destination_parent in parent_identities:
        return False
    ancestors = tuple(
        path
        for path in parent_identities
        if destination_parent.is_relative_to(path)
    )
    if not ancestors:
        return False
    ancestor = max(ancestors, key=lambda path: len(path.parts))
    relative_parts = destination_parent.relative_to(ancestor).parts
    if not relative_parts:
        return False
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(ancestor, flags)
    try:
        metadata = os.fstat(descriptor)
        if (metadata.st_dev, metadata.st_ino) != parent_identities[ancestor]:
            raise MutationExecutionError(
                f"destination parent changed: {ancestor}", restored=False
            )
        try:
            os.stat(
                relative_parts[0],
                dir_fd=descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            return True
        return False
    finally:
        os.close(descriptor)


def _recover_entry(
    repository: ManifestRepository,
    path: Path,
    manifest: dict[str, object],
    index: int,
    record: RecoveryRecord,
    output: Output,
    *,
    parent_identities: Mapping[Path, tuple[int, int]],
) -> str | None:
    destination = record.destination
    try:
        if _unapplied_record_has_verified_missing_parent(
            record,
            parent_identities,
        ):
            _mark_recovered(
                repository,
                path,
                manifest,
                index,
                record,
                destination,
                output,
                already=True,
            )
            return None
        prepared_record = prepare_recovery_record(
            record,
            expected_identities=parent_identities,
        )
    except MutationExecutionError as error:
        return (
            f"{destination}: {error}{_retained_quarantine_suffix(record)}; "
            "manual intervention required"
        )
    except OSError as error:
        return (
            f"{destination}: recovery path is unavailable: {error}"
            f"{_retained_quarantine_suffix(record)}; "
            "manual intervention required"
        )
    if prepared_record != record:
        repository.checkpoint_entry_recovery(
            path,
            manifest,
            index,
            prepared_record,
        )
    try:
        result = recover_mutation(
            prepared_record,
            expected_identities=parent_identities,
        )
    except MutationExecutionError as error:
        return (
            f"{destination}: {error}"
            f"{_retained_quarantine_suffix(prepared_record)}; "
            "manual intervention required"
        )
    except OSError as error:
        return (
            f"{destination}: recovery path is unavailable: {error}"
            f"{_retained_quarantine_suffix(prepared_record)}; "
            "manual intervention required"
        )
    recovered_record = result.record or prepared_record
    if not result.recovered:
        return (
            f"{destination}: {result.reason}"
            f"{_retained_quarantine_suffix(recovered_record)}; "
            "manual intervention required"
        )

    _mark_recovered(
        repository,
        path,
        manifest,
        index,
        recovered_record,
        destination,
        output,
        already=result.already_recovered,
    )
    return None


def run_recovery(
    *,
    environ: Mapping[str, str] | None = None,
    system: str | None = None,
    apply: bool = False,
    yes: bool = False,
    output: Output = print,
) -> int:
    """Describe or explicitly apply recovery for the latest interrupted operation."""

    repository = ManifestRepository.from_environment(environ)
    pending = repository.pending()
    if pending is None:
        output("No interrupted dotfiles operation needs recovery.")
        return 0
    path = pending.path
    manifest = pending.data
    entries = manifest.get("entries", [])
    if not isinstance(entries, list):
        raise RecoveryError(f"invalid recovery entries in {path}")
    records, parent_identities = _validate_entries(manifest, entries, environ, system)
    _report_recovery(path, manifest, records, output)
    if not apply:
        output("Dry run only. Apply with: ./bootstrap.sh recover --apply --yes")
        return 0
    if not yes:
        raise RecoveryError("recovery mutation requires both --apply and --yes")

    _persist_progress(repository, path, manifest)

    unresolved: list[str] = []
    for index in reversed(range(len(records))):
        record = records[index]
        if not record.mutation_started or record.recovered:
            continue
        message = _recover_entry(
            repository,
            path,
            manifest,
            index,
            record,
            output,
            parent_identities=parent_identities[index],
        )
        if message is not None:
            unresolved.append(message)

    if unresolved:
        for message in unresolved:
            output(f"[FAIL] {message}")
        _persist_progress(repository, path, manifest)
        raise RecoveryError(f"recovery remains incomplete; manifest preserved at {path}")

    repository.complete_recovery(manifest)
    output("Recovery completed. Re-running recovery is safe.")
    return 0
