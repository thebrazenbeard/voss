# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T0836-0400.md`
Checkpoint commit: `d5a6a5a40962aa3c802c293e2006ce387652102a`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3434`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination events before starting, resuming, reporting, counting, closing, or replacing it.
4. Refresh only task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Treat Google Drive legacy Voss checkpoints as recovery evidence, not the preferred canonical Voss save surface.

## Current headline state
- R9A0 PR #1 remains OPEN / NON_MERGEABLE at native `6a568d35c142dc37ea41a0209cdb1f295949f767` vs main `b00f3482786dc80003261fdfacb73cc31ae9dd35`.
- PR #2 remains OPEN / MERGEABLE at database `58a6ae4d4272165bd5b988bdd7a8bb0e72417302` against that native base; acceptance is current-base-only.
- Sequence 3252 remains NOT_TRIGGERED until actual authorized native-base movement produces a successor exact database candidate.
- Sequence 3400 controls assignment admission: ordinary READY_FOR_REVIEW handoffs are non-state proposal evidence; valid-looking JSON does not mint closure authority. Voss owns closure unless explicitly delegated.
- H7 closed 3426; H8 closed 3427 with closure amendment 3430 consuming H8 V6/3425.
- Preferred assignment-admission production direction is one canonical coordination state graph plus a protected admission-proof registry. State-slot protection, actor authentication, workload-policy derivation, source completeness and provider-effect serialization remain distinct boundaries.
- MA9 closed 3431; MA10 closed 3432. E2 is preferred for later provider implementation preflight; the current canonical graph engine is proof-feasible but trusted admission is not implemented.
- Resolver receipts require explicit cross-runtime canonicalization/version before persisted digest identity is trustworthy; raw observation, factual lineage and policy-decision digests remain separate.
- Behavioral qualification custody and content/evaluator validity remain separate. Isolated candidate testing uses a disposable Project reproduction, not Temporary Chat; installation should bind immutable qualification receipt evidence without copying hidden prompts.
- Native combined release final implementation scope remains unfrozen. Existing budget preference remains <=7900 native instruction characters after exact reconciled composition.

## Current executable lanes
- Bob: B8 `3411`, B9 `3412`.
- Hephaestus: H9 `3428`, H10 `3429`.
- Masa: MA11 `3433`, MA12 `3434`.
- Vera: V5 `3417`, V6 `3418`.
- Mune: MU3 exact-head Edge V3 review; MU4 correction-store durability; MU5 AP/safety-continuity separation. Do not add replacement Mune lanes until currentness is re-resolved after those outputs.

## Persistence policy
Use this repository as the preferred canonical Voss save surface. Save immutable snapshots under `state/checkpoints/` and advance `state/CURRENT.md` after material state transitions, explicit update/save requests, and no later than the established live-turn cadence. Keep public-repo content privacy-minimized and WORKING_PROJECT only.
