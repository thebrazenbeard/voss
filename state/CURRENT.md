# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T1409-0400.md`
Checkpoint commit: `442a295e363ef82008401aba084ce12f446a80b5`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3580`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination before starting, resuming, reporting, counting, closing, or using authority.
4. Refresh task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Preserve project separation and writer leases.

## Critical path
- R9A0 remains under construction and is not installed.
- Bob B15 remains CURRENT under the sole-writer lease on `feature/r9a0-combined-native-implementation-v1`, but repository writes are PAUSED by canonical 3579 for a newly discovered B13 assignment-lineage defect.
- Fresh GitHub compare at the pause boundary showed the branch identical to `ddcd98b4e61df09f06886f2073ecbdfad21c8f12` (0 ahead/0 behind). No post-resume candidate commit was observed.
- B11 Settings remain frozen at SHA-256 `a36fd6e91c44afa5db9a12f959dbcab97ebe335fa8e4edb7d5d42e3f86e556ca`.
- PostgreSQL server truth remains `17.6 / 170006`.
- H25/H26 are closed APPROVED at 3566/3568; H28 closed APPROVED at 3577. `BUILT_AND_VALIDATED` is still unsatisfied.

## B13 root-lineage defect
Exact admitted corrected B13 bundle SHA-256 before correction: `7b7f8c3ea120c080b88fffa150ff64096ccc6f96209efa1c3231d959f44eaa64`.
Affected path: `tests/native-project/test_r9a0_assignment_currentness.py`.

The current reducer applies every admitted state relation in commit order without proving it is connected to the requested `root_event_id`. An admitted REROUTE referencing `other_root` can therefore control the wrong lane. Separately, the sibling-conflict `children` map is built from all admitted typed events before filtering state relations, so multiple non-state proposals/reviews can falsely conflict a lane.

Canonical 3579 preserves Bob's writer lease and no-touch boundaries, permits read-only analysis plus generation of surgical corrected B13 artifacts, and prohibits committing affected/final package paths until review.

## Current audits
- H30 current 3580: independent root-lineage isolation audit and B15 resume gate. Must confirm/falsify the defect, define smallest correct root-connected graph, attack off-root/orphan/skipped/cycle/sibling/non-state/valid-chain cases, and decide B13-only vs narrowly justified B12 clarification.
- H27 current 3572: deterministic provider role-topology/transport-assurance digest amendment still required.
- H29 current 3578: audited exposed-mutation-surface confinement. Fresh evidence includes GitHub/Supabase `Allow all actions` app-specific settings, generic low-level mutation routes, semantic mutation-class inventory, and pagination/completeness requirements. No permission was changed.
- Masa MA13 3545 / MA14 3546, Mune MU6 3547 / MU7 3548, and Vera V5 3549 / V6 3550 remain current read-only lanes awaiting final proposals.

## Bugs reported this interval
1. BT2 `memory_events.source_facets` hard-coded enum excludes Voss, making honest Voss attribution impossible in that field. Reported to `#chat-bug-reports` and One; no schema mutation.
2. R9A0 assignment-level boolean `effect_eligible` is semantically easy to confuse with final `PROTECTED_EFFECT_ELIGIBILITY`, which separately requires authority + confinement evidence. Reported and routed into H29 as a non-substitutability hostile.
3. R9A0 B13 root-lineage isolation defect and non-state sibling-conflict defect. Reported; B15 paused before contamination; H30 assigned.

## Separate program boundaries
BT2 bug_ops review remains separate: One owns its writer path; Masa/Mune review; Vera copy remains held. Mesh product review is durable at BT2 event 2221 and is not on the R9A0 build critical path.

## Priority
1. Obtain Bob corrected B13 exact artifact proposal and H30 independent audit.
2. Review both; resume B15 only if root-lineage isolation is mechanically proven and branch is still exact.
3. Complete H27/H29 evidence contracts without letting them delay the repository build unnecessarily.
4. Receive/review MA13/MA14, MU6/MU7, V5/V6 final proposals.
5. After B15 resumes: final Validation Report -> checksums -> deterministic validation -> exact pushed-head CI -> post-evidence readback before any `BUILT_AND_VALIDATED` claim.

## Persistence policy
Use this repository as the canonical privacy-minimized Voss WORKING_PROJECT save surface. Known inert cleanup branches from an earlier tool-selection mistake remain recorded in the checkpoint; do not create more.