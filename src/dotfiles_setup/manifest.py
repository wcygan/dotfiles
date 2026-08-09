"""Durable, content-free operation journaling for setup mutations."""

from __future__ import annotations

import json
import os
import stat
import tempfile
import time
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from dotfiles_setup.errors import ManifestError

SCHEMA_VERSION = 1
VALID_STATES = {"planned", "applying", "completed", "failed", "recovery-needed"}


def state_directory(environ: Mapping[str, str] | None = None) -> Path:
    values = os.environ if environ is None else environ
    home = Path(values.get("HOME", str(Path.home()))).expanduser().resolve()
    configured = Path(values.get("XDG_STATE_HOME", "")).expanduser()
    root = (
        configured.resolve(strict=False) if configured.is_absolute() else home / ".local" / "state"
    )
    return root / "dotfiles"


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.parent.chmod(0o700)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "w") as file:
                json.dump(value, file, indent=2, sort_keys=True)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    except OSError as error:
        raise ManifestError(f"cannot write operation manifest {path}: {error}") from error


def read_manifest(path: Path) -> dict[str, Any]:
    try:
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode):
            raise ManifestError(f"operation manifest is not a regular file: {path}")
        if hasattr(os, "getuid") and metadata.st_uid != os.getuid():
            raise ManifestError(f"operation manifest is not owned by the current user: {path}")
        if metadata.st_mode & 0o022:
            raise ManifestError(f"operation manifest is writable by another user: {path}")
        value = json.loads(path.read_text())
    except ManifestError:
        raise
    except (OSError, json.JSONDecodeError) as error:
        raise ManifestError(f"cannot read operation manifest {path}: {error}") from error
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise ManifestError(f"unsupported operation manifest at {path}")
    if value.get("state") not in VALID_STATES:
        raise ManifestError(f"invalid operation state in {path}")
    return value


class OperationJournal:
    """Atomically persist one mutating command's recovery-relevant metadata."""

    def __init__(
        self,
        command: str,
        repo_root: Path,
        *,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self.directory = state_directory(environ)
        self.active_path = self.directory / "current.json"
        self.completed_path = self.directory / "completed.json"
        self.recovery_path = self.directory / "recovery-needed.json"
        if self.active_path.exists():
            active = read_manifest(self.active_path)
            if active["state"] == "completed":
                _atomic_json(self.completed_path, active)
        for pending_path in (self.recovery_path, self.active_path):
            if not pending_path.exists():
                continue
            pending = read_manifest(pending_path)
            if pending["state"] in {"applying", "recovery-needed"}:
                raise ManifestError(
                    f"an interrupted setup operation is recorded at {pending_path}; "
                    "run ./bootstrap.sh recover before making more changes"
                )
        timestamp = int(time.time())
        self.data: dict[str, Any] = {
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
        _atomic_json(self.active_path, self.data)

    def _write(self) -> None:
        self.data["updated_at"] = int(time.time())
        _atomic_json(self.active_path, self.data)

    def transition(self, state: str) -> None:
        if state not in VALID_STATES:
            raise ManifestError(f"invalid operation state: {state}")
        self.data["state"] = state
        self._write()
        if state == "completed":
            _atomic_json(self.completed_path, self.data)
        elif state == "recovery-needed":
            _atomic_json(self.recovery_path, self.data)

    def add_link_entry(self, entry: dict[str, Any]) -> int:
        entries = self.data["entries"]
        assert isinstance(entries, list)
        entries.append(entry)
        self._write()
        return len(entries) - 1

    def update_link_entry(self, index: int, **changes: Any) -> None:
        entries = self.data["entries"]
        assert isinstance(entries, list)
        entry = entries[index]
        assert isinstance(entry, dict)
        entry.update(changes)
        self._write()

    def record_operation(self, name: str, status: str) -> None:
        operations = self.data["operations"]
        assert isinstance(operations, list)
        operations.append({"name": name, "status": status})
        self._write()
