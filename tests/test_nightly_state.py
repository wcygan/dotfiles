"""Explicit states and legal transitions for the nightly updater."""

from __future__ import annotations

import pytest

from dotfiles_setup.nightly_state import (
    NightlyStateError,
    RunDecision,
    SchedulerEvent,
    SchedulerObservation,
    SchedulerPhase,
    acceptance_error,
    phase_of,
    run_result,
    transition_state,
)


def test_phase_of_recognizes_each_durable_shape() -> None:
    assert phase_of(None) is SchedulerPhase.UNCONFIGURED
    assert phase_of({}) is SchedulerPhase.UNCONFIGURED
    assert phase_of({"requested_enabled": False, "enabled": False}) is SchedulerPhase.DISABLED
    assert phase_of({"requested_enabled": True, "enabled": False}) is SchedulerPhase.REQUESTED
    assert (
        phase_of(
            {"requested_enabled": True, "enabled": True, "health_token": "a" * 32}
        )
        is SchedulerPhase.ENABLED
    )
    assert phase_of({"requested_enabled": True, "enabled": True}) is SchedulerPhase.UNKNOWN
    # Manifests written before requested_enabled was split fall back to enabled.
    assert (
        phase_of({"enabled": True, "health_token": "a" * 32})
        is SchedulerPhase.ENABLED
    )
    assert phase_of({"enabled": False}) is SchedulerPhase.DISABLED


def test_enable_records_intent_before_commit() -> None:
    requested = transition_state({}, SchedulerEvent.REQUEST_ENABLE)
    assert phase_of(requested) is SchedulerPhase.REQUESTED
    assert requested["requested_enabled"] is True
    assert requested["enabled"] is False

    enabled = transition_state(requested, SchedulerEvent.COMMIT_ENABLE, token="a" * 32)
    assert phase_of(enabled) is SchedulerPhase.ENABLED
    assert enabled["health_token"] == "a" * 32


def test_commit_enable_requires_a_probe_token() -> None:
    requested = transition_state({}, SchedulerEvent.REQUEST_ENABLE)
    with pytest.raises(NightlyStateError, match="without a probe token"):
        transition_state(requested, SchedulerEvent.COMMIT_ENABLE)


def test_disable_from_enabled_clears_the_probe_token() -> None:
    enabled = transition_state(
        transition_state({}, SchedulerEvent.REQUEST_ENABLE),
        SchedulerEvent.COMMIT_ENABLE,
        token="b" * 32,
    )
    disabled = transition_state(enabled, SchedulerEvent.REQUEST_DISABLE)
    assert phase_of(disabled) is SchedulerPhase.DISABLED
    assert disabled["requested_enabled"] is False
    assert disabled["enabled"] is False
    assert disabled["health_token"] is None


def test_disabled_disable_is_an_idempotent_self_loop() -> None:
    disabled = {"requested_enabled": False, "enabled": False}
    result = transition_state(disabled, SchedulerEvent.REQUEST_DISABLE)
    assert phase_of(result) is SchedulerPhase.DISABLED
    assert result["requested_enabled"] is False
    assert result["enabled"] is False
    assert result["health_token"] is None


def test_illegal_transition_is_rejected() -> None:
    disabled = {"requested_enabled": False, "enabled": False}
    with pytest.raises(NightlyStateError, match="cannot commit-enable"):
        transition_state(disabled, SchedulerEvent.COMMIT_ENABLE, token="c" * 32)


def test_reset_returns_to_an_empty_configuration() -> None:
    enabled = transition_state(
        transition_state({}, SchedulerEvent.REQUEST_ENABLE),
        SchedulerEvent.COMMIT_ENABLE,
        token="d" * 32,
    )
    assert transition_state(enabled, SchedulerEvent.RESET) == {}


def test_disabled_with_a_registered_timer_is_not_accepted() -> None:
    error = acceptance_error(SchedulerObservation(SchedulerPhase.DISABLED, True))
    assert error is not None and "still registered" in error


def test_disabled_without_a_timer_is_accepted() -> None:
    assert acceptance_error(SchedulerObservation(SchedulerPhase.DISABLED, False)) is None


def test_unconfigured_with_a_registered_timer_is_not_accepted() -> None:
    error = acceptance_error(SchedulerObservation(SchedulerPhase.UNCONFIGURED, True))
    assert error is not None and "without setup state" in error


def test_requested_and_unknown_are_never_accepted() -> None:
    for phase in (SchedulerPhase.REQUESTED, SchedulerPhase.UNKNOWN):
        assert acceptance_error(SchedulerObservation(phase, False)) is not None


def test_enabled_requires_a_registered_timer() -> None:
    assert acceptance_error(SchedulerObservation(SchedulerPhase.ENABLED, True)) is None
    error = acceptance_error(SchedulerObservation(SchedulerPhase.ENABLED, False))
    assert error is not None and "not registered" in error


@pytest.mark.parametrize(
    "decision, exit_code, changed, expected",
    [
        (RunDecision.PROCEED, 0, False, "observed"),
        (RunDecision.PROCEED, 0, True, "installed"),
        (RunDecision.PROCEED, 1, False, "failed"),
        (RunDecision.SKIP_WINDOW, 0, False, "skipped-window"),
        (RunDecision.SKIP_DISABLED, 0, False, "skipped-disabled"),
        (RunDecision.SKIP_DIRTY, 0, False, "skipped-dirty"),
        (RunDecision.SKIP_RECOVERY, 0, False, "skipped-recovery"),
        (RunDecision.SKIP_STATE_CHANGED, 0, False, "skipped-state-changed"),
    ],
)
def test_run_result_covers_every_decision(
    decision: RunDecision, exit_code: int, changed: bool, expected: str
) -> None:
    assert run_result(decision, exit_code=exit_code, lock_changed=changed) == expected
