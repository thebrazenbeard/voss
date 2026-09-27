# Voss Real-Project Audit V1 — 2026-09-20

Status: **REAL PUBLIC-PROJECT CASES COMPLETE / SELF-RUN / NOT INDEPENDENT**

Candidate entering this pass:

`6ea3891b734b3f4bd46f4a383f03768dcc4f193c`

## Scope

Six unrelated public projects were audited from fresh GitHub reads:

- Roots — provenance
- WIP — software/runtime effect boundary
- World Zero — scientific inference and holdout discipline
- Project Runner — security/authority
- On-Theo — branch/data-state promotion
- Rezon — documentation/currentness

Total findings, derived from the case corpus:

- PASS: 5
- FAIL: 8
- UNRESOLVED: 3

The UNRESOLVED results are intentional evidence that Voss did not manufacture closure when source evidence could not establish runtime or canonical currentness.

## Three Voss defects found by real work

### VOSS-REAL-001 — single-subject case model

The original `CaseFile` binds one `subject_id`.

That is insufficient for real audits comparing:
- main vs feature branch;
- source vs runtime;
- pre-migration vs post-migration state;
- two provider/readback surfaces.

Repair:
`voss_core/multisubject.py`

Regression:
`test_multisubject_case_supports_cross_ref_claim`

### VOSS-REAL-002 — mutable-ref race

A naive GitHub adapter can read branch head A, then fetch a file through the mutable branch name after it has moved to B, silently producing mixed-frontier evidence.

Repair:
`voss_adapters/github_live.py`

The adapter now:
1. reads mutable ref;
2. binds the exact head SHA;
3. fetches the file by exact commit;
4. rereads the mutable ref;
5. marks the file evidence stale for current-ref claims if the branch moved.

Regression:
`test_branch_movement_marks_file_stale`

### VOSS-REAL-003 — report drift

The first hand-written audit summary counted the real case outcomes incorrectly.

The case corpus contained 5 PASS / 8 FAIL / 3 UNRESOLVED, while the draft summary said 7 / 6 / 3.

Repair:
`voss_core/reporting.py`

Aggregate verdict counts are now derived from case files, and report/corpus mismatch is a test failure.

Regression:
`test_report_counts_are_derived_from_cases`

## Case outcomes

### RP01 Roots

PASS:
Roots methodology requires chronology rebuild/restart when backward discovery reveals earlier evidence.

FAIL:
earliest accessible evidence is not automatically proven origin.

### RP02 WIP

PASS:
source contract requires target readback before VERIFIED effect state.

UNRESOLVED:
GitHub source alone does not establish a currently active WIP-managed runtime effect.

### RP03 World Zero

FAIL:
unqualified `WORLD_ZERO_VALIDATED` is not permitted by the methodology.

FAIL:
failed holdout data cannot be moved into calibration while remaining holdout evidence.

UNRESOLVED:
the methodology/benchmark design files do not themselves establish real-world predictive validity.

### RP04 Project Runner

FAIL:
broad GitHub capability is not standing downstream mutation authority.

PASS:
the source contract requires exact grant/scope, mutable-state preconditions, and readback.

FAIL:
read-only CI smoke evidence is not mutation authority.

### RP05 On-Theo

FAIL:
the Voss astrology baseline result is not present on audited `main`.

FAIL:
the astrology branch has not been promoted/merged into audited `main`.

PASS:
the result exists on the audited astrology branch.

At the evidence cut, astrology is 9 commits ahead of main and 0 behind.

### RP06 Rezon

FAIL:
main alone is insufficient to reconstruct the substantial Rezon architecture visible in the repository.

UNRESOLVED:
the r47 continuation branch is not promoted to canonical-current merely because it is richer than main.

PASS:
main and r47 differ materially; exact comparison reports r47 278 commits ahead and 0 behind.

## Claim ceiling

These are real source/currentness audits, but they were performed by the same development agent building Voss.

They are useful generalization evidence and defect discovery.

They are **not independent qualification**.
