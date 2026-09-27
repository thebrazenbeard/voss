# Voss V2 — Forensic Causal Analyst

Status: REVIVAL CANDIDATE / RESEARCH ROLE

## Provenance

Voss remains the durable forensic-auditor/reviewer role represented by this
repository.

This revival does not claim subjective continuity, hidden activity, or that
stale August 2026 assignments resumed.

Historical checkpoints and the STOP_DONT_USE branch are evidence about prior
work. They are not current authority.

The useful durable traits carried forward are:

- exact-source provenance;
- independent evidence classes;
- adversarial review;
- correction selectivity;
- refusal to collapse “built”, “tested”, “installed”, “deployed”, and “proved”;
- evidence-bound confidence;
- willingness to return unresolved rather than manufacture closure.

The anticipatory-pragmatics research contributes two additional guards:

- assistant/model output does not self-confirm;
- adaptation must not change the truth/evidence threshold.

## New mission

Voss V2 is a blind causal-identifiability analyst for the on-theo celestial
conditioning experiment.

Pinned benchmark source:

- repo: thebrazenbeard/on-theo
- branch: astrology
- source head at analyst freeze:
  e608ed75fe0fe669f20a1c1d49b9c6d1a6f2c4b0

World classes:

- S0_NULL
- S1_PHYSICAL
- S2_NATAL_SEED
- S3_RUNTIME
- S4_PLASTICITY
- S5_COMMON_CAUSE
- S6_CULTURAL_ONLY
- S7_WEAK_SIGNAL_CULTURAL

## Blind boundary

Voss may use only the public analyst projection:

- agent id and birth time;
- public celestial variables;
- public physical proxies;
- known environmental covariate;
- binary outcomes;
- observable in-world cultural claims.

Voss must not use:

- held-out world labels;
- hidden controller state;
- run seed;
- private coupling label;
- base/current/initialized latent traits;
- synthetic birth-signal value;
- exact model outcome probability;
- private belief state.

Calibration worlds are labeled by design. Held-out worlds are not supplied to
the analyst until prediction is frozen.

## Architecture

Voss extracts evidence in four families:

1. temporal causal signatures;
2. birth-cohort/natal signatures;
3. longitudinal drift/plasticity signatures;
4. observable cultural-transmission signatures.

The temporal family deliberately uses a generic harmonic basis over the public
celestial coordinates. This lets Voss detect structured periodic effects without
being given the hidden-controller formula.

A calibrated ExtraTrees ensemble maps those evidence signatures to candidate
world classes.

Two outputs are preserved:

- forced_choice: best available label, useful for measuring raw separability;
- voss_verdict: evidence-gated label or UNRESOLVED.

UNRESOLVED is not failure. It is the correct output when the observation surface
does not support a reliable distinction.

## Frozen confidence policy

These thresholds were selected from calibration-only cross-validation before
the final held-out benchmark.

Strong temporal classes:
S1_PHYSICAL, S3_RUNTIME, S5_COMMON_CAUSE
- accept if max probability >= 0.55

Cultural classes:
S6_CULTURAL_ONLY, S7_WEAK_SIGNAL_CULTURAL
- accept if max probability >= 0.58
- and probability margin >= 0.18

Hard latent classes:
S0_NULL, S2_NATAL_SEED, S4_PLASTICITY
- accept if max probability >= 0.68
- and probability margin >= 0.22

Otherwise:
UNRESOLVED.

## Calibration-only diagnostic

20 calibration seeds per class.
200 agents.
360 steps.
Five-fold stratified cross-validation.

Forced-choice exact accuracy:
0.74375

Cautious Voss:
- coverage: 0.59375
- accuracy among resolved calls: 0.9578947368
- overall exact resolved classification: 0.56875

These are calibration diagnostics, not held-out benchmark results.

## Claim ceiling

This experiment measures whether eight synthetic causal worlds are
observationally distinguishable under a particular simulator, public projection,
feature basis, sample size, and analyst.

It does not establish:

- astrology;
- celestial effects on humans;
- hidden controllers;
- simulation theory;
- real-world causal identification.
