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
from typing import NamedTuple

from dotfiles_setup.errors import LockError
from dotfiles_setup.paths import UserPathContext


def lock_path(environ: Mapping[str, str] | None = None) -> Path:
    """Return a user-scoped lock path outside the repository."""

    return UserPathContext.from_environment(environ).mutation_lock_path


@contextmanager
def mutation_lock(
    operation: str,
    *,
    environ: Mapping[str, str] | None = None,
) -> Iterator[Path]:
    """Acquire the setup lock without waiting and retain its inode after release."""

    path = lock_path(environ)
    parent_chain: list[_BoundDirectory] = []
    descriptor: int | None = None
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        parent_chain = _open_parent_chain(path.parent)
        parent_descriptor = parent_chain[-1].descriptor
        descriptor = os.open(
            path.name,
            os.O_RDWR
            | os.O_CREAT
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            0o600,
            dir_fd=parent_descriptor,
        )
        _require_visible_parent_chain(parent_chain, path.parent)
    except OSError as error:
        try:
            if descriptor is not None:
                os.close(descriptor)
        finally:
            _close_parent_chain(parent_chain)
        raise LockError(f"cannot open mutation lock {path}: {error.strerror}") from error

    assert descriptor is not None
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
        try:
            _require_visible_parent_chain(parent_chain, path.parent)
        except OSError as error:
            raise LockError(
                f"mutation lock parent changed during acquisition: {path.parent}"
            ) from error
        yield path
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            try:
                os.close(descriptor)
            finally:
                _close_parent_chain(parent_chain)


class _BoundDirectory(NamedTuple):
    """One directory bound to its visible parent entry."""

    descriptor: int
    parent_descriptor: int | None
    name: str | None
    device: int
    inode: int


def _open_parent_chain(path: Path) -> list[_BoundDirectory]:
    """Open an absolute directory through a no-follow descriptor walk."""

    if not path.is_absolute():
        raise OSError(errno.EINVAL, "mutation lock parent must be absolute", str(path))
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    chain: list[_BoundDirectory] = []
    try:
        descriptor = os.open(path.anchor, flags)
        metadata = os.fstat(descriptor)
        chain.append(
            _BoundDirectory(
                descriptor,
                None,
                None,
                metadata.st_dev,
                metadata.st_ino,
            )
        )
        for part in path.parts[1:]:
            visible = os.stat(part, dir_fd=descriptor, follow_symlinks=False)
            if not stat.S_ISDIR(visible.st_mode):
                raise OSError(
                    errno.ENOTDIR,
                    "mutation lock parent component is not a directory",
                    str(path),
                )
            child_descriptor = os.open(part, flags, dir_fd=descriptor)
            try:
                opened = os.fstat(child_descriptor)
                if (opened.st_dev, opened.st_ino) != (
                    visible.st_dev,
                    visible.st_ino,
                ):
                    raise OSError(
                        errno.ESTALE,
                        "mutation lock parent changed during traversal",
                        str(path),
                    )
            except Exception:
                os.close(child_descriptor)
                raise
            chain.append(
                _BoundDirectory(
                    child_descriptor,
                    descriptor,
                    part,
                    opened.st_dev,
                    opened.st_ino,
                )
            )
            descriptor = child_descriptor
        return chain
    except Exception:
        _close_parent_chain(chain)
        raise


def _require_visible_parent_chain(
    chain: list[_BoundDirectory],
    path: Path,
) -> None:
    """Reject a parent component that no longer names its opened directory."""

    for directory in chain[1:]:
        assert directory.parent_descriptor is not None
        assert directory.name is not None
        try:
            visible = os.stat(
                directory.name,
                dir_fd=directory.parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError as error:
            raise OSError(
                errno.ESTALE,
                "mutation lock parent changed during acquisition",
                str(path),
            ) from error
        if (
            not stat.S_ISDIR(visible.st_mode)
            or (visible.st_dev, visible.st_ino) != (directory.device, directory.inode)
        ):
            raise OSError(
                errno.ESTALE,
                "mutation lock parent changed during acquisition",
                str(path),
            )


def _close_parent_chain(chain: list[_BoundDirectory]) -> None:
    """Close a parent descriptor chain in reverse order."""

    for directory in reversed(chain):
        os.close(directory.descriptor)
