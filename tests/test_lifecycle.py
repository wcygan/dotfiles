"""Explicit lifecycle models for operation journals and recovery entries."""

from __future__ import annotations

from pathlib import Path

import pytest

from dotfiles_setup.errors import ManifestError
from dotfiles_setup.lifecycle import (
    ENTRY_TRANSITIONS,
    OPERATION_TRANSITIONS,
    RECOVERY_TRANSITIONS,
    EntryEvent,
    EntryPhase,
    EntryProgress,
    LifecycleError,
    OperationState,
    RecoveryEvent,
    RecoveryPhase,
    advance_operation,
    advance_recovery,
    coerce_operation_state,
)
from dotfiles_setup.manifest import OperationJournal
from dotfiles_setup.mutations import LinkRecoveryRecord


def _environment(home: Path) -> dict[str, str]:
    return {
        "HOME": str(home),
        "XDG_CACHE_HOME": str(home / ".cache"),
        "XDG_STATE_HOME": str(home / ".local/state"),
    }


def _link_entry(destination: Path) -> LinkRecoveryRecord:
    return LinkRecoveryRecord(
        destination=destination,
        source=destination.with_name("source"),
        prior_kind="absent",
        prior_target=None,
        prior_device=None,
        prior_inode=None,
        backup=None,
        result_kind="symlink",
        result_target=str(destination.with_name("source")),
    )


@pytest.mark.parametrize(
    ("source", "target"),
    [
        (source, target)
        for source, targets in OPERATION_TRANSITIONS.items()
        for target in sorted(targets)
    ],
)
def test_declared_operation_transitions_are_accepted(
    source: OperationState, target: OperationState
) -> None:
    assert advance_operation(source, target) is target
    assert advance_operation(source.value, target.value) is target


def test_undeclared_operation_transitions_are_rejected() -> None:
    for source in OperationState:
        for target in OperationState:
            if target in OPERATION_TRANSITIONS[source]:
                continue
            with pytest.raises(LifecycleError, match="cannot move an operation"):
                advance_operation(source, target)


def test_unknown_operation_states_are_rejected() -> None:
    with pytest.raises(LifecycleError, match="invalid operation state"):
        coerce_operation_state("archived")


def test_journal_rejects_a_transition_back_to_applying(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))

    journal.transition("applying")
    journal.transition("completed")

    with pytest.raises(ManifestError, match="cannot move an operation"):
        journal.transition("applying")
    assert journal.state is OperationState.COMPLETED


def test_journal_allows_downgrading_an_unpersisted_completion(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))

    journal.transition("applying")
    journal.transition("completed")
    journal.transition("recovery-needed")

    assert journal.state is OperationState.RECOVERY_NEEDED
    assert journal.recovery_path.is_file()


def test_journal_state_round_trips_as_an_operation_state(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))

    assert journal.state is OperationState.PLANNED
    journal.transition("applying")

    assert journal.data["state"] == "applying"
    reread = journal.repository.read(journal.active_path)
    assert reread["state"] == "applying"


@pytest.mark.parametrize(
    ("phase", "event", "expected"),
    [
        (phase, event, target)
        for phase, transitions in ENTRY_TRANSITIONS.items()
        for event, target in sorted(transitions.items())
    ],
)
def test_declared_entry_transitions_are_accepted(
    phase: EntryPhase, event: EntryEvent, expected: EntryPhase
) -> None:
    start = _progress_for(phase)

    assert start.phase is phase
    assert start.advance(event).phase is expected


def test_undeclared_entry_transitions_are_rejected() -> None:
    for phase, transitions in ENTRY_TRANSITIONS.items():
        for event in EntryEvent:
            if event in transitions:
                continue
            with pytest.raises(LifecycleError, match="cannot"):
                _progress_for(phase).advance(event)


def test_restored_false_is_not_a_restored_entry() -> None:
    progress = EntryProgress.from_manifest(
        {"mutation_started": True, "applied": True, "recovered": False, "restored": False}
    )

    assert progress.phase is EntryPhase.APPLIED
    assert progress.fields()["restored"] is False


def test_journal_rejects_restarting_an_applied_entry(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))
    index = journal.add_entry(_link_entry(tmp_path / "destination"))

    journal.mark_started(index)
    journal.mark_applied(index)

    with pytest.raises(ManifestError, match="cannot start"):
        journal.mark_started(index)
    assert journal.entry(index).applied


def test_journal_writes_only_changed_progress_flags(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))
    destination = tmp_path / "destination"
    index = journal.add_link_entry(
        {
            "destination": str(destination),
            "source": str(destination.with_name("source")),
            "prior_kind": "absent",
            "prior_target": None,
            "prior_device": None,
            "prior_inode": None,
            "backup": None,
            "result_kind": "symlink",
            "result_target": str(destination.with_name("source")),
        }
    )

    journal.mark_started(index)

    raw = journal.data["entries"][index]
    assert raw["mutation_started"] is True
    assert "applied" not in raw
    assert "recovered" not in raw
    assert "restored" not in raw


def test_journal_restore_clears_active_progress(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))
    index = journal.add_entry(_link_entry(tmp_path / "destination"))

    journal.mark_started(index)
    journal.mark_applied(index)
    journal.mark_restored(index)

    record = journal.entry(index)
    assert record.restored
    assert record.recovered
    assert not record.mutation_started
    assert not record.applied
    assert journal.pending_entries == ()


def test_journal_rejects_an_illegal_entry_replacement(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))
    index = journal.add_entry(_link_entry(tmp_path / "destination"))
    journal.mark_started(index)
    journal.mark_applied(index)

    with pytest.raises(ManifestError, match="replacement for operation journal entry"):
        journal.replace_entry(
            index,
            _restored_entry(tmp_path / "destination"),
        )
    assert journal.entry(index).applied


def test_journal_requires_a_started_entry_before_recovery(tmp_path: Path) -> None:
    journal = OperationJournal("link", tmp_path, environ=_environment(tmp_path))
    index = journal.add_entry(_link_entry(tmp_path / "destination"))

    with pytest.raises(ManifestError, match="cannot recover"):
        journal.mark_recovered(index)


def _restored_entry(destination: Path) -> LinkRecoveryRecord:
    return LinkRecoveryRecord(
        destination=destination,
        source=destination.with_name("source"),
        prior_kind="absent",
        prior_target=None,
        prior_device=None,
        prior_inode=None,
        backup=None,
        result_kind="symlink",
        result_target=str(destination.with_name("source")),
        recovered=True,
        restored=True,
    )


def _progress_for(phase: EntryPhase) -> EntryProgress:
    return {
        EntryPhase.PLANNED: EntryProgress(),
        EntryPhase.STARTED: EntryProgress(mutation_started=True),
        EntryPhase.APPLIED: EntryProgress(mutation_started=True, applied=True),
        EntryPhase.RECOVERED: EntryProgress(mutation_started=True, recovered=True),
        EntryPhase.RECOVERED_APPLIED: EntryProgress(
            mutation_started=True, applied=True, recovered=True
        ),
        EntryPhase.RESTORED: EntryProgress(recovered=True, restored=True),
    }[phase]


@pytest.mark.parametrize(
    ("source", "event", "target"),
    [
        (phase, event, target)
        for phase, transitions in RECOVERY_TRANSITIONS.items()
        for event, target in sorted(transitions.items())
    ],
)
def test_declared_recovery_transitions_are_accepted(
    source: RecoveryPhase, event: RecoveryEvent, target: RecoveryPhase
) -> None:
    kwargs = {"confirmed": True} if event is RecoveryEvent.APPLY else {}
    assert advance_recovery(source, event, **kwargs) is target


def test_undeclared_recovery_transitions_are_rejected() -> None:
    for source, transitions in RECOVERY_TRANSITIONS.items():
        for event in RecoveryEvent:
            if event in transitions:
                continue
            with pytest.raises(LifecycleError, match="cannot"):
                advance_recovery(source, event, confirmed=True)


def test_recovery_apply_requires_confirmation() -> None:
    with pytest.raises(LifecycleError, match="requires both"):
        advance_recovery(RecoveryPhase.PENDING, RecoveryEvent.APPLY)


def test_recovery_terminal_phases_reject_further_events() -> None:
    for phase in (RecoveryPhase.INCOMPLETE, RecoveryPhase.COMPLETED):
        with pytest.raises(LifecycleError, match="cannot"):
            advance_recovery(phase, RecoveryEvent.DISCOVER)
