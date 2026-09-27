from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExperimentValidity(str, Enum):
    CONFIRMATORY_VALID = "CONFIRMATORY_VALID"
    EXPLORATORY_ONLY = "EXPLORATORY_ONLY"
    INVALID_LEAKAGE = "INVALID_LEAKAGE"
    REQUIRES_FRESH_HOLDOUT = "REQUIRES_FRESH_HOLDOUT"


@dataclass(frozen=True)
class ExperimentProtocol:
    calibration_ids: tuple[str, ...]
    holdout_ids: tuple[str, ...]
    hidden_fields: tuple[str, ...]
    analyst_visible_fields: tuple[str, ...]
    frozen_before_execution: bool


def evaluate_protocol(
    protocol: ExperimentProtocol,
    *,
    tuned_after_holdout: bool = False,
) -> ExperimentValidity:
    if set(protocol.calibration_ids) & set(protocol.holdout_ids):
        return ExperimentValidity.INVALID_LEAKAGE

    if set(protocol.hidden_fields) & set(protocol.analyst_visible_fields):
        return ExperimentValidity.INVALID_LEAKAGE

    if tuned_after_holdout:
        return ExperimentValidity.REQUIRES_FRESH_HOLDOUT

    if not protocol.frozen_before_execution:
        return ExperimentValidity.EXPLORATORY_ONLY

    return ExperimentValidity.CONFIRMATORY_VALID
