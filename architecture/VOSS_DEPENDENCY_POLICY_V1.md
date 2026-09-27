# Voss Dependency Policy V1

Status: PORTFOLIO-SYNTHESIZED / CORE INVARIANT

## Rule

Voss may borrow architecture from the wider portfolio without becoming dependent on the
portfolio for ordinary forensic reasoning.

## Why

The portfolio contains excellent specialized systems for orchestration, communication,
provenance, recovery, reasoning, chronology, semantic state, training, and project
control.

Making all of them a mandatory shared spine would create:

- correlated failure;
- circular evidence;
- blast-radius expansion;
- reviewer independence loss;
- bootstrapping deadlocks;
- difficulty auditing the auditor.

## Dependency classes

### CORE

Lives in Voss and must be sufficient for a manual evidence-backed case:

- case envelope;
- evidence ontology;
- claim/rival model;
- operator semantics;
- findings;
- influence firewall;
- effect/currentness semantics;
- result receipt.

### OPTIONAL_ADAPTER

May improve evidence acquisition or execution:

- repository/provider readers;
- provenance systems;
- reasoning engines;
- chronology services;
- communication buses;
- orchestration systems;
- recovery systems;
- semantic stores.

Loss of an optional adapter may produce UNAVAILABLE/BLOCKED for that evidence route.
It must not make Voss forget what a claim or evidence record means.

### FIXTURE_SOURCE

A project used to test Voss against a real domain.

It never becomes part of Voss's authority.

### HISTORICAL_REFERENCE

May explain why an invariant exists.

It is not current control.

## Independence firewall

If Voss delegates analysis to another system, the returned result is evidence/input,
not an automatic verdict.

If several workers share model, prompt lineage, context, or prior outputs, Voss records
that correlation and does not count them as independent solely because there are
multiple messages.

## Public/private boundary

Voss is public.

Private portfolio material may inform public-safe abstractions, but private repository
payloads, exact private source maps, and confidential mechanisms must not be copied
into Voss without separate publication authority.
