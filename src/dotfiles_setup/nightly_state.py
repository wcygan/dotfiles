"""Explicit states and legal transitions for the local nightly updater.

Two machines live here:

- the scheduler configuration persisted in ``schedule.json``;
- one nightly invocation's outcome persisted in ``last-run.json``.

Both are pure: nothing in this module reads or writes storage or starts a
process. ``nightly_schedule`` and ``nightly`` translate these decisions into
durable writes and scheduler commands.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class NightlyStateError(ValueError):
    """A requested nightly transition is not legal from the current state."""


class SchedulerPhase(StrEnum):
    """Every durable phase of the nightly scheduler configuration."""

    UNCONFIGURED = "unconfigured"
    DISABLED = "disabled"
    REQUESTED = "requested"
    ENABLED = "enabled"
    UNKNOWN = "unknown"


class SchedulerEvent(StrEnum):
    """A request that changes the durable scheduler configuration."""

    REQUEST_ENABLE = "request-enable"
    REQUEST_DISABLE = "request-disable"
    COMMIT_ENABLE = "commit-enable"
    RESET = "reset"


# ``request-enable`` records intent and disables the timer for the duration of
# setup. ``commit-enable`` is legal only after the installation probe succeeds,
# so ``enabled`` never claims a scheduler that was not probed. ``request-disable``
# is a self-loop from ``disabled`` so a repeated disable stays idempotent.
SCHEDULER_TRANSITIONS: dict[SchedulerPhase, dict[SchedulerEvent, SchedulerPhase]] = {
    SchedulerPhase.UNCONFIGURED: {
        SchedulerEvent.REQUEST_ENABLE: SchedulerPhase.REQUESTED,
        SchedulerEvent.REQUEST_DISABLE: SchedulerPhase.DISABLED,
    },
    SchedulerPhase.DISABLED: {
        SchedulerEvent.REQUEST_ENABLE: SchedulerPhase.REQUESTED,
        SchedulerEvent.REQUEST_DISABLE: SchedulerPhase.DISABLED,
        SchedulerEvent.RESET: SchedulerPhase.UNCONFIGURED,
    },
    SchedulerPhase.REQUESTED: {
        SchedulerEvent.REQUEST_ENABLE: SchedulerPhase.REQUESTED,
        SchedulerEvent.REQUEST_DISABLE: SchedulerPhase.DISABLED,
        SchedulerEvent.COMMIT_ENABLE: SchedulerPhase.ENABLED,
        SchedulerEvent.RESET: SchedulerPhase.UNCONFIGURED,
    },
    SchedulerPhase.ENABLED: {
        SchedulerEvent.REQUEST_ENABLE: SchedulerPhase.REQUESTED,
        SchedulerEvent.REQUEST_DISABLE: SchedulerPhase.DISABLED,
        SchedulerEvent.RESET: SchedulerPhase.UNCONFIGURED,
    },
    SchedulerPhase.UNKNOWN: {
        SchedulerEvent.REQUEST_ENABLE: SchedulerPhase.REQUESTED,
        SchedulerEvent.REQUEST_DISABLE: SchedulerPhase.DISABLED,
        SchedulerEvent.RESET: SchedulerPhase.UNCONFIGURED,
    },
}


def phase_of(state: Mapping[str, Any] | None) -> SchedulerPhase:
    """Return the one durable phase implied by ``schedule.json``.

    ``requested_enabled`` falls back to ``enabled`` for manifests written
    before the two flags were split. A requested phase that also claims to be
    enabled without a probe token is ``UNKNOWN``: the acceptance check rejects
    it instead of trusting the contradictory flags.
    """

    if not state:
        return SchedulerPhase.UNCONFIGURED
    enabled = bool(state.get("enabled"))
    requested = bool(state.get("requested_enabled", enabled))
    if not requested:
        return SchedulerPhase.DISABLED
    if enabled:
        return (
            SchedulerPhase.ENABLED
            if state.get("health_token")
            else SchedulerPhase.UNKNOWN
        )
    return SchedulerPhase.REQUESTED


def transition_state(
    state: Mapping[str, Any],
    event: SchedulerEvent,
    *,
    token: str | None = None,
) -> dict[str, Any]:
    """Return a new configuration dictionary after one legal request.

    The caller still owns the atomic write and the scheduler commands. This
    function rejects illegal movement, such as committing an enable without a
    probe token or resetting a phase that has no reset edge.
    """

    current = phase_of(state)
    target = SCHEDULER_TRANSITIONS[current].get(event)
    if target is None:
        raise NightlyStateError(
            f"cannot {event.value} the nightly scheduler in the {current.value} phase"
        )
    if target is SchedulerPhase.ENABLED and not token:
        raise NightlyStateError("cannot enable nightly updates without a probe token")
    updated = dict(state)
    if target is SchedulerPhase.UNCONFIGURED:
        return {}
    if target is SchedulerPhase.DISABLED:
        updated.update(
            requested_enabled=False,
            enabled=False,
            health_token=None,
        )
    elif target is SchedulerPhase.REQUESTED:
        updated.update(requested_enabled=True, enabled=False)
    elif target is SchedulerPhase.ENABLED:
        updated.update(requested_enabled=True, enabled=True, health_token=token)
    return updated


@dataclass(frozen=True)
class SchedulerObservation:
    """The durable phase together with what the operating system reports."""

    phase: SchedulerPhase
    registered: bool


def acceptance_error(observation: SchedulerObservation) -> str | None:
    """Return the reason this observation is not acceptable, or ``None``.

    ``ENABLED`` is only partly accepted here; the caller still verifies the
    generated files, the probe token, and the next timer run. Every other phase
    is fully decided by this function.
    """

    if observation.phase is SchedulerPhase.UNCONFIGURED:
        if observation.registered:
            return "nightly scheduler is still registered without setup state"
        return None
    if observation.phase is SchedulerPhase.DISABLED:
        if observation.registered:
            return (
                "nightly updates are disabled but the scheduler is still registered; "
                "run ./bootstrap.sh nightly-schedule disable"
            )
        return None
    if observation.phase is SchedulerPhase.REQUESTED:
        return "nightly updates were requested but scheduler setup is incomplete"
    if observation.phase is SchedulerPhase.UNKNOWN:
        return "nightly updates are marked enabled without a completed scheduler probe"
    if not observation.registered:
        return "nightly scheduler is enabled but not registered"
    return None


class RunDecision(StrEnum):
    """What one timer invocation decides before it may mutate the checkout."""

    PROCEED = "proceed"
    SKIP_WINDOW = "skipped-window"
    SKIP_DISABLED = "skipped-disabled"
    SKIP_DIRTY = "skipped-dirty"
    SKIP_RECOVERY = "skipped-recovery"
    SKIP_STATE_CHANGED = "skipped-state-changed"


def run_result(
    decision: RunDecision,
    *,
    exit_code: int,
    lock_changed: bool,
) -> str:
    """Return the durable ``result`` value for ``last-run.json``."""

    if decision is not RunDecision.PROCEED:
        return decision.value
    if exit_code:
        return "failed"
    return "installed" if lock_changed else "observed"
