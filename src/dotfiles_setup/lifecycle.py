"""Explicit lifecycle states and legal transitions for setup mutations.

Two machines live here:

- an operation run, persisted as ``state`` in the operation journal;
- one recovery record, persisted as four monotonic progress flags.

Both are pure: nothing in this module reads or writes durable storage. The
journal and record adapters translate these decisions into manifest writes.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Any, Final


class LifecycleError(ValueError):
    """A requested lifecycle transition is not legal from the current state."""


class OperationState(StrEnum):
    """Every durable state of one mutating setup command."""

    PLANNED = "planned"
    APPLYING = "applying"
    COMPLETED = "completed"
    FAILED = "failed"
    RECOVERY_NEEDED = "recovery-needed"


TERMINAL_OPERATION_STATES: Final[frozenset[OperationState]] = frozenset(
    {OperationState.COMPLETED, OperationState.FAILED}
)
FAILURE_OPERATION_STATES: Final[frozenset[OperationState]] = frozenset(
    {OperationState.FAILED, OperationState.RECOVERY_NEEDED}
)

# Self-loops are legal: a checkpoint may be re-recorded after a retry.
# A completed operation may be downgraded to recovery-needed when its own
# completion record cannot be persisted.
OPERATION_TRANSITIONS: Final[Mapping[OperationState, frozenset[OperationState]]] = {
    OperationState.PLANNED: frozenset(
        {
            OperationState.PLANNED,
            OperationState.APPLYING,
            OperationState.COMPLETED,
            OperationState.RECOVERY_NEEDED,
        }
    ),
    OperationState.APPLYING: frozenset(
        {
            OperationState.APPLYING,
            OperationState.COMPLETED,
            OperationState.FAILED,
            OperationState.RECOVERY_NEEDED,
        }
    ),
    OperationState.COMPLETED: frozenset(
        {OperationState.COMPLETED, OperationState.RECOVERY_NEEDED}
    ),
    OperationState.FAILED: frozenset({OperationState.FAILED}),
    OperationState.RECOVERY_NEEDED: frozenset(
        {OperationState.RECOVERY_NEEDED, OperationState.COMPLETED}
    ),
}


def coerce_operation_state(value: str | OperationState) -> OperationState:
    """Return one validated operation state."""

    try:
        return OperationState(value)
    except ValueError as error:
        raise LifecycleError(f"invalid operation state: {value}") from error


def advance_operation(
    current: str | OperationState,
    target: str | OperationState,
) -> OperationState:
    """Return the target state when the journal may record it."""

    source = coerce_operation_state(current)
    destination = coerce_operation_state(target)
    if destination not in OPERATION_TRANSITIONS[source]:
        raise LifecycleError(
            f"cannot move an operation from {source.value} to {destination.value}"
        )
    return destination


class EntryPhase(StrEnum):
    """Every durable phase of one recovery record."""

    PLANNED = "planned"
    STARTED = "started"
    APPLIED = "applied"
    RECOVERED = "recovered"
    RECOVERED_APPLIED = "recovered-applied"
    RESTORED = "restored"


class EntryEvent(StrEnum):
    """Every progress checkpoint a recovery record accepts."""

    START = "start"
    APPLY = "apply"
    RECOVER = "recover"
    RESTORE = "restore"


ENTRY_TRANSITIONS: Final[Mapping[EntryPhase, Mapping[EntryEvent, EntryPhase]]] = {
    EntryPhase.PLANNED: {
        EntryEvent.START: EntryPhase.STARTED,
        EntryEvent.APPLY: EntryPhase.APPLIED,
        EntryEvent.RESTORE: EntryPhase.RESTORED,
    },
    EntryPhase.STARTED: {
        EntryEvent.START: EntryPhase.STARTED,
        EntryEvent.APPLY: EntryPhase.APPLIED,
        EntryEvent.RECOVER: EntryPhase.RECOVERED,
        EntryEvent.RESTORE: EntryPhase.RESTORED,
    },
    EntryPhase.APPLIED: {
        EntryEvent.APPLY: EntryPhase.APPLIED,
        EntryEvent.RECOVER: EntryPhase.RECOVERED_APPLIED,
        EntryEvent.RESTORE: EntryPhase.RESTORED,
    },
    EntryPhase.RECOVERED: {
        EntryEvent.RECOVER: EntryPhase.RECOVERED,
        EntryEvent.RESTORE: EntryPhase.RESTORED,
    },
    EntryPhase.RECOVERED_APPLIED: {
        EntryEvent.RECOVER: EntryPhase.RECOVERED_APPLIED,
        EntryEvent.RESTORE: EntryPhase.RESTORED,
    },
    EntryPhase.RESTORED: {
        EntryEvent.RECOVER: EntryPhase.RESTORED,
        EntryEvent.RESTORE: EntryPhase.RESTORED,
    },
}

_PHASE_FLAGS: Final[Mapping[EntryPhase, tuple[bool, bool, bool, bool | None]]] = {
    EntryPhase.PLANNED: (False, False, False, None),
    EntryPhase.STARTED: (True, False, False, None),
    EntryPhase.APPLIED: (True, True, False, None),
    EntryPhase.RECOVERED: (True, False, True, None),
    EntryPhase.RECOVERED_APPLIED: (True, True, True, None),
    EntryPhase.RESTORED: (False, False, True, True),
}


@dataclass(frozen=True, kw_only=True)
class EntryProgress:
    """One recovery record's monotonic progress, validated at construction."""

    mutation_started: bool = False
    applied: bool = False
    recovered: bool = False
    restored: bool | None = None

    @classmethod
    def from_manifest(cls, raw: Mapping[str, Any]) -> EntryProgress:
        """Decode and validate the persisted progress flags."""

        progress = cls(
            mutation_started=_flag(raw, "mutation_started"),
            applied=_flag(raw, "applied"),
            recovered=_flag(raw, "recovered"),
            restored=_optional_flag(raw, "restored"),
        )
        _ = progress.phase
        return progress

    @property
    def phase(self) -> EntryPhase:
        """Return the phase implied by the progress flags."""

        if self.applied and not self.mutation_started:
            raise LifecycleError("recovery entry is applied without a started mutation")
        if self.restored is True and not self.recovered:
            raise LifecycleError("recovery entry is restored without completed recovery")
        if self.restored is True and (self.mutation_started or self.applied):
            raise LifecycleError(
                "recovery entry is restored while mutation progress remains active"
            )
        if self.recovered and not self.mutation_started and self.restored is not True:
            raise LifecycleError("recovery entry is recovered without a started mutation")
        flags = (
            self.mutation_started,
            self.applied,
            self.recovered,
            True if self.restored is True else None,
        )
        for phase, expected in _PHASE_FLAGS.items():
            if flags == expected:
                return phase
        raise LifecycleError("recovery entry has an unsupported progress combination")

    def fields(self) -> dict[str, bool]:
        """Return the persisted flags, omitting an unset ``restored`` value."""

        fields: dict[str, bool] = {
            "mutation_started": self.mutation_started,
            "applied": self.applied,
            "recovered": self.recovered,
        }
        if self.restored is not None:
            fields["restored"] = self.restored
        return fields

    def advance(self, event: EntryEvent) -> EntryProgress:
        """Return the progress after one legal checkpoint."""

        transitions = ENTRY_TRANSITIONS[self.phase]
        try:
            next_phase = transitions[event]
        except KeyError as error:
            raise LifecycleError(
                f"cannot {event.value} a recovery entry in the {self.phase.value} phase"
            ) from error
        started, applied, recovered, restored = _PHASE_FLAGS[next_phase]
        return replace(
            self,
            mutation_started=started,
            applied=applied,
            recovered=recovered,
            restored=restored,
        )


def _flag(raw: Mapping[str, Any], key: str) -> bool:
    value = raw.get(key, False)
    if not isinstance(value, bool):
        raise LifecycleError(f"recovery entry has an invalid {key}")
    return value


def _optional_flag(raw: Mapping[str, Any], key: str) -> bool | None:
    if key not in raw:
        return None
    value = raw[key]
    if not isinstance(value, bool):
        raise LifecycleError(f"recovery entry has an invalid {key}")
    return value


class RecoveryPhase(StrEnum):
    """Every phase of one recovery invocation."""

    IDLE = "idle"
    PENDING = "pending"
    APPLYING = "applying"
    INCOMPLETE = "incomplete"
    COMPLETED = "completed"


class RecoveryEvent(StrEnum):
    """Every decision a recovery invocation makes."""

    DISCOVER = "discover"
    PREVIEW = "preview"
    APPLY = "apply"
    ENTRY_FAILED = "entry-failed"
    FINISH = "finish"


RECOVERY_TRANSITIONS: Mapping[RecoveryPhase, Mapping[RecoveryEvent, RecoveryPhase]] = {
    RecoveryPhase.IDLE: {RecoveryEvent.DISCOVER: RecoveryPhase.PENDING},
    RecoveryPhase.PENDING: {
        RecoveryEvent.PREVIEW: RecoveryPhase.PENDING,
        RecoveryEvent.APPLY: RecoveryPhase.APPLYING,
    },
    RecoveryPhase.APPLYING: {
        RecoveryEvent.ENTRY_FAILED: RecoveryPhase.INCOMPLETE,
        RecoveryEvent.FINISH: RecoveryPhase.COMPLETED,
    },
    RecoveryPhase.INCOMPLETE: {},
    RecoveryPhase.COMPLETED: {},
}


def advance_recovery(
    phase: RecoveryPhase,
    event: RecoveryEvent,
    *,
    confirmed: bool | None = None,
) -> RecoveryPhase:
    """Return the next recovery phase, rejecting illegal movement.

    ``APPLY`` carries the explicit ``--yes`` confirmation as a guard; a preview
    remains in ``PENDING`` so a later apply can still start from the same
    discovered manifest.
    """

    if event is RecoveryEvent.APPLY and not confirmed:
        raise LifecycleError("recovery mutation requires both --apply and --yes")
    target = RECOVERY_TRANSITIONS[phase].get(event)
    if target is None:
        raise LifecycleError(f"cannot {event.value} recovery in the {phase.value} phase")
    return target
