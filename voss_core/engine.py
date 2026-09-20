from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping

from .types import (
    Claim,
    Evidence,
    Finding,
    VerdictState,
    index_evidence,
    validate_finding,
)


Evaluator = Callable[
    [Claim, Mapping[str, Evidence]],
    Finding,
]


@dataclass
class AuditEngine:
    evaluator: Evaluator

    def run(
        self,
        claims: Iterable[Claim],
        evidence: Iterable[Evidence],
    ) -> list[Finding]:
        evidence_index = index_evidence(evidence)
        findings: list[Finding] = []

        for claim in claims:
            finding = self.evaluator(
                claim,
                evidence_index,
            )
            validate_finding(
                finding,
                claim,
                evidence_index,
            )
            findings.append(finding)

        return findings


def unresolved_by_default(
    claim: Claim,
    evidence: Mapping[str, Evidence],
) -> Finding:
    relevant = tuple(
        item.id
        for item in evidence.values()
        if (
            claim.id in item.supports
            or claim.id in item.contradicts
        )
    )

    return Finding(
        id=f"finding:{claim.id}",
        state=VerdictState.UNRESOLVED,
        claim_id=claim.id,
        evidence_ids=relevant,
        rationale=(
            "No project-specific evaluator established "
            "sufficient evidence."
        ),
        claim_ceiling=claim.ceiling,
    )
