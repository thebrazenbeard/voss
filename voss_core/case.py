from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class CaseModelError(ValueError):
    pass


class EvidenceOrigin(str, Enum):
    USER_DIRECT = "USER_DIRECT"
    PRIMARY_SOURCE = "PRIMARY_SOURCE"
    DIRECT_READBACK = "DIRECT_READBACK"
    OBSERVED_INTERACTION = "OBSERVED_INTERACTION"
    EXTERNAL_IMPORTED = "EXTERNAL_IMPORTED"
    DERIVED = "DERIVED"
    MODEL_INFERENCE = "MODEL_INFERENCE"
    HISTORICAL_RECORD = "HISTORICAL_RECORD"
    UNKNOWN = "UNKNOWN"


class EvidenceFidelity(str, Enum):
    SOURCE_BYTES_RANGE = "SOURCE_BYTES_RANGE"
    EXACT_UTF8_SPAN = "EXACT_UTF8_SPAN"
    VERIFIED_EXTRACTION_REPRESENTATION = "VERIFIED_EXTRACTION_REPRESENTATION"
    DIRECT_STRUCTURED_READBACK = "DIRECT_STRUCTURED_READBACK"
    PROJECTION = "PROJECTION"
    SUMMARY = "SUMMARY"
    UNKNOWN = "UNKNOWN"


class EpistemicStatus(str, Enum):
    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    INFERRED = "INFERRED"
    HYPOTHESIS = "HYPOTHESIS"
    DISPUTED = "DISPUTED"
    UNKNOWN = "UNKNOWN"
    SUPERSEDED = "SUPERSEDED"


class CurrentnessStatus(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"


class PropositionType(str, Enum):
    FACT = "FACT"
    HYPOTHESIS = "HYPOTHESIS"
    INFERENCE = "INFERENCE"
    PREFERENCE = "PREFERENCE"
    DESIRE = "DESIRE"
    CHOICE = "CHOICE"
    CONSENT = "CONSENT"
    INTENT = "INTENT"
    AUTHORITY = "AUTHORITY"
    IDENTITY = "IDENTITY"
    RELATIONSHIP_STATUS = "RELATIONSHIP_STATUS"
    RUNTIME_STATE = "RUNTIME_STATE"
    EFFECT_STATE = "EFFECT_STATE"
    DECISION = "DECISION"
    OTHER = "OTHER"


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    source_ref: str
    subject_id: str
    proposition: str
    origin: EvidenceOrigin
    fidelity: EvidenceFidelity
    epistemic_status: EpistemicStatus
    currentness: CurrentnessStatus = CurrentnessStatus.UNKNOWN
    immutable_ref: str | None = None
    event_time: str | None = None
    observation_time: str | None = None
    record_time: str | None = None
    retrieval_time: str | None = None
    independence_group: str | None = None
    derived_from: tuple[str, ...] = ()
    supports: tuple[str, ...] = ()
    contradicts: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not all((self.id, self.source_ref, self.subject_id, self.proposition)):
            raise CaseModelError(
                "evidence identity/source/subject/proposition must be non-empty"
            )

        if (
            self.origin in {
                EvidenceOrigin.DERIVED,
                EvidenceOrigin.MODEL_INFERENCE,
            }
            and not self.derived_from
        ):
            raise CaseModelError(
                f"{self.origin.value} evidence requires derived_from provenance"
            )

        if self.id in self.derived_from:
            raise CaseModelError(
                "evidence cannot derive from itself"
            )

        exact_fidelity = {
            EvidenceFidelity.SOURCE_BYTES_RANGE,
            EvidenceFidelity.EXACT_UTF8_SPAN,
            EvidenceFidelity.VERIFIED_EXTRACTION_REPRESENTATION,
            EvidenceFidelity.DIRECT_STRUCTURED_READBACK,
        }

        if (
            self.fidelity in exact_fidelity
            and not self.immutable_ref
        ):
            raise CaseModelError(
                f"{self.fidelity.value} requires immutable_ref"
            )

    @property
    def independence_key(self) -> str:
        return self.independence_group or self.id


@dataclass(frozen=True)
class ClaimRecord:
    id: str
    subject_id: str
    proposition: str
    proposition_type: PropositionType
    scope: str | None = None
    rivals: tuple[str, ...] = ()
    claim_ceiling: str | None = None
    required_origins: tuple[EvidenceOrigin, ...] = ()
    required_fidelities: tuple[EvidenceFidelity, ...] = ()


@dataclass(frozen=True)
class CaseFile:
    case_id: str
    literal_task: str
    subject_id: str
    source_frontier: str
    claims: tuple[ClaimRecord, ...] = ()
    evidence: tuple[EvidenceRecord, ...] = ()

    def validate(self) -> "CaseFile":
        if not all(
            (
                self.case_id,
                self.literal_task,
                self.subject_id,
                self.source_frontier,
            )
        ):
            raise CaseModelError(
                "case identity/task/subject/frontier must be non-empty"
            )

        claim_ids: set[str] = set()

        for claim in self.claims:
            if claim.id in claim_ids:
                raise CaseModelError(
                    f"duplicate claim id: {claim.id}"
                )
            claim_ids.add(claim.id)

            if claim.subject_id != self.subject_id:
                raise CaseModelError(
                    f"claim {claim.id} subject mismatch"
                )

        evidence_ids: set[str] = set()

        for item in self.evidence:
            if item.id in evidence_ids:
                raise CaseModelError(
                    f"duplicate evidence id: {item.id}"
                )
            evidence_ids.add(item.id)

            if item.subject_id != self.subject_id:
                raise CaseModelError(
                    f"evidence {item.id} subject mismatch"
                )

        for item in self.evidence:
            missing = [
                ref
                for ref in item.derived_from + item.supersedes
                if ref not in evidence_ids
            ]

            if missing:
                raise CaseModelError(
                    f"evidence {item.id} references missing evidence: {missing}"
                )

            unknown_claims = [
                claim_id
                for claim_id in item.supports + item.contradicts
                if claim_id not in claim_ids
            ]

            if unknown_claims:
                raise CaseModelError(
                    f"evidence {item.id} references unknown claims: {unknown_claims}"
                )

        return self

    def independent_support_count(
        self,
        claim_id: str,
    ) -> int:
        groups = {
            item.independence_key
            for item in self.evidence
            if claim_id in item.supports
        }
        return len(groups)


def evidence_satisfies_claim(
    claim: ClaimRecord,
    evidence: Iterable[EvidenceRecord],
) -> bool:
    matched = [
        item
        for item in evidence
        if claim.id in item.supports
    ]

    if not matched:
        return False

    origins = {
        item.origin
        for item in matched
    }
    fidelities = {
        item.fidelity
        for item in matched
    }

    return (
        set(claim.required_origins).issubset(origins)
        and set(claim.required_fidelities).issubset(fidelities)
    )
