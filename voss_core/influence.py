from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .case import CaseModelError


class InfluenceClass(str, Enum):
    RELATIONSHIP_STATE = "RELATIONSHIP_STATE"
    USER_PREFERENCE = "USER_PREFERENCE"
    PROJECT_GOAL = "PROJECT_GOAL"
    COMMERCIAL_SIGNAL = "COMMERCIAL_SIGNAL"
    REVIEWER_CONSENSUS = "REVIEWER_CONSENSUS"
    ROLE_PRESTIGE = "ROLE_PRESTIGE"
    MODEL_CONFIDENCE = "MODEL_CONFIDENCE"
    AFFECTIVE_SIGNAL = "AFFECTIVE_SIGNAL"
    TIME_PRESSURE = "TIME_PRESSURE"


@dataclass(frozen=True)
class InfluenceSignal:
    id: str
    influence_class: InfluenceClass
    source: str
    summary: str


class InfluenceFirewall:
    """Protect verdict semantics from non-evidentiary social/contextual pressure."""

    @staticmethod
    def validate_verdict_inputs(
        *,
        evidence_ids: Iterable[str],
        influence_ids: Iterable[str],
    ) -> None:
        del evidence_ids

        used = tuple(influence_ids)

        if used:
            raise CaseModelError(
                "influence signals may shape presentation/scheduling, "
                "not factual verdict inputs; record claim-relevant "
                "material as typed evidence instead"
            )
