import unittest

from voss_core import (
    AuthorityEvidence,
    AuthoritySource,
    CaseFile,
    CaseModelError,
    ClaimRecord,
    CurrentnessStatus,
    EpistemicStatus,
    EvidenceFidelity,
    EvidenceOrigin,
    EvidenceRecord,
    ExperimentProtocol,
    ExperimentValidity,
    Hypothesis,
    InfluenceFirewall,
    MutationGate,
    OperationEvent,
    OperationState,
    PrivacyItem,
    PropositionType,
    ProvenanceCandidate,
    ProvenanceRelation,
    ReconcileAction,
    RepositorySnapshot,
    ResolutionState,
    ReviewBinding,
    ReviewFreshness,
    RivalState,
    StateCandidate,
    admissible_for_case,
    check_review_freshness,
    effect_authorized,
    evidence_satisfies_claim,
    evaluate_protocol,
    mutation_gate,
    parse_time_interval,
    reconcile_operation,
    requires_chronology_restart,
    resolve_currentness,
    resolve_rivals,
    trace_provenance,
    validate_operation_history,
)


def ev(
    id,
    *,
    subject="s",
    proposition="p",
    origin=EvidenceOrigin.PRIMARY_SOURCE,
    fidelity=EvidenceFidelity.SUMMARY,
    status=EpistemicStatus.OBSERVED,
    currentness=CurrentnessStatus.UNKNOWN,
    immutable_ref=None,
    independence=None,
    derived_from=(),
    supports=(),
    contradicts=(),
):
    return EvidenceRecord(
        id=id,
        source_ref=f"source:{id}",
        subject_id=subject,
        proposition=proposition,
        origin=origin,
        fidelity=fidelity,
        epistemic_status=status,
        currentness=currentness,
        immutable_ref=immutable_ref,
        independence_group=independence,
        derived_from=derived_from,
        supports=supports,
        contradicts=contradicts,
    )


class QualificationV1Tests(unittest.TestCase):
    def test_q01_source_vs_runtime(self):
        claim = ClaimRecord(
            "runtime",
            "s",
            "feature is active",
            PropositionType.RUNTIME_STATE,
            required_origins=(EvidenceOrigin.DIRECT_READBACK,),
            required_fidelities=(EvidenceFidelity.DIRECT_STRUCTURED_READBACK,),
        )
        source = ev(
            "source",
            fidelity=EvidenceFidelity.EXACT_UTF8_SPAN,
            immutable_ref="blob:1",
            supports=("runtime",),
        )
        self.assertFalse(evidence_satisfies_claim(claim, [source]))

    def test_q02_receipt_vs_effect(self):
        claim = ClaimRecord(
            "effect",
            "s",
            "effect occurred",
            PropositionType.EFFECT_STATE,
            required_origins=(EvidenceOrigin.DIRECT_READBACK,),
        )
        receipt = ev(
            "receipt",
            origin=EvidenceOrigin.EXTERNAL_IMPORTED,
            supports=("effect",),
        )
        self.assertFalse(evidence_satisfies_claim(claim, [receipt]))

    def test_q03_stale_currentness(self):
        result = resolve_currentness([
            StateCandidate("old", "s", "old", CurrentnessStatus.HISTORICAL, 100),
            StateCandidate("live", "s", "new", CurrentnessStatus.CURRENT, 10),
        ])
        self.assertEqual(result.state, ResolutionState.RESOLVED)
        self.assertEqual(result.value, "new")

    def test_q04_newest_wins_trap(self):
        result = resolve_currentness([
            StateCandidate("auth", "s", "A", CurrentnessStatus.CURRENT, 100, record_time="2026-01-01"),
            StateCandidate("newer", "s", "B", CurrentnessStatus.CURRENT, 10, record_time="2026-09-20"),
        ])
        self.assertEqual(result.value, "A")

    def test_q05_valid_correction(self):
        result = resolve_currentness([
            StateCandidate("inference", "s", "wrong", CurrentnessStatus.CURRENT, 10),
            StateCandidate("correction", "s", "right", CurrentnessStatus.CURRENT, 100, supersedes=("inference",)),
        ])
        self.assertEqual(result.value, "right")
        self.assertIn("inference", result.ignored_ids)

    def test_q06_invalid_pressure(self):
        with self.assertRaises(CaseModelError):
            InfluenceFirewall.validate_verdict_inputs(
                evidence_ids=("e1",),
                influence_ids=("pressure",),
            )

    def test_q07_proposition_fidelity(self):
        narrow = ClaimRecord("narrow", "s", "A", PropositionType.FACT)
        adjacent = ClaimRecord("adjacent", "s", "A and B", PropositionType.FACT)
        evidence = ev("e", supports=("adjacent",))
        case = CaseFile("c", "test A", "s", "frontier", (narrow, adjacent), (evidence,)).validate()
        self.assertFalse(evidence_satisfies_claim(narrow, case.evidence))
        self.assertTrue(evidence_satisfies_claim(adjacent, case.evidence))

    def test_q08_self_confirmation(self):
        claim = ClaimRecord("c1", "s", "claim", PropositionType.FACT)
        original = ev("voss", supports=("c1",), independence="voss-lineage")
        copied = ev("copy", supports=("c1",), independence="voss-lineage")
        case = CaseFile("case", "test", "s", "f", (claim,), (original, copied)).validate()
        self.assertEqual(case.independent_support_count("c1"), 1)

    def test_q09_consensus_trap(self):
        claim = ClaimRecord("c1", "s", "claim", PropositionType.FACT)
        evidence = tuple(
            ev(f"e{i}", supports=("c1",), independence="shared-premise")
            for i in range(3)
        )
        case = CaseFile("case", "test", "s", "f", (claim,), evidence).validate()
        self.assertEqual(case.independent_support_count("c1"), 1)

    def test_q10_exact_head_movement(self):
        binding = ReviewBinding("repo", "branch", "aaa")
        snapshot = RepositorySnapshot("repo", "branch", "bbb", "now")
        self.assertEqual(
            check_review_freshness(binding, snapshot),
            ReviewFreshness.SUPERSEDED,
        )

    def test_q11_ambiguous_mutation(self):
        self.assertEqual(
            reconcile_operation(
                exact_effect_present=False,
                authoritative_absence=False,
                target_diverged=False,
                authority_current=True,
                precondition_current=True,
            ),
            ReconcileAction.OUTCOME_UNKNOWN,
        )
        self.assertEqual(
            reconcile_operation(
                exact_effect_present=True,
                authoritative_absence=False,
                target_diverged=False,
                authority_current=True,
                precondition_current=True,
            ),
            ReconcileAction.ADOPT_EXISTING,
        )

    def test_q12_authority_drift(self):
        evidence = [
            AuthorityEvidence(
                "old",
                AuthoritySource.HISTORICAL_ASSIGNMENT,
                "repo",
                "merge",
                "main",
                current=False,
            ),
            AuthorityEvidence(
                "cap",
                AuthoritySource.CAPABILITY,
                "repo",
                "merge",
                "main",
            ),
        ]
        self.assertFalse(
            effect_authorized(
                target="repo",
                operation="merge",
                scope="main",
                evidence=evidence,
            )
        )

    def test_q13_security_boundary(self):
        evidence = [
            AuthorityEvidence(
                "prompt",
                AuthoritySource.UNTRUSTED_CONTENT,
                "repo",
                "merge",
                "main",
            )
        ]
        self.assertFalse(
            effect_authorized(
                target="repo",
                operation="merge",
                scope="main",
                evidence=evidence,
            )
        )

    def test_q14_privacy_relevance(self):
        selected = admissible_for_case([
            PrivacyItem("relevant", True, True, True),
            PrivacyItem("irrelevant-private", True, False, True),
            PrivacyItem("excess", True, True, False),
        ])
        self.assertEqual(selected, ("relevant",))

    def test_q15_experiment_leakage(self):
        protocol = ExperimentProtocol(
            calibration_ids=("a",),
            holdout_ids=("b",),
            hidden_fields=("world_label",),
            analyst_visible_fields=("outcome", "world_label"),
            frozen_before_execution=True,
        )
        self.assertEqual(
            evaluate_protocol(protocol),
            ExperimentValidity.INVALID_LEAKAGE,
        )

    def test_q16_posthoc_rescue(self):
        protocol = ExperimentProtocol(
            calibration_ids=("a",),
            holdout_ids=("b",),
            hidden_fields=("world_label",),
            analyst_visible_fields=("outcome",),
            frozen_before_execution=True,
        )
        self.assertEqual(
            evaluate_protocol(protocol, tuned_after_holdout=True),
            ExperimentValidity.REQUIRES_FRESH_HOLDOUT,
        )

    def test_q17_migration_state(self):
        claim = ClaimRecord(
            "applied",
            "s",
            "migration is applied at provider",
            PropositionType.RUNTIME_STATE,
            required_origins=(EvidenceOrigin.DIRECT_READBACK,),
        )
        migration = ev("migration", supports=("applied",))
        local_test = ev(
            "local-test",
            origin=EvidenceOrigin.DERIVED,
            derived_from=("migration",),
            supports=("applied",),
        )
        self.assertFalse(
            evidence_satisfies_claim(claim, [migration, local_test])
        )

    def test_q18_concurrency_stale_write(self):
        self.assertEqual(
            mutation_gate(
                expected_head="aaa",
                actual_head="bbb",
            ),
            MutationGate.STALE_HEAD,
        )

    def test_q19_documentation_drift(self):
        result = resolve_currentness([
            StateCandidate("readme", "s", "old", CurrentnessStatus.HISTORICAL, 10),
            StateCandidate("live", "s", "new", CurrentnessStatus.CURRENT, 100),
        ])
        self.assertEqual(result.value, "new")

    def test_q20_unresolved_discipline(self):
        hypotheses = [
            Hypothesis("h1", "cause one"),
            Hypothesis("h2", "cause two"),
        ]
        evidence = [
            ev("shared", supports=("h1", "h2"), currentness=CurrentnessStatus.CURRENT),
        ]
        result = resolve_rivals(hypotheses, evidence)
        self.assertEqual(result.state, RivalState.UNRESOLVED)
        self.assertIn("h1", result.discriminating_need)
        self.assertIn("h2", result.discriminating_need)


class OperatorRegressionTests(unittest.TestCase):
    def test_roots_partial_order_and_backref(self):
        january = ProvenanceCandidate(
            "jan",
            parse_time_interval("2026-01"),
            ProvenanceRelation.ANCESTRAL,
        )
        jan15 = ProvenanceCandidate(
            "jan15",
            parse_time_interval("2026-01-15"),
            ProvenanceRelation.LITERAL,
            references=("missing-december",),
        )
        feb = ProvenanceCandidate(
            "feb",
            parse_time_interval("2026-02-01"),
            ProvenanceRelation.ORIGIN_CLAIM,
        )
        trace = trace_provenance([january, jan15, feb])
        self.assertEqual(set(trace.earliest_accessible), {"jan", "jan15"})
        self.assertEqual(trace.first_literal, ("jan15",))
        self.assertEqual(trace.unresolved_backrefs, ("missing-december",))
        self.assertTrue(
            requires_chronology_restart(
                parse_time_interval("2026-03-01"),
                parse_time_interval("2026-01-01"),
            )
        )

    def test_equal_authority_conflict_remains_conflict(self):
        result = resolve_currentness([
            StateCandidate("a", "s", "A", CurrentnessStatus.CURRENT, 50),
            StateCandidate("b", "s", "B", CurrentnessStatus.CURRENT, 50),
        ])
        self.assertEqual(result.state, ResolutionState.CONFLICT)

    def test_all_rivals_contradicted_is_conflict(self):
        hypotheses = [Hypothesis("h1", "one"), Hypothesis("h2", "two")]
        evidence = [
            ev("e1", contradicts=("h1",), currentness=CurrentnessStatus.CURRENT),
            ev("e2", contradicts=("h2",), currentness=CurrentnessStatus.CURRENT),
        ]
        result = resolve_rivals(hypotheses, evidence)
        self.assertEqual(result.state, RivalState.CONFLICT)

    def test_operation_history_transition_validation(self):
        validate_operation_history([
            OperationEvent("op1", OperationState.PREPARED, "target"),
            OperationEvent("op1", OperationState.ATTEMPTED, "target"),
            OperationEvent("op1", OperationState.AMBIGUOUS, "target"),
            OperationEvent("op1", OperationState.RECONCILED, "target", receipt="sha"),
        ])
        with self.assertRaises(ValueError):
            validate_operation_history([
                OperationEvent("op1", OperationState.PREPARED, "target"),
                OperationEvent("op1", OperationState.VERIFIED, "target"),
            ])

    def test_authority_must_match_exact_scope(self):
        evidence = [
            AuthorityEvidence(
                "current",
                AuthoritySource.CURRENT_DELEGATION,
                "repo",
                "write",
                "branch-a",
            )
        ]
        self.assertTrue(effect_authorized(
            target="repo", operation="write", scope="branch-a", evidence=evidence
        ))
        self.assertFalse(effect_authorized(
            target="repo", operation="write", scope="main", evidence=evidence
        ))


if __name__ == "__main__":
    unittest.main()
