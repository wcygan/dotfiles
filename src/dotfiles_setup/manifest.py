"""Durable, content-free operation journaling for setup mutations."""

from __future__ import annotations

import json
import os
import stat
import time
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotfiles_setup.errors import ManifestError
from dotfiles_setup.mutations import RecoveryRecord, decode_recovery_record
from dotfiles_setup.paths import UserPathContext

SCHEMA_VERSION = 1
VALID_STATES = {"planned", "applying", "completed", "failed", "recovery-needed"}


def state_directory(environ: Mapping[str, str] | None = None) -> Path:
    """Return the setup state directory for a compatible caller."""

    return UserPathContext.from_environment(environ).state_directory


@contextmanager
def _open_manifest_directory(path: Path, *, create: bool) -> Iterator[int]:
    """Open or create a directory through a no-follow descriptor walk."""

    absolute = Path(os.path.abspath(path))
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(absolute.anchor, flags)
    try:
        for part in absolute.parts[1:]:
            try:
                next_descriptor = os.open(part, flags, dir_fd=descriptor)
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    os.mkdir(part, mode=0o700, dir_fd=descriptor)
                except FileExistsError:
                    pass
                else:
                    os.fsync(descriptor)
                next_descriptor = os.open(part, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        yield descriptor
    finally:
        os.close(descriptor)


@contextmanager
def _open_manifest_parent(path: Path) -> Iterator[tuple[int, str]]:
    """Open a manifest parent without following path symlinks."""

    absolute = Path(os.path.abspath(path))
    with _open_manifest_directory(absolute.parent, create=False) as descriptor:
        yield descriptor, absolute.name


def _manifest_entry_present(path: Path) -> bool:
    """Report whether a manifest entry exists without following links."""

    try:
        with _open_manifest_parent(path) as (parent_descriptor, name):
            os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except FileNotFoundError:
        return False
    except OSError as error:
        raise ManifestError(f"cannot inspect operation manifest {path}: {error}") from error
    return True


def _require_visible_directory(path: Path, descriptor: int) -> None:
    """Reject a directory that no longer owns its configured path."""

    expected = os.fstat(descriptor)
    with _open_manifest_directory(path, create=False) as visible_descriptor:
        visible = os.fstat(visible_descriptor)
    if (visible.st_dev, visible.st_ino) != (expected.st_dev, expected.st_ino):
        raise OSError(f"operation state directory changed: {path}")


def _create_manifest_temporary(parent_descriptor: int, name: str) -> tuple[int, str]:
    """Create one private temporary file in an open manifest directory."""

    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    for _attempt in range(32):
        temporary_name = f".{name}.{uuid.uuid4().hex}"
        try:
            descriptor = os.open(
                temporary_name,
                flags,
                0o600,
                dir_fd=parent_descriptor,
            )
        except FileExistsError:
            continue
        return descriptor, temporary_name
    raise FileExistsError(f"cannot create a temporary manifest for {name}")


def _remove_manifest(path: Path) -> None:
    """Remove a manifest and sync its bound parent directory."""

    absolute = Path(os.path.abspath(path))
    with _open_manifest_directory(absolute.parent, create=False) as parent_descriptor:
        with suppress(FileNotFoundError):
            os.unlink(absolute.name, dir_fd=parent_descriptor)
        os.fsync(parent_descriptor)
        _require_visible_directory(absolute.parent, parent_descriptor)


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    absolute = Path(os.path.abspath(path))
    temporary_name: str | None = None
    try:
        with _open_manifest_directory(absolute.parent, create=True) as parent_descriptor:
            os.fchmod(parent_descriptor, 0o700)
            _require_visible_directory(absolute.parent, parent_descriptor)
            descriptor, temporary_name = _create_manifest_temporary(
                parent_descriptor,
                absolute.name,
            )
            try:
                os.fchmod(descriptor, 0o600)
                file = os.fdopen(descriptor, "w", encoding="utf-8")
                descriptor = -1
                with file:
                    json.dump(value, file, indent=2, sort_keys=True)
                    file.write("\n")
                    file.flush()
                    os.fsync(file.fileno())
                os.replace(
                    temporary_name,
                    absolute.name,
                    src_dir_fd=parent_descriptor,
                    dst_dir_fd=parent_descriptor,
                )
                temporary_name = None
                os.fsync(parent_descriptor)
                _require_visible_directory(absolute.parent, parent_descriptor)
            finally:
                if descriptor >= 0:
                    os.close(descriptor)
                if temporary_name is not None:
                    try:
                        os.unlink(temporary_name, dir_fd=parent_descriptor)
                    except FileNotFoundError:
                        pass
                    else:
                        os.fsync(parent_descriptor)
    except OSError as error:
        raise ManifestError(f"cannot write operation manifest {path}: {error}") from error


def _read_manifest(path: Path) -> dict[str, Any]:
    descriptor: int | None = None
    try:
        with _open_manifest_parent(path) as (parent_descriptor, name):
            metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if not stat.S_ISREG(metadata.st_mode):
                raise ManifestError(
                    f"operation manifest is not a regular file: {path}"
                )
            if hasattr(os, "getuid") and metadata.st_uid != os.getuid():
                raise ManifestError(
                    f"operation manifest is not owned by the current user: {path}"
                )
            if metadata.st_mode & 0o022:
                raise ManifestError(
                    f"operation manifest is writable by another user: {path}"
                )
            descriptor = os.open(
                name,
                os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NONBLOCK", 0)
                | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=parent_descriptor,
            )
            opened = os.fstat(descriptor)
            if (
                not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino)
                != (metadata.st_dev, metadata.st_ino)
                or opened.st_mode != metadata.st_mode
                or opened.st_uid != metadata.st_uid
                or opened.st_size != metadata.st_size
                or opened.st_mtime_ns != metadata.st_mtime_ns
                or opened.st_ctime_ns != metadata.st_ctime_ns
            ):
                raise ManifestError(
                    f"operation manifest changed during inspection: {path}"
                )
            with os.fdopen(descriptor, encoding="utf-8") as file:
                descriptor = None
                value = json.load(file)
                after = os.fstat(file.fileno())
            visible = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if (
                (after.st_dev, after.st_ino) != (metadata.st_dev, metadata.st_ino)
                or after.st_mode != opened.st_mode
                or after.st_uid != opened.st_uid
                or after.st_size != opened.st_size
                or after.st_mtime_ns != opened.st_mtime_ns
                or after.st_ctime_ns != opened.st_ctime_ns
                or (visible.st_dev, visible.st_ino)
                != (metadata.st_dev, metadata.st_ino)
                or not stat.S_ISREG(visible.st_mode)
                or visible.st_mode != after.st_mode
                or visible.st_uid != after.st_uid
                or visible.st_size != after.st_size
                or visible.st_mtime_ns != after.st_mtime_ns
                or visible.st_ctime_ns != after.st_ctime_ns
            ):
                raise ManifestError(
                    f"operation manifest changed during inspection: {path}"
                )
    except ManifestError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ManifestError(f"cannot read operation manifest {path}: {error}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise ManifestError(f"unsupported operation manifest at {path}")
    if value.get("state") not in VALID_STATES:
        raise ManifestError(f"invalid operation state in {path}")
    return value


@dataclass(frozen=True)
class PendingManifest:
    """The selected durable manifest for an interrupted operation."""

    path: Path
    data: dict[str, Any]


class ManifestRepository:
    """Own durable schema-v1 manifest storage and recovery checkpoints."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.active_path = directory / "current.json"
        self.completed_path = directory / "completed.json"
        self.recovery_path = directory / "recovery-needed.json"

    @classmethod
    def from_environment(
        cls,
        environ: Mapping[str, str] | None = None,
    ) -> ManifestRepository:
        """Create a repository for the supplied user environment."""

        return cls(state_directory(environ))

    def read(self, path: Path) -> dict[str, Any]:
        """Read and validate one manifest file."""

        return _read_manifest(path)

    def write(self, path: Path, value: dict[str, Any]) -> None:
        """Atomically write one content-free manifest file."""

        _atomic_json(path, value)

    def start(self, command: str, repo_root: Path) -> dict[str, Any]:
        """Create a planned operation without replacing interrupted work."""

        if _manifest_entry_present(self.active_path):
            active = self.read(self.active_path)
            if active["state"] == "completed":
                self.write(self.completed_path, active)
        for pending_path in (self.recovery_path, self.active_path):
            if not _manifest_entry_present(pending_path):
                continue
            pending = self.read(pending_path)
            if pending["state"] in {"applying", "recovery-needed"}:
                raise ManifestError(
                    f"an interrupted setup operation is recorded at {pending_path}; "
                    "run ./bootstrap.sh recover before making more changes"
                )
        timestamp = int(time.time())
        data: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "repository_root": str(repo_root.resolve()),
            "operation_id": str(uuid.uuid4()),
            "command": command,
            "created_at": timestamp,
            "updated_at": timestamp,
            "state": "planned",
            "entries": [],
            "operations": [],
            "recovery_guidance": "Run ./bootstrap.sh recover before making more setup changes.",
        }
        self.write(self.active_path, data)
        return data

    def pending(self) -> PendingManifest | None:
        """Select the authoritative interrupted-operation manifest."""

        if _manifest_entry_present(self.recovery_path):
            value = self.read(self.recovery_path)
            if value["state"] == "recovery-needed":
                return PendingManifest(self.recovery_path, value)
        if _manifest_entry_present(self.active_path):
            value = self.read(self.active_path)
            if value["state"] in {"applying", "recovery-needed"}:
                return PendingManifest(self.active_path, value)
        return None

    def checkpoint_recovery(self, path: Path, manifest: dict[str, Any]) -> None:
        """Persist recovery progress at both durable recovery locations."""

        manifest["state"] = "recovery-needed"
        manifest["updated_at"] = int(time.time())
        self.write(path, manifest)
        self.write(self.recovery_path, manifest)

    def checkpoint_entry_recovery(
        self,
        path: Path,
        manifest: dict[str, Any],
        index: int,
        entry: RecoveryRecord,
    ) -> None:
        """Replace one typed entry and persist its recovery progress."""

        entries = manifest.get("entries")
        if not isinstance(entries, list):
            raise ManifestError("operation manifest has invalid recovery entries")
        try:
            entries[index] = entry.to_manifest()
        except IndexError as error:
            raise ManifestError(f"operation manifest has no entry {index}") from error
        self.checkpoint_recovery(path, manifest)

    def complete_recovery(self, manifest: dict[str, Any]) -> None:
        """Persist recovery completion and remove the pending marker."""

        entries = manifest.get("entries")
        if not isinstance(entries, list):
            raise ManifestError("operation manifest has invalid recovery entries")
        for index, raw in enumerate(entries):
            if not isinstance(raw, dict):
                raise ManifestError(
                    f"operation manifest entry {index} is not a recovery record"
                )
            try:
                entry = decode_recovery_record(raw)
            except ValueError as error:
                raise ManifestError(
                    f"operation manifest entry {index} is invalid: {error}"
                ) from error
            if entry.mutation_started and not (entry.recovered or entry.restored):
                raise ManifestError(
                    f"operation manifest entry {index} still needs recovery"
                )
        manifest["state"] = "completed"
        manifest["updated_at"] = int(time.time())
        self.write(self.active_path, manifest)
        self.write(self.completed_path, manifest)
        try:
            _remove_manifest(self.recovery_path)
        except OSError as error:
            raise ManifestError(
                f"cannot remove recovery manifest {self.recovery_path}: {error}"
            ) from error


def read_manifest(path: Path) -> dict[str, Any]:
    """Read one manifest through the compatibility facade."""

    return ManifestRepository(path.parent).read(path)


class OperationJournal:
    """Atomically persist one mutating command's recovery-relevant metadata."""

    def __init__(
        self,
        command: str,
        repo_root: Path,
        *,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self.repository = ManifestRepository.from_environment(environ)
        self.directory = self.repository.directory
        self.active_path = self.repository.active_path
        self.completed_path = self.repository.completed_path
        self.recovery_path = self.repository.recovery_path
        self.data = self.repository.start(command, repo_root)

    def _write(self) -> None:
        self.data["updated_at"] = int(time.time())
        self.repository.write(self.active_path, self.data)

    @property
    def state(self) -> str:
        """Return the current journal state."""

        state = self.data.get("state")
        if not isinstance(state, str):
            raise ManifestError("operation journal has no valid state")
        return state

    @property
    def failed_operations(self) -> tuple[str, ...]:
        """Return operation names that reported failure."""

        operations = self.data.get("operations")
        if not isinstance(operations, list):
            raise ManifestError("operation journal has invalid operations")
        return tuple(
            str(operation["name"])
            for operation in operations
            if isinstance(operation, dict)
            and isinstance(operation.get("name"), str)
            and operation.get("status") == "failed"
        )

    @property
    def pending_entries(self) -> tuple[RecoveryRecord, ...]:
        """Return started entries that still need recovery."""

        entries = self.data.get("entries")
        if not isinstance(entries, list):
            raise ManifestError("operation journal has invalid recovery entries")
        decoded = tuple(self._decode_entry(raw) for raw in entries)
        return tuple(
            entry
            for entry in decoded
            if entry.mutation_started and not entry.recovered and not entry.restored
        )

    def entry(self, index: int) -> RecoveryRecord:
        """Return one typed recovery entry."""

        entries = self.data.get("entries")
        if not isinstance(entries, list):
            raise ManifestError("operation journal has invalid recovery entries")
        try:
            raw = entries[index]
        except IndexError as error:
            raise ManifestError(f"operation journal has no entry {index}") from error
        return self._decode_entry(raw)

    @staticmethod
    def _decode_entry(raw: Any) -> RecoveryRecord:
        if not isinstance(raw, dict):
            raise ManifestError("operation journal contains an invalid recovery entry")
        try:
            return decode_recovery_record(raw)
        except ValueError as error:
            raise ManifestError(f"invalid recovery entry: {error}") from error

    def transition(self, state: str) -> None:
        if state not in VALID_STATES:
            raise ManifestError(f"invalid operation state: {state}")
        self.data["state"] = state
        self._write()
        if state == "completed":
            self.repository.write(self.completed_path, self.data)
        elif state == "recovery-needed":
            self.repository.write(self.recovery_path, self.data)

    def add_entry(self, entry: RecoveryRecord) -> int:
        """Append one typed recovery record."""

        entries = self.data["entries"]
        assert isinstance(entries, list)
        entries.append(entry.to_manifest())
        self._write()
        return len(entries) - 1

    def replace_entry(self, index: int, entry: RecoveryRecord) -> None:
        """Replace one typed record after its staged identity is known."""

        entries = self.data["entries"]
        assert isinstance(entries, list)
        try:
            current = entries[index]
        except IndexError as error:
            raise ManifestError(f"operation journal has no entry {index}") from error
        if not isinstance(current, dict):
            raise ManifestError(f"operation journal entry {index} is invalid")
        replacement = entry.to_manifest()
        for field in ("mutation_started", "applied", "recovered", "restored"):
            if current.get(field) is True:
                replacement[field] = True
        entries[index] = replacement
        self._write()

    def mark_started(self, index: int) -> None:
        """Record that an entry can require recovery."""

        self._update_entry(index, mutation_started=True)

    def mark_applied(self, index: int) -> None:
        """Record that an entry reached its planned result."""

        self._update_entry(index, mutation_started=True, applied=True)

    def mark_recovered(self, index: int) -> None:
        """Record that recovery restored an entry."""

        self._update_entry(index, recovered=True)

    def mark_restored(self, index: int) -> None:
        """Record that immediate rollback restored an entry."""

        self._update_entry(
            index,
            mutation_started=False,
            applied=False,
            restored=True,
            recovered=True,
        )

    def _update_entry(self, index: int, **changes: Any) -> None:
        entries = self.data["entries"]
        assert isinstance(entries, list)
        try:
            entry = entries[index]
        except IndexError as error:
            raise ManifestError(f"operation journal has no entry {index}") from error
        if not isinstance(entry, dict):
            raise ManifestError(f"operation journal entry {index} is invalid")
        entry.update(changes)
        self._write()

    def add_link_entry(self, entry: dict[str, Any]) -> int:
        """Append a raw entry through the schema-v1 compatibility facade."""

        entries = self.data["entries"]
        assert isinstance(entries, list)
        entries.append(entry)
        self._write()
        return len(entries) - 1

    def update_link_entry(self, index: int, **changes: Any) -> None:
        """Update a raw entry through the schema-v1 compatibility facade."""

        self._update_entry(index, **changes)

    def record_operation(self, name: str, status: str) -> None:
        operations = self.data["operations"]
        assert isinstance(operations, list)
        operations.append({"name": name, "status": status})
        self._write()
