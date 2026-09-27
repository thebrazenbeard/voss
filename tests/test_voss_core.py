import unittest

from voss_core.engine import (
    AuditEngine,
    unresolved_by_default,
)
from voss_core.types import (
    Claim,
    EffectState,
    Evidence,
    EvidenceClass,
    EvidenceError,
    Finding,
    VerdictState,
    index_evidence,
    validate_finding,
)


class CoreInvariantTests(unittest.TestCase):
    def test_duplicate_evidence_rejected(self):
        evidence = Evidence(
            "e1",
            EvidenceClass.PRIMARY_SOURCE,
            "source",
            "proposition",
        )

        with self.assertRaises(EvidenceError):
            index_evidence(
                [evidence, evidence]
            )

    def test_pass_requires_declared_evidence_class(self):
        claim = Claim(
            "c1",
            "artifact is installed",
            (
                EvidenceClass.DIRECT_READBACK,
            ),
        )

        evidence = {
            "e1": Evidence(
                "e1",
                EvidenceClass.RECEIPT,
                "receipt",
                "upload accepted",
            )
        }

        finding = Finding(
            "f1",
            VerdictState.PASS,
            "c1",
            ("e1",),
            "bad promotion",
        )

        with self.assertRaises(EvidenceError):
            validate_finding(
                finding,
                claim,
                evidence,
            )

    def test_runtime_state_requires_readback(self):
        claim = Claim(
            "c1",
            "runtime active",
        )

        evidence = {
            "e1": Evidence(
                "e1",
                EvidenceClass.PRIMARY_SOURCE,
                "repo",
                "source exists",
            )
        }

        finding = Finding(
            "f1",
            VerdictState.UNRESOLVED,
            "c1",
            ("e1",),
            "source only",
            effect_state=EffectState.ACTIVE,
        )

        with self.assertRaises(EvidenceError):
            validate_finding(
                finding,
                claim,
                evidence,
            )

    def test_unresolved_default_is_valid(self):
        claim = Claim(
            "c1",
            "unknown proposition",
        )

        evidence = [
            Evidence(
                "e1",
                EvidenceClass.HISTORICAL,
                "archive",
                "old claim",
                supports=("c1",),
            )
        ]

        result = AuditEngine(
            unresolved_by_default
        ).run(
            [claim],
            evidence,
        )

        self.assertEqual(
            result[0].state,
            VerdictState.UNRESOLVED,
        )
        self.assertEqual(
            result[0].evidence_ids,
            ("e1",),
        )


if __name__ == "__main__":
    unittest.main()
