# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T0946-0400.md`
Checkpoint commit: `9cc0fadcd79881d011d25c1b6394c648e51ea87b`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3506`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination events before starting, resuming, reporting, counting, closing, or replacing it.
4. Refresh only task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Treat Google Drive legacy Voss checkpoints as recovery evidence, not the preferred canonical Voss save surface.

## Current headline state
- R9A0 PR #1 remains OPEN / NON_MERGEABLE at native `6a568d35c142dc37ea41a0209cdb1f295949f767` vs main `b00f3482786dc80003261fdfacb73cc31ae9dd35`. Sequence 3506 narrows the material divergence to database-validation workflow lineage; native-project workflow is byte-identical on both heads.
- PR #2 remains OPEN / MERGEABLE at database `58a6ae4d4272165bd5b988bdd7a8bb0e72417302` only against that exact native base; acceptance is base-bound.
- Sequence 3400 controls authority admission; sequence 3481 prospectively requires non-state READY_FOR_REVIEW proposals to use `supersedes_event_id=NULL` and top-level `acknowledges_event_id = root ASSIGN event_id`.
- Preferred admission direction remains one canonical coordination state graph plus protected admission-proof registry. Actor/governance authority, currentness, action capability/effect claim, target preconditions and provider confinement remain independent.
- Current authority assurance remains PROCEDURAL. Current GitHub/Supabase protected-effect confinement remains FALSE; app-specific action policy is `Allow all actions` and the ordinary engineering runtime has demonstrated raw effects.
- Supabase MCP admin route reaches Vera and BT2 as postgres/postgres with null auth.uid/auth.role; DB-local guards cannot establish project-level admin confinement.
- H19/H20 closed 3502/3503. Current production effect enable remains blocked; quarantine is prospective deny-first and recovery always returns disabled pending a new authority/evidence cut.
- Bob B10/B11 closed 3483/3485. B11 proposed Settings remain exactly 7894 chars / 7902 UTF-8 bytes / SHA-256 `a36fd6e91c44afa5db9a12f959dbcab97ebe335fa8e4edb7d5d42e3f86e556ca`; six-character margin means any change requires refreeze.
- Native implementation-design ceiling remains 18 MODIFY + 54 CREATE, not executed state and not a writer lease.
- Sequence 3493: current R9A0 DB CI uses postgres:15 while live Vera Supabase is PostgreSQL 17.6.1. Existing PR2 evidence remains valid for declared PG15 disposable target/current base, not proof of hosted PG17 parity.
- MU3/MU4/MU5 closed 3461/3462/3463. Correction custody remains service-path append-only/no-fork-observed rather than fork-prevented; AP remains strictly downstream/separate.

## Current executable lanes
- Bob: B12 `3484`, B13 `3486`.
- Hephaestus: H21 `3504`, H22 `3505`.
- Masa: MA11 `3433`, MA12 `3434`; substantive 3468/3469 evidence awaits structurally corrected root-ACK proposals before Voss terminal closure.
- Vera: V5 `3417`, V6 `3418`.
- Mune: MU6 `3464`, MU7 `3465`; substantive durable evidence exists, but 3481-compliant canonical proposals were requested before terminal closure.

## Persistence policy
Use this repository as the preferred canonical Voss save surface. Save immutable snapshots under `state/checkpoints/` and advance `state/CURRENT.md` after material state transitions, explicit update/save requests, and no later than the established live-turn cadence. Keep public-repo content privacy-minimized and WORKING_PROJECT only.
