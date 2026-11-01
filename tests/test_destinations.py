"""One classification for every managed destination."""

from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup.destinations import (
    DestinationState,
    FileKind,
    classify,
    state_for,
)


def test_absent_destination(tmp_path: Path) -> None:
    result = classify(tmp_path / "missing")

    assert result.kind is FileKind.ABSENT
    assert result.state is DestinationState.ABSENT
    assert result.needs_replacement


def test_correct_symlink(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("managed")
    destination = tmp_path / "destination"
    destination.symlink_to(source)

    result = classify(destination, source)

    assert result.kind is FileKind.SYMLINK
    assert result.state is DestinationState.CORRECT
    assert result.target == str(source)
    assert not result.needs_replacement


def test_stale_symlink_to_another_repo(tmp_path: Path) -> None:
    source = tmp_path / "repo" / "config"
    source.mkdir(parents=True)
    other = tmp_path / "other-repo" / "config"
    other.mkdir(parents=True)
    destination = tmp_path / "destination"
    destination.symlink_to(other)

    result = classify(destination, source)

    assert result.kind is FileKind.SYMLINK
    assert result.state is DestinationState.STALE
    assert result.needs_replacement


def test_broken_symlink(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("managed")
    destination = tmp_path / "destination"
    destination.symlink_to(tmp_path / "missing")

    result = classify(destination, source)

    assert result.kind is FileKind.SYMLINK
    assert result.state is DestinationState.BROKEN
    assert result.needs_replacement


def test_unmanaged_file(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("managed")
    destination = tmp_path / "destination"
    destination.write_text("local")

    result = classify(destination, source)

    assert result.kind is FileKind.FILE
    assert result.state is DestinationState.UNMANAGED_FILE
    assert result.needs_replacement


def test_unmanaged_directory(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("managed")
    destination = tmp_path / "destination"
    destination.mkdir()

    result = classify(destination, source)

    assert result.kind is FileKind.DIRECTORY
    assert result.state is DestinationState.UNMANAGED_DIRECTORY
    assert result.needs_replacement


@pytest.mark.parametrize("kind", list(FileKind))
def test_state_for_is_total(kind: FileKind) -> None:
    assert state_for(kind) in set(DestinationState)


def test_state_for_symlink_needs_the_expected_result() -> None:
    assert state_for(FileKind.SYMLINK) is DestinationState.UNMANAGED_OTHER
    assert state_for(FileKind.SYMLINK, matches_expected=True) is DestinationState.CORRECT
    assert state_for(FileKind.SYMLINK, matches_expected=False) is DestinationState.STALE
