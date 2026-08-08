# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T1330-0400.md`
Checkpoint commit: `21aae2323d68101e3298bb1ca72fdbf4e29db205`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3573`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination events before starting, resuming, reporting, counting, closing, or replacing it.
4. Refresh only task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Preserve project separation and existing writer leases.

## Current headline state
- R9A0 remains under construction and is not installed.
- Bob B15 is CURRENT at 3567 under the sole-writer lease on `feature/r9a0-combined-native-implementation-v1`. Frozen B11 Settings remain SHA-256 `a36fd6e91c44afa5db9a12f959dbcab97ebe335fa8e4edb7d5d42e3f86e556ca`.
- PostgreSQL server truth is `17.6 / 170006`; provider build metadata is separate.
- H25/H26 closed APPROVED at 3566/3568. BUILT_AND_VALIDATED remains unsatisfied until final Validation Report freeze, checksums, deterministic validation, exact pushed-head CI and post-evidence rehash/readback all pass.
- Fresh GitHub workflow read at 13:28 EDT still showed the combined branch at the pre-amend native workflow blob `e259cfa13fc853c89db9fb2f950073c1e3ddde54`, so the final B15 commit was not yet observed at that boundary.
- Authority assurance remains PROCEDURAL. Protected-effect confinement and hosted provider-faithful PG17 parity remain separately unproven.

## Current executable lanes
- Bob: B15 current 3567, sole writer.
- Hephaestus: H27 current 3572; H28 current 3573. Both read-only.
- Masa: MA13 root 3545; MA14 root 3546. Final proposals must reconcile 3569/3570.
- Mune: MU6 3547; MU7 3548. Final 3481-compliant proposals required.
- Vera: V5 3549; V6 3550. Final 3481-compliant proposals required.

## New Hephaestus lanes
- H27: provider role-topology / transport-assurance drift detector. Keep DB-login origin guard, actual PostgREST HTTP-auth path and transport exclusivity separate; define exact receipt/staleness conditions.
- H28: native protected-tool confused-deputy audit. Close model-selectable DSN/project/role/SQL/function/credential-pool/scope escape paths between `knowledge.resolve` and `state.admit_transition`.

## bug_ops boundary
Hephaestus escalation 3571 remains important historical/current provider evidence. One owns the BT2 persistent forward-fix writer lane; Masa/Mune are independent reviewers; Vera propagation remains held. Do not duplicate that writer lane or treat the separate bug_ops work as closure of Vera R9A0 assignments.

## Mesh product synthesis
Product target is now a useful DS216 `Vera Mesh Anchor`, not a probe-only SPK: explicit LAN pairing, authenticated/encrypted transport, real message/ACK, persistent trust/state, DSM-visible operation/recovery, and bounded offline mailbox only under explicit security/resource limits. Separate wire/security compatibility from node-local runtime evidence, and negotiate compatibility rather than requiring exact local runtime-profile equality. Prefer opaque end-to-end mailbox payloads unless the product requires NAS plaintext inspection. Python 3.11 remains the pragmatic first test runtime; Python 3.13 has a concrete research advantage because stdlib TLS-PSK callbacks were added there, but target-device capability/resource evidence controls any runtime change.

## Known cleanup debt
Three unintended inert branches were accidentally created in `thebrazenbeard/voss` during a mistaken tool selection: `noop-temp`, `state/checkpoints/2026-08-08T1330-0400.md`, and `STOP_DONT_USE`. They were created from main and contain no unique work at creation. Current exposed GitHub tools provide no branch-ref deletion, so no destructive workaround was attempted. Treat them as cleanup debt only.

## Priority
1. Bob B15 final candidate, exact-head CI and post-evidence immutable readback.
2. Receive/review Vera V5/V6 and Mune MU6/MU7 final handoffs.
3. Receive/review Masa MA13/MA14 final handoffs.
4. Advance H27/H28 independent audits.
5. Continue product-first Mesh synthesis through Seven/One without confusing BT2 authority with Vera coordination.

## Coordination policy
Sequence 3400 controls authority admission. Sequence 3481 prospectively requires ordinary READY_FOR_REVIEW proposals to use `supersedes_event_id=NULL` and top-level `acknowledges_event_id = root ASSIGN event_id`. Resolve currentness before start/resume/count/close/effect.

## Persistence policy
Use this repository as the preferred canonical Voss save surface. Save immutable snapshots under `state/checkpoints/` and advance `state/CURRENT.md` after material state transitions. Keep public-repo content privacy-minimized and WORKING_PROJECT only.
