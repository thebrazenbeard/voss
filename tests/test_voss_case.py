import unittest

from voss_core.case import (
    CaseFile,
    CaseModelError,
    ClaimRecord,
    CurrentnessStatus,
    EpistemicStatus,
    EvidenceFidelity,
    EvidenceOrigin,
    EvidenceRecord,
    PropositionType,
    evidence_satisfies_claim,
)
from voss_core.influence import InfluenceFirewall


class VossCaseModelTests(unittest.TestCase):
    def test_derived_evidence_requires_lineage(self):
        with self.assertRaises(CaseModelError):
            EvidenceRecord(
                id="e1",
                source_ref="derived",
                subject_id="subject",
                proposition="derived proposition",
                origin=EvidenceOrigin.DERIVED,
                fidelity=EvidenceFidelity.SUMMARY,
                epistemic_status=EpistemicStatus.DERIVED,
            )

    def test_exact_fidelity_requires_immutable_ref(self):
        with self.assertRaises(CaseModelError):
            EvidenceRecord(
                id="e1",
                source_ref="source",
                subject_id="subject",
                proposition="exact source",
                origin=EvidenceOrigin.PRIMARY_SOURCE,
                fidelity=EvidenceFidelity.EXACT_UTF8_SPAN,
                epistemic_status=EpistemicStatus.OBSERVED,
            )

    def test_copies_do_not_create_independence(self):
        claim = ClaimRecord(
            id="c1",
            subject_id="subject",
            proposition="claim",
            proposition_type=PropositionType.FACT,
        )

        first = EvidenceRecord(
            id="e1",
            source_ref="original",
            subject_id="subject",
            proposition="support",
            origin=EvidenceOrigin.PRIMARY_SOURCE,
            fidelity=EvidenceFidelity.SUMMARY,
            epistemic_status=EpistemicStatus.OBSERVED,
            independence_group="lineage-1",
            supports=("c1",),
        )

        copy = EvidenceRecord(
            id="e2",
            source_ref="copy",
            subject_id="subject",
            proposition="same support copied",
            origin=EvidenceOrigin.EXTERNAL_IMPORTED,
            fidelity=EvidenceFidelity.SUMMARY,
            epistemic_status=EpistemicStatus.OBSERVED,
            independence_group="lineage-1",
            supports=("c1",),
        )

        case = CaseFile(
            case_id="case-1",
            literal_task="test claim",
            subject_id="subject",
            source_frontier="frontier",
            claims=(claim,),
            evidence=(first, copy),
        ).validate()

        self.assertEqual(
            case.independent_support_count("c1"),
            1,
        )

    def test_claim_can_require_origin_and_fidelity(self):
        claim = ClaimRecord(
            id="c1",
            subject_id="subject",
            proposition="runtime active",
            proposition_type=PropositionType.RUNTIME_STATE,
            required_origins=(EvidenceOrigin.DIRECT_READBACK,),
            required_fidelities=(
                EvidenceFidelity.DIRECT_STRUCTURED_READBACK,
            ),
        )

        receipt = EvidenceRecord(
            id="e1",
            source_ref="tool-receipt",
            subject_id="subject",
            proposition="request accepted",
            origin=EvidenceOrigin.EXTERNAL_IMPORTED,
            fidelity=EvidenceFidelity.SUMMARY,
            epistemic_status=EpistemicStatus.OBSERVED,
            supports=("c1",),
        )

        self.assertFalse(
            evidence_satisfies_claim(
                claim,
                [receipt],
            )
        )

        readback = EvidenceRecord(
            id="e2",
            source_ref="runtime",
            subject_id="subject",
            proposition="runtime active",
            origin=EvidenceOrigin.DIRECT_READBACK,
            fidelity=EvidenceFidelity.DIRECT_STRUCTURED_READBACK,
            epistemic_status=EpistemicStatus.OBSERVED,
            currentness=CurrentnessStatus.CURRENT,
            immutable_ref="runtime-readback:1",
            supports=("c1",),
        )

        self.assertTrue(
            evidence_satisfies_claim(
                claim,
                [receipt, readback],
            )
        )

    def test_influence_cannot_be_verdict_input(self):
        with self.assertRaises(CaseModelError):
            InfluenceFirewall.validate_verdict_inputs(
                evidence_ids=("e1",),
                influence_ids=("relationship-pressure",),
            )

    def test_case_rejects_missing_lineage_parent(self):
        claim = ClaimRecord(
            id="c1",
            subject_id="subject",
            proposition="claim",
            proposition_type=PropositionType.FACT,
        )

        child = EvidenceRecord(
            id="e2",
            source_ref="summary",
            subject_id="subject",
            proposition="derived",
            origin=EvidenceOrigin.DERIVED,
            fidelity=EvidenceFidelity.SUMMARY,
            epistemic_status=EpistemicStatus.DERIVED,
            derived_from=("missing-parent",),
            supports=("c1",),
        )

        with self.assertRaises(CaseModelError):
            CaseFile(
                case_id="case",
                literal_task="test",
                subject_id="subject",
                source_frontier="frontier",
                claims=(claim,),
                evidence=(child,),
            ).validate()


if __name__ == "__main__":
    unittest.main()
