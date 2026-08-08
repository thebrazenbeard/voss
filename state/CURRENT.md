# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T0810-0400.md`
Checkpoint commit: `029cc65ec673709882368e3b1e8c0722d9213ea8`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3418`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination events before starting, resuming, reporting, or counting it.
4. Refresh only task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Treat Google Drive legacy Voss checkpoints as recovery evidence, not the preferred canonical Voss save surface.

## Current headline state
- R9A0 PR #1 remains OPEN / NON_MERGEABLE at native `6a568d35c142dc37ea41a0209cdb1f295949f767` vs main `b00f3482786dc80003261fdfacb73cc31ae9dd35`.
- PR #2 remains OPEN / MERGEABLE at database `58a6ae4d4272165bd5b988bdd7a8bb0e72417302` against that native base; acceptance is current-base-only.
- Sequence 3252 remains NOT_TRIGGERED until actual authorized native-base movement produces a successor exact database candidate.
- Sequence 3400 controls assignment admission: ordinary READY_FOR_REVIEW handoffs are non-state evidence/proposals; valid-looking JSON does not mint closure authority. Voss owns closure unless explicitly delegated.
- Safety semantic/provenance design is frozen; correction-storage custody remains unfrozen pending MU4.
- Knowledge Resolver V1 has a coherent design but is not implemented. Trusted admission, workload-policy derivation, source completeness and provider-effect serialization remain distinct boundaries.
- Native combined release budget is feasible only by refactoring; preferred candidate ceiling <=7900 chars. Emerging existing-file scope is 18 MODIFY after Retrieval + Recovery/Cold Start/Post-Install/Installation Receipt corrections; final implementation scope is not frozen.

## Current executable lanes
- Bob: B8 `3411`, B9 `3412`.
- Hephaestus: H7 `3413`, H8 `3414`.
- Masa: MA9 `3415`, MA10 `3416`.
- Vera: V5 `3417`, V6 `3418`.
- Mune: MU3 exact-head Edge V3 review; MU4 correction-store durability; MU5 AP/safety-continuity separation. Do not add replacements until currentness is re-resolved after those outputs.

## Persistence policy
Use this repository as the preferred canonical Voss save surface. Save immutable snapshots under `state/checkpoints/` and advance `state/CURRENT.md` after material state transitions, explicit update/save requests, and no later than the established 10-turn live-turn cadence. Keep public-repo content privacy-minimized and WORKING_PROJECT only.
