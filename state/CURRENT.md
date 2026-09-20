# Voss Current State

Status: REAL_PROJECT_GENERALIZATION_V1 / SIX_LIVE_CASES_COMPLETE / FREEZE_NEXT
Record class: WORKING_PROJECT
Canonical development branch: `revival/voss-forensic-analyst-v2-20260920`
Verified predecessor head for this real-project pass:
`6ea3891b734b3f4bd46f4a383f03768dcc4f193c`

## Mission

Build Voss into a durable cross-project forensic reasoning system that can audit real heterogeneous projects without collapsing source, currentness, authority, runtime, effect, provenance, scientific inference, or documentation state.

## Real-project audit corpus

Report:
`qualification/REAL_PROJECT_AUDIT_REPORT_20260920_V1.json`
`qualification/REAL_PROJECT_AUDIT_REPORT_20260920_V1.md`

Cases:
- `cases/real/20260920/RP01_ROOTS_PROVENANCE.json`
- `cases/real/20260920/RP02_WIP_SOURCE_RUNTIME.json`
- `cases/real/20260920/RP03_WORLD_ZERO_SCIENCE.json`
- `cases/real/20260920/RP04_PROJECT_RUNNER_AUTHORITY.json`
- `cases/real/20260920/RP05_ON_THEO_BRANCH_DATA_STATE.json`
- `cases/real/20260920/RP06_REZON_DOCUMENTATION_CURRENTNESS.json`

Domains:
- provenance
- software/runtime
- scientific inference
- security/authority
- migration/data-state
- documentation/currentness

Findings derived from case corpus:
- PASS: 5
- FAIL: 8
- UNRESOLVED: 3

These are self-run real-project audits, not independent qualification.

## Real defects found and repaired

### VOSS-REAL-001 — multi-subject cases

Problem:
single-subject `CaseFile` cannot faithfully represent real cross-ref/source-vs-runtime comparison cases.

Repair:
`voss_core/multisubject.py`

### VOSS-REAL-002 — live GitHub mutable-ref race

Problem:
reading a file through a mutable branch name can silently mix frontiers if the branch moves between ref and content reads.

Repair:
`voss_adapters/github_live.py`

Protocol:
read ref -> fetch file by exact head -> reread ref -> mark stale if moved.

Adapter contract:
`architecture/GITHUB_LIVE_ADAPTER_V1.md`

### VOSS-REAL-003 — aggregate report drift

Problem:
the first manually written report counts did not match the actual case corpus.

Repair:
`voss_core/reporting.py`

Rule:
aggregate verdict counts are derived from case files; mismatches fail regression.

## Preserved prior qualification

Synthetic/unit qualification predecessor:
- 35 / 35 local self-run PASS
- Q01-Q20 executable
- prior core/case regressions preserved

Receipt:
`qualification/SELF_RUN_RECEIPT_20260920_V1.json`

## Current verification ceiling

The live project evidence was read directly from GitHub and bound to exact commit/blob identities.

New adapter/multi-subject/reporting source has been syntax-checked and regression cases prepared.

This pass must not be called independent qualification.

## Next frontier

1. Commit this real-project corpus and repairs.
2. Verify exact readback.
3. Freeze that exact candidate commit.
4. Create a holdout/evaluator packet that does not contain expected verdicts.
5. Do not modify the frozen candidate while evaluating it.
6. Use a genuinely separate evaluator runtime/person before claiming independent behavioral qualification.
7. Convert independent failures into a new post-freeze development candidate, never by editing the evaluated candidate.

No merge to `main`, deployment, provider mutation, or private-source publication is authorized.
