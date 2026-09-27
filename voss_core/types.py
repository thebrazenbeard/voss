from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class EvidenceClass(str, Enum):
    PRIMARY_SOURCE = "PRIMARY_SOURCE"
    DIRECT_READBACK = "DIRECT_READBACK"
    RECEIPT = "RECEIPT"
    DERIVED = "DERIVED"
    INFERENCE = "INFERENCE"
    HISTORICAL = "HISTORICAL"
    CLAIM = "CLAIM"
    UNKNOWN = "UNKNOWN"


class VerdictState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"
    BLOCKED = "BLOCKED"
    CONFLICT = "CONFLICT"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EffectState(str, Enum):
    NOT_ATTEMPTED = "NOT_ATTEMPTED"
    PLANNED = "PLANNED"
    SOURCE_WRITTEN = "SOURCE_WRITTEN"
    BUILT = "BUILT"
    TESTED = "TESTED"
    DELIVERED = "DELIVERED"
    INSTALLED = "INSTALLED"
    ACTIVE = "ACTIVE"
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"


@dataclass(frozen=True)
class Evidence:
    id: str
    evidence_class: EvidenceClass
    source: str
    proposition: str
    immutable_ref: str | None = None
    supports: tuple[str, ...] = ()
    contradicts: tuple[str, ...] = ()
    notes: str | None = None


@dataclass(frozen=True)
class Claim:
    id: str
    proposition: str
    required_evidence_classes: tuple[EvidenceClass, ...] = ()
    ceiling: str | None = None


@dataclass(frozen=True)
class Finding:
    id: str
    state: VerdictState
    claim_id: str
    evidence_ids: tuple[str, ...]
    rationale: str
    claim_ceiling: str | None = None
    effect_state: EffectState | None = None


class EvidenceError(ValueError):
    pass


def index_evidence(
    evidence: Iterable[Evidence],
) -> dict[str, Evidence]:
    indexed: dict[str, Evidence] = {}

    for item in evidence:
        if item.id in indexed:
            raise EvidenceError(
                f"duplicate evidence id: {item.id}"
            )
        indexed[item.id] = item

    return indexed


def validate_finding(
    finding: Finding,
    claim: Claim,
    evidence: Mapping[str, Evidence],
) -> None:
    if finding.claim_id != claim.id:
        raise EvidenceError(
            f"finding {finding.id} targets "
            f"{finding.claim_id}, expected {claim.id}"
        )

    missing = [
        evidence_id
        for evidence_id in finding.evidence_ids
        if evidence_id not in evidence
    ]

    if missing:
        raise EvidenceError(
            f"missing evidence: {missing}"
        )

    if (
        finding.state == VerdictState.PASS
        and claim.required_evidence_classes
    ):
        observed = {
            evidence[evidence_id].evidence_class
            for evidence_id in finding.evidence_ids
        }
        required = set(
            claim.required_evidence_classes
        )

        if not required.issubset(observed):
            lacking = sorted(
                item.value
                for item in required - observed
            )
            raise EvidenceError(
                "PASS lacks required evidence classes: "
                f"{lacking}"
            )

    runtime_or_effect = {
        EffectState.INSTALLED,
        EffectState.ACTIVE,
        EffectState.OBSERVED,
        EffectState.VERIFIED,
    }

    if (
        finding.effect_state in runtime_or_effect
        and not any(
            evidence[evidence_id].evidence_class
            == EvidenceClass.DIRECT_READBACK
            for evidence_id in finding.evidence_ids
        )
    ):
        raise EvidenceError(
            "runtime/effect state requires "
            "DIRECT_READBACK evidence"
        )
