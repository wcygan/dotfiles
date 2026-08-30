from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup import manifest as manifest_module
from dotfiles_setup.errors import ManifestError
from dotfiles_setup.manifest import ManifestRepository, OperationJournal
from dotfiles_setup.mutations import LinkRecoveryRecord


@pytest.mark.parametrize("method", ["start", "pending"])
def test_broken_recovery_marker_is_not_treated_as_absent(
    tmp_path: Path, method: str
) -> None:
    repository = ManifestRepository(tmp_path / "state")
    repository.directory.mkdir()
    repository.recovery_path.symlink_to(repository.directory / "missing.json")

    with pytest.raises(ManifestError, match="not a regular file"):
        if method == "start":
            repository.start("link", tmp_path)
        else:
            repository.pending()

    assert repository.recovery_path.is_symlink()
    assert not repository.active_path.exists()


@pytest.mark.parametrize("method", ["start", "pending"])
def test_directory_recovery_marker_is_not_treated_as_absent(
    tmp_path: Path, method: str
) -> None:
    repository = ManifestRepository(tmp_path / "state")
    repository.recovery_path.mkdir(parents=True)

    with pytest.raises(ManifestError, match="not a regular file"):
        if method == "start":
            repository.start("link", tmp_path)
        else:
            repository.pending()

    assert repository.recovery_path.is_dir()
    assert not repository.active_path.exists()


def test_manifest_write_rejects_a_state_directory_swap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = ManifestRepository(tmp_path / "state")
    displaced = tmp_path / "displaced-state"
    original_replace = manifest_module.os.replace

    def swap_directory(
        source: str,
        destination: str,
        *,
        src_dir_fd: int | None = None,
        dst_dir_fd: int | None = None,
    ) -> None:
        assert src_dir_fd is not None
        assert src_dir_fd == dst_dir_fd
        repository.directory.rename(displaced)
        repository.directory.mkdir()
        original_replace(
            source,
            destination,
            src_dir_fd=src_dir_fd,
            dst_dir_fd=dst_dir_fd,
        )

    monkeypatch.setattr(manifest_module.os, "replace", swap_directory)

    with pytest.raises(ManifestError, match="state directory changed"):
        repository.write(repository.active_path, {"state": "planned"})

    assert not repository.active_path.exists()
    assert (displaced / repository.active_path.name).is_file()
    assert list(repository.directory.iterdir()) == []


def test_recovery_completion_rejects_a_state_directory_swap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    values = {"HOME": str(tmp_path / "home")}
    journal = OperationJournal("link", tmp_path, environ=values)
    journal.transition("recovery-needed")
    repository = journal.repository
    displaced = repository.directory.with_name("displaced-state")
    original_unlink = manifest_module.os.unlink

    def swap_directory(path: str, *, dir_fd: int | None = None) -> None:
        assert path == repository.recovery_path.name
        assert dir_fd is not None
        repository.directory.rename(displaced)
        repository.directory.mkdir()
        original_unlink(path, dir_fd=dir_fd)

    monkeypatch.setattr(manifest_module.os, "unlink", swap_directory)

    with pytest.raises(ManifestError, match="state directory changed"):
        repository.complete_recovery(journal.data)

    assert not repository.recovery_path.exists()
    assert not (displaced / repository.recovery_path.name).exists()
    assert (displaced / repository.active_path.name).is_file()
    assert (displaced / repository.completed_path.name).is_file()
    assert list(repository.directory.iterdir()) == []


def test_complete_recovery_rejects_an_unrecovered_started_entry(
    tmp_path: Path,
) -> None:
    values = {"HOME": str(tmp_path / "home")}
    journal = OperationJournal("link", tmp_path, environ=values)
    index = journal.add_entry(
        LinkRecoveryRecord(
            destination=tmp_path / "destination",
            source=tmp_path / "source",
            prior_kind="absent",
            prior_target=None,
            prior_device=None,
            prior_inode=None,
            backup=None,
            result_kind="symlink",
            result_target=str(tmp_path / "source"),
        )
    )
    journal.mark_started(index)
    journal.transition("recovery-needed")

    with pytest.raises(ManifestError, match="entry 0 still needs recovery"):
        journal.repository.complete_recovery(journal.data)

    assert journal.data["state"] == "recovery-needed"
    assert journal.recovery_path.is_file()
