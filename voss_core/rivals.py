from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .case import (
    CurrentnessStatus,
    EpistemicStatus,
    EvidenceRecord,
)


class RivalState(str, Enum):
    SUPPORTED = "SUPPORTED"
    UNRESOLVED = "UNRESOLVED"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class Hypothesis:
    id: str
    proposition: str


@dataclass(frozen=True)
class HypothesisAssessment:
    hypothesis_id: str
    support_groups: tuple[str, ...]
    contradiction_groups: tuple[str, ...]
    eliminated: bool


@dataclass(frozen=True)
class RivalResolution:
    state: RivalState
    winner: str | None
    live_hypotheses: tuple[str, ...]
    assessments: tuple[HypothesisAssessment, ...]
    discriminating_need: str | None


def _admissible(item: EvidenceRecord) -> bool:
    return (
        item.currentness
        not in {
            CurrentnessStatus.STALE,
            CurrentnessStatus.SUPERSEDED,
        }
        and item.epistemic_status
        not in {
            EpistemicStatus.HYPOTHESIS,
            EpistemicStatus.UNKNOWN,
            EpistemicStatus.SUPERSEDED,
        }
    )


def resolve_rivals(
    hypotheses: list[Hypothesis],
    evidence: list[EvidenceRecord],
) -> RivalResolution:
    assessments = []

    for hypothesis in hypotheses:
        support = {
            item.independence_key
            for item in evidence
            if _admissible(item)
            and hypothesis.id in item.supports
        }
        contradiction = {
            item.independence_key
            for item in evidence
            if _admissible(item)
            and hypothesis.id in item.contradicts
        }

        assessments.append(
            HypothesisAssessment(
                hypothesis_id=hypothesis.id,
                support_groups=tuple(sorted(support)),
                contradiction_groups=tuple(sorted(contradiction)),
                eliminated=bool(contradiction),
            )
        )

    live = [
        assessment
        for assessment in assessments
        if not assessment.eliminated
    ]

    if not live:
        return RivalResolution(
            RivalState.CONFLICT,
            None,
            (),
            tuple(assessments),
            "All declared rivals are contradicted; expand or repair the hypothesis set.",
        )

    supported_live = [
        assessment
        for assessment in live
        if assessment.support_groups
    ]

    if len(live) == 1 and len(supported_live) == 1:
        return RivalResolution(
            RivalState.SUPPORTED,
            live[0].hypothesis_id,
            (live[0].hypothesis_id,),
            tuple(assessments),
            None,
        )

    live_ids = tuple(
        assessment.hypothesis_id
        for assessment in live
    )
    return RivalResolution(
        RivalState.UNRESOLVED,
        None,
        live_ids,
        tuple(assessments),
        (
            "Acquire evidence that has different predicted outcomes for: "
            + ", ".join(live_ids)
        ),
    )
