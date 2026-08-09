"""Per-user advisory locking for mutating setup commands."""

from __future__ import annotations

import errno
import fcntl
import json
import os
import stat
import time
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path

from dotfiles_setup.errors import LockError


def lock_path(environ: Mapping[str, str] | None = None) -> Path:
    """Return a user-scoped lock path outside the repository."""

    values = os.environ if environ is None else environ
    home = Path(values.get("HOME", str(Path.home()))).expanduser().resolve()
    configured = Path(values.get("XDG_CACHE_HOME", "")).expanduser()
    cache_home = configured.resolve(strict=False) if configured.is_absolute() else home / ".cache"
    return cache_home / "dotfiles" / "setup.lock"


@contextmanager
def mutation_lock(
    operation: str,
    *,
    environ: Mapping[str, str] | None = None,
) -> Iterator[Path]:
    """Acquire the setup lock without waiting and retain its inode after release."""

    path = lock_path(environ)
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_CLOEXEC"):
            flags |= os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags, 0o600)
    except OSError as error:
        raise LockError(f"cannot open mutation lock {path}: {error.strerror}") from error

    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise LockError(f"mutation lock is not a regular file: {path}")
        if hasattr(os, "getuid") and metadata.st_uid != os.getuid():
            raise LockError(f"mutation lock is not owned by the current user: {path}")
        os.fchmod(descriptor, 0o600)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            if error.errno in {errno.EACCES, errno.EAGAIN}:
                raise LockError(
                    f"another dotfiles setup operation is running (lock: {path}); "
                    "wait for it to finish and retry"
                ) from error
            raise LockError(f"cannot acquire mutation lock {path}: {error.strerror}") from error

        payload = json.dumps(
            {"operation": operation, "pid": os.getpid(), "started_at": int(time.time())},
            sort_keys=True,
        )
        os.ftruncate(descriptor, 0)
        os.write(descriptor, payload.encode())
        os.fsync(descriptor)
        yield path
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)
