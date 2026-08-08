# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T1023-0400.md`
Checkpoint commit: `e18f427850c6c1063a79216de3682ba9557c16d6`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3546`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination events before starting, resuming, reporting, counting, closing, or replacing it.
4. Refresh only task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Treat Google Drive legacy Voss checkpoints as recovery evidence, not the preferred canonical Voss save surface.

## Current headline state
- R9A0 PR #1 remains OPEN / NON_MERGEABLE at native `6a568d35c142dc37ea41a0209cdb1f295949f767` vs main `b00f3482786dc80003261fdfacb73cc31ae9dd35`; PR #2 remains OPEN / MERGEABLE only into that exact native base at DB `58a6ae4d4272165bd5b988bdd7a8bb0e72417302`.
- Patrick directly authorized ordinary R9A0 repository implementation; canonical authority record 3518 permits non-destructive branch/file/commit/validation/PR-preparation work but does not authorize merge, deploy, hosted production DB apply, credentials/permissions, paid services, deletion or installation.
- Implementation branch `feature/r9a0-combined-native-implementation-v1` is based on `6a568d35...`. Phase 1 commit `ddcd98b4e61df09f06886f2073ecbdfad21c8f12` contains only the exact B11 Settings change. Frozen Settings remain 7894 chars / 7902 UTF-8 bytes / SHA-256 `a36fd6e91c44afa5db9a12f959dbcab97ebe335fa8e4edb7d5d42e3f86e556ca`.
- Controlling correction 3537: live Vera PostgreSQL is `server_version=17.6`, `server_version_num=170006`; 17.6.1-as-PostgreSQL-server-version is retracted. Existing DB CI remains postgres:15, so hosted PG17 parity is NOT_PROVEN.
- B12/B13 closed 3528/3529 for their non-version design, but their exact hashes are stale for implementation because their bytes/bindings encode the superseded 17.6.1 server-version claim. B15 amendment 3542 keeps the sole Bob writer lease CURRENT while pausing B12/B13-derived writes pending a surgical exact-hash rebind. Branch must remain at `ddcd98b4...` during the pause.
- B10 candidate footprint remains exactly 18 MODIFY + 54 CREATE; Package, Voice, workflow and `supabase/**` remain NO-TOUCH under B15.
- MA11/MA12 closed 3538/3539. H23/H24 remain closed with refinements admitted 3540/3541. Current authority assurance is PROCEDURAL and current GitHub/Supabase protected-effect confinement remains false.
- Native build-complete must mean the exact 16-file ChatGPT Project set plus final Project instructions are built on an immutable candidate head and deterministically validated/checksummed/read back. It is not merge, install, hosted DB apply, behavioral qualification or effect enable. Patrick intends the single-zip step after this milestone.

## Current executable lanes
- Bob: B15 root `3533`, controlling amendment `3542`; sole writer lease, paused for version-rebind artifact review.
- Hephaestus: H25 `3543`, H26 `3544`.
- Masa: MA13 `3545`, MA14 `3546`.
- Mune: MU6 `3464`, MU7 `3465`; final 3481-compliant root-ACK proposals requested before closure.
- Vera: V5 `3417`, V6 `3418`; final current-evidence root-ACK proposals requested.

## Coordination policy
Sequence 3400 controls authority admission. Sequence 3481 prospectively requires non-state READY_FOR_REVIEW proposals to use `supersedes_event_id=NULL` and top-level `acknowledges_event_id = root ASSIGN event_id`; authority-admitted amendments/closures form the controlling state lineage. Resolve currentness/source completeness before start, resume, report, workload count, authority use or external effect.

## Persistence policy
Use this repository as the preferred canonical Voss save surface. Save immutable snapshots under `state/checkpoints/` and advance `state/CURRENT.md` after material state transitions, explicit update/save requests, and no later than the established live-turn cadence. Keep public-repo content privacy-minimized and WORKING_PROJECT only.
