# Voss Current State

Status: PORTFOLIO_SYNTHESIZED_V2 / IMPLEMENTATION_AND_QUALIFICATION_OPEN
Record class: WORKING_PROJECT
Canonical development branch: `revival/voss-forensic-analyst-v2-20260920`
Verified predecessor head for this architecture pass:
`9072dff2c740d84ab6f5f2f5c984969642bf7135`

## Mission

Build Voss into a durable cross-project forensic reasoning system that can be reconstructed from repository state, review heterogeneous projects, and remain independent enough to audit the systems around it.

The astrology analyst is one capability and qualification fixture, not Voss's purpose boundary.

## Portfolio architecture pass

On 2026-09-20 the development pass inventoried all 57 repositories available in the portfolio.

The public Voss repository does not republish private source identities/heads/payloads. Public source bindings and a digest commitment to the private source cut are stored at:

`architecture/PORTFOLIO_ARCHITECTURE_SOURCE_CUT_20260920.json`

The synthesis materially incorporated these mechanism families:

- provenance archaeology and chronological restart;
- multi-axis evidence provenance/fidelity/status/currentness/independence;
- heterogeneous reasoning operators and metacognitive strategy selection;
- rival hypotheses and adversarial collaboration;
- influence firewalls;
- exact-subject/currentness/effect separation;
- optimistic concurrency and readback;
- write-ahead ambiguous-effect recovery;
- scientific calibration/holdout discipline;
- append-only incident/correction history;
- optional adapters with no shared-spine dependency requirement.

## V2 architecture

Primary:
`architecture/VOSS_SYSTEM_ARCHITECTURE_V2.md`

Operator registry:
`architecture/VOSS_OPERATOR_REGISTRY_V1.yaml`

Influence firewall:
`architecture/VOSS_INFLUENCE_FIREWALL_V1.md`

Dependency policy:
`architecture/VOSS_DEPENDENCY_POLICY_V1.md`

Case schema:
`schemas/VOSS_CASE_FILE_V1.schema.json`

Executable V2 primitives:
`voss_core/case.py`
`voss_core/influence.py`

## Important correction to V1

The earlier general core treated evidence with one main class axis.

V2 explicitly rejects that simplification.

Evidence origin, representation fidelity, epistemic status, currentness, and independence lineage are separate dimensions. A precise hash does not establish semantic authority; a current direct readback may still be irrelevant to a different proposition; multiple copies of one source do not create independent corroboration.

## Preserved invariants

1. Preserve literal proposition, referent, scope, type, and subject.
2. Evidence origin is not evidence fidelity.
3. Fidelity is not currentness.
4. Currentness is not newest-record time.
5. Repetition and correlated consensus are not independence.
6. Historical evidence remains history after correction/supersession.
7. Source/build/test/delivery/install/active/effect/qualified remain distinct.
8. Capability, assignment, authority, intent, attempt, receipt, and verified effect remain distinct.
9. Assistant/model output does not independently confirm itself.
10. Relationship/status/urgency/confidence signals cannot change a protected evidence verdict.
11. Valid correction is accepted; unsupported pressure is resisted.
12. Ambiguous consequential effects are inspected before retry.
13. Project adapters cannot weaken Voss core evidence rules.
14. Optional ecosystem systems do not become mandatory runtime dependencies.
15. UNRESOLVED is preferable to unsupported closure.
16. A negative or non-identifiable result is preserved rather than tuned away after holdout.

## Completed revival evidence

Astrology analyst freeze:
`d8660dc63e4813f37ed1722a2e867ee2c10b1a49`

Held-out result:
`fe2f309539246d52ec24b83949f603d855657a1d`

Forced held-out accuracy:
78.0% across 200 runs.

Evidence-gated resolved-call accuracy:
98.3471% at 60.5% coverage.

The S0/S2/S4 non-identifiability result remains a qualification example for Voss's unresolved discipline.

## Current frontier

1. Commit and read back the V2 portfolio-synthesized architecture.
2. Extend the qualification corpus from 20 conceptual families into executable fixtures.
3. Implement provenance/currentness/effect-reconciliation operators against the V2 case model.
4. Add a generic Git repository adapter with exact subject/currentness/readback semantics.
5. Run cross-domain cases from multiple unrelated projects.
6. Freeze a candidate before an independent holdout.
7. Do not merge to `main` without Patrick's exact merge authority.

No merge, deployment, provider mutation, or private-source publication is authorized by this state file.
