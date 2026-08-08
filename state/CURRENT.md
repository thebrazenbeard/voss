# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T1259-0400.md`
Checkpoint commit: `8948489cc491d46212c05428f98ddd1b7e2c8879`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3570`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination events before starting, resuming, reporting, counting, closing, or replacing it.
4. Refresh only task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Treat Google Drive legacy Voss checkpoints as recovery evidence, not the preferred canonical Voss save surface.

## Current headline state
- R9A0 remains under construction and is not installed. Canonical 3518 authorizes bounded ordinary repository implementation but not merge, deployment, hosted production DB apply, credentials/permissions, paid services, deletion or installation.
- Implementation branch `feature/r9a0-combined-native-implementation-v1` was freshly verified identical to `ddcd98b4e61df09f06886f2073ecbdfad21c8f12` before B15 resumed. Frozen B11 Settings remain 7894 chars / 7902 UTF-8 bytes / SHA-256 `a36fd6e91c44afa5db9a12f959dbcab97ebe335fa8e4edb7d5d42e3f86e556ca`.
- PostgreSQL server truth is `17.6` / `170006`. Corrected B12/B13 exact artifacts are independently verified and admitted; provider `database.version 17.6.1.147` is a separate provider-build datum, not server_version.
- H25 closed APPROVED at 3566. B15 is CURRENT and repository writes RESUMED at 3567 under Bob's sole-writer lease. H26 closed APPROVED at 3568 with the exact pre-zip BUILT_AND_VALIDATED gate.
- B15 now admits exactly one workflow semantic addition: add the combined implementation branch to native workflow `push.branches`; proposed workflow SHA-256 `66dfcfbab459528bb9cb4898ca60328825285bf9bacc3422364d957a182411d3`. Remaining ceiling from current head is 18 MODIFY +54 CREATE =72 paths. Settings, Package and Voice remain no-touch.
- Final B15 evidence order: freeze Validation Report -> generate checksums -> deterministic local validation -> exact pushed-head CI -> post-evidence candidate rehash/readback. Current candidate is not yet BUILT_AND_VALIDATED.
- Authority assurance remains PROCEDURAL. Protected-effect confinement remains unproven/false; hosted provider-faithful PG17 parity remains NOT_PROVEN. These do not block authorized ordinary repo implementation.

## Current executable lanes
- Bob: B15 current state head `3567` (`47a61211-d7de-44a9-a655-e8ef971a6582`), sole writer, writes resumed.
- Hephaestus: H25 complete `3566`; H26 complete `3568`; continuing read-only peer challenge support for Masa.
- Masa: MA13 root `3545`, MA14 root `3546`; peer challenges `3569` and `3570` must be reconciled before final proposals.
- Mune: MU6 controlling amendment `3547`, MU7 controlling amendment `3548`; final 3481-compliant R9A0 proposals still required. Do not conflate separate `bug_ops` work with these lanes.
- Vera: V5 controlling amendment `3549`, V6 controlling amendment `3550`; final 3481-compliant proposals still required. Current 3566-3568 evidence update sent on Slack.

## Corrected B12/B13 exact hashes
- Contract `7cc34d03438a84e924be9ce01518c947ddf925b43ffe91e1a1e607df1a93fdd9`
- schema `093b0ff4b953e721d1e1ba72ac43659d4a1fd7d6d2bcf3cfccba55c3a8901817`
- validator `f3dc2d6fdf6da60fd18ce35138b4a098897d293abeeedd510ce8c28a4abd4908`
- B13 manifest `0c9c675dd80759ff6fa1973392e94f19cd6acc95ba70537cad920674e823b56e`
- B13 bundle `7b7f8c3ea120c080b88fffa150ff64096ccc6f96209efa1c3231d959f44eaa64`, 55 files / 65468 exact file bytes

## Current peer-review corrections
MA13 must split DB-login-origin proof, actual PostgREST HTTP-path proof and transport exclusivity. `session_user` proves database login origin across SET ROLE but not HTTP traversal/exclusivity; connector identity comes from pinned sidecar/config. Claims JSON is not an authority factor.

MA14 must use one canonical normalized request byte string after duplicate-aware raw-wire validation, bind its digest/version into the one-use capability, and derive authoritative DB transition fields from the same bytes inside one atomic transaction. Correctness must not depend on pooled-session continuity or prior GUC/temp/SET state.

## Priority
1. Bob B15 final candidate build, exact-head CI and immutable review.
2. Vera V5/V6 and Mune MU6/MU7 structurally correct final handoffs/closures when they arrive.
3. Masa MA13/MA14 reconciliation and final handoffs.
4. Once H26 gate is actually satisfied, notify Patrick that the native Project file set + final Project instructions are BUILT_AND_VALIDATED and ready for the single-ZIP step.

## Coordination policy
Sequence 3400 controls authority admission. Sequence 3481 prospectively requires non-state READY_FOR_REVIEW proposals to use `supersedes_event_id=NULL` and top-level `acknowledges_event_id = root ASSIGN event_id`; authority-admitted amendments/closures form the controlling state lineage. B15 future closure must supersede current state event `47a61211-d7de-44a9-a655-e8ef971a6582` and ACK the exact accepted final Bob proposal.

## Persistence policy
Use this repository as the preferred canonical Voss save surface. Save immutable snapshots under `state/checkpoints/` and advance `state/CURRENT.md` after material state transitions, explicit update/save requests, and no later than the established live-turn cadence. Keep public-repo content privacy-minimized and WORKING_PROJECT only.
