"""Typed, content-free records for reversible setup mutations."""

from __future__ import annotations

import ctypes
import errno
import hashlib
import os
import stat
import sys
import time
import uuid
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Literal, Protocol


class MutationRecordError(ValueError):
    """A recovery entry does not match the supported schema."""


class MutationExecutionError(RuntimeError):
    """A planned mutation batch could not complete safely."""

    def __init__(self, message: str, *, restored: bool) -> None:
        super().__init__(message)
        self.restored = restored


def _required_string(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str):
        raise MutationRecordError(f"recovery entry has an invalid {key}")
    return value


def _optional_string(raw: Mapping[str, Any], key: str) -> str | None:
    value = raw.get(key)
    if value is not None and not isinstance(value, str):
        raise MutationRecordError(f"recovery entry has an invalid {key}")
    return value


def _optional_integer(raw: Mapping[str, Any], key: str) -> int | None:
    value = raw.get(key)
    if value is not None and (not isinstance(value, int) or isinstance(value, bool)):
        raise MutationRecordError(f"recovery entry has an invalid {key}")
    return value


def _progress(raw: Mapping[str, Any], key: str) -> bool:
    value = raw.get(key, False)
    if not isinstance(value, bool):
        raise MutationRecordError(f"recovery entry has an invalid {key}")
    return value


def _restored(raw: Mapping[str, Any]) -> bool | None:
    if "restored" not in raw:
        return None
    value = raw["restored"]
    if not isinstance(value, bool):
        raise MutationRecordError("recovery entry has an invalid restored flag")
    return value


def _progress_state(
    raw: Mapping[str, Any],
) -> tuple[bool, bool, bool, bool | None]:
    """Decode and validate one monotonic recovery progress state."""

    mutation_started = _progress(raw, "mutation_started")
    applied = _progress(raw, "applied")
    recovered = _progress(raw, "recovered")
    restored = _restored(raw)
    if applied and not mutation_started:
        raise MutationRecordError(
            "recovery entry is applied without a started mutation"
        )
    if restored is True and not recovered:
        raise MutationRecordError(
            "recovery entry is restored without completed recovery"
        )
    if restored is True and (mutation_started or applied):
        raise MutationRecordError(
            "recovery entry is restored while mutation progress remains active"
        )
    if recovered and not mutation_started and restored is not True:
        raise MutationRecordError(
            "recovery entry is recovered without a started mutation"
        )
    return mutation_started, applied, recovered, restored


@dataclass(frozen=True, kw_only=True)
class LinkRecoveryRecord:
    """Recovery metadata for one managed-link replacement or removal."""

    destination: Path
    source: Path
    prior_kind: str
    prior_target: str | None
    prior_device: int | None
    prior_inode: int | None
    backup: Path | None
    result_kind: str
    result_target: str | None
    result_backup: Path | None = None
    mutation_started: bool = False
    applied: bool = False
    recovered: bool = False
    restored: bool | None = None
    _extra_fields: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)
    _include_entry_type: bool = field(default=True, repr=False, compare=False)
    _present_fields: frozenset[str] | None = field(
        default=None, repr=False, compare=False
    )

    @property
    def entry_type(self) -> Literal["link"]:
        """Return the record discriminator."""

        return "link"

    def to_manifest(self) -> dict[str, Any]:
        """Return the schema-v1 dictionary without file contents."""

        value = dict(self._extra_fields)
        if self._include_entry_type:
            value["entry_type"] = "link"
        fields = {
            "destination": str(self.destination),
            "source": str(self.source),
            "prior_kind": self.prior_kind,
            "prior_target": self.prior_target,
            "prior_device": self.prior_device,
            "prior_inode": self.prior_inode,
            "backup": str(self.backup) if self.backup is not None else None,
            "result_kind": self.result_kind,
            "result_target": self.result_target,
            "mutation_started": self.mutation_started,
            "applied": self.applied,
            "recovered": self.recovered,
        }
        value.update(
            {
                key: item
                for key, item in fields.items()
                if self._present_fields is None
                or key in self._present_fields
                or (key in {"mutation_started", "applied", "recovered"} and item is True)
            }
        )
        if self.result_backup is not None:
            value["result_backup"] = str(self.result_backup)
        if self.restored is not None and (
            self._present_fields is None or "restored" in self._present_fields or self.restored
        ):
            value["restored"] = self.restored
        return value

    @classmethod
    def from_manifest(
        cls,
        raw: Mapping[str, Any],
        *,
        legacy: bool = False,
    ) -> LinkRecoveryRecord:
        """Decode a schema-v1 link entry."""

        mutation_started, applied, recovered, restored = _progress_state(raw)
        prior_kind = _required_string(raw, "prior_kind")
        prior_target = _optional_string(raw, "prior_target")
        prior_device = _optional_integer(raw, "prior_device")
        prior_inode = _optional_integer(raw, "prior_inode")
        backup_value = _optional_string(raw, "backup")
        backup = Path(backup_value) if backup_value is not None else None
        result_kind = _required_string(raw, "result_kind")
        result_target = _optional_string(raw, "result_target")
        result_backup_value = _optional_string(raw, "result_backup")
        result_backup = (
            Path(result_backup_value) if result_backup_value is not None else None
        )
        identity_is_complete = (prior_device is None) == (prior_inode is None)
        prior_state_is_valid = (
            prior_kind == "absent"
            and prior_target is None
            and prior_device is None
            and backup is None
        ) or (
            prior_kind == "symlink"
            and prior_target is not None
            and (
                backup is None
                or (backup is not None and prior_device is not None)
            )
        ) or (
            prior_kind in {"file", "directory"}
            and prior_target is None
            and prior_device is not None
            and backup is not None
        )
        if not identity_is_complete or not prior_state_is_valid:
            raise MutationRecordError("link recovery entry has an invalid prior state")
        result_state_is_valid = (
            result_kind == "symlink" and result_target is not None
        ) or (
            result_kind == "absent"
            and result_target is None
            and result_backup is None
        )
        if not result_state_is_valid:
            raise MutationRecordError("link recovery entry has an invalid result state")
        known = {
            "entry_type",
            "destination",
            "source",
            "prior_kind",
            "prior_target",
            "prior_device",
            "prior_inode",
            "backup",
            "result_backup",
            "result_kind",
            "result_target",
            "mutation_started",
            "applied",
            "recovered",
            "restored",
        }
        return cls(
            destination=Path(_required_string(raw, "destination")),
            source=Path(_required_string(raw, "source")),
            prior_kind=prior_kind,
            prior_target=prior_target,
            prior_device=prior_device,
            prior_inode=prior_inode,
            backup=backup,
            result_backup=result_backup,
            result_kind=result_kind,
            result_target=result_target,
            mutation_started=mutation_started,
            applied=applied,
            recovered=recovered,
            restored=restored,
            _extra_fields={key: value for key, value in raw.items() if key not in known},
            _include_entry_type=not legacy,
            _present_fields=frozenset(raw),
        )


@dataclass(frozen=True, kw_only=True)
class FileRecoveryRecord:
    """Recovery metadata for one local-file replacement."""

    destination: Path
    visible_destination: Path
    source: str
    prior_kind: str
    prior_target: str | None
    prior_hash: str | None
    prior_mode: int | None = None
    prior_device: int | None = None
    prior_inode: int | None = None
    backup: Path | None
    result_hash: str
    result_mode: int | None = None
    result_device: int | None = None
    result_inode: int | None = None
    visible_kind: str | None = None
    visible_target: str | None = None
    visible_device: int | None = None
    visible_inode: int | None = None
    result_backup: Path | None = None
    stage_path: Path | None = None
    stage_device: int | None = None
    stage_inode: int | None = None
    mutation_started: bool = False
    applied: bool = False
    recovered: bool = False
    restored: bool | None = None
    _extra_fields: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)
    _present_fields: frozenset[str] | None = field(
        default=None, repr=False, compare=False
    )

    @property
    def entry_type(self) -> Literal["file"]:
        """Return the record discriminator."""

        return "file"

    @property
    def result_kind(self) -> str:
        """Return the only valid result kind for a file record."""

        return "file"

    @property
    def result_target(self) -> None:
        """Return the schema-v1 empty target for a file record."""

        return None

    def to_manifest(self) -> dict[str, Any]:
        """Return the schema-v1 dictionary without file contents."""

        value = dict(self._extra_fields)
        fields = {
            "entry_type": "file",
            "destination": str(self.destination),
            "visible_destination": str(self.visible_destination),
            "source": self.source,
            "prior_kind": self.prior_kind,
            "prior_target": self.prior_target,
            "prior_hash": self.prior_hash,
            "backup": str(self.backup) if self.backup is not None else None,
            "result_kind": "file",
            "result_target": None,
            "result_hash": self.result_hash,
            "mutation_started": self.mutation_started,
            "applied": self.applied,
            "recovered": self.recovered,
        }
        value.update(
            {
                key: item
                for key, item in fields.items()
                if self._present_fields is None
                or key in self._present_fields
                or (key in {"mutation_started", "applied", "recovered"} and item is True)
            }
        )
        prior_metadata = {
            "prior_mode": self.prior_mode,
            "prior_device": self.prior_device,
            "prior_inode": self.prior_inode,
        }
        value.update(
            {
                key: item
                for key, item in prior_metadata.items()
                if item is not None
                and (self._present_fields is None or key in self._present_fields)
            }
        )
        result_metadata = {
            "result_mode": self.result_mode,
            "result_device": self.result_device,
            "result_inode": self.result_inode,
        }
        value.update(
            {
                key: item
                for key, item in result_metadata.items()
                if item is not None
                and (self._present_fields is None or key in self._present_fields)
            }
        )
        visible_fields = {
            "visible_kind": self.visible_kind,
            "visible_target": self.visible_target,
            "visible_device": self.visible_device,
            "visible_inode": self.visible_inode,
        }
        value.update(
            {
                key: item
                for key, item in visible_fields.items()
                if item is not None
                and (self._present_fields is None or key in self._present_fields)
            }
        )
        if self.result_backup is not None:
            value["result_backup"] = str(self.result_backup)
        if self.stage_path is not None:
            value["stage_path"] = str(self.stage_path)
        if self.stage_device is not None:
            value["stage_device"] = self.stage_device
        if self.stage_inode is not None:
            value["stage_inode"] = self.stage_inode
        if self.restored is not None and (
            self._present_fields is None or "restored" in self._present_fields or self.restored
        ):
            value["restored"] = self.restored
        return value

    @classmethod
    def from_manifest(cls, raw: Mapping[str, Any]) -> FileRecoveryRecord:
        """Decode a schema-v1 file entry."""

        if raw.get("result_kind") != "file" or raw.get("result_target") is not None:
            raise MutationRecordError("file recovery entry has an invalid result state")
        mutation_started, applied, recovered, restored = _progress_state(raw)
        prior_kind = _required_string(raw, "prior_kind")
        prior_target = _optional_string(raw, "prior_target")
        prior_hash = _optional_string(raw, "prior_hash")
        backup_value = _optional_string(raw, "backup")
        backup = Path(backup_value) if backup_value is not None else None
        prior_mode = _optional_integer(raw, "prior_mode")
        prior_device = _optional_integer(raw, "prior_device")
        prior_inode = _optional_integer(raw, "prior_inode")
        result_mode = _optional_integer(raw, "result_mode")
        result_device = _optional_integer(raw, "result_device")
        result_inode = _optional_integer(raw, "result_inode")
        identity_is_complete = (prior_device is None) == (prior_inode is None)
        metadata_is_valid = (
            (
                prior_kind == "file"
                and (
                    (prior_mode is None and prior_device is None)
                    or (prior_mode is not None and prior_device is not None)
                )
            )
            or (prior_kind == "symlink" and prior_mode is None)
            or (
                prior_kind == "absent"
                and prior_mode is None
                and prior_device is None
            )
        )
        if not identity_is_complete or not metadata_is_valid:
            raise MutationRecordError("file recovery entry has invalid prior metadata")
        result_metadata = (result_mode, result_device, result_inode)
        if any(item is not None for item in result_metadata) and any(
            item is None for item in result_metadata
        ):
            raise MutationRecordError("file recovery entry has invalid result metadata")
        prior_state_is_valid = (
            prior_kind == "absent"
            and prior_target is None
            and prior_hash is None
            and backup is None
        ) or (
            prior_kind == "file"
            and prior_target is None
            and prior_hash is not None
            and backup is not None
        ) or (
            prior_kind == "symlink"
            and prior_target is not None
            and prior_hash is None
        )
        if not prior_state_is_valid:
            raise MutationRecordError("file recovery entry has an invalid prior state")
        known = {
            "entry_type",
            "destination",
            "visible_destination",
            "source",
            "prior_kind",
            "prior_target",
            "prior_hash",
            "prior_mode",
            "prior_device",
            "prior_inode",
            "backup",
            "result_backup",
            "result_kind",
            "result_target",
            "result_hash",
            "result_mode",
            "result_device",
            "result_inode",
            "stage_path",
            "stage_device",
            "stage_inode",
            "visible_kind",
            "visible_target",
            "visible_device",
            "visible_inode",
            "mutation_started",
            "applied",
            "recovered",
            "restored",
        }
        return cls(
            destination=Path(_required_string(raw, "destination")),
            visible_destination=Path(_required_string(raw, "visible_destination")),
            source=_required_string(raw, "source"),
            prior_kind=prior_kind,
            prior_target=prior_target,
            prior_hash=prior_hash,
            prior_mode=prior_mode,
            prior_device=prior_device,
            prior_inode=prior_inode,
            backup=backup,
            result_backup=(
                Path(result_backup_value)
                if (
                    result_backup_value := _optional_string(raw, "result_backup")
                ) is not None
                else None
            ),
            result_hash=_required_string(raw, "result_hash"),
            result_mode=result_mode,
            result_device=result_device,
            result_inode=result_inode,
            stage_path=(
                Path(stage_value)
                if (stage_value := _optional_string(raw, "stage_path")) is not None
                else None
            ),
            stage_device=_optional_integer(raw, "stage_device"),
            stage_inode=_optional_integer(raw, "stage_inode"),
            visible_kind=_optional_string(raw, "visible_kind"),
            visible_target=_optional_string(raw, "visible_target"),
            visible_device=_optional_integer(raw, "visible_device"),
            visible_inode=_optional_integer(raw, "visible_inode"),
            mutation_started=mutation_started,
            applied=applied,
            recovered=recovered,
            restored=restored,
            _extra_fields={key: value for key, value in raw.items() if key not in known},
            _present_fields=frozenset(raw),
        )


@dataclass(frozen=True, kw_only=True)
class DirectoryRecoveryRecord:
    """Recovery metadata for one empty directory creation."""

    destination: Path
    result_device: int
    result_inode: int
    authority_root_was_missing: bool = False
    result_backup: Path | None = None
    stage_path: Path | None = None
    stage_device: int | None = None
    stage_inode: int | None = None
    mutation_started: bool = False
    applied: bool = False
    recovered: bool = False
    restored: bool | None = None
    _extra_fields: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)
    _present_fields: frozenset[str] | None = field(
        default=None, repr=False, compare=False
    )

    entry_type: Literal["directory"] = field(default="directory", init=False)
    prior_kind: Literal["absent"] = field(default="absent", init=False)
    prior_target: None = field(default=None, init=False)
    backup: None = field(default=None, init=False)
    result_kind: Literal["directory"] = field(default="directory", init=False)
    result_target: None = field(default=None, init=False)

    def to_manifest(self) -> dict[str, Any]:
        """Return the schema-v1 directory entry."""

        value = dict(self._extra_fields)
        fields = {
            "entry_type": "directory",
            "destination": str(self.destination),
            "prior_kind": "absent",
            "backup": None,
            "result_kind": "directory",
            "result_target": None,
            "result_device": self.result_device,
            "result_inode": self.result_inode,
            "authority_root_was_missing": self.authority_root_was_missing,
            "mutation_started": self.mutation_started,
            "applied": self.applied,
            "recovered": self.recovered,
        }
        value.update(
            {
                key: item
                for key, item in fields.items()
                if self._present_fields is None
                or key in self._present_fields
                or (key in {"mutation_started", "applied", "recovered"} and item is True)
            }
        )
        if self.restored is not None and (
            self._present_fields is None or "restored" in self._present_fields or self.restored
        ):
            value["restored"] = self.restored
        if self.result_backup is not None:
            value["result_backup"] = str(self.result_backup)
        if self.stage_path is not None:
            value["stage_path"] = str(self.stage_path)
        if self.stage_device is not None:
            value["stage_device"] = self.stage_device
        if self.stage_inode is not None:
            value["stage_inode"] = self.stage_inode
        return value

    @classmethod
    def from_manifest(cls, raw: Mapping[str, Any]) -> DirectoryRecoveryRecord:
        """Decode a schema-v1 directory entry."""

        if (
            raw.get("prior_kind") != "absent"
            or raw.get("backup") is not None
            or raw.get("result_kind") != "directory"
            or raw.get("result_target") is not None
        ):
            raise MutationRecordError("directory recovery entry has an invalid state")
        known = {
            "entry_type",
            "destination",
            "prior_kind",
            "backup",
            "result_kind",
            "result_target",
            "result_device",
            "result_inode",
            "authority_root_was_missing",
            "result_backup",
            "stage_path",
            "stage_device",
            "stage_inode",
            "mutation_started",
            "applied",
            "recovered",
            "restored",
        }
        result_device = _optional_integer(raw, "result_device")
        result_inode = _optional_integer(raw, "result_inode")
        root_was_missing = raw.get("authority_root_was_missing", False)
        if not isinstance(root_was_missing, bool):
            raise MutationRecordError(
                "directory recovery entry has an invalid authority root flag"
            )
        if result_device is None or result_inode is None:
            raise MutationRecordError("directory recovery entry has no result identity")
        mutation_started, applied, recovered, restored = _progress_state(raw)
        return cls(
            destination=Path(_required_string(raw, "destination")),
            result_device=result_device,
            result_inode=result_inode,
            authority_root_was_missing=root_was_missing,
            result_backup=(
                Path(result_backup_value)
                if (
                    result_backup_value := _optional_string(raw, "result_backup")
                ) is not None
                else None
            ),
            stage_path=(
                Path(stage_value)
                if (stage_value := _optional_string(raw, "stage_path")) is not None
                else None
            ),
            stage_device=_optional_integer(raw, "stage_device"),
            stage_inode=_optional_integer(raw, "stage_inode"),
            mutation_started=mutation_started,
            applied=applied,
            recovered=recovered,
            restored=restored,
            _extra_fields={key: value for key, value in raw.items() if key not in known},
            _present_fields=frozenset(raw),
        )


RecoveryRecord = LinkRecoveryRecord | FileRecoveryRecord | DirectoryRecoveryRecord


def decode_recovery_record(raw: Mapping[str, Any]) -> RecoveryRecord:
    """Decode a supported schema-v1 recovery entry."""

    if "entry_type" not in raw:
        return LinkRecoveryRecord.from_manifest(raw, legacy=True)
    entry_type = raw.get("entry_type")
    if entry_type == "link":
        return LinkRecoveryRecord.from_manifest(raw)
    if entry_type == "file":
        return FileRecoveryRecord.from_manifest(raw)
    if entry_type == "directory":
        return DirectoryRecoveryRecord.from_manifest(raw)
    raise MutationRecordError(f"unsupported recovery entry type: {entry_type!r}")


@dataclass(frozen=True, kw_only=True)
class SymlinkMutation:
    """Declare one managed symlink installation or removal."""

    destination: Path
    source: Path
    present: bool = True


@dataclass(frozen=True, kw_only=True)
class FileInputState:
    """The exact file input used to prepare replacement contents."""

    kind: Literal["absent", "file", "symlink"]
    content_hash: str | None = None
    link_target: str | None = None
    mode: int | None = None

    def __post_init__(self) -> None:
        if self.kind == "absent":
            valid = (
                self.content_hash is None
                and self.link_target is None
                and self.mode is None
            )
        elif self.kind == "file":
            valid = (
                self.content_hash is not None
                and self.link_target is None
                and self.mode is not None
            )
        elif self.kind == "symlink":
            valid = self.link_target is not None and (
                (self.content_hash is None and self.mode is None)
                or (self.content_hash is not None and self.mode is not None)
            )
        else:
            valid = False
        if not valid:
            raise ValueError(f"invalid {self.kind} file input state")


@dataclass(frozen=True)
class CapturedFileInput:
    """Descriptor-bound file contents and the state that produced them."""

    state: FileInputState
    contents: bytes | None
    device: int | None
    inode: int | None


@dataclass(frozen=True, kw_only=True)
class FileMutation:
    """Declare one complete local-file replacement."""

    destination: Path
    visible_destination: Path
    source: str
    contents: bytes
    mode: int | None = None
    precondition: FileInputState | None = None


@dataclass(frozen=True, kw_only=True)
class DirectoryMutation:
    """Declare one required empty directory."""

    destination: Path
    mode: int | None = None

Mutation = SymlinkMutation | FileMutation | DirectoryMutation


@dataclass(frozen=True)
class MutationResult:
    """Describe one applied mutation without exposing journal mechanics."""

    mutation: Mutation
    backup: Path | None


@dataclass(frozen=True)
class MutationRecoveryResult:
    """Describe one guarded recovery attempt."""

    recovered: bool
    already_recovered: bool = False
    reason: str | None = None
    record: RecoveryRecord | None = None


@dataclass(frozen=True)
class VerifiedDirectoryEntry:
    """One accepted descendant in a guarded directory tree."""

    relative_path: Path
    kind: Literal["file", "directory"]
    device: int
    inode: int
    content_hash: str | None = None

    def __post_init__(self) -> None:
        normalized = Path(os.path.normpath(self.relative_path))
        if (
            self.relative_path.is_absolute()
            or normalized != self.relative_path
            or self.relative_path == Path(".")
            or ".." in self.relative_path.parts
        ):
            raise ValueError("verified directory entry path must be relative")
        if (self.kind == "file") != (self.content_hash is not None):
            raise ValueError("verified file entries require one content hash")


@dataclass(frozen=True)
class VerifiedDirectory:
    """One exact directory tree approved for guarded removal."""

    path: Path
    device: int
    inode: int
    entries: tuple[VerifiedDirectoryEntry, ...]


def remove_verified_directories(
    directories: tuple[VerifiedDirectory, ...],
    *,
    parent_identity: tuple[int, int],
    parent_parent_identity: tuple[int, int],
) -> tuple[Path, ...]:
    """Move accepted directories to retained descriptor-bound quarantines."""

    if not directories:
        return ()
    parent = directories[0].path.parent
    if any(directory.path.parent != parent for directory in directories):
        raise MutationExecutionError(
            "verified removal directories do not share one parent",
            restored=True,
        )
    expected = {
        parent: parent_identity,
        parent.parent: parent_parent_identity,
    }
    quarantined: list[tuple[VerifiedDirectory, Path]] = []
    additional_retained: list[Path] = []
    try:
        for directory in directories:
            quarantine = _runtime_cleanup_backup(directory.path)
            try:
                _move_no_replace(
                    directory.path,
                    quarantine,
                    expected_identities=expected,
                )
            except Exception:
                try:
                    metadata = _path_metadata(
                        quarantine,
                        expected_identities=expected,
                    )
                    original = _path_metadata(
                        directory.path,
                        expected_identities=expected,
                    )
                except Exception:
                    additional_retained.append(quarantine)
                else:
                    if metadata is not None and (
                        metadata.st_dev,
                        metadata.st_ino,
                    ) == (directory.device, directory.inode) and original is None:
                        quarantined.append((directory, quarantine))
                    elif metadata is not None:
                        additional_retained.append(quarantine)
                raise
            quarantined.append((directory, quarantine))
            metadata = _path_metadata(
                quarantine,
                expected_identities=expected,
            )
            if metadata is None or (
                metadata.st_dev,
                metadata.st_ino,
            ) != (directory.device, directory.inode):
                raise MutationExecutionError(
                    f"verified directory changed during quarantine: {directory.path}",
                    restored=False,
                )
    except Exception as error:
        raise _cleanup_rollback_error(
            "cannot quarantine verified directories",
            error,
            quarantined,
            expected,
            additional_retained=additional_retained,
        ) from error

    try:
        with _open_directory(parent, expected_identities=expected) as parent_descriptor:
            for directory, quarantine in quarantined:
                _validate_verified_directory_at(
                    parent_descriptor,
                    quarantine,
                    directory,
                )
    except Exception as error:
        raise _cleanup_rollback_error(
            "verified directory contents changed after acceptance",
            error,
            quarantined,
            expected,
        ) from error

    return tuple(quarantine for _directory, quarantine in quarantined)


def capture_verified_directory(path: Path, descriptor: int) -> VerifiedDirectory:
    """Capture one stable regular-file directory tree from an open descriptor."""

    metadata = os.fstat(descriptor)
    if not stat.S_ISDIR(metadata.st_mode):
        raise MutationExecutionError(
            f"verified path is not a directory: {path}", restored=True
        )
    entries: list[VerifiedDirectoryEntry] = []
    _capture_verified_entries(descriptor, Path(), entries, path)
    snapshot = VerifiedDirectory(
        path,
        metadata.st_dev,
        metadata.st_ino,
        tuple(sorted(entries, key=lambda entry: str(entry.relative_path))),
    )
    _verify_verified_entries(descriptor, snapshot.entries, path)
    return snapshot


def _capture_verified_entries(
    descriptor: int,
    relative_parent: Path,
    entries: list[VerifiedDirectoryEntry],
    display_root: Path,
) -> None:
    with os.scandir(descriptor) as scanned:
        candidates = sorted(scanned, key=lambda entry: entry.name)
    names = tuple(entry.name for entry in candidates)
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    for candidate in candidates:
        relative = relative_parent / candidate.name
        metadata = candidate.stat(follow_symlinks=False)
        if stat.S_ISDIR(metadata.st_mode):
            entries.append(
                VerifiedDirectoryEntry(
                    relative,
                    "directory",
                    metadata.st_dev,
                    metadata.st_ino,
                )
            )
            child = os.open(candidate.name, flags, dir_fd=descriptor)
            try:
                opened = os.fstat(child)
                if (opened.st_dev, opened.st_ino) != (
                    metadata.st_dev,
                    metadata.st_ino,
                ):
                    raise MutationExecutionError(
                        f"verified directory changed during acceptance: "
                        f"{display_root / relative}",
                        restored=True,
                    )
                _capture_verified_entries(child, relative, entries, display_root)
            finally:
                os.close(child)
        elif stat.S_ISREG(metadata.st_mode):
            digest = _verified_file_hash_at(
                descriptor,
                candidate.name,
                expected_identity=(metadata.st_dev, metadata.st_ino),
                display_path=display_root / relative,
            )
            entries.append(
                VerifiedDirectoryEntry(
                    relative,
                    "file",
                    metadata.st_dev,
                    metadata.st_ino,
                    digest,
                )
            )
        else:
            raise MutationExecutionError(
                f"verified directory has an unsupported entry: "
                f"{display_root / relative}",
                restored=True,
            )
    with os.scandir(descriptor) as rescanned:
        current_names = tuple(sorted(entry.name for entry in rescanned))
    if current_names != names:
        raise MutationExecutionError(
            f"verified directory changed during acceptance: {display_root}",
            restored=True,
        )


def _cleanup_rollback_error(
    action: str,
    primary: Exception,
    quarantined: list[tuple[VerifiedDirectory, Path]],
    expected_identities: Mapping[Path, tuple[int, int]],
    *,
    additional_retained: Iterable[Path] = (),
) -> MutationExecutionError:
    failures: list[str] = []
    for directory, quarantine in reversed(quarantined):
        try:
            _restore_changed_path(
                quarantine,
                directory.path,
                expected_identities=expected_identities,
            )
        except (MutationExecutionError, OSError) as error:
            failures.append(f"{quarantine} -> {directory.path}: {error}")
    retained_candidates = (
        quarantine
        for _, quarantine in quarantined
        if quarantine.exists() or quarantine.is_symlink()
    )
    retained = tuple(
        dict.fromkeys((*retained_candidates, *additional_retained))
    )
    details = [f"{action}: {primary}"]
    if failures:
        details.append(f"restore failures: {'; '.join(failures)}")
    if retained:
        details.append(f"retained quarantine: {', '.join(map(str, retained))}")
    return MutationExecutionError(
        "; ".join(details),
        restored=not failures and not retained,
    )


def _validate_verified_directory_at(
    parent_descriptor: int,
    quarantine: Path,
    directory: VerifiedDirectory,
) -> None:
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(quarantine.name, flags, dir_fd=parent_descriptor)
    try:
        metadata = os.fstat(descriptor)
        if (metadata.st_dev, metadata.st_ino) != (directory.device, directory.inode):
            raise MutationExecutionError(
                f"quarantined directory changed: {quarantine}",
                restored=False,
            )
        _verify_verified_entries(descriptor, directory.entries, quarantine)
    finally:
        os.close(descriptor)


def _verified_children(
    entries: tuple[VerifiedDirectoryEntry, ...],
) -> dict[Path, tuple[VerifiedDirectoryEntry, ...]]:
    children: dict[Path, list[VerifiedDirectoryEntry]] = {}
    for entry in entries:
        children.setdefault(entry.relative_path.parent, []).append(entry)
    return {
        parent: tuple(sorted(items, key=lambda item: item.relative_path.name))
        for parent, items in children.items()
    }


def _verify_verified_entries(
    descriptor: int,
    entries: tuple[VerifiedDirectoryEntry, ...],
    display_root: Path,
) -> None:
    children = _verified_children(entries)
    _verify_verified_directory_contents(
        descriptor,
        Path(),
        children,
        display_root,
    )


def _verify_verified_directory_contents(
    descriptor: int,
    relative: Path,
    children: Mapping[Path, tuple[VerifiedDirectoryEntry, ...]],
    display_root: Path,
) -> None:
    expected = children.get(relative, ())
    with os.scandir(descriptor) as scanned:
        names = tuple(sorted(entry.name for entry in scanned))
    expected_names = tuple(entry.relative_path.name for entry in expected)
    if names != expected_names:
        raise MutationExecutionError(
            f"verified directory contents changed after acceptance: "
            f"{display_root / relative}",
            restored=False,
        )
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    for entry in expected:
        name = entry.relative_path.name
        metadata = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        if (metadata.st_dev, metadata.st_ino) != (entry.device, entry.inode):
            raise MutationExecutionError(
                f"verified directory entry changed after acceptance: "
                f"{display_root / entry.relative_path}",
                restored=False,
            )
        if entry.kind == "file":
            digest = _verified_file_hash_at(
                descriptor,
                name,
                expected_identity=(entry.device, entry.inode),
                display_path=display_root / entry.relative_path,
            )
            if digest != entry.content_hash:
                raise MutationExecutionError(
                    f"verified file changed after acceptance: "
                    f"{display_root / entry.relative_path}",
                    restored=False,
                )
            continue
        if not stat.S_ISDIR(metadata.st_mode):
            raise MutationExecutionError(
                f"verified directory entry changed after acceptance: "
                f"{display_root / entry.relative_path}",
                restored=False,
            )
        child = os.open(name, directory_flags, dir_fd=descriptor)
        try:
            _verify_verified_directory_contents(
                child,
                entry.relative_path,
                children,
                display_root,
            )
        finally:
            os.close(child)


def _verified_file_hash_at(
    parent_descriptor: int,
    name: str,
    *,
    expected_identity: tuple[int, int],
    display_path: Path,
) -> str:
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    descriptor = os.open(name, flags, dir_fd=parent_descriptor)
    open_descriptor: int | None = descriptor
    try:
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or (before.st_dev, before.st_ino) != expected_identity
        ):
            raise MutationExecutionError(
                f"verified file changed: {display_path}", restored=False
            )
        with os.fdopen(descriptor, "rb") as file:
            open_descriptor = None
            digest = hashlib.sha256()
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
            after = os.fstat(file.fileno())
        if (
            (after.st_dev, after.st_ino) != expected_identity
            or after.st_size != before.st_size
            or after.st_mtime_ns != before.st_mtime_ns
            or stat.S_IMODE(after.st_mode) != stat.S_IMODE(before.st_mode)
        ):
            raise MutationExecutionError(
                f"verified file changed while reading: {display_path}",
                restored=False,
            )
        visible = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        if (
            (visible.st_dev, visible.st_ino) != expected_identity
            or visible.st_size != after.st_size
            or visible.st_mtime_ns != after.st_mtime_ns
            or stat.S_IMODE(visible.st_mode) != stat.S_IMODE(after.st_mode)
        ):
            raise MutationExecutionError(
                f"verified file changed after reading: {display_path}",
                restored=False,
            )
        return digest.hexdigest()
    finally:
        if open_descriptor is not None:
            os.close(open_descriptor)


class MutationJournal(Protocol):
    """The journal behavior required inside mutation execution."""

    def add_entry(self, entry: RecoveryRecord) -> int: ...

    def replace_entry(self, index: int, entry: RecoveryRecord) -> None: ...

    def mark_started(self, index: int) -> None: ...

    def mark_applied(self, index: int) -> None: ...

    def mark_restored(self, index: int) -> None: ...

    def transition(self, state: str) -> None: ...


@dataclass
class _PlannedMutation:
    mutation: Mutation
    record: RecoveryRecord
    journal_index: int | None = None
    staged: Path | None = None
    staged_device: int | None = None
    staged_inode: int | None = None
    started: bool = False
    result_installed: bool = False
    requested: bool = True
    parent_identities: tuple[tuple[Path, int, int], ...] = ()
    bound_parent_identities: dict[Path, tuple[int, int]] = field(default_factory=dict)


def execute_mutations(
    mutations: tuple[Mutation, ...],
    *,
    journal: MutationJournal | None = None,
    timestamp: int | None = None,
    authority_roots: tuple[Path, ...] = (),
) -> tuple[MutationResult, ...]:
    """Plan and atomically apply a guarded, reversible mutation batch."""

    suffix = int(time.time()) if timestamp is None else timestamp
    plans: list[_PlannedMutation] = []
    try:
        roots = _normalize_authority_roots(authority_roots)
        expanded = _expand_mutations(mutations, roots)
        plans = _plan_mutations(expanded, suffix, roots)
        plans = [
            *sorted(
                (
                    plan
                    for plan in plans
                    if isinstance(plan.mutation, DirectoryMutation)
                ),
                key=lambda plan: len(plan.mutation.destination.parts),
            ),
            *(
                plan
                for plan in plans
                if not isinstance(plan.mutation, DirectoryMutation)
            ),
        ]
        if journal is not None:
            for plan in plans:
                plan.journal_index = journal.add_entry(plan.record)
        _stage_mutations(plans, journal, roots)
    except Exception as error:
        retained_stage = _has_retained_stage(plans)
        checkpoint_error = _transition_error(
            journal,
            "recovery-needed" if retained_stage else "failed",
        )
        detail = f"; cannot checkpoint failure: {checkpoint_error}" if checkpoint_error else ""
        quarantine_detail = _retained_quarantine_detail(plans)
        raise MutationExecutionError(
            f"cannot prepare filesystem mutations: {error}{detail}{quarantine_detail}",
            restored=not retained_stage and checkpoint_error is None,
        ) from error

    try:
        for plan in plans:
            _apply_mutation(plan, plans, journal, roots)
    except Exception as error:
        restored, rollback_failures = _rollback_mutations(plans, journal)
        if _has_retained_stage(plans):
            restored = False
        checkpoint_error = _transition_error(
            journal,
            "failed" if restored else "recovery-needed",
        )
        if checkpoint_error is not None:
            restored = False
        rollback_detail = (
            f"; rollback failures: {'; '.join(rollback_failures)}"
            if rollback_failures
            else ""
        )
        quarantine_detail = _retained_quarantine_detail(plans)
        raise MutationExecutionError(
            f"cannot apply filesystem mutations: {error}"
            + rollback_detail
            + (
                f"; cannot checkpoint failure: {checkpoint_error}"
                if checkpoint_error is not None
                else ""
            )
            + quarantine_detail,
            restored=restored,
        ) from error
    return tuple(
        MutationResult(
            plan.mutation,
            plan.record.backup,
        )
        for plan in plans
        if plan.requested
    )


def _transition_error(
    journal: MutationJournal | None,
    state: str,
) -> Exception | None:
    if journal is None:
        return None
    try:
        journal.transition(state)
    except Exception as error:  # noqa: BLE001 - preserve the primary mutation failure
        return error
    return None


def _has_retained_stage(plans: list[_PlannedMutation]) -> bool:
    """Report whether a recorded stage remains after an interrupted batch."""

    return any(
        plan.started
        and plan.staged is not None
        and (plan.staged.exists() or plan.staged.is_symlink())
        for plan in plans
    )


def _retained_quarantine_detail(plans: list[_PlannedMutation]) -> str:
    """Report every stage or result quarantine that remains after failure."""

    retained: list[Path] = []
    for plan in plans:
        stage_path = getattr(plan.record, "stage_path", None)
        for path in (plan.staged, stage_path, plan.record.result_backup):
            if (
                path is not None
                and path not in retained
                and (path.exists() or path.is_symlink())
            ):
                retained.append(path)
    return f"; retained quarantine: {', '.join(map(str, retained))}" if retained else ""


def _expand_mutations(
    mutations: tuple[Mutation, ...],
    authority_roots: tuple[Path, ...],
) -> tuple[tuple[Mutation, bool], ...]:
    required: set[Path] = set()
    explicit_directories = {
        mutation.destination
        for mutation in mutations
        if isinstance(mutation, DirectoryMutation)
    }
    for mutation in mutations:
        _require_authorized_parent(mutation.destination, authority_roots)
        target = (
            mutation.destination
            if isinstance(mutation, DirectoryMutation)
            else mutation.destination.parent
        )
        root = _authority_root(target, authority_roots)
        while not target.exists():
            required.add(target)
            if target == root or target.parent == target:
                break
            target = target.parent
    automatic = tuple(
        (DirectoryMutation(destination=destination), False)
        for destination in sorted(
            required - explicit_directories,
            key=lambda path: (len(path.parts), str(path)),
        )
    )
    requested: list[tuple[Mutation, bool]] = []
    for mutation in mutations:
        if isinstance(mutation, DirectoryMutation) and mutation.destination.exists():
            if not mutation.destination.is_dir():
                raise MutationExecutionError(
                    f"required directory path has another type: {mutation.destination}",
                    restored=True,
                )
            continue
        if (
            isinstance(mutation, SymlinkMutation)
            and mutation.present
            and mutation.destination.is_symlink()
            and _symlink_target_matches(
                mutation.destination,
                os.readlink(mutation.destination),
                mutation.source,
            )
        ):
            continue
        requested.append((mutation, True))
    return (*automatic, *requested)


def _plan_mutations(
    mutations: tuple[tuple[Mutation, bool], ...],
    timestamp: int,
    authority_roots: tuple[Path, ...],
) -> list[_PlannedMutation]:
    plans: list[_PlannedMutation] = []
    destinations: set[Path] = set()
    reserved_backups: set[Path] = set()
    reserved_stages: set[Path] = set()
    for mutation, requested in mutations:
        destination = mutation.destination
        if destination in destinations:
            raise MutationExecutionError(
                f"destination is planned more than once: {destination}", restored=True
            )
        destinations.add(destination)
        _check_parent(destination, authority_roots)
        parent_identities = _parent_identities(destination, authority_roots)
        current_file_input: CapturedFileInput | None = None
        if isinstance(mutation, FileMutation):
            current_file_input = capture_file_input(destination)
            if (
                mutation.precondition is not None
                and current_file_input.state != mutation.precondition
            ):
                raise MutationExecutionError(
                    f"file input changed after preparation: {destination}",
                    restored=True,
                )
            prior_kind = current_file_input.state.kind
            prior_target = current_file_input.state.link_target
            prior_device = None
            prior_inode = None
        else:
            prior_kind, prior_target, prior_device, prior_inode = _classify(
                destination
            )
        if isinstance(mutation, DirectoryMutation):
            if prior_kind != "absent":
                raise MutationExecutionError(
                    f"required directory changed after planning: {destination}",
                    restored=True,
                )
            record = DirectoryRecoveryRecord(
                destination=destination,
                result_device=0,
                result_inode=0,
                authority_root_was_missing=destination in authority_roots,
                result_backup=_unique_result_backup(destination, reserved_backups),
                stage_path=_unique_stage_path(destination, reserved_stages),
            )
        elif isinstance(mutation, SymlinkMutation):
            if mutation.present and not mutation.source.exists():
                raise MutationExecutionError(
                    f"managed source is missing: {mutation.source}", restored=True
                )
            if not mutation.present and prior_kind != "symlink":
                raise MutationExecutionError(
                    f"removal destination is no longer a symlink: {destination}",
                    restored=True,
                )
            if (
                not mutation.present
                and not _symlink_target_matches(destination, prior_target, mutation.source)
            ):
                raise MutationExecutionError(
                    f"removal destination is no longer managed: {destination}",
                    restored=True,
                )
            backup = None
            if prior_kind != "absent":
                backup = _unique_backup(destination, timestamp, reserved_backups)
            result_backup = (
                _unique_result_backup(destination, reserved_backups)
                if mutation.present
                else None
            )
            record: RecoveryRecord = LinkRecoveryRecord(
                destination=destination,
                source=mutation.source,
                prior_kind=prior_kind,
                prior_target=prior_target,
                prior_device=prior_device,
                prior_inode=prior_inode,
                backup=backup,
                result_kind="symlink" if mutation.present else "absent",
                result_target=str(mutation.source) if mutation.present else None,
                result_backup=result_backup,
            )
        else:
            assert current_file_input is not None
            prior_hash = (
                current_file_input.state.content_hash
                if prior_kind == "file"
                else None
            )
            prior_mode = (
                current_file_input.state.mode if prior_kind == "file" else None
            )
            if prior_kind == "file" and prior_hash is None:
                raise MutationExecutionError(
                    f"file destination changed during planning: {destination}",
                    restored=True,
                )
            visible_kind = None
            visible_target = None
            visible_device = None
            visible_inode = None
            if mutation.visible_destination != destination:
                (
                    visible_kind,
                    visible_target,
                    visible_device,
                    visible_inode,
                ) = _classify(mutation.visible_destination)
                if visible_kind != "symlink" or not _symlink_target_matches(
                    mutation.visible_destination,
                    visible_target,
                    destination,
                ):
                    raise MutationExecutionError(
                        "visible file destination changed after inspection: "
                        f"{mutation.visible_destination}",
                        restored=True,
                    )
            backup = None
            if prior_kind == "file":
                backup = _numbered_backup(destination, timestamp, reserved_backups)
            elif prior_kind == "symlink":
                backup = _unique_backup(destination, timestamp, reserved_backups)
            record = FileRecoveryRecord(
                destination=destination,
                visible_destination=mutation.visible_destination,
                source=mutation.source,
                prior_kind=prior_kind,
                prior_target=prior_target,
                prior_hash=prior_hash,
                prior_mode=prior_mode,
                prior_device=current_file_input.device,
                prior_inode=current_file_input.inode,
                backup=backup,
                result_hash=hashlib.sha256(mutation.contents).hexdigest(),
                visible_kind=visible_kind,
                visible_target=visible_target,
                visible_device=visible_device,
                visible_inode=visible_inode,
                result_backup=_unique_result_backup(destination, reserved_backups),
                stage_path=_unique_stage_path(destination, reserved_stages),
            )
        plans.append(
            _PlannedMutation(
                mutation,
                record,
                requested=requested,
                parent_identities=parent_identities,
            )
        )
    return plans


def _stage_mutations(
    plans: list[_PlannedMutation],
    journal: MutationJournal | None,
    authority_roots: tuple[Path, ...],
) -> None:
    for plan in plans:
        if not isinstance(plan.mutation, (DirectoryMutation, FileMutation)):
            continue
        parent_identities = _require_parent_identities(plan, (), authority_roots)
        plan.bound_parent_identities = parent_identities
        if journal is not None and plan.journal_index is not None:
            journal.mark_started(plan.journal_index)
        plan.started = True
        if isinstance(plan.mutation, DirectoryMutation):
            assert isinstance(plan.record, DirectoryRecoveryRecord)
            assert plan.record.stage_path is not None
            temporary = plan.record.stage_path
            with _open_parent(
                temporary, expected_identities=parent_identities
            ) as parent_descriptor:
                os.mkdir(temporary.name, mode=0o700, dir_fd=parent_descriptor)
                declared_mode = (
                    0o755 if plan.mutation.mode is None else plan.mutation.mode
                )
                os.chmod(
                    temporary.name,
                    declared_mode,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                plan.staged = temporary
                identity = os.stat(
                    temporary.name,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                os.fsync(parent_descriptor)
            plan.staged_device = identity.st_dev
            plan.staged_inode = identity.st_ino
            assert isinstance(plan.record, DirectoryRecoveryRecord)
            plan.record = replace(
                plan.record,
                result_device=identity.st_dev,
                result_inode=identity.st_ino,
                stage_device=identity.st_dev,
                stage_inode=identity.st_ino,
            )
            if journal is not None and plan.journal_index is not None:
                journal.replace_entry(plan.journal_index, plan.record)
            continue
        mutation = plan.mutation
        assert isinstance(mutation, FileMutation)
        assert isinstance(plan.record, FileRecoveryRecord)
        assert plan.record.stage_path is not None
        temporary = plan.record.stage_path
        with _open_parent(
            temporary, expected_identities=parent_identities
        ) as parent_descriptor:
            descriptor = os.open(
                temporary.name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
                dir_fd=parent_descriptor,
            )
            plan.staged = temporary
            open_descriptor: int | None = descriptor
            try:
                if mutation.mode is not None:
                    os.fchmod(descriptor, mutation.mode)
                with os.fdopen(descriptor, "wb") as file:
                    open_descriptor = None
                    file.write(mutation.contents)
                    file.flush()
                    os.fsync(file.fileno())
                    identity = os.fstat(file.fileno())
                os.fsync(parent_descriptor)
            finally:
                if open_descriptor is not None:
                    os.close(open_descriptor)
        plan.staged_device = identity.st_dev
        plan.staged_inode = identity.st_ino
        plan.record = replace(
            plan.record,
            result_mode=stat.S_IMODE(identity.st_mode),
            result_device=identity.st_dev,
            result_inode=identity.st_ino,
            stage_device=identity.st_dev,
            stage_inode=identity.st_ino,
        )
        if journal is not None and plan.journal_index is not None:
            journal.replace_entry(plan.journal_index, plan.record)


def _apply_mutation(
    plan: _PlannedMutation,
    plans: list[_PlannedMutation],
    journal: MutationJournal | None,
    authority_roots: tuple[Path, ...],
) -> None:
    if not plan.started and journal is not None and plan.journal_index is not None:
        journal.mark_started(plan.journal_index)
    plan.started = True
    parent_identities = _require_parent_identities(plan, plans, authority_roots)
    plan.bound_parent_identities = parent_identities
    _require_visible_destination(plan.record)
    _capture_prior(plan.record, parent_identities)
    _require_visible_destination(plan.record)
    if isinstance(plan.mutation, DirectoryMutation):
        _apply_directory(plan, parent_identities)
    elif isinstance(plan.mutation, SymlinkMutation):
        _apply_symlink(plan, parent_identities)
    else:
        _apply_file(plan, parent_identities)
    if isinstance(plan.record, (FileRecoveryRecord, DirectoryRecoveryRecord)):
        plan.record = replace(
            plan.record,
            stage_path=None,
            stage_device=None,
            stage_inode=None,
        )
        if journal is not None and plan.journal_index is not None:
            journal.replace_entry(plan.journal_index, plan.record)
    _require_visible_destination(plan.record)
    if journal is not None and plan.journal_index is not None:
        journal.mark_applied(plan.journal_index)


def _capture_prior(
    record: RecoveryRecord,
    parent_identities: Mapping[Path, tuple[int, int]],
) -> None:
    """Move the live prior object before validating its recorded identity."""

    destination = record.destination
    if record.prior_kind == "absent":
        if destination.exists() or destination.is_symlink():
            raise MutationExecutionError(
                f"destination changed after planning: {destination}", restored=True
            )
        return
    backup = record.backup
    if backup is None:
        raise MutationExecutionError(
            f"planned backup is missing for {destination}", restored=False
        )
    if backup.exists() or backup.is_symlink():
        raise MutationExecutionError(
            f"planned backup path appeared: {backup}", restored=True
        )
    try:
        _move_no_replace(
            destination,
            backup,
            expected_identities=parent_identities,
        )
    except FileExistsError as error:
        raise MutationExecutionError(
            f"planned backup path appeared: {backup}", restored=True
        ) from error
    except FileNotFoundError as error:
        raise MutationExecutionError(
            f"destination changed after planning: {destination}", restored=True
        ) from error
    if not _matches_prior_at(
        record,
        backup,
        expected_identities=parent_identities,
    ):
        _restore_changed_path(
            backup,
            destination,
            expected_identities=parent_identities,
        )
        raise MutationExecutionError(
            f"destination changed while mutation started; restored {destination}",
            restored=True,
        )


def _apply_symlink(
    plan: _PlannedMutation,
    parent_identities: Mapping[Path, tuple[int, int]],
) -> None:
    mutation = plan.mutation
    assert isinstance(mutation, SymlinkMutation)
    destination = mutation.destination
    if mutation.present:
        _create_symlink(
            mutation.source,
            destination,
            expected_identities=parent_identities,
        )
    plan.result_installed = True


def _apply_directory(
    plan: _PlannedMutation,
    parent_identities: Mapping[Path, tuple[int, int]],
) -> None:
    mutation = plan.mutation
    assert isinstance(mutation, DirectoryMutation)
    assert plan.staged is not None
    staged = plan.staged
    _require_staged_result(plan.record, staged, parent_identities)
    _move_no_replace(
        staged,
        mutation.destination,
        expected_identities=parent_identities,
    )
    plan.result_installed = True
    _require_staged_result(plan.record, mutation.destination, parent_identities)
    plan.staged = None


def _apply_file(
    plan: _PlannedMutation,
    parent_identities: Mapping[Path, tuple[int, int]],
) -> None:
    mutation = plan.mutation
    assert isinstance(mutation, FileMutation)
    assert plan.staged is not None
    staged = plan.staged
    _require_staged_result(plan.record, staged, parent_identities)
    _move_no_replace(
        staged,
        mutation.destination,
        expected_identities=parent_identities,
    )
    plan.result_installed = True
    _require_staged_result(plan.record, mutation.destination, parent_identities)
    plan.staged = None


def _require_staged_result(
    record: FileRecoveryRecord | DirectoryRecoveryRecord,
    path: Path,
    expected_identities: Mapping[Path, tuple[int, int]],
) -> None:
    """Reject a staged object that does not match its durable record."""

    try:
        metadata = _path_metadata(path, expected_identities=expected_identities)
    except OSError as error:
        raise MutationExecutionError(
            f"staged result is unavailable: {path}", restored=False
        ) from error
    expected_identity = (record.stage_device, record.stage_inode)
    if (
        metadata is None
        or None in expected_identity
        or (metadata.st_dev, metadata.st_ino) != expected_identity
    ):
        raise MutationExecutionError(
            f"staged result identity changed: {path}", restored=False
        )
    if isinstance(record, DirectoryRecoveryRecord):
        if not _empty_directory_matches(
            path,
            expected_identity=(record.stage_device, record.stage_inode),
            expected_identities=expected_identities,
        ):
            raise MutationExecutionError(
                f"staged directory result changed: {path}", restored=False
            )
        return
    if not _file_result_matches(
        record,
        path,
        expected_identities=expected_identities,
    ):
        raise MutationExecutionError(
            f"staged file result changed: {path}", restored=False
        )


def _rollback_mutations(
    plans: list[_PlannedMutation], journal: MutationJournal | None
) -> tuple[bool, tuple[str, ...]]:
    complete = True
    failures: list[str] = []
    for plan in reversed(plans):
        if not plan.started:
            continue
        reason = _rollback_mutation(plan)
        if reason is not None:
            complete = False
            failures.append(f"{plan.record.destination}: {reason}")
            continue
        if journal is not None and plan.journal_index is not None:
            try:
                journal.mark_restored(plan.journal_index)
            except Exception as error:
                complete = False
                failures.append(
                    f"{plan.record.destination}: cannot checkpoint restored state: {error}"
                )
    return complete, tuple(failures)


def _rollback_mutation(plan: _PlannedMutation) -> str | None:
    record = plan.record
    expected = plan.bound_parent_identities
    try:
        if _matches_prior(record, expected_identities=expected):
            return None
        prior_error = _required_prior_backup_error(
            record,
            expected_identities=expected,
        )
        if prior_error is not None:
            return prior_error
        if plan.result_installed:
            result_error = _capture_result(record, expected_identities=expected)
            if result_error is not None:
                return result_error
        elif _path_present(record.destination, expected_identities=expected):
            return "current state changed"
        return _restore_prior(record, expected_identities=expected)
    except (MutationExecutionError, OSError) as error:
        return str(error) or error.__class__.__name__


def prepare_recovery_record(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> RecoveryRecord:
    """Reserve a durable quarantine path before recovery moves a result."""

    if (
        record.result_backup is None
        and not (
            isinstance(record, LinkRecoveryRecord) and record.result_kind == "absent"
        )
        and _matches_result(record, expected_identities=expected_identities)
    ):
        return replace(
            record,
            result_backup=_runtime_result_backup(record.destination),
        )
    return record


def recover_mutation(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> MutationRecoveryResult:
    """Restore one recorded mutation without overwriting changed state."""

    working_record = prepare_recovery_record(
        record,
        expected_identities=expected_identities,
    )
    _require_visible_destination(
        working_record,
        expected_identities=expected_identities,
    )
    retained_error = _retained_result_error(
        working_record,
        expected_identities=expected_identities,
    )
    if retained_error is not None:
        return MutationRecoveryResult(False, reason=retained_error, record=working_record)
    if _matches_prior(record, expected_identities=expected_identities):
        return MutationRecoveryResult(
            True,
            already_recovered=True,
            record=working_record,
        )
    prior_error = _required_prior_backup_error(
        working_record,
        expected_identities=expected_identities,
    )
    if prior_error is not None:
        return MutationRecoveryResult(
            False,
            reason=prior_error,
            record=working_record,
        )
    reason = _capture_result(
        working_record,
        expected_identities=expected_identities,
    )
    _require_visible_destination(
        working_record,
        expected_identities=expected_identities,
    )
    if reason is not None:
        destination_present = _path_present(
            record.destination,
            expected_identities=expected_identities,
        )
        result_preserved = _result_backup_matches(
            working_record,
            expected_identities=expected_identities,
        )
        if record.applied or destination_present or result_preserved:
            return MutationRecoveryResult(False, reason=reason, record=working_record)
    reason = _restore_prior(
        working_record,
        expected_identities=expected_identities,
    )
    _require_visible_destination(
        working_record,
        expected_identities=expected_identities,
    )
    if reason is not None:
        return MutationRecoveryResult(False, reason=reason, record=working_record)
    if not _matches_prior(record, expected_identities=expected_identities):
        return MutationRecoveryResult(
            False,
            reason="restored state verification failed",
            record=working_record,
        )
    return MutationRecoveryResult(True, record=working_record)


def _capture_result(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str | None:
    """Move an installed result to its recorded quarantine before validation."""

    destination = record.destination
    if isinstance(record, LinkRecoveryRecord) and record.result_kind == "absent":
        if _path_present(destination, expected_identities=expected_identities):
            return "current state changed"
        return None
    result_backup = record.result_backup
    if result_backup is None:
        return (
            None
            if _matches_result(record, expected_identities=expected_identities)
            else "current state changed"
        )
    if _path_present(result_backup, expected_identities=expected_identities):
        if _path_present(destination, expected_identities=expected_identities):
            return f"result quarantine path is occupied: {result_backup}"
        return (
            None
            if _matches_result_at(
                record,
                result_backup,
                expected_identities=expected_identities,
            )
            else "quarantined state changed"
        )
    if not _path_present(destination, expected_identities=expected_identities):
        return "current state changed"
    if not _matches_result_at(
        record,
        destination,
        expected_identities=expected_identities,
    ):
        return "current state changed"
    try:
        _move_no_replace(
            destination,
            result_backup,
            expected_identities=expected_identities,
        )
    except FileExistsError:
        return f"result quarantine path is occupied: {result_backup}"
    except OSError as error:
        return str(error)
    if not _matches_result_at(
        record,
        result_backup,
        expected_identities=expected_identities,
    ):
        _restore_changed_quarantine(
            record,
            expected_identities=expected_identities,
        )
        return f"current state changed; preserved at {result_backup}"
    if isinstance(record, DirectoryRecoveryRecord):
        try:
            if not _directory_is_empty(
                result_backup,
                expected_identities=expected_identities,
            ):
                _restore_changed_quarantine(
                    record,
                    expected_identities=expected_identities,
                )
                return f"current directory is not empty; preserved at {destination}"
        except OSError as error:
            _restore_changed_quarantine(
                record,
                expected_identities=expected_identities,
            )
            return str(error)
    return None


def _restore_prior(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str | None:
    destination = record.destination
    backup = record.backup
    try:
        if _path_present(destination, expected_identities=expected_identities):
            return "current state changed"
        if backup is not None and _path_present(
            backup,
            expected_identities=expected_identities,
        ):
            _move_no_replace(
                backup,
                destination,
                expected_identities=expected_identities,
            )
            backup_error = _backup_error(
                record,
                destination,
                expected_identities=expected_identities,
            )
            if backup_error is not None:
                quarantine = _runtime_changed_backup(destination)
                try:
                    _move_no_replace(
                        destination,
                        quarantine,
                        expected_identities=expected_identities,
                    )
                except OSError as error:
                    return (
                        f"{backup_error}; changed backup remains at {destination}: {error}"
                    )
                return f"{backup_error}; changed backup preserved at {quarantine}"
        elif record.prior_kind == "symlink" and record.prior_target is not None:
            _create_symlink(
                record.prior_target,
                destination,
                expected_identities=expected_identities,
            )
        elif record.prior_kind == "absent":
            return None
        else:
            return "backup is missing"
    except OSError as error:
        return str(error)
    return None


def _backup_error(
    record: RecoveryRecord,
    backup: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str | None:
    if not _path_present(backup, expected_identities=expected_identities):
        return "backup is missing"
    if isinstance(record, FileRecoveryRecord):
        metadata_error = _file_prior_metadata_error(
            record,
            backup,
            expected_identities=expected_identities,
        )
        if metadata_error is not None:
            return metadata_error
        if record.prior_kind == "symlink":
            try:
                if (
                    _path_readlink(
                        backup,
                        expected_identities=expected_identities,
                    )
                    == record.prior_target
                ):
                    return None
            except OSError as error:
                return str(error)
            return "backup target changed"
        if (
            record.prior_kind != "file"
            or record.prior_hash is None
            or
            _file_hash(backup, expected_identities=expected_identities)
            != record.prior_hash
        ):
            return "backup contents changed"
        return None
    try:
        metadata = _path_metadata(
            backup,
            expected_identities=expected_identities,
        )
    except OSError as error:
        return str(error)
    if metadata is None:
        return "backup is missing"
    if metadata.st_dev != record.prior_device or metadata.st_ino != record.prior_inode:
        return "backup identity changed"
    return None


def _required_prior_backup_error(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str | None:
    """Validate a backup that is required before the current result can move."""

    if record.prior_kind not in {"file", "directory"}:
        return None
    backup = record.backup
    if backup is None:
        return "required prior backup is missing"
    error = _backup_error(
        record,
        backup,
        expected_identities=expected_identities,
    )
    return f"required prior backup is invalid: {error}" if error is not None else None


def _file_prior_metadata_error(
    record: FileRecoveryRecord,
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str | None:
    """Validate optional file backup identity and mode metadata."""

    try:
        metadata = _path_metadata(path, expected_identities=expected_identities)
    except OSError as error:
        return str(error)
    if metadata is None:
        return "backup is missing"
    expected_type_matches = (
        record.prior_kind == "file" and stat.S_ISREG(metadata.st_mode)
    ) or (record.prior_kind == "symlink" and stat.S_ISLNK(metadata.st_mode))
    if not expected_type_matches:
        return "backup type changed"
    if (
        record.prior_device is not None
        and record.prior_inode is not None
        and (metadata.st_dev, metadata.st_ino)
        != (record.prior_device, record.prior_inode)
    ):
        return "backup identity changed"
    if (
        record.prior_kind == "file"
        and record.prior_mode is not None
        and stat.S_IMODE(metadata.st_mode) != record.prior_mode
    ):
        return "backup mode changed"
    return None


def _matches_prior(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    return _matches_prior_at(
        record,
        record.destination,
        expected_identities=expected_identities,
    )


def _matches_prior_at(
    record: RecoveryRecord,
    destination: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    if record.prior_kind == "absent":
        return not _path_present(destination, expected_identities=expected_identities)
    if isinstance(record, FileRecoveryRecord):
        return (
            _backup_error(
                record,
                destination,
                expected_identities=expected_identities,
            )
            is None
        )
    if record.prior_kind == "symlink":
        try:
            metadata = _path_metadata(
                destination,
                expected_identities=expected_identities,
            )
            return (
                metadata is not None
                and stat.S_ISLNK(metadata.st_mode)
                and _path_readlink(
                    destination,
                    expected_identities=expected_identities,
                )
                == record.prior_target
            )
        except OSError:
            return False
    try:
        metadata = _path_metadata(
            destination,
            expected_identities=expected_identities,
        )
    except OSError:
        return False
    if metadata is None:
        return False
    return metadata.st_dev == record.prior_device and metadata.st_ino == record.prior_inode


def _matches_result(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    return _matches_result_at(
        record,
        record.destination,
        expected_identities=expected_identities,
    )


def _matches_result_at(
    record: RecoveryRecord,
    destination: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    if isinstance(record, DirectoryRecoveryRecord):
        return _empty_directory_matches(
            destination,
            expected_identity=(record.result_device, record.result_inode),
            expected_identities=expected_identities,
        )
    if isinstance(record, FileRecoveryRecord):
        return _file_result_matches(
            record,
            destination,
            expected_identities=expected_identities,
        )
    if record.result_kind == "absent":
        return not _path_present(destination, expected_identities=expected_identities)
    try:
        metadata = _path_metadata(
            destination,
            expected_identities=expected_identities,
        )
        return (
            metadata is not None
            and stat.S_ISLNK(metadata.st_mode)
            and _path_readlink(
                destination,
                expected_identities=expected_identities,
            )
            == record.result_target
        )
    except OSError:
        return False


def _file_result_matches(
    record: FileRecoveryRecord,
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    """Match a file result, with identity metadata for newly written records."""

    result_metadata = (record.result_mode, record.result_device, record.result_inode)
    if all(item is None for item in result_metadata):
        return (
            _file_hash(path, expected_identities=expected_identities)
            == record.result_hash
        )
    if any(item is None for item in result_metadata):
        return False
    assert record.result_mode is not None
    assert record.result_device is not None
    assert record.result_inode is not None
    try:
        with _open_parent(
            path,
            expected_identities=expected_identities,
        ) as parent_descriptor:
            metadata = os.stat(
                path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            expected_identity = (record.result_device, record.result_inode)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or (metadata.st_dev, metadata.st_ino) != expected_identity
            ):
                return False
            contents, mode = _read_regular_file_at(
                path,
                parent_descriptor,
                expected_identity=expected_identity,
                nofollow=True,
            )
    except (MutationExecutionError, OSError):
        return False
    return (
        mode == record.result_mode
        and hashlib.sha256(contents).hexdigest() == record.result_hash
    )


def _empty_directory_matches(
    path: Path,
    *,
    expected_identity: tuple[int | None, int | None],
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    """Match one empty directory through its descriptor-bound namespace entry."""

    if None in expected_identity:
        return False
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        with _open_parent(
            path,
            expected_identities=expected_identities,
        ) as parent_descriptor:
            descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
            try:
                metadata = os.fstat(descriptor)
                if (
                    not stat.S_ISDIR(metadata.st_mode)
                    or (metadata.st_dev, metadata.st_ino) != expected_identity
                    or os.listdir(descriptor)
                ):
                    return False
                visible = os.stat(
                    path.name,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                return (visible.st_dev, visible.st_ino) == expected_identity
            finally:
                os.close(descriptor)
    except OSError:
        return False


def _result_backup_matches(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    backup = record.result_backup
    return backup is not None and _matches_result_at(
        record,
        backup,
        expected_identities=expected_identities,
    )


def _restore_changed_quarantine(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> None:
    """Restore a moved competing object without replacing another object."""

    backup = record.result_backup
    destination = record.destination
    if backup is None:
        return
    _restore_changed_path(
        backup,
        destination,
        expected_identities=expected_identities,
    )


def _restore_changed_path(
    backup: Path,
    destination: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> None:
    """Restore a quarantined object without replacing the destination."""

    backup_metadata = _path_metadata(
        backup,
        expected_identities=expected_identities,
    )
    if _path_present(destination, expected_identities=expected_identities):
        raise MutationExecutionError(
            f"cannot restore {backup} to occupied destination {destination}; "
            f"retained quarantine: {backup}",
            restored=False,
        )
    try:
        _move_no_replace(
            backup,
            destination,
            expected_identities=expected_identities,
        )
    except OSError as error:
        try:
            retained_metadata = _path_metadata(
                backup,
                expected_identities=expected_identities,
            )
            restored_metadata = _path_metadata(
                destination,
                expected_identities=expected_identities,
            )
        except Exception as inspection_error:
            detail = f"restore state is uncertain: {inspection_error}"
        else:
            original_identity = (
                (backup_metadata.st_dev, backup_metadata.st_ino)
                if backup_metadata is not None
                else None
            )
            if (
                original_identity is not None
                and restored_metadata is not None
                and (restored_metadata.st_dev, restored_metadata.st_ino)
                == original_identity
                and retained_metadata is None
            ):
                detail = "namespace restore completed, but directory sync failed"
            elif retained_metadata is not None:
                detail = f"retained quarantine: {backup}"
            else:
                detail = "restore state is uncertain; inspect both paths"
        raise MutationExecutionError(
            f"cannot restore {backup} to {destination}: {error}; {detail}",
            restored=False,
        ) from error


def _retained_result_error(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str | None:
    """Accept a verified retained quarantine and reject a changed one."""

    backup = record.result_backup
    if backup is None or not _path_present(
        backup,
        expected_identities=expected_identities,
    ):
        return None
    if _matches_result_at(
        record,
        backup,
        expected_identities=expected_identities,
    ):
        if isinstance(record, DirectoryRecoveryRecord):
            try:
                if not _directory_is_empty(
                    backup,
                    expected_identities=expected_identities,
                ):
                    return f"retained directory quarantine is not empty: {backup}"
            except OSError as error:
                return str(error)
        return None
    return f"retained result quarantine changed: {backup}"


def _require_visible_destination(
    record: RecoveryRecord,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> None:
    """Reject a visible symlink that changed after file inspection."""

    if not isinstance(record, FileRecoveryRecord) or record.visible_kind is None:
        return
    visible = record.visible_destination
    try:
        metadata = _path_metadata(
            visible,
            expected_identities=expected_identities,
        )
        if metadata is None:
            raise FileNotFoundError(visible)
        target = _path_readlink(
            visible,
            expected_identities=expected_identities,
        )
    except OSError as error:
        raise MutationExecutionError(
            f"visible file destination changed: {visible}", restored=True
        ) from error
    if (
        not stat.S_ISLNK(metadata.st_mode)
        or target != record.visible_target
        or metadata.st_dev != record.visible_device
        or metadata.st_ino != record.visible_inode
        or not _symlink_target_matches(visible, target, record.destination)
    ):
        raise MutationExecutionError(
            f"visible file destination changed: {visible}", restored=True
        )


def _path_metadata(
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> os.stat_result | None:
    """Read leaf metadata through its verified parent directory."""

    with _open_parent(
        path, expected_identities=expected_identities
    ) as parent_descriptor:
        try:
            return os.stat(
                path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            return None


def _path_present(
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    """Report whether a leaf exists under its verified parent directory."""

    return _path_metadata(path, expected_identities=expected_identities) is not None


def _path_readlink(
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str:
    """Read one symlink through its verified parent directory."""

    with _open_parent(path, expected_identities=expected_identities) as parent_descriptor:
        return os.readlink(path.name, dir_fd=parent_descriptor)


def _directory_is_empty(
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> bool:
    """Inspect one directory through its verified parent directory."""

    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    with _open_parent(path, expected_identities=expected_identities) as parent_descriptor:
        descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
        try:
            return not os.listdir(descriptor)
        finally:
            os.close(descriptor)


@contextmanager
def _open_directory(
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> Iterator[int]:
    """Open one absolute directory without following any path symlink."""

    if not path.is_absolute():
        raise OSError(errno.EINVAL, "directory path must be absolute", str(path))
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path.anchor, flags)
    current = Path(path.anchor)
    try:
        _require_descriptor_identity(current, descriptor, expected_identities)
        for part in path.parts[1:]:
            next_descriptor = os.open(part, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
            current /= part
            _require_descriptor_identity(current, descriptor, expected_identities)
        yield descriptor
    finally:
        os.close(descriptor)


@contextmanager
def _open_parent(
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> Iterator[int]:
    """Open a path parent through a descriptor-bound directory walk."""

    with _open_directory(
        path.parent,
        expected_identities=expected_identities,
    ) as descriptor:
        yield descriptor


def _require_descriptor_identity(
    path: Path,
    descriptor: int,
    expected_identities: Mapping[Path, tuple[int, int]] | None,
) -> None:
    """Reject an opened directory that differs from its planned identity."""

    if expected_identities is None or path not in expected_identities:
        return
    metadata = os.fstat(descriptor)
    if (metadata.st_dev, metadata.st_ino) != expected_identities[path]:
        raise MutationExecutionError(
            f"destination parent changed: {path}", restored=False
        )


def _create_symlink(
    source: Path | str,
    destination: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> None:
    """Create a symlink relative to its verified parent directory."""

    with _open_parent(
        destination,
        expected_identities=expected_identities,
    ) as parent_descriptor:
        os.symlink(source, destination.name, dir_fd=parent_descriptor)
        os.fsync(parent_descriptor)


def _move_no_replace(
    source: Path,
    destination: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> None:
    """Move one filesystem object without replacing a competing object."""

    if source.parent == destination.parent:
        with _open_parent(
            source,
            expected_identities=expected_identities,
        ) as parent_descriptor:
            _rename_no_replace(
                source,
                parent_descriptor,
                destination,
                parent_descriptor,
            )
            os.fsync(parent_descriptor)
        return
    with _open_parent(
        source,
        expected_identities=expected_identities,
    ) as source_parent, _open_parent(
        destination,
        expected_identities=expected_identities,
    ) as destination_parent:
        _rename_no_replace(
            source,
            source_parent,
            destination,
            destination_parent,
        )
        os.fsync(source_parent)
        os.fsync(destination_parent)


def _rename_no_replace(
    source: Path,
    source_parent: int,
    destination: Path,
    destination_parent: int,
) -> None:
    """Rename one entry through already opened directory descriptors."""

    libc = ctypes.CDLL(None, use_errno=True)
    source_bytes = os.fsencode(source.name)
    destination_bytes = os.fsencode(destination.name)
    if sys.platform.startswith("linux"):
        rename = getattr(libc, "renameat2", None)
        if rename is None:
            raise OSError(errno.ENOTSUP, "renameat2 is unavailable", str(source))
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(
            source_parent,
            source_bytes,
            destination_parent,
            destination_bytes,
            1,
        )
    elif sys.platform == "darwin":
        rename = getattr(libc, "renameatx_np", None)
        if rename is None:
            raise OSError(errno.ENOTSUP, "renameatx_np is unavailable", str(source))
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(
            source_parent,
            source_bytes,
            destination_parent,
            destination_bytes,
            4,
        )
    else:
        raise OSError(
            errno.ENOTSUP,
            "atomic no-replace moves are unavailable on this platform",
            str(source),
        )
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), str(destination))


def _classify(path: Path) -> tuple[str, str | None, int | None, int | None]:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return "absent", None, None, None
    if stat.S_ISLNK(metadata.st_mode):
        return "symlink", os.readlink(path), metadata.st_dev, metadata.st_ino
    if stat.S_ISREG(metadata.st_mode):
        return "file", None, metadata.st_dev, metadata.st_ino
    if stat.S_ISDIR(metadata.st_mode):
        return "directory", None, metadata.st_dev, metadata.st_ino
    return "unsupported", None, metadata.st_dev, metadata.st_ino


def _symlink_target_matches(
    destination: Path,
    target: str | None,
    expected_source: Path,
) -> bool:
    if target is None:
        return False
    target_path = Path(target)
    resolved_target = (
        target_path if target_path.is_absolute() else destination.parent / target_path
    ).resolve(strict=False)
    return resolved_target == expected_source.resolve(strict=False)


def _file_hash(
    path: Path,
    *,
    expected_identities: Mapping[Path, tuple[int, int]] | None = None,
) -> str | None:
    try:
        with _open_parent(
            path,
            expected_identities=expected_identities,
        ) as parent_descriptor:
            descriptor = os.open(
                path.name,
                os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=parent_descriptor,
            )
            open_descriptor: int | None = descriptor
            try:
                if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                    return None
                with os.fdopen(descriptor, "rb") as file:
                    open_descriptor = None
                    digest = hashlib.sha256()
                    for chunk in iter(lambda: file.read(1024 * 1024), b""):
                        digest.update(chunk)
                    return digest.hexdigest()
            finally:
                if open_descriptor is not None:
                    os.close(open_descriptor)
    except OSError:
        return None


def capture_file_input(path: Path) -> CapturedFileInput:
    """Read a supported file input and bind its state to opened descriptors."""

    try:
        return _capture_file_input(path)
    except FileNotFoundError:
        return CapturedFileInput(FileInputState(kind="absent"), None, None, None)


def _capture_file_input(path: Path) -> CapturedFileInput:
    """Capture one file input whose parent can be opened."""

    with _open_parent(path) as parent_descriptor:
        try:
            metadata = os.stat(
                path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            return CapturedFileInput(FileInputState(kind="absent"), None, None, None)
        if stat.S_ISREG(metadata.st_mode):
            contents, mode = _read_regular_file_at(
                path,
                parent_descriptor,
                expected_identity=(metadata.st_dev, metadata.st_ino),
                nofollow=True,
            )
            return CapturedFileInput(
                FileInputState(
                    kind="file",
                    content_hash=hashlib.sha256(contents).hexdigest(),
                    mode=mode,
                ),
                contents,
                metadata.st_dev,
                metadata.st_ino,
            )
        if not stat.S_ISLNK(metadata.st_mode):
            raise MutationExecutionError(
                f"unsupported file input type at {path}", restored=True
            )
        target = os.readlink(path.name, dir_fd=parent_descriptor)
        target_path = Path(target)
        referent = (
            target_path if target_path.is_absolute() else path.parent / target_path
        ).resolve(strict=False)
        try:
            contents, mode = _read_regular_file(referent)
        except FileNotFoundError:
            contents = None
            mode = None
        current = os.stat(
            path.name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if (
            (current.st_dev, current.st_ino) != (metadata.st_dev, metadata.st_ino)
            or not stat.S_ISLNK(current.st_mode)
            or os.readlink(path.name, dir_fd=parent_descriptor) != target
        ):
            raise MutationExecutionError(
                f"file input changed during inspection: {path}", restored=True
            )
        return CapturedFileInput(
            FileInputState(
                kind="symlink",
                content_hash=(
                    hashlib.sha256(contents).hexdigest()
                    if contents is not None
                    else None
                ),
                link_target=target,
                mode=mode,
            ),
            contents,
            metadata.st_dev,
            metadata.st_ino,
        )


def _read_regular_file(path: Path) -> tuple[bytes, int]:
    """Read one regular file through its descriptor-bound parent."""

    with _open_parent(path) as parent_descriptor:
        try:
            metadata = os.stat(
                path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=True,
            )
        except FileNotFoundError:
            raise
        if not stat.S_ISREG(metadata.st_mode):
            raise MutationExecutionError(
                f"file input referent is not a regular file: {path}", restored=True
            )
        return _read_regular_file_at(
            path,
            parent_descriptor,
            expected_identity=(metadata.st_dev, metadata.st_ino),
            nofollow=False,
        )


def _read_regular_file_at(
    path: Path,
    parent_descriptor: int,
    *,
    expected_identity: tuple[int, int],
    nofollow: bool,
) -> tuple[bytes, int]:
    """Read one stable regular file from an already opened parent."""

    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NONBLOCK", 0)
        | (getattr(os, "O_NOFOLLOW", 0) if nofollow else 0)
    )
    descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
    open_descriptor: int | None = descriptor
    try:
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or (before.st_dev, before.st_ino) != expected_identity
        ):
            raise MutationExecutionError(
                f"file input changed during inspection: {path}", restored=True
            )
        with os.fdopen(descriptor, "rb") as file:
            open_descriptor = None
            contents = file.read()
            after = os.fstat(file.fileno())
        if (
            (after.st_dev, after.st_ino) != expected_identity
            or after.st_size != before.st_size
            or after.st_mtime_ns != before.st_mtime_ns
        ):
            raise MutationExecutionError(
                f"file input changed during inspection: {path}", restored=True
            )
        visible = os.stat(
            path.name,
            dir_fd=parent_descriptor,
            follow_symlinks=not nofollow,
        )
        if (visible.st_dev, visible.st_ino) != expected_identity:
            raise MutationExecutionError(
                f"file input changed during inspection: {path}", restored=True
            )
        return contents, stat.S_IMODE(before.st_mode)
    finally:
        if open_descriptor is not None:
            os.close(open_descriptor)


def _normalize_authority_roots(roots: tuple[Path, ...]) -> tuple[Path, ...]:
    candidates = tuple(
        dict.fromkeys(root.expanduser().resolve(strict=False) for root in roots)
    )
    normalized = tuple(
        root
        for root in candidates
        if not any(root != other and root.is_relative_to(other) for other in candidates)
    )
    for root in normalized:
        try:
            metadata = root.lstat()
        except FileNotFoundError:
            parent = root.parent
            try:
                parent_metadata = parent.lstat()
            except OSError as error:
                raise MutationExecutionError(
                    f"managed path root parent does not exist: {parent}", restored=True
                ) from error
            if stat.S_ISLNK(parent_metadata.st_mode) or not stat.S_ISDIR(
                parent_metadata.st_mode
            ):
                raise MutationExecutionError(
                    f"managed path root parent is unsafe: {parent}", restored=True
                ) from None
            continue
        except OSError as error:
            raise MutationExecutionError(
                f"cannot inspect managed path root: {root}", restored=True
            ) from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise MutationExecutionError(
                f"managed path root is not a directory: {root}", restored=True
            )
    return normalized


def _authority_root(path: Path, roots: tuple[Path, ...]) -> Path | None:
    candidates = tuple(
        root for root in roots if path == root or path.is_relative_to(root)
    )
    return max(candidates, key=lambda root: len(root.parts), default=None)


def _require_authorized_parent(path: Path, roots: tuple[Path, ...]) -> None:
    if not roots:
        _existing_parent(path)
        return
    root = _authority_root(path, roots)
    if root is None:
        raise MutationExecutionError(
            f"destination is outside managed path roots: {path}", restored=True
        )
    current = root
    if not root.exists():
        if path != root and not path.is_relative_to(root):
            raise MutationExecutionError(
                f"destination is outside managed path root: {path}", restored=True
            )
        return
    relative_parent = path.parent.relative_to(root)
    for part in relative_parent.parts:
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise MutationExecutionError(
                f"destination has an unsafe parent path: {current}", restored=True
            )


def _parent_identities(
    path: Path,
    roots: tuple[Path, ...],
) -> tuple[tuple[Path, int, int], ...]:
    root = _authority_root(path, roots) if roots else _existing_parent(path)
    if root is None:
        return ()
    identities: list[tuple[Path, int, int]] = []
    current = root if root.exists() else root.parent
    while True:
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        identities.append((current, metadata.st_dev, metadata.st_ino))
        if current == path.parent:
            break
        relative = path.parent.relative_to(current)
        current /= relative.parts[0]
    return tuple(identities)


def _require_parent_identities(
    plan: _PlannedMutation,
    plans: Iterable[_PlannedMutation],
    roots: tuple[Path, ...],
) -> dict[Path, tuple[int, int]]:
    _require_authorized_parent(plan.mutation.destination, roots)
    expected = {
        path: (device, inode) for path, device, inode in plan.parent_identities
    }
    for other in plans:
        if not isinstance(other.record, DirectoryRecoveryRecord):
            continue
        destination = other.record.destination
        parent = plan.mutation.destination.parent
        if parent == destination or parent.is_relative_to(destination):
            expected[destination] = (
                other.record.result_device,
                other.record.result_inode,
            )
    for path, identity in expected.items():
        try:
            metadata = path.lstat()
        except OSError as error:
            raise MutationExecutionError(
                f"destination parent changed: {path}", restored=False
            ) from error
        if (metadata.st_dev, metadata.st_ino) != identity:
            raise MutationExecutionError(
                f"destination parent changed: {path}", restored=False
            )
    return expected


def _check_parent(path: Path, roots: tuple[Path, ...]) -> None:
    _require_authorized_parent(path, roots)
    ancestor = _existing_parent(path)
    if not ancestor.is_dir() or not os.access(ancestor, os.W_OK | os.X_OK):
        raise MutationExecutionError(
            f"parent directory is not writable for {path}: {ancestor}", restored=True
        )


def _existing_parent(path: Path) -> Path:
    ancestor = path.parent
    while not ancestor.exists():
        if ancestor.parent == ancestor:
            raise MutationExecutionError(
                f"cannot find a writable parent for {path}", restored=True
            )
        ancestor = ancestor.parent
    try:
        metadata = ancestor.lstat()
    except OSError as error:
        raise MutationExecutionError(
            f"cannot inspect a parent for {path}: {ancestor}", restored=True
        ) from error
    if stat.S_ISLNK(metadata.st_mode):
        raise MutationExecutionError(
            f"parent path must not be a symlink: {ancestor}", restored=True
        )
    return ancestor


def _numbered_backup(
    path: Path, timestamp: int, reserved: set[Path]
) -> Path:
    candidate = path.with_name(f"{path.name}.backup.{timestamp}")
    suffix = 1
    while candidate.exists() or candidate.is_symlink() or candidate in reserved:
        candidate = path.with_name(f"{path.name}.backup.{timestamp}.{suffix}")
        suffix += 1
    reserved.add(candidate)
    return candidate


def _unique_backup(path: Path, timestamp: int, reserved: set[Path]) -> Path:
    base = _numbered_backup(path, timestamp, reserved)
    reserved.discard(base)
    candidate = base.with_name(f"{base.name}.{uuid.uuid4().hex}")
    while candidate.exists() or candidate.is_symlink() or candidate in reserved:
        candidate = base.with_name(f"{base.name}.{uuid.uuid4().hex}")
    reserved.add(candidate)
    return candidate


def _unique_result_backup(path: Path, reserved: set[Path]) -> Path:
    ancestor = _existing_parent(path)
    candidate = ancestor / f".{path.name}.dotfiles-result.{uuid.uuid4().hex}"
    while candidate.exists() or candidate.is_symlink() or candidate in reserved:
        candidate = ancestor / f".{path.name}.dotfiles-result.{uuid.uuid4().hex}"
    reserved.add(candidate)
    return candidate


def _runtime_result_backup(path: Path) -> Path:
    candidate = path.with_name(f".{path.name}.dotfiles-result.{uuid.uuid4().hex}")
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(f".{path.name}.dotfiles-result.{uuid.uuid4().hex}")
    return candidate


def _runtime_changed_backup(path: Path) -> Path:
    candidate = path.with_name(f".{path.name}.dotfiles-changed.{uuid.uuid4().hex}")
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(f".{path.name}.dotfiles-changed.{uuid.uuid4().hex}")
    return candidate


def _runtime_cleanup_backup(path: Path) -> Path:
    candidate = path.with_name(f".{path.name}.dotfiles-cleanup.{uuid.uuid4().hex}")
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(
            f".{path.name}.dotfiles-cleanup.{uuid.uuid4().hex}"
        )
    return candidate


def _unique_stage_path(path: Path, reserved: set[Path]) -> Path:
    ancestor = _existing_parent(path)
    candidate = ancestor / f".{path.name}.dotfiles.{uuid.uuid4().hex}"
    while candidate.exists() or candidate.is_symlink() or candidate in reserved:
        candidate = ancestor / f".{path.name}.dotfiles.{uuid.uuid4().hex}"
    reserved.add(candidate)
    return candidate
