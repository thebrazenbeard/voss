from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .case import CurrentnessStatus


class ResolutionState(str, Enum):
    RESOLVED = "RESOLVED"
    UNRESOLVED = "UNRESOLVED"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class StateCandidate:
    id: str
    subject_id: str
    value: str
    currentness: CurrentnessStatus
    authority_level: int
    supersedes: tuple[str, ...] = ()
    record_time: str | None = None


@dataclass(frozen=True)
class CurrentnessResolution:
    state: ResolutionState
    value: str | None
    winner_ids: tuple[str, ...]
    ignored_ids: tuple[str, ...]
    rationale: str


def resolve_currentness(
    candidates: list[StateCandidate],
) -> CurrentnessResolution:
    if not candidates:
        return CurrentnessResolution(
            ResolutionState.UNRESOLVED,
            None,
            (),
            (),
            "No state candidates were supplied.",
        )

    subject_ids = {candidate.subject_id for candidate in candidates}
    if len(subject_ids) != 1:
        raise ValueError("currentness candidates must bind one subject")

    superseded = {
        target
        for candidate in candidates
        if candidate.currentness == CurrentnessStatus.CURRENT
        for target in candidate.supersedes
    }

    eligible = [
        candidate
        for candidate in candidates
        if candidate.id not in superseded
        and candidate.currentness == CurrentnessStatus.CURRENT
    ]

    ignored = tuple(
        sorted(
            candidate.id
            for candidate in candidates
            if candidate not in eligible
        )
    )

    if not eligible:
        return CurrentnessResolution(
            ResolutionState.UNRESOLVED,
            None,
            (),
            ignored,
            "No non-superseded CURRENT evidence exists.",
        )

    top_authority = max(
        candidate.authority_level
        for candidate in eligible
    )
    top = [
        candidate
        for candidate in eligible
        if candidate.authority_level == top_authority
    ]

    values = {candidate.value for candidate in top}

    if len(values) != 1:
        return CurrentnessResolution(
            ResolutionState.CONFLICT,
            None,
            tuple(sorted(candidate.id for candidate in top)),
            ignored,
            "Equally authoritative current evidence conflicts.",
        )

    value = next(iter(values))
    return CurrentnessResolution(
        ResolutionState.RESOLVED,
        value,
        tuple(sorted(candidate.id for candidate in top)),
        ignored,
        (
            "Resolved from current evidence at the highest declared "
            "authority level; record time was not used as a truth rule."
        ),
    )
