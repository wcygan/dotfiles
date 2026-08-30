"""Capture one local file without crossing its allowed path scope."""

from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path

from dotfiles_setup.mutations import (
    CapturedFileInput,
    FileInputState,
    MutationExecutionError,
    _open_parent,
    _read_regular_file_at,
)


@dataclass(frozen=True)
class ScopedFileInput:
    """A visible file path and its safely captured effective input."""

    visible_path: Path
    effective_path: Path
    captured: CapturedFileInput


class FileInputOutsideScopeError(ValueError):
    """A visible symlink resolves outside its allowed path scope."""

    def __init__(self, visible_path: Path, effective_path: Path) -> None:
        super().__init__(f"{visible_path} -> {effective_path}")
        self.visible_path = visible_path
        self.effective_path = effective_path


def capture_scoped_file_input(
    visible_path: Path,
    *,
    scope_root: Path,
) -> ScopedFileInput:
    """Bind a visible path, enforce its scope, and capture its effective file."""

    scope = scope_root.expanduser().resolve(strict=False)
    parent_bound = False
    try:
        with _open_parent(visible_path) as parent_descriptor:
            parent_bound = True
            parent_identity = _descriptor_identity(parent_descriptor)
            try:
                metadata = os.stat(
                    visible_path.name,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                _require_still_absent(visible_path, parent_identity)
                return ScopedFileInput(
                    visible_path,
                    visible_path,
                    _absent_file_input(),
                )

            if stat.S_ISREG(metadata.st_mode):
                captured = _capture_regular_file(
                    visible_path,
                    parent_descriptor,
                    metadata,
                )
                _require_same_regular_file(
                    visible_path,
                    parent_identity,
                    (metadata.st_dev, metadata.st_ino),
                )
                return ScopedFileInput(visible_path, visible_path, captured)

            if not stat.S_ISLNK(metadata.st_mode):
                raise MutationExecutionError(
                    f"unsupported file input type at {visible_path}",
                    restored=True,
                )

            target = os.readlink(visible_path.name, dir_fd=parent_descriptor)
            effective_path = _resolved_link_target(visible_path, target)
            _require_in_scope(visible_path, effective_path, scope)
            captured = _capture_effective_file(effective_path)
            _require_same_symlink(
                visible_path,
                parent_identity,
                (metadata.st_dev, metadata.st_ino),
                target,
                effective_path,
                scope,
            )
            return ScopedFileInput(visible_path, effective_path, captured)
    except FileNotFoundError as error:
        if parent_bound:
            raise MutationExecutionError(
                f"file input changed during inspection: {visible_path}",
                restored=True,
            ) from error
        return ScopedFileInput(visible_path, visible_path, _absent_file_input())


def _capture_effective_file(path: Path) -> CapturedFileInput:
    """Capture a resolved regular file without following its leaf."""

    try:
        with _open_parent(path) as parent_descriptor:
            parent_identity = _descriptor_identity(parent_descriptor)
            try:
                metadata = os.stat(
                    path.name,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                _require_still_absent(path, parent_identity)
                return _absent_file_input()
            if not stat.S_ISREG(metadata.st_mode):
                raise MutationExecutionError(
                    f"file input changed during inspection: {path}",
                    restored=True,
                )
            captured = _capture_regular_file(path, parent_descriptor, metadata)
            _require_same_regular_file(
                path,
                parent_identity,
                (metadata.st_dev, metadata.st_ino),
            )
            return captured
    except FileNotFoundError:
        return _absent_file_input()


def _capture_regular_file(
    path: Path,
    parent_descriptor: int,
    metadata: os.stat_result,
) -> CapturedFileInput:
    """Capture one regular file through its bound parent descriptor."""

    identity = (metadata.st_dev, metadata.st_ino)
    try:
        contents, mode = _read_regular_file_at(
            path,
            parent_descriptor,
            expected_identity=identity,
            nofollow=True,
        )
    except MutationExecutionError:
        raise
    except OSError as error:
        raise MutationExecutionError(
            f"file input changed during inspection: {path}",
            restored=True,
        ) from error
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


def _require_still_absent(
    path: Path,
    expected_parent: tuple[int, int],
) -> None:
    """Reject a visible entry or parent that appeared during inspection."""

    try:
        with _open_parent(path) as parent_descriptor:
            if _descriptor_identity(parent_descriptor) != expected_parent:
                raise MutationExecutionError(
                    f"file input changed during inspection: {path}",
                    restored=True,
                )
            try:
                os.stat(path.name, dir_fd=parent_descriptor, follow_symlinks=False)
            except FileNotFoundError:
                return
    except FileNotFoundError:
        pass
    raise MutationExecutionError(
        f"file input changed during inspection: {path}",
        restored=True,
    )


def _require_same_regular_file(
    path: Path,
    expected_parent: tuple[int, int],
    expected_file: tuple[int, int],
) -> None:
    """Reject a visible regular file or parent that changed after capture."""

    try:
        with _open_parent(path) as parent_descriptor:
            metadata = os.stat(
                path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            matches = (
                _descriptor_identity(parent_descriptor) == expected_parent
                and stat.S_ISREG(metadata.st_mode)
                and (metadata.st_dev, metadata.st_ino) == expected_file
            )
    except OSError as error:
        raise MutationExecutionError(
            f"file input changed during inspection: {path}",
            restored=True,
        ) from error
    if not matches:
        raise MutationExecutionError(
            f"file input changed during inspection: {path}",
            restored=True,
        )


def _require_same_symlink(
    path: Path,
    expected_parent: tuple[int, int],
    expected_link: tuple[int, int],
    expected_target: str,
    expected_effective: Path,
    scope: Path,
) -> None:
    """Reject a visible symlink, parent, or resolved target that changed."""

    try:
        with _open_parent(path) as parent_descriptor:
            metadata = os.stat(
                path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            target = os.readlink(path.name, dir_fd=parent_descriptor)
            effective = _resolved_link_target(path, target)
            _require_in_scope(path, effective, scope)
            matches = (
                _descriptor_identity(parent_descriptor) == expected_parent
                and stat.S_ISLNK(metadata.st_mode)
                and (metadata.st_dev, metadata.st_ino) == expected_link
                and target == expected_target
                and effective == expected_effective
            )
    except FileInputOutsideScopeError:
        raise
    except OSError as error:
        raise MutationExecutionError(
            f"file input changed during inspection: {path}",
            restored=True,
        ) from error
    if not matches:
        raise MutationExecutionError(
            f"file input changed during inspection: {path}",
            restored=True,
        )


def _resolved_link_target(path: Path, target: str) -> Path:
    """Resolve one recorded link target without reading its file contents."""

    target_path = Path(target)
    candidate = target_path if target_path.is_absolute() else path.parent / target_path
    return candidate.resolve(strict=False)


def _require_in_scope(visible_path: Path, effective_path: Path, scope: Path) -> None:
    """Reject an effective path outside the supplied scope root."""

    if not effective_path.is_relative_to(scope):
        raise FileInputOutsideScopeError(visible_path, effective_path)


def _descriptor_identity(descriptor: int) -> tuple[int, int]:
    """Return one opened filesystem object's stable identity."""

    metadata = os.fstat(descriptor)
    return metadata.st_dev, metadata.st_ino


def _absent_file_input() -> CapturedFileInput:
    """Return the standard state for one absent file input."""

    return CapturedFileInput(FileInputState(kind="absent"), None, None, None)
