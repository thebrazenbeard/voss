# Voss V2 Blind Astrology Benchmark — Held-Out Results

Status: HELD_OUT_COMPLETE / UNMERGED

Analyst frozen before held-out evaluation:

`d8660dc63e4813f37ed1722a2e867ee2c10b1a49`

Pinned on-theo source:

`e608ed75fe0fe669f20a1c1d49b9c6d1a6f2c4b0`

## Protocol

Calibration:
- 20 labeled seeds per world;
- 160 calibration runs total;
- 200 agents;
- 360 steps.

Held-out:
- 25 unseen seeds per world;
- 200 held-out runs total;
- seed families begin at 30000 and advance by 1000 per world;
- no held-out feature, model, threshold, or seed schedule was changed after the analyst commit was frozen.

## Forced-choice result

Exact:
156 / 200

Accuracy:
78.0%

Three world families separate strongly:

- S1_PHYSICAL: 25 / 25
- S3_RUNTIME: 25 / 25
- S5_COMMON_CAUSE: 25 / 25

The cultural pair is also mostly separable:

- S6_CULTURAL_ONLY: 24 / 25
- S7_WEAK_SIGNAL_CULTURAL: 23 / 25

The hard failure is the latent trio:

- S0_NULL: 8 / 25
- S2_NATAL_SEED: 15 / 25
- S4_PLASTICITY: 11 / 25

Within those 75 runs, forced-choice accuracy is only 34 / 75 = 45.33%.

That is above three-way chance, but not remotely strong enough to claim reliable
identifiability.

## Evidence-gated Voss result

Voss is allowed to return `UNRESOLVED`.

Resolved:
121 / 200

Coverage:
60.5%

Correct among resolved:
119 / 121

Resolved-call accuracy:
98.3471%

Overall exact resolved classification:
119 / 200 = 59.5%

Only two resolved calls were wrong:
- one S0_NULL run was called S2_NATAL_SEED;
- one S4_PLASTICITY run was called S2_NATAL_SEED.

## Per-world cautious behavior

S1_PHYSICAL:
25 correct, 0 unresolved.

S3_RUNTIME:
25 correct, 0 unresolved.

S5_COMMON_CAUSE:
25 correct, 0 unresolved.

S6_CULTURAL_ONLY:
20 correct, 5 unresolved.

S7_WEAK_SIGNAL_CULTURAL:
19 correct, 6 unresolved.

S2_NATAL_SEED:
5 correct, 20 unresolved.

S0_NULL:
0 correct, 1 incorrect S2 call, 24 unresolved.

S4_PLASTICITY:
0 correct, 1 incorrect S2 call, 24 unresolved.

## What the confusion matrix says

### S1 physical is identifiable

The public inverse-square/tidal/illumination feature family leaves a strong
aggregate temporal signature.

### S3 runtime is identifiable

The time-local angular/periodic signal is strong enough that Voss separates it
cleanly from ordinary physical mediation.

### S5 hidden common cause is identifiable in this simulator

The analyst was not given the hidden controller variable.

Its generic harmonic basis nevertheless discovers a strong public-state
signature. The most important learned feature is the correlation with the
generic harmonic `sin(p2 + 2*p4)`.

That matters because the simulator's hidden state is deterministically related
to public celestial coordinates. This result therefore shows recoverability of
a latent common-cause signature in this synthetic world; it does not imply that
real hidden causes are generally recoverable.

### S6 versus S7 is mostly identifiable

The presence of observable cultural claims identifies the cultural family.
The weak real signal in S7 supplies additional information, but the distinction
is not perfect.

### S0 versus S2 versus S4 is not reliably identifiable

This is the central negative result.

S2's birth-seed effect is detectable often enough to beat chance but not enough
for reliable classification.

S4's plasticity effect primarily changes a latent learning-rate/random-walk
process. Under 200 agents, 360 steps, binary outcomes, and the current public
projection, that effect is extremely difficult to distinguish from S0 null.

The correct conclusion is not “Voss needs to guess harder.”

The observation surface does not currently carry enough usable information for
a reliable S0/S2/S4 separation.

## Why this is scientifically useful

The experiment has now falsified an assumption embedded in the original design:
that all eight causal worlds would necessarily be identifiable from the same
public tables.

They are not.

That means future work should change the experiment rather than post-hoc tune
this held-out benchmark.

Candidate next tests:

1. longer longitudinal windows;
2. more agents;
3. repeated continuous outcomes rather than binary-only observations;
4. intervention or perturbation channels;
5. predeclared plasticity-sensitive observables;
6. a second fresh held-out benchmark after any redesign.

## Claim ceiling

These results apply only to the synthetic on-theo simulator and Voss V2
observation surface.

They are not evidence for astrology, celestial influence on real humans,
simulation theory, or a real hidden controller.
