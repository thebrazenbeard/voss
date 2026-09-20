from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .case import CaseModelError, EvidenceRecord, PropositionType


class SubjectKind(str, Enum):
    REPOSITORY_REF = "REPOSITORY_REF"
    FILE_BLOB = "FILE_BLOB"
    RUNTIME = "RUNTIME"
    DATASET = "DATASET"
    PROVIDER_STATE = "PROVIDER_STATE"
    OTHER = "OTHER"


@dataclass(frozen=True)
class SubjectBinding:
    id: str
    kind: SubjectKind
    locator: str
    immutable_ref: str | None = None
    mutable: bool = False


@dataclass(frozen=True)
class CrossSubjectClaim:
    id: str
    subject_ids: tuple[str, ...]
    proposition: str
    proposition_type: PropositionType
    claim_ceiling: str | None = None


@dataclass(frozen=True)
class MultiSubjectCaseFile:
    case_id: str
    literal_task: str
    source_frontier: str
    subjects: tuple[SubjectBinding, ...]
    claims: tuple[CrossSubjectClaim, ...]
    evidence: tuple[EvidenceRecord, ...]

    def validate(self) -> "MultiSubjectCaseFile":
        if not self.case_id or not self.literal_task or not self.source_frontier:
            raise CaseModelError(
                "case identity/task/frontier must be non-empty"
            )

        subject_ids: set[str] = set()
        for subject in self.subjects:
            if not subject.id or not subject.locator:
                raise CaseModelError(
                    "subject id/locator must be non-empty"
                )
            if subject.id in subject_ids:
                raise CaseModelError(
                    f"duplicate subject id: {subject.id}"
                )
            subject_ids.add(subject.id)

        claim_ids: set[str] = set()
        for claim in self.claims:
            if claim.id in claim_ids:
                raise CaseModelError(
                    f"duplicate claim id: {claim.id}"
                )
            claim_ids.add(claim.id)

            missing = set(claim.subject_ids) - subject_ids
            if missing:
                raise CaseModelError(
                    f"claim {claim.id} references "
                    f"missing subjects: {sorted(missing)}"
                )

        evidence_ids: set[str] = set()
        for item in self.evidence:
            if item.id in evidence_ids:
                raise CaseModelError(
                    f"duplicate evidence id: {item.id}"
                )
            evidence_ids.add(item.id)

            if item.subject_id not in subject_ids:
                raise CaseModelError(
                    f"evidence {item.id} subject mismatch"
                )

            unknown = (
                set(item.supports + item.contradicts)
                - claim_ids
            )
            if unknown:
                raise CaseModelError(
                    f"evidence {item.id} references "
                    f"unknown claims: {sorted(unknown)}"
                )

        return self
