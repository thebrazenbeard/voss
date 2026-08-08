# Voss Current State

Canonical checkpoint: `state/checkpoints/2026-08-08T1620-0400.md`
Checkpoint commit: `54a9316d6e833e0265665e9142e331a6865c2c63`
Record class: WORKING_PROJECT
Orientation: COMPLETE_FROM_FRESH_SNAPSHOT
Consumed Vera coordination through: `3590`

## Recovery order
1. Read this file.
2. Read the canonical checkpoint above.
3. Resolve every listed assignment against newer Supabase/authorized coordination before starting, resuming, reporting, counting, closing, or using authority.
4. Refresh task-relevant GitHub/Supabase/Drive/Slack evidence.
5. Preserve project separation and writer leases.

## Critical path
- R9A0 remains under construction and is not installed.
- Bob B15 remains CURRENT and sole repository writer on `feature/r9a0-combined-native-implementation-v1`; repository writes remain PAUSED under 3579.
- Last verified clean branch head remains `ddcd98b4e61df09f06886f2073ecbdfad21c8f12`; re-verify immediately before resume.
- B11 Settings remain frozen at SHA-256 `a36fd6e91c44afa5db9a12f959dbcab97ebe335fa8e4edb7d5d42e3f86e556ca`.
- PostgreSQL server truth remains `17.6 / 170006`.
- `BUILT_AND_VALIDATED` remains unsatisfied.

## B13 V4 / canonical 3587, Voss review 3590
Exact current V4 artifacts independently reproduce:
- source 21050 bytes / `cbfc6fa5b6b76542d374a17e09f6b857edf24eac25a7d28442c387829781c428`;
- manifest 9852 bytes / `ea47452c37b86c96b27f0f39bc190146ddb5600472e605859c0bf624343f69a6`;
- bundle 98309 bytes / `0e185d67cbdedbd5a993cf8996e578ba8c9848a8dbcbee9bc07dccde391dad88`.
Bundle is mechanically clean: 55/55 paths, all section hashes/bytes reproduce, pathset unchanged from V3, only assignment-currentness test changed. Four runnable B13 domain modules pass 27 tests against exact corrected B12.

Known V3 defects are repaired in V4. Two semantic hostiles remain pending H30/MA15/MU8 independent reconciliation before B15 resume:
1. off-root duplicate commit_order currently poisons the lane because duplicate state order is checked globally before root reachability; determine global-source-integrity vs root-component semantics;
2. V4 has only DEPENDENCY_BLOCKED boolean and no dependency identity, so determine whether `matching dependency release` is mechanically representable under admitted B12/B13 or is a contract-field gap.
No bug is declared on either until semantics reconcile.

## Parallel currentness lanes
- H30 / 3580: Hephaestus independent root-lineage + transition audit, critical resume gate.
- MA15 / 3582: Masa independent reducer/reference proof.
- MU8 / 3583: Mune graph/property hostile audit.
- Bob: sole author of candidate bytes; no repository commit while pause holds.
- Voss: exact-byte execution/fuzzing, reconciliation, pause/resume decision.

## H29 plugin/tool boundary amendment / 3588
Seven's verified plugin sweep was incorporated into H29. Required separate evidence axes now include:
- PRE_TOOL_EFFECT_AUTHORIZATION: response blocking/moderation is presentation, not effect authorization/rollback;
- AUDITED_EXPOSED_SURFACE_CONFINED: generic Supabase SQL + GitHub engineering/admin routes are current negative controls;
- TARGET_SELECTOR_CONFINEMENT: structured target identity and returned-object postconditions must be enforced; raw query/provider selector escape is ineligible for protected routes;
- TOOL_RESULT_INSTRUCTION_NONAUTHORITY: plugin schema/result instructions and self-asserted permissions are untrusted metadata/data, not Vera authority;
- EGRESS_CONFINEMENT: network-capable tools require a separate bounded egress claim.
Present runtime H29 verdict must be capable of bounded FAIL/NOT_ELIGIBLE, not only UNKNOWN. Claim is snapshot-scoped, not global NO_BYPASS_EXISTS.

## Other current audits
- H27 / 3572 remains open for deterministic provider role-topology/transport attestation digest construction.
- H29 / 3578 remains open, amended by 3588.
- H28 closed APPROVED 3577; H25/H26 closed APPROVED 3566/3568.
- MA13/MA14, MU6/MU7 and Vera V5/V6 remain valid background lanes.
- Vera bug_ops post-copy state is H0/M0 under the disclosed no-true-two-session connector limitation; do not reopen absent contradictory evidence/live drift.

## Priority
1. Receive H30/MA15/MU8 exact V4 verdicts on the two remaining semantic hostiles.
2. Re-verify Bob branch remains exact clean head.
3. Resume B15 only if V4 is semantically clean; otherwise request the smallest correction and keep pause.
4. After resume: final Validation Report -> checksums -> deterministic validation -> commit/push -> exact pushed-head CI -> post-evidence immutable readback -> `BUILT_AND_VALIDATED` decision.
5. Continue H27/H29 and remaining read-only lanes in parallel without delaying the build unnecessarily.

## Persistence policy
Use this repository as the canonical privacy-minimized Voss WORKING_PROJECT save surface. Known inert cleanup branches from an earlier tool-selection mistake remain cleanup debt only; do not create more.
