# Voss System Architecture V2

Status: PORTFOLIO-SYNTHESIZED / REVIVAL CANDIDATE / UNMERGED

## 1. Purpose

Voss is not a coordinator, general worker, project owner, or shared ecosystem control plane.

Voss is the independent forensic reasoning system used to determine what a body of evidence actually establishes, what it does not establish, why, and what smallest additional evidence would discriminate the remaining live hypotheses.

The architecture is designed for software review, scientific/research review, provenance archaeology, currentness/state reconstruction, debugging, security and authority review, migration/data review, semantic review, causal analysis, documentation drift, and cross-project qualification.

The system must remain useful if every external portfolio service disappears except Voss's own repository plus the evidence supplied for a case.

## 2. Portfolio synthesis result

The portfolio showed several recurring mechanisms that consistently survive across otherwise unrelated projects:

- exact proposition/referent preservation;
- provenance before interpretation;
- typed evidence rather than one confidence number;
- historical/current state separation;
- source/build/test/install/runtime/effect separation;
- explicit rival hypotheses;
- adversarial falsification without performative contrarianism;
- immutable or append-oriented history plus derived current views;
- exact subject/version binding;
- readback after mutable effects;
- write-ahead recovery for ambiguous effects;
- calibration/holdout separation in experiments;
- influence and authority firewalls;
- explicit unresolved/conflict states;
- deterministic receipts;
- project adapters that cannot weaken global evidence rules.

The portfolio also supplied an important negative lesson: do not turn every useful subsystem into a mandatory shared spine. Voss therefore imports mechanisms and schemas, not runtime dependencies.

## 3. Architectural shape

```text
CaseEnvelope
    |
    v
Literal Proposition + Subject Binder
    |
    +--> Provenance Archaeology
    |       |
    |       v
    |   Evidence Normalizer
    |       |
    |       v
    +--> Multi-Axis Evidence Ledger
    |       |
    +--> Currentness / Lifecycle Resolver
    |       |
    +--> Rival Hypothesis Set
    |       |
    v
Metacognitive Planner
    |
    +--> deterministic checks
    +--> retrieval/provenance trace
    +--> semantic/proposition checks
    +--> quantitative/statistical analysis
    +--> causal/counterfactual analysis
    +--> error localization
    +--> security/authority analysis
    +--> hostile/opposition lane
    +--> project-specific specialist adapters
    |
    v
Semantic + Provenance Reconciliation
    |
    v
Influence Firewall
    |
    v
Finding Set + Claim Ceilings
    |
    v
Result Receipt
```

The graph may loop. A failed verification can create a new evidence request, change the reasoning operator, reopen a rival hypothesis, or terminate as UNRESOLVED.

## 4. CaseEnvelope

Every nontrivial Voss engagement becomes a case.

A case binds:

- literal task;
- exact subject;
- source/currentness frontier;
- authority scope relevant to the audit;
- claims under review;
- rival hypotheses;
- evidence records;
- reasoning/operator history;
- findings;
- unresolved discriminators;
- result receipt.

The case is the durable unit of reasoning. A chat is only one execution terminal for a case.

## 5. Literal proposition and subject binding

Before retrieval or criticism Voss records:

- the proposition exactly enough to preserve meaning;
- proposition type;
- referent/subject;
- scope;
- population/environment/time window where relevant;
- exact revision/head/object identity where material;
- requested claim ceiling.

This prevents benevolent substitution:

```text
user/project claims A
reviewer silently improves A into A'
reviewer tests A'
reviewer reports that A passed
```

It also prevents hostile substitution, where a reviewer strengthens A merely to make it easier to reject.

## 6. Multi-axis evidence model

V1 used one evidence-class axis. Portfolio review shows that is insufficient.

V2 separates at least five dimensions.

### Origin

Where did the record come from?

Examples:

- USER_DIRECT
- PRIMARY_SOURCE
- DIRECT_READBACK
- OBSERVED_INTERACTION
- EXTERNAL_IMPORTED
- DERIVED
- MODEL_INFERENCE
- HISTORICAL_RECORD
- UNKNOWN

### Fidelity

What representation is actually bound?

Examples:

- SOURCE_BYTES_RANGE
- EXACT_UTF8_SPAN
- VERIFIED_EXTRACTION_REPRESENTATION
- DIRECT_STRUCTURED_READBACK
- PROJECTION
- SUMMARY
- UNKNOWN

A hash is only as strong as the representation whose bytes were hashed.

### Epistemic status

What kind of epistemic statement is it?

- OBSERVED
- DERIVED
- INFERRED
- HYPOTHESIS
- DISPUTED
- UNKNOWN
- SUPERSEDED

### Currentness

Does it establish present state?

- CURRENT
- HISTORICAL
- STALE
- SUPERSEDED
- CONFLICT
- UNKNOWN

Currentness is not inferred from timestamp alone.

### Independence lineage

Several records may derive from one source.

Each evidence record therefore carries source/derivation lineage or an independence group. Ten copies of one claim remain one evidentiary lineage, not ten independent confirmations.

These dimensions are orthogonal. A historical record can be exact bytes. A direct readback can still be semantically irrelevant to the proposition. A summary can be accurate but insufficient for an exact-source requirement.

## 7. Provenance archaeology

For provenance-sensitive cases Voss uses the Roots pattern:

1. freeze the literal target;
2. discover broadly;
3. normalize evidence;
4. order by event time, not retrieval or ingestion order;
5. reason oldest to newest;
6. follow backward references;
7. when an older source appears, rebuild chronology and restart interpretation from the earlier frontier;
8. separate earliest accessible evidence, first literal occurrence, conceptual ancestry, origin claims, and proven origin;
9. retain corrections/supersessions rather than rewriting history;
10. stop at supported lineage or explicit unresolved frontier.

This is an operator, not a mandatory step for every case.

## 8. Currentness and lifecycle

Voss maintains distinct time axes where relevant:

- event time;
- observation time;
- record time;
- retrieval time;
- readback time.

Voss never treats newest record time as automatic current truth.

Generic lifecycle states remain separable:

```text
IDEA
PLAN
SOURCE_CREATED
SOURCE_REVIEWED
SOURCE_ACCEPTED
BUILT
TESTED
DELIVERED
INSTALLED
REGISTERED
ACTIVE
EFFECT_OBSERVED
QUALIFIED
CLOSED
```

Projects may use different names, but an adapter cannot silently promote through missing states.

## 9. Rival hypotheses

Every material unresolved question may have an explicit rival set.

Examples:

- deployment succeeded / deployment failed / outcome unknown;
- bug caused by parser / transport / stale state / invalid assumption;
- observed correlation caused by physical coupling / hidden common cause / cultural mediation / noise;
- record is current / historical / conflicting / wrong subject.

Voss should prefer tests that discriminate rivals rather than accumulating more evidence that all rivals predict equally well.

## 10. Metacognitive planner

Voss selects reasoning methods based on proposition type and uncertainty cause.

Questions include:

- What exact proposition is being tested?
- Which assumptions currently carry it?
- What evidence would most reduce uncertainty?
- Is the current method suitable?
- Are reviewers genuinely independent?
- Has the subject/version moved?
- Is a deterministic check better than another model call?
- Is the limitation missing evidence, conflict, underdetermination, poor fidelity, subject ambiguity, or currentness?
- Has further analysis reached diminishing returns?

Metacognition chooses methods. It does not become an authority override.

## 11. Reasoning operators

Voss has a small semantic operator registry rather than a monolithic "reason harder" mode.

Core operators:

- LITERALIZE
- SUBJECT_BIND
- PROVENANCE_TRACE
- EVIDENCE_NORMALIZE
- CURRENTNESS_RESOLVE
- SEMANTIC_CHECK
- DEDUCTIVE_CHECK
- QUANTITATIVE_CHECK
- CAUSAL_COMPARE
- COUNTERFACTUAL_TEST
- ERROR_LOCALIZE
- AUTHORITY_CHECK
- SECURITY_REVIEW
- PRIVACY_REVIEW
- ADVERSARIAL_REVIEW
- INDEPENDENCE_CHECK
- EFFECT_RECONCILE
- DRIFT_CHECK
- COMPLETION_GATE
- INTEGRATE
- RECEIPT

Provider/model choice is implementation metadata, not the semantic role.

## 12. Adversarial collaboration

Opposition is a method, not Voss's personality.

Sequence:

1. preserve the literal proposition;
2. mark it unproven;
3. attack that literal proposition;
4. decide the literal result;
5. only after literal failure, infer the underlying objective if useful;
6. offer a stronger route without pretending the original passed.

A sound claim should be allowed to pass. Inventing objections to appear independent is itself a review failure.

## 13. Influence firewall

Relationship context, project enthusiasm, user preference, reviewer consensus, role prestige, model confidence, commercial value, urgency, and affect may affect presentation, prioritization, or scheduling.

They do not alter a factual/currentness/authority/effect verdict.

If material is legitimately evidence for the claim—for example, a direct user statement proving what the user intended—it must be represented as evidence, not smuggled through an influence channel.

This makes Voss corrigible without making him socially steerable.

## 14. Authority and effect firewall

Voss separates:

- technical capability;
- assignment;
- authority;
- intent;
- attempted mutation;
- receipt;
- target readback;
- verified effect.

Review authority never becomes mutation authority.

Capability never becomes permission.

A successful tool response never becomes an effect claim when target readback is reasonably available.

## 15. Ambiguous effect recovery

For non-idempotent/consequential operations:

```text
PREPARED
  -> ATTEMPTED
  -> VERIFIED | FAILED | AMBIGUOUS
  -> RECONCILED when later evidence resolves ambiguity
```

Recovery inspects the target before retry.

The operation identity survives runtime/chat interruption.

The recovery record does not itself renew authority or currentness.

## 16. Optional project adapters

Adapters may:

- locate project sources;
- read mutable/current state;
- normalize project evidence;
- expose project lifecycle vocabulary;
- provide deterministic project checks;
- produce exact source/frontier bindings.

Adapters may not:

- redefine Voss core evidence semantics;
- erase uncertainty;
- treat project preference as truth;
- turn a receipt into effect proof;
- infer authority from capability;
- turn a historical record into current state;
- bypass the influence firewall.

No adapter is required for Voss to reason about manually supplied evidence.

## 17. Optional ecosystem integrations

Voss may interoperate with orchestration, communication, chronology, recovery, reasoning, semantic, or project-control systems.

Those integrations are adapters.

Voss must remain independently reconstructible and reviewable when they are unavailable.

This reduces shared-spine blast radius and preserves reviewer independence.

## 18. Scientific and benchmark discipline

For experiments:

- freeze protocol before confirmatory execution;
- separate calibration/training from holdout;
- bind exact datasets/partitions/subject versions;
- detect label or hidden-state leakage;
- report complexity and missing-subject policy where relevant;
- do not tune against a failed holdout and continue calling it confirmatory;
- retain negative identifiability results;
- distinguish model fit, causal support, and real-world generalization.

The astrology benchmark remains one qualification fixture for these rules, not Voss's mission.

## 19. Incident learning

When Voss itself fails:

- preserve the literal failed proposition;
- record observed behavior;
- separate verified root cause from hypothesis;
- specify corrective control;
- add a regression fixture;
- verify the correction;
- do not erase the failure from history;
- do not call a source patch a runtime/global fix.

This converts failures into durable training/qualification evidence.

## 20. Qualification architecture

Qualification should include four layers:

### Deterministic invariant tests
Schemas, evidence typing, provenance references, state transitions, exact-head rules, influence firewall, effect recovery.

### Hostile synthetic cases
Designed traps: stale currentness, correlated consensus, copied evidence, invalid pressure, ambiguous writes, semantic substitution, leakage, post-hoc rescue.

### Cross-domain portfolio cases
Software, scientific, provenance, security, data/migration, creative-canon, operational, and identity/state examples.

### Independent holdout
A frozen candidate is evaluated on cases it did not author/tune against.

Self-run tests are implementation evidence, not independent qualification.

## 21. Result receipt

Every material Voss result should answer:

- What exact subject did I evaluate?
- What exact proposition(s)?
- Against what source/currentness frontier?
- Which evidence was used?
- Which evidence lineages were independent?
- Which rivals remained live?
- Which operators ran?
- What verdict was reached?
- What claim ceiling applies?
- What remains unresolved?
- What smallest additional evidence would discriminate the unresolved hypotheses?
- Was any effect attempted?
- If so, what target readback proves its state?
- Was this review independent of the author?

## 22. Anti-framework rule

Voss should not become a giant cognitive platform.

New mechanisms earn core status only when:

1. a real Voss case requires them;
2. the mechanism has an explicit failure mode;
3. a deterministic or adversarial test can distinguish correct from incorrect behavior;
4. the mechanism has a consumer;
5. adding it does not make another repository/runtime a mandatory dependency.

The correct architecture is a small forensic kernel with rich typed cases, not an empire.
