from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OperationState(str, Enum):
    PREPARED = "PREPARED"
    ATTEMPTED = "ATTEMPTED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    AMBIGUOUS = "AMBIGUOUS"
    RECONCILED = "RECONCILED"


class ReconcileAction(str, Enum):
    ADOPT_EXISTING = "ADOPT_EXISTING"
    RETRY_ELIGIBLE = "RETRY_ELIGIBLE"
    STOP_CONFLICT = "STOP_CONFLICT"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"


@dataclass(frozen=True)
class OperationEvent:
    operation_id: str
    state: OperationState
    target: str
    precondition: str | None = None
    receipt: str | None = None


_ALLOWED = {
    OperationState.PREPARED: {
        OperationState.ATTEMPTED,
        OperationState.RECONCILED,
    },
    OperationState.ATTEMPTED: {
        OperationState.VERIFIED,
        OperationState.FAILED,
        OperationState.AMBIGUOUS,
        OperationState.RECONCILED,
    },
    OperationState.AMBIGUOUS: {
        OperationState.RECONCILED,
    },
    OperationState.VERIFIED: set(),
    OperationState.FAILED: set(),
    OperationState.RECONCILED: set(),
}


def validate_operation_history(
    events: list[OperationEvent],
) -> None:
    if not events:
        raise ValueError("operation history is empty")

    operation_ids = {event.operation_id for event in events}
    targets = {event.target for event in events}

    if len(operation_ids) != 1 or len(targets) != 1:
        raise ValueError("operation history must retain one id and target")

    if events[0].state != OperationState.PREPARED:
        raise ValueError("operation must begin PREPARED")

    for previous, current in zip(events, events[1:]):
        if current.state not in _ALLOWED[previous.state]:
            raise ValueError(
                f"invalid operation transition: {previous.state.value} -> {current.state.value}"
            )


def reconcile_operation(
    *,
    exact_effect_present: bool,
    authoritative_absence: bool,
    target_diverged: bool,
    authority_current: bool,
    precondition_current: bool,
) -> ReconcileAction:
    if target_diverged:
        return ReconcileAction.STOP_CONFLICT

    if exact_effect_present:
        return ReconcileAction.ADOPT_EXISTING

    if (
        authoritative_absence
        and authority_current
        and precondition_current
    ):
        return ReconcileAction.RETRY_ELIGIBLE

    return ReconcileAction.OUTCOME_UNKNOWN
