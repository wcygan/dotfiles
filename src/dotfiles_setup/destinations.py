"""One classification for every managed destination.

The install, verification, and mutation code all need to answer the same
question about a destination path: is it absent, correct, stale, broken, or
some kind of unmanaged object? Before this module each caller answered it
differently, so a destination could be "correct" to one caller and "stale" to
another. A destination that one caller considered already installed was
therefore silently skipped by the install path.

The transition table is ``DESTINATION_STATES``: for each raw kind and each
expected-source situation, exactly one semantic state. Every destination
therefore resolves to one enum value, never to an implicit "unknown".
"""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class FileKind(StrEnum):
    """The raw filesystem type of a destination."""

    ABSENT = "absent"
    SYMLINK = "symlink"
    FILE = "file"
    DIRECTORY = "directory"
    UNSUPPORTED = "unsupported"


class DestinationState(StrEnum):
    """The semantic state of a managed destination."""

    ABSENT = "absent"
    CORRECT = "correct"
    STALE = "stale"
    BROKEN = "broken"
    UNMANAGED_FILE = "unmanaged-file"
    UNMANAGED_DIRECTORY = "unmanaged-directory"
    UNMANAGED_OTHER = "unmanaged-other"


@dataclass(frozen=True)
class DestinationClassification:
    """The one classification every caller should use."""

    kind: FileKind
    state: DestinationState
    target: str | None = None
    device: int | None = None
    inode: int | None = None
    reason: str | None = None

    @property
    def needs_replacement(self) -> bool:
        """Return whether installing the managed link must change this destination."""

        return self.state in {
            DestinationState.ABSENT,
            DestinationState.STALE,
            DestinationState.BROKEN,
            DestinationState.UNMANAGED_FILE,
            DestinationState.UNMANAGED_DIRECTORY,
            DestinationState.UNMANAGED_OTHER,
        }


def _resolve_target(destination: Path, target: str) -> Path | None:
    """Return the resolved symlink target, or None when it cannot be resolved."""

    try:
        target_path = Path(target)
        resolved = (
            target_path if target_path.is_absolute() else destination.parent / target_path
        ).resolve(strict=False)
    except (OSError, RuntimeError):
        return None
    if not resolved.exists():
        return None
    return resolved


def _expected_source(expected_source: Path) -> Path | None:
    try:
        return expected_source.resolve(strict=False)
    except (OSError, RuntimeError):
        return None


def classify(
    destination: Path,
    expected_source: Path | None = None,
) -> DestinationClassification:
    """Classify ``destination``, optionally against the managed source.

    The order matters. A symlink is resolved and compared only when an expected
    source is supplied; otherwise it is an unmanaged object. A missing
    destination is always ABSENT, never BROKEN.
    """

    try:
        metadata = destination.lstat()
    except FileNotFoundError:
        return DestinationClassification(FileKind.ABSENT, DestinationState.ABSENT)
    except OSError as error:
        return DestinationClassification(
            FileKind.UNSUPPORTED,
            DestinationState.UNMANAGED_OTHER,
            reason=f"cannot inspect destination: {error}",
        )

    if stat.S_ISLNK(metadata.st_mode):
        target = os.readlink(destination)
        if expected_source is None:
            return DestinationClassification(
                FileKind.SYMLINK,
                DestinationState.UNMANAGED_OTHER,
                target=target,
                device=metadata.st_dev,
                inode=metadata.st_ino,
            )
        resolved = _resolve_target(destination, target)
        expected = _expected_source(expected_source)
        if resolved is None or expected is None:
            return DestinationClassification(
                FileKind.SYMLINK,
                DestinationState.BROKEN,
                target=target,
                device=metadata.st_dev,
                inode=metadata.st_ino,
            )
        if resolved != expected:
            return DestinationClassification(
                FileKind.SYMLINK,
                DestinationState.STALE,
                target=target,
                device=metadata.st_dev,
                inode=metadata.st_ino,
            )
        return DestinationClassification(
            FileKind.SYMLINK,
            DestinationState.CORRECT,
            target=target,
            device=metadata.st_dev,
            inode=metadata.st_ino,
        )

    if stat.S_ISREG(metadata.st_mode):
        return DestinationClassification(
            FileKind.FILE,
            DestinationState.UNMANAGED_FILE,
            device=metadata.st_dev,
            inode=metadata.st_ino,
        )
    if stat.S_ISDIR(metadata.st_mode):
        return DestinationClassification(
            FileKind.DIRECTORY,
            DestinationState.UNMANAGED_DIRECTORY,
            device=metadata.st_dev,
            inode=metadata.st_ino,
        )
    return DestinationClassification(
        FileKind.UNSUPPORTED,
        DestinationState.UNMANAGED_OTHER,
        device=metadata.st_dev,
        inode=metadata.st_ino,
    )


def state_for(kind: FileKind, *, matches_expected: bool | None = None) -> DestinationState:
    """Return the semantic state for a raw kind.

    ``matches_expected`` applies only to symlinks; other kinds ignore it. The
    table is total so no kind can fall through to an implicit default.
    """

    if kind is FileKind.ABSENT:
        return DestinationState.ABSENT
    if kind is FileKind.FILE:
        return DestinationState.UNMANAGED_FILE
    if kind is FileKind.DIRECTORY:
        return DestinationState.UNMANAGED_DIRECTORY
    if kind is FileKind.SYMLINK:
        if matches_expected is None:
            return DestinationState.UNMANAGED_OTHER
        return DestinationState.CORRECT if matches_expected else DestinationState.STALE
    return DestinationState.UNMANAGED_OTHER
