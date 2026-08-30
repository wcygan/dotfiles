from __future__ import annotations

import os
import stat
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pytest

import dotfiles_setup.mutations as mutations_module
from dotfiles_setup.mutations import (
    DirectoryMutation,
    DirectoryRecoveryRecord,
    FileMutation,
    FileRecoveryRecord,
    LinkRecoveryRecord,
    MutationExecutionError,
    MutationRecordError,
    RecoveryRecord,
    SymlinkMutation,
    decode_recovery_record,
    execute_mutations,
    recover_mutation,
)


class RecordingJournal:
    def __init__(self) -> None:
        self.entries: list[RecoveryRecord] = []
        self.events: list[tuple[str, Any]] = []
        self.state = "planned"

    def add_entry(self, entry: RecoveryRecord) -> int:
        self.entries.append(entry)
        self.events.append(("added", entry.destination))
        return len(self.entries) - 1

    def replace_entry(self, index: int, entry: RecoveryRecord) -> None:
        self.entries[index] = entry
        self.events.append(("replaced", index))

    def mark_started(self, index: int) -> None:
        self.events.append(("started", index))

    def mark_applied(self, index: int) -> None:
        self.events.append(("applied", index))

    def mark_restored(self, index: int) -> None:
        self.events.append(("restored", index))

    def transition(self, state: str) -> None:
        self.state = state
        self.events.append(("state", state))


def test_link_record_uses_an_explicit_type_and_contains_no_contents(tmp_path: Path) -> None:
    record = LinkRecoveryRecord(
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

    value = record.to_manifest()

    assert value == {
        "entry_type": "link",
        "destination": str(tmp_path / "destination"),
        "source": str(tmp_path / "source"),
        "prior_kind": "absent",
        "prior_target": None,
        "prior_device": None,
        "prior_inode": None,
        "backup": None,
        "result_kind": "symlink",
        "result_target": str(tmp_path / "source"),
        "mutation_started": False,
        "applied": False,
        "recovered": False,
    }
    assert "contents" not in value


def test_file_record_uses_the_file_discriminator(tmp_path: Path) -> None:
    record = FileRecoveryRecord(
        destination=tmp_path / ".zshrc",
        visible_destination=tmp_path / ".zshrc",
        source="shell-handoff",
        prior_kind="absent",
        prior_target=None,
        prior_hash=None,
        backup=None,
        result_hash="result-hash",
    )

    assert record.to_manifest()["entry_type"] == "file"


def test_file_record_accepts_legacy_hash_only_result_metadata(tmp_path: Path) -> None:
    destination = tmp_path / "settings"
    destination.write_text("managed")
    raw = FileRecoveryRecord(
        destination=destination,
        visible_destination=destination,
        source="test",
        prior_kind="absent",
        prior_target=None,
        prior_hash=None,
        backup=None,
        result_hash=mutations_module.hashlib.sha256(b"managed").hexdigest(),
    ).to_manifest()

    record = decode_recovery_record(raw)

    assert isinstance(record, FileRecoveryRecord)
    assert mutations_module._matches_result(record)
    assert "result_mode" not in record.to_manifest()


def test_file_record_accepts_a_legacy_symlink_prior_without_backup(
    tmp_path: Path,
) -> None:
    raw = {
        "entry_type": "file",
        "destination": str(tmp_path / "config.toml"),
        "visible_destination": str(tmp_path / "config.toml"),
        "source": "codex-template",
        "prior_kind": "symlink",
        "prior_target": str(tmp_path / "prior.toml"),
        "prior_hash": None,
        "backup": None,
        "result_kind": "file",
        "result_target": None,
        "result_hash": "result-hash",
        "mutation_started": True,
        "applied": True,
        "recovered": False,
    }

    record = decode_recovery_record(raw)

    assert isinstance(record, FileRecoveryRecord)
    assert record.backup is None
    assert record.prior_target == str(tmp_path / "prior.toml")


def test_decode_accepts_a_legacy_link_without_an_entry_type(tmp_path: Path) -> None:
    raw = {
        "destination": str(tmp_path / "destination"),
        "source": str(tmp_path / "source"),
        "prior_kind": "absent",
        "prior_target": None,
        "backup": None,
        "result_kind": "symlink",
        "result_target": str(tmp_path / "source"),
        "mutation_started": True,
        "applied": True,
        "recovered": False,
        "future_safe_field": "preserve-me",
    }

    record = decode_recovery_record(raw)

    assert isinstance(record, LinkRecoveryRecord)
    assert "entry_type" not in record.to_manifest()
    assert record.to_manifest()["future_safe_field"] == "preserve-me"


def test_decode_accepts_a_legacy_symlink_link_without_backup(tmp_path: Path) -> None:
    raw = {
        "destination": str(tmp_path / "destination"),
        "source": str(tmp_path / "source"),
        "prior_kind": "symlink",
        "prior_target": str(tmp_path / "prior"),
        "prior_device": 11,
        "prior_inode": 12,
        "backup": None,
        "result_kind": "symlink",
        "result_target": str(tmp_path / "source"),
        "mutation_started": True,
        "applied": True,
        "recovered": False,
    }

    record = decode_recovery_record(raw)

    assert isinstance(record, LinkRecoveryRecord)
    assert record.backup is None
    assert record.prior_device == 11
    assert record.prior_inode == 12


def test_decode_preserves_missing_legacy_link_fields(tmp_path: Path) -> None:
    raw = {
        "destination": str(tmp_path / "destination"),
        "source": str(tmp_path / "source"),
        "prior_kind": "absent",
        "result_kind": "symlink",
        "result_target": str(tmp_path / "source"),
        "mutation_started": True,
    }

    value = decode_recovery_record(raw).to_manifest()

    assert value == raw


def test_decode_rejects_an_unknown_entry_type() -> None:
    with pytest.raises(MutationRecordError, match="unsupported recovery entry type"):
        decode_recovery_record({"entry_type": "command"})


def _record_for_type(entry_type: str, tmp_path: Path) -> RecoveryRecord:
    if entry_type == "link":
        return LinkRecoveryRecord(
            destination=tmp_path / "link",
            source=tmp_path / "source",
            prior_kind="absent",
            prior_target=None,
            prior_device=None,
            prior_inode=None,
            backup=None,
            result_kind="symlink",
            result_target=str(tmp_path / "source"),
        )
    if entry_type == "file":
        return FileRecoveryRecord(
            destination=tmp_path / "file",
            visible_destination=tmp_path / "file",
            source="npmrc",
            prior_kind="absent",
            prior_target=None,
            prior_hash=None,
            backup=None,
            result_hash="result-hash",
        )
    return DirectoryRecoveryRecord(
        destination=tmp_path / "directory",
        result_device=1,
        result_inode=2,
    )


@pytest.mark.parametrize("entry_type", ("link", "file", "directory"))
@pytest.mark.parametrize(
    ("changes", "message"),
    (
        ({"mutation_started": False, "applied": True}, "applied without"),
        (
            {"mutation_started": False, "recovered": True, "restored": False},
            "recovered without",
        ),
        (
            {"mutation_started": True, "recovered": False, "restored": True},
            "restored without",
        ),
        (
            {"mutation_started": True, "recovered": True, "restored": True},
            "progress remains active",
        ),
        (
            {
                "mutation_started": True,
                "applied": True,
                "recovered": True,
                "restored": True,
            },
            "progress remains active",
        ),
    ),
)
def test_decode_rejects_invalid_progress_states(
    tmp_path: Path,
    entry_type: str,
    changes: dict[str, bool],
    message: str,
) -> None:
    raw = _record_for_type(entry_type, tmp_path).to_manifest()
    raw.update(changes)

    with pytest.raises(MutationRecordError, match=message):
        decode_recovery_record(raw)


@pytest.mark.parametrize("entry_type", ("link", "file", "directory"))
def test_decode_accepts_terminal_immediate_rollback_progress(
    tmp_path: Path, entry_type: str
) -> None:
    raw = _record_for_type(entry_type, tmp_path).to_manifest()
    raw.update(
        mutation_started=False,
        applied=False,
        recovered=True,
        restored=True,
    )

    record = decode_recovery_record(raw)

    assert record.recovered
    assert record.restored
    assert not record.mutation_started
    assert not record.applied


def test_decode_rejects_an_absent_link_prior_with_a_backup(tmp_path: Path) -> None:
    raw = LinkRecoveryRecord(
        destination=tmp_path / "destination",
        source=tmp_path / "source",
        prior_kind="absent",
        prior_target=None,
        prior_device=None,
        prior_inode=None,
        backup=None,
        result_kind="symlink",
        result_target=str(tmp_path / "source"),
    ).to_manifest()
    raw["backup"] = str(tmp_path / "injected-backup")

    with pytest.raises(MutationRecordError, match="invalid prior state"):
        decode_recovery_record(raw)


def test_batch_planning_fails_before_any_destination_changes(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_text("managed")
    destination = tmp_path / "destination"
    destination.write_text("local")

    with pytest.raises(MutationExecutionError, match="managed source is missing"):
        execute_mutations(
            (
                SymlinkMutation(destination=destination, source=source),
                SymlinkMutation(
                    destination=tmp_path / "second",
                    source=tmp_path / "missing",
                ),
            )
        )

    assert destination.read_text() == "local"
    assert not destination.is_symlink()


def test_file_mutation_rejects_mode_drift_before_journaling(tmp_path: Path) -> None:
    destination = tmp_path / "settings"
    destination.write_text("original")
    destination.chmod(0o600)
    captured = mutations_module.capture_file_input(destination)
    destination.chmod(0o644)
    journal = RecordingJournal()

    with pytest.raises(MutationExecutionError, match="changed after preparation"):
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                    precondition=captured.state,
                ),
            ),
            journal=journal,
        )

    assert journal.entries == []
    assert destination.read_text() == "original"
    assert stat.S_IMODE(destination.stat().st_mode) == 0o644
    assert not tuple(tmp_path.glob(".settings.dotfiles.*"))


def test_file_mutation_rejects_a_file_to_directory_race(tmp_path: Path) -> None:
    destination = tmp_path / "settings"
    destination.write_text("original")
    captured = mutations_module.capture_file_input(destination)
    destination.unlink()
    destination.mkdir()
    journal = RecordingJournal()

    with pytest.raises(MutationExecutionError, match="unsupported file input type"):
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                    precondition=captured.state,
                ),
            ),
            journal=journal,
        )

    assert journal.entries == []
    assert destination.is_dir()


def test_missing_file_hash_never_validates_a_prior_file(tmp_path: Path) -> None:
    destination = tmp_path / "settings"
    destination.write_text("original")
    record = FileRecoveryRecord(
        destination=destination,
        visible_destination=destination,
        source="test",
        prior_kind="file",
        prior_target=None,
        prior_hash=None,
        backup=tmp_path / "backup",
        result_hash="result-hash",
    )

    assert not mutations_module._matches_prior_at(record, destination)
    with pytest.raises(MutationRecordError, match="invalid prior state"):
        decode_recovery_record(record.to_manifest())


def test_batch_journals_every_record_before_the_first_destination_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sources = (tmp_path / "source-one", tmp_path / "source-two")
    for source in sources:
        source.write_text("managed")
    journal = RecordingJournal()
    real_symlink = mutations_module._create_symlink

    def checked_symlink(
        source: Path | str, destination: Path | str, **kwargs: object
    ) -> None:
        assert len(journal.entries) == 2
        real_symlink(source, destination, **kwargs)

    monkeypatch.setattr(mutations_module, "_create_symlink", checked_symlink)

    execute_mutations(
        tuple(
            SymlinkMutation(destination=tmp_path / f"link-{index}", source=source)
            for index, source in enumerate(sources)
        ),
        journal=journal,
    )

    assert journal.events[:2] == [
        ("added", tmp_path / "link-0"),
        ("added", tmp_path / "link-1"),
    ]


def test_file_install_preserves_a_destination_that_appears_after_planning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "settings"
    journal = RecordingJournal()
    real_move = mutations_module._move_no_replace

    def competing_move(source: Path, target: Path, **kwargs: object) -> None:
        if target == destination and ".dotfiles." in source.name:
            target.write_text("user change")
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", competing_move)

    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                ),
            ),
            journal=journal,
        )

    assert not failure.value.restored
    assert destination.read_text() == "user change"


@pytest.mark.parametrize("change", ("chmod", "same-content-replacement"))
def test_immediate_rollback_preserves_a_changed_file_result(
    tmp_path: Path,
    change: str,
) -> None:
    destination = tmp_path / "settings"
    destination.write_text("original")

    class ChangingJournal(RecordingJournal):
        def mark_applied(self, index: int) -> None:
            super().mark_applied(index)
            if change == "chmod":
                destination.chmod(0o644)
            else:
                replacement = tmp_path / "replacement"
                replacement.write_bytes(b"managed")
                replacement.chmod(0o600)
                os.replace(replacement, destination)
            raise OSError("injected checkpoint failure")

    journal = ChangingJournal()
    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                ),
            ),
            journal=journal,
            timestamp=3,
        )

    assert not failure.value.restored
    assert destination.read_bytes() == b"managed"
    record = journal.entries[0]
    assert isinstance(record, FileRecoveryRecord)
    assert record.result_mode == 0o600
    assert record.result_device is not None
    assert record.result_inode is not None
    if change == "chmod":
        assert stat.S_IMODE(destination.stat().st_mode) == 0o644
    else:
        assert destination.stat().st_ino != record.result_inode
    assert record.backup is not None
    assert record.backup.read_text() == "original"


def test_immediate_rollback_reports_a_retained_result_quarantine(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "settings"
    destination.write_text("original")

    class FailingJournal(RecordingJournal):
        def mark_applied(self, index: int) -> None:
            super().mark_applied(index)
            raise OSError("injected checkpoint failure")

    journal = FailingJournal()
    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                ),
            ),
            journal=journal,
            timestamp=4,
        )

    record = journal.entries[0]
    assert isinstance(record, FileRecoveryRecord)
    assert record.result_backup is not None
    assert record.result_backup.read_bytes() == b"managed"
    assert destination.read_text() == "original"
    message = str(failure.value)
    assert "retained quarantine" in message
    assert str(record.result_backup) in message


def test_file_stage_substitution_is_rejected_after_the_namespace_move(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "settings"
    journal = RecordingJournal()
    real_move = mutations_module._move_no_replace
    swapped = False

    def substitute_stage(source: Path, target: Path, **kwargs: object) -> None:
        nonlocal swapped
        if target == destination and ".dotfiles." in source.name:
            source.unlink()
            source.write_bytes(b"managed")
            source.chmod(0o600)
            swapped = True
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", substitute_stage)

    with pytest.raises(MutationExecutionError, match="staged result identity changed") as failure:
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                ),
            ),
            journal=journal,
        )

    assert swapped
    assert not failure.value.restored
    assert destination.read_bytes() == b"managed"
    record = journal.entries[0]
    assert isinstance(record, FileRecoveryRecord)
    assert destination.stat().st_ino != record.result_inode


def test_directory_stage_substitution_is_rejected_after_the_namespace_move(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "created"
    journal = RecordingJournal()
    real_move = mutations_module._move_no_replace
    swapped = False

    def substitute_stage(source: Path, target: Path, **kwargs: object) -> None:
        nonlocal swapped
        if target == destination and ".dotfiles." in source.name:
            source.rmdir()
            source.mkdir()
            swapped = True
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", substitute_stage)

    with pytest.raises(MutationExecutionError, match="staged result identity changed") as failure:
        execute_mutations(
            (DirectoryMutation(destination=destination),),
            journal=journal,
        )

    assert swapped
    assert not failure.value.restored
    assert destination.is_dir()
    record = journal.entries[0]
    assert isinstance(record, DirectoryRecoveryRecord)
    assert destination.stat().st_ino != record.result_inode


def test_directory_stage_child_injection_is_rejected_after_the_namespace_move(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "created"
    journal = RecordingJournal()
    real_move = mutations_module._move_no_replace
    injected = False

    def inject_child(source: Path, target: Path, **kwargs: object) -> None:
        nonlocal injected
        if target == destination and ".dotfiles." in source.name:
            source.joinpath("rogue").write_text("user state")
            injected = True
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", inject_child)

    with pytest.raises(MutationExecutionError, match="staged directory result changed") as failure:
        execute_mutations(
            (DirectoryMutation(destination=destination),),
            journal=journal,
        )

    assert injected
    assert not failure.value.restored
    assert destination.joinpath("rogue").read_text() == "user state"
    assert journal.state == "recovery-needed"


def test_directory_mutation_installs_with_the_declared_mode(tmp_path: Path) -> None:
    destination = tmp_path / "created"
    execute_mutations((DirectoryMutation(destination=destination),))
    assert stat.S_IMODE(destination.stat().st_mode) == 0o755

    restricted = tmp_path / "restricted"
    execute_mutations((DirectoryMutation(destination=restricted, mode=0o700),))
    assert stat.S_IMODE(restricted.stat().st_mode) == 0o700


def test_reverse_rollback_preserves_a_changed_applied_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destinations = (tmp_path / "first", tmp_path / "second")
    destinations[0].write_text("old one")
    destinations[1].write_text("old two")
    journal = RecordingJournal()
    real_move = mutations_module._move_no_replace
    calls = 0

    def fail_second_move(source: Path, target: Path, **kwargs: object) -> None:
        nonlocal calls
        if target in destinations and ".dotfiles." in source.name:
            calls += 1
            if calls == 2:
                destinations[0].write_text("user change")
                raise OSError("injected failure")
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", fail_second_move)

    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            tuple(
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=f"new {index}".encode(),
                )
                for index, destination in enumerate(destinations)
            ),
            journal=journal,
            timestamp=42,
        )

    assert not failure.value.restored
    assert destinations[0].read_text() == "user change"
    assert destinations[1].read_text() == "old two"
    assert journal.state == "recovery-needed"
    assert f"{destinations[0]}: current state changed" in str(failure.value)


def test_apply_preserves_a_file_swapped_during_started_checkpoint(
    tmp_path: Path,
) -> None:
    old_source = tmp_path / "old-source"
    new_source = tmp_path / "new-source"
    old_source.write_text("old")
    new_source.write_text("new")
    destination = tmp_path / "destination"
    destination.symlink_to(old_source)

    class SwappingJournal(RecordingJournal):
        def mark_started(self, index: int) -> None:
            super().mark_started(index)
            destination.unlink()
            destination.write_text("user change")

    journal = SwappingJournal()
    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (SymlinkMutation(destination=destination, source=new_source),),
            journal=journal,
        )

    assert not failure.value.restored
    assert destination.read_text() == "user change"
    assert not destination.is_symlink()


def test_rollback_preserves_a_result_swapped_at_the_move_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "destination"
    destination.write_text("old")
    real_move = mutations_module._move_no_replace

    def move_with_swap(source: Path, target: Path, **kwargs: object) -> None:
        if ".dotfiles-result." in Path(target).name:
            destination.write_text("user change")
        real_move(source, target, **kwargs)

    class FailingJournal(RecordingJournal):
        def mark_applied(self, index: int) -> None:
            super().mark_applied(index)
            raise OSError("injected checkpoint failure")

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_with_swap)

    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                ),
            ),
            journal=FailingJournal(),
        )

    assert not failure.value.restored
    assert destination.read_text() == "user change"


def test_backup_capture_does_not_replace_a_competing_object(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "destination"
    destination.write_text("original")
    source = tmp_path / "source"
    source.write_text("managed")
    real_move = mutations_module._move_no_replace
    competing_backup: Path | None = None

    def move_with_competitor(
        move_source: Path, move_destination: Path, **kwargs: object
    ) -> None:
        nonlocal competing_backup
        if move_source == destination and ".backup." in move_destination.name:
            competing_backup = move_destination
            move_destination.write_text("competing")
        real_move(move_source, move_destination, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_with_competitor)

    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations((SymlinkMutation(destination=destination, source=source),))

    assert failure.value.restored
    assert destination.read_text() == "original"
    assert competing_backup is not None
    assert competing_backup.read_text() == "competing"


def test_prior_capture_rejects_a_parent_replaced_before_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = tmp_path / "parent"
    parent.mkdir()
    displaced = tmp_path / "displaced"
    destination = parent / "destination"
    destination.write_text("original")
    source = tmp_path / "source"
    source.write_text("managed")
    real_matches = mutations_module._matches_prior_at
    swapped = False

    def matches_after_swap(*args: object, **kwargs: object) -> bool:
        nonlocal swapped
        if not swapped:
            swapped = True
            parent.rename(displaced)
            parent.mkdir()
            (parent / "destination.backup.42").write_text("competing")
        return real_matches(*args, **kwargs)

    monkeypatch.setattr(mutations_module, "_matches_prior_at", matches_after_swap)

    with pytest.raises(MutationExecutionError, match="destination parent changed"):
        execute_mutations(
            (SymlinkMutation(destination=destination, source=source),),
            timestamp=42,
        )

    displaced_backups = tuple(displaced.glob("destination.backup.42.*"))
    assert len(displaced_backups) == 1
    assert displaced_backups[0].read_text() == "original"
    assert (parent / "destination.backup.42").read_text() == "competing"
    assert not destination.exists()


def test_file_mutation_rejects_a_changed_visible_symlink(
    tmp_path: Path,
) -> None:
    original = tmp_path / "original"
    replacement = tmp_path / "replacement"
    original.write_text("original")
    replacement.write_text("replacement")
    visible = tmp_path / "visible"
    visible.symlink_to(original)

    class SwappingJournal(RecordingJournal):
        def mark_started(self, index: int) -> None:
            super().mark_started(index)
            visible.unlink()
            visible.symlink_to(replacement)

    journal = SwappingJournal()
    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (
                FileMutation(
                    destination=original,
                    visible_destination=visible,
                    source="test",
                    contents=b"managed",
                ),
            ),
            journal=journal,
        )

    assert not failure.value.restored
    assert journal.state == "recovery-needed"
    assert any(
        isinstance(entry, FileRecoveryRecord)
        and entry.stage_path is not None
        and entry.stage_path.exists()
        for entry in journal.entries
    )
    assert original.read_text() == "original"
    assert replacement.read_text() == "replacement"
    assert visible.resolve() == replacement


def test_prior_directory_restore_does_not_replace_a_competing_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "destination"
    backup = tmp_path / "destination.backup.1"
    backup.mkdir()
    identity = backup.lstat()
    record = LinkRecoveryRecord(
        destination=destination,
        source=tmp_path / "source",
        prior_kind="directory",
        prior_target=None,
        prior_device=identity.st_dev,
        prior_inode=identity.st_ino,
        backup=backup,
        result_kind="symlink",
        result_target=str(tmp_path / "source"),
    )
    real_move = mutations_module._move_no_replace

    def move_with_competitor(source: Path, target: Path, **kwargs: object) -> None:
        if source == backup and target == destination:
            destination.mkdir()
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_with_competitor)

    reason = mutations_module._restore_prior(record)

    assert reason is not None
    assert destination.is_dir()
    assert backup.is_dir()


def test_changed_directory_restore_does_not_replace_a_competing_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "destination"
    backup = tmp_path / "quarantine"
    backup.mkdir()
    real_move = mutations_module._move_no_replace

    def move_with_competitor(source: Path, target: Path, **kwargs: object) -> None:
        if source == backup and target == destination:
            destination.mkdir()
        real_move(source, target, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_with_competitor)

    with pytest.raises(MutationExecutionError, match="retained quarantine") as failure:
        mutations_module._restore_changed_path(backup, destination)

    assert not failure.value.restored
    assert destination.is_dir()
    assert backup.is_dir()


def test_changed_file_backup_is_quarantined_after_the_move(tmp_path: Path) -> None:
    destination = tmp_path / "settings"
    backup = tmp_path / "settings.backup.1"
    backup.write_text("changed")
    record = FileRecoveryRecord(
        destination=destination,
        visible_destination=destination,
        source="test",
        prior_kind="file",
        prior_target=None,
        prior_hash=mutations_module.hashlib.sha256(b"original").hexdigest(),
        backup=backup,
        result_hash=mutations_module.hashlib.sha256(b"managed").hexdigest(),
    )

    reason = mutations_module._restore_prior(record)

    assert reason is not None and "contents changed" in reason
    assert not destination.exists()
    assert not backup.exists()
    quarantines = list(tmp_path.glob(".settings.dotfiles-changed.*"))
    assert len(quarantines) == 1
    assert quarantines[0].read_text() == "changed"


def test_symlink_backup_is_retained_after_success(tmp_path: Path) -> None:
    old_source = tmp_path / "old"
    old_source.write_text("old")
    source = tmp_path / "source"
    source.write_text("managed")
    destination = tmp_path / "destination"
    destination.symlink_to(old_source)

    execute_mutations(
        (SymlinkMutation(destination=destination, source=source),),
        timestamp=5,
    )

    backups = list(tmp_path.glob("destination.backup.5.*"))
    assert len(backups) == 1
    assert backups[0].is_symlink()
    assert backups[0].resolve() == old_source


def test_symlink_creation_uses_the_opened_parent_descriptor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = tmp_path / "parent"
    parent.mkdir()
    displaced = tmp_path / "displaced"
    outside = tmp_path / "outside"
    outside.mkdir()
    source = tmp_path / "source"
    source.write_text("managed")
    real_symlink = os.symlink

    def swap_parent(
        link_source: Path | str,
        link_destination: Path | str,
        *,
        dir_fd: int | None = None,
    ) -> None:
        parent.rename(displaced)
        real_symlink(outside, parent, target_is_directory=True)
        real_symlink(link_source, link_destination, dir_fd=dir_fd)

    monkeypatch.setattr(mutations_module.os, "symlink", swap_parent)

    mutations_module._create_symlink(source, parent / "destination")

    assert not (outside / "destination").exists()
    assert (displaced / "destination").is_symlink()
    assert (displaced / "destination").resolve() == source


def test_mutation_rejects_a_real_parent_replaced_before_descriptor_open(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = tmp_path / "parent"
    parent.mkdir()
    displaced = tmp_path / "displaced"
    source = tmp_path / "source"
    source.write_text("managed")
    destination = parent / "destination"
    real_symlink = mutations_module._create_symlink

    def swap_parent(
        link_source: Path | str,
        link_destination: Path,
        **kwargs: object,
    ) -> None:
        parent.rename(displaced)
        parent.mkdir()
        real_symlink(link_source, link_destination, **kwargs)

    monkeypatch.setattr(mutations_module, "_create_symlink", swap_parent)

    with pytest.raises(MutationExecutionError, match="destination parent changed"):
        execute_mutations((SymlinkMutation(destination=destination, source=source),))

    assert not (parent / "destination").exists()
    assert not (displaced / "destination").exists()


def test_same_parent_move_reuses_one_directory_descriptor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.write_text("managed")
    real_open_parent = mutations_module._open_parent
    calls = 0

    @contextmanager
    def counting_open_parent(path: Path, **kwargs: object) -> Iterator[int]:
        nonlocal calls
        calls += 1
        with real_open_parent(path, **kwargs) as descriptor:
            yield descriptor

    monkeypatch.setattr(mutations_module, "_open_parent", counting_open_parent)

    mutations_module._move_no_replace(source, destination)

    assert calls == 1
    assert destination.read_text() == "managed"


def test_namespace_mutations_sync_their_parent_directories(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    source.write_text("managed")
    real_fsync = os.fsync
    synced: list[int] = []

    def recording_fsync(descriptor: int) -> None:
        synced.append(descriptor)
        real_fsync(descriptor)

    monkeypatch.setattr(mutations_module.os, "fsync", recording_fsync)

    link = tmp_path / "link"
    mutations_module._create_symlink(source, link)
    link_sync_count = len(synced)
    moved = tmp_path / "moved"
    mutations_module._move_no_replace(link, moved)

    assert link_sync_count == 1
    assert len(synced) == 2


def test_verified_removal_tracks_a_quarantine_before_sync_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = tmp_path / "skills"
    parent.mkdir()
    skill = parent / "animate"
    skill.mkdir()
    skill.joinpath("SKILL.md").write_text("validated\n")
    descriptor = os.open(skill, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        verified = mutations_module.capture_verified_directory(skill, descriptor)
    finally:
        os.close(descriptor)
    parent_identity = parent.lstat()
    parent_parent_identity = tmp_path.lstat()
    real_move = mutations_module._move_no_replace
    failed = False

    def move_then_fail(source: Path, destination: Path, **kwargs: object) -> None:
        nonlocal failed
        real_move(source, destination, **kwargs)
        if not failed:
            failed = True
            raise OSError("injected directory sync failure")

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_then_fail)

    with pytest.raises(MutationExecutionError, match="directory sync failure") as failure:
        mutations_module.remove_verified_directories(
            (verified,),
            parent_identity=(parent_identity.st_dev, parent_identity.st_ino),
            parent_parent_identity=(
                parent_parent_identity.st_dev,
                parent_parent_identity.st_ino,
            ),
        )

    assert failure.value.restored
    assert skill.joinpath("SKILL.md").read_text() == "validated\n"
    assert not tuple(parent.glob(".animate.dotfiles-cleanup.*"))


def test_verified_removal_retains_a_file_changed_after_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = tmp_path / "skills"
    parent.mkdir()
    skill = parent / "animate"
    skill.mkdir()
    skill.joinpath("SKILL.md").write_text("validated\n")
    descriptor = os.open(skill, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        verified = mutations_module.capture_verified_directory(skill, descriptor)
    finally:
        os.close(descriptor)
    parent_identity = parent.lstat()
    parent_parent_identity = tmp_path.lstat()
    real_hash = mutations_module._verified_file_hash_at
    changed = False

    def change_after_hash(
        parent_descriptor: int,
        name: str,
        *,
        expected_identity: tuple[int, int],
        display_path: Path,
    ) -> str:
        nonlocal changed
        digest = real_hash(
            parent_descriptor,
            name,
            expected_identity=expected_identity,
            display_path=display_path,
        )
        if not changed:
            changed = True
            descriptor = os.open(
                name,
                os.O_WRONLY | os.O_TRUNC,
                dir_fd=parent_descriptor,
            )
            try:
                os.write(descriptor, b"competing\n")
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        return digest

    monkeypatch.setattr(
        mutations_module,
        "_verified_file_hash_at",
        change_after_hash,
    )

    mutations_module.remove_verified_directories(
        (verified,),
        parent_identity=(parent_identity.st_dev, parent_identity.st_ino),
        parent_parent_identity=(
            parent_parent_identity.st_dev,
            parent_parent_identity.st_ino,
        ),
    )

    quarantines = tuple(parent.glob(".*.dotfiles-cleanup.*"))
    assert len(quarantines) == 1
    assert quarantines[0].joinpath("SKILL.md").read_text() == "competing\n"
    assert not skill.exists()


def test_verified_removal_reports_every_failed_restore_and_retained_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = tmp_path / "skills"
    parent.mkdir()
    skills = (parent / "animate", parent / "audit")
    verified: list[mutations_module.VerifiedDirectory] = []
    for skill in skills:
        skill.mkdir()
        skill.joinpath("SKILL.md").write_text("validated\n")
        descriptor = os.open(skill, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            verified.append(
                mutations_module.capture_verified_directory(skill, descriptor)
            )
        finally:
            os.close(descriptor)
    parent_identity = parent.lstat()
    parent_parent_identity = tmp_path.lstat()
    rejected = False

    def reject_after_competitors_appear(
        parent_descriptor: int,
        quarantine: Path,
        directory: mutations_module.VerifiedDirectory,
    ) -> None:
        del parent_descriptor, quarantine, directory
        nonlocal rejected
        if not rejected:
            rejected = True
            for skill in skills:
                skill.mkdir()
        raise MutationExecutionError("injected validation failure", restored=False)

    monkeypatch.setattr(
        mutations_module,
        "_validate_verified_directory_at",
        reject_after_competitors_appear,
    )

    with pytest.raises(MutationExecutionError, match="restore failures") as failure:
        mutations_module.remove_verified_directories(
            tuple(verified),
            parent_identity=(parent_identity.st_dev, parent_identity.st_ino),
            parent_parent_identity=(
                parent_parent_identity.st_dev,
                parent_parent_identity.st_ino,
            ),
        )

    message = str(failure.value)
    assert "retained quarantine" in message
    assert all(skill.name in message for skill in skills)
    assert all(skill.is_dir() for skill in skills)
    quarantines = tuple(parent.glob(".*.dotfiles-cleanup.*"))
    assert len(quarantines) == 2
    assert all(path.joinpath("SKILL.md").is_file() for path in quarantines)


def test_verified_removal_retains_the_complete_quarantine(tmp_path: Path) -> None:
    parent = tmp_path / "skills"
    parent.mkdir()
    skill = parent / "animate"
    skill.mkdir()
    skill.joinpath("SKILL.md").write_text("validated\n")
    descriptor = os.open(skill, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        verified = mutations_module.capture_verified_directory(skill, descriptor)
    finally:
        os.close(descriptor)
    parent_identity = parent.lstat()
    parent_parent_identity = tmp_path.lstat()

    retained = mutations_module.remove_verified_directories(
        (verified,),
        parent_identity=(parent_identity.st_dev, parent_identity.st_ino),
        parent_parent_identity=(
            parent_parent_identity.st_dev,
            parent_parent_identity.st_ino,
        ),
    )

    assert len(retained) == 1
    assert retained[0].parent == parent
    assert ".dotfiles-cleanup." in retained[0].name
    assert not skill.exists()
    tombstones = tuple(parent.iterdir())
    assert len(tombstones) == 1
    assert ".dotfiles-cleanup." in tombstones[0].name
    assert tombstones[0] == retained[0]
    assert tombstones[0].is_dir()
    assert tombstones[0].joinpath("SKILL.md").read_text() == "validated\n"


def test_missing_parent_directories_are_journaled_before_file_install(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "nested" / "deeper" / "settings"
    journal = RecordingJournal()

    execute_mutations(
        (
            FileMutation(
                destination=destination,
                visible_destination=destination,
                source="test",
                contents=b"managed",
            ),
        ),
        journal=journal,
    )

    assert destination.read_bytes() == b"managed"
    assert [type(entry) for entry in journal.entries] == [
        DirectoryRecoveryRecord,
        DirectoryRecoveryRecord,
        FileRecoveryRecord,
    ]


@pytest.mark.parametrize("failure_point", ("stat", "fsync"))
def test_directory_stage_failure_remains_recoverable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_point: str,
) -> None:
    destination = tmp_path / "created"
    journal = RecordingJournal()
    if failure_point == "stat":
        real_stat = mutations_module.os.stat

        def fail_stage_stat(
            path: Path | str,
            *,
            dir_fd: int | None = None,
            follow_symlinks: bool = True,
        ) -> os.stat_result:
            if dir_fd is not None and str(path).startswith(".created.dotfiles."):
                raise OSError("injected stage stat failure")
            return real_stat(path, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

        monkeypatch.setattr(mutations_module.os, "stat", fail_stage_stat)
    else:
        monkeypatch.setattr(
            mutations_module.os,
            "fsync",
            lambda _descriptor: (_ for _ in ()).throw(
                OSError("injected stage fsync failure")
            ),
        )

    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (DirectoryMutation(destination=destination),),
            journal=journal,
        )

    assert not failure.value.restored
    assert journal.state == "recovery-needed"
    assert not destination.exists()
    stages = tuple(tmp_path.glob(".created.dotfiles.*"))
    assert len(stages) == 1
    assert stages[0].is_dir()
    assert "retained quarantine" in str(failure.value)
    assert str(stages[0]) in str(failure.value)


def test_file_stage_path_is_journaled_before_stage_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "settings"
    journal = RecordingJournal()
    real_open = mutations_module.os.open

    def checked_open(
        path: Path | str,
        flags: int,
        mode: int = 0o777,
        *,
        dir_fd: int | None = None,
    ) -> int:
        if flags & os.O_CREAT:
            record = journal.entries[0]
            assert isinstance(record, FileRecoveryRecord)
            assert record.stage_path is not None
            assert record.stage_path.name == Path(path).name
            assert journal.events[0] == ("added", destination)
        return real_open(path, flags, mode, dir_fd=dir_fd)

    monkeypatch.setattr(mutations_module.os, "open", checked_open)

    execute_mutations(
        (
            FileMutation(
                destination=destination,
                visible_destination=destination,
                source="test",
                contents=b"managed",
            ),
        ),
        journal=journal,
    )


def test_hard_interruption_retains_an_unverified_stage_and_allows_recovery(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "settings"

    class InterruptingJournal(RecordingJournal):
        def replace_entry(self, index: int, entry: RecoveryRecord) -> None:
            raise SystemExit("injected interruption")

    journal = InterruptingJournal()
    with pytest.raises(SystemExit, match="injected interruption"):
        execute_mutations(
            (
                FileMutation(
                    destination=destination,
                    visible_destination=destination,
                    source="test",
                    contents=b"managed",
                ),
            ),
            journal=journal,
        )

    record = journal.entries[0]
    assert isinstance(record, FileRecoveryRecord)
    assert record.stage_path is not None and record.stage_path.exists()
    assert record.stage_device is None

    result = recover_mutation(record)

    assert result.recovered
    assert result.already_recovered
    assert record.stage_path.exists()


def test_recovery_accepts_and_retains_an_owned_directory_quarantine(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "created"
    quarantine = tmp_path / ".created.dotfiles-result.test"
    quarantine.mkdir()
    identity = quarantine.lstat()
    record = DirectoryRecoveryRecord(
        destination=destination,
        result_device=identity.st_dev,
        result_inode=identity.st_ino,
        result_backup=quarantine,
        mutation_started=True,
        applied=True,
    )

    result = recover_mutation(record)

    assert result.recovered
    assert result.already_recovered
    assert quarantine.is_dir()


def test_directory_rollback_preserves_a_swap_at_the_quarantine_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    directory = tmp_path / "created"
    failing = tmp_path / "failing"
    source = tmp_path / "source"
    source.write_text("managed")
    real_move = mutations_module._move_no_replace
    displaced = tmp_path / "owned-directory"

    def move_with_swap(
        move_source: Path, move_destination: Path, **kwargs: object
    ) -> None:
        if move_source == directory and ".dotfiles-result." in move_destination.name:
            directory.rename(displaced)
            directory.mkdir()
        real_move(move_source, move_destination, **kwargs)

    class FailingJournal(RecordingJournal):
        def mark_started(self, index: int) -> None:
            super().mark_started(index)
            if self.entries[index].destination == failing:
                raise OSError("injected failure")

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_with_swap)

    with pytest.raises(MutationExecutionError) as failure:
        execute_mutations(
            (
                DirectoryMutation(destination=directory),
                SymlinkMutation(destination=failing, source=source),
            ),
            journal=FailingJournal(),
        )

    assert not failure.value.restored
    assert directory.is_dir()
    assert displaced.is_dir()


def test_directory_recovery_preserves_a_swap_at_the_quarantine_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "created"
    destination.mkdir()
    identity = destination.lstat()
    quarantine = tmp_path / ".created.dotfiles-result.test"
    record = DirectoryRecoveryRecord(
        destination=destination,
        result_device=identity.st_dev,
        result_inode=identity.st_ino,
        result_backup=quarantine,
        mutation_started=True,
        applied=True,
    )
    real_move = mutations_module._move_no_replace
    displaced = tmp_path / "owned-directory"

    def move_with_swap(
        move_source: Path, move_destination: Path, **kwargs: object
    ) -> None:
        if move_source == destination and move_destination == quarantine:
            destination.rename(displaced)
            destination.mkdir()
        real_move(move_source, move_destination, **kwargs)

    monkeypatch.setattr(mutations_module, "_move_no_replace", move_with_swap)

    result = recover_mutation(record)

    assert not result.recovered
    assert destination.is_dir()
    assert displaced.is_dir()


def test_mutation_rejects_a_symlinked_parent_outside_authority(tmp_path: Path) -> None:
    home = tmp_path / "home"
    outside = tmp_path / "outside"
    home.mkdir()
    outside.mkdir()
    (home / ".local").symlink_to(outside, target_is_directory=True)

    with pytest.raises(MutationExecutionError, match="unsafe parent"):
        execute_mutations(
            (DirectoryMutation(destination=home / ".local" / "bin"),),
            authority_roots=(home,),
        )

    assert not (outside / "bin").exists()


def test_removal_rejects_a_symlink_to_an_unmanaged_source(tmp_path: Path) -> None:
    managed_source = tmp_path / "managed"
    unmanaged_source = tmp_path / "unmanaged"
    managed_source.write_text("managed")
    unmanaged_source.write_text("unmanaged")
    destination = tmp_path / "destination"
    destination.symlink_to(unmanaged_source)

    with pytest.raises(MutationExecutionError, match="no longer managed"):
        execute_mutations(
            (
                SymlinkMutation(
                    destination=destination,
                    source=managed_source,
                    present=False,
                ),
            )
        )

    assert destination.resolve() == unmanaged_source
