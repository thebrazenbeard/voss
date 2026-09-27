# Voss Project Adapter Contract V1

Status: REVIVAL CANDIDATE

## Purpose

Voss core rules are project-independent.

A project adapter supplies the project-specific vocabulary, source locations,
frontiers, evidence acquisition, and claims needed for an audit.

This prevents each project from silently redefining what counts as proof.

## Required adapter responsibilities

An adapter must be able to provide a project snapshot containing:

- stable project identifier;
- exact source frontier;
- mutable/current frontier when applicable;
- current assignment/authority scope when relevant;
- known conflicts or unavailable sources.

The adapter should then normalize project evidence into Voss evidence classes.

## Evidence acquisition

An adapter may retrieve from:

- Git repositories;
- database/provider readbacks;
- CI systems;
- files and manifests;
- issue/PR systems;
- experiment datasets;
- logs;
- approved communication/state systems;
- other exact project sources.

An adapter must preserve the source's provenance and cannot silently strengthen its
meaning.

## Claims

Project claims should be atomic enough that a verdict has a clear meaning.

Bad:
“Release is good.”

Better:
- exact source head matches candidate;
- required test suite passes exact head;
- deployment receipt exists;
- runtime reports candidate version;
- protected effect was independently observed.

Each claim can then require the evidence types appropriate to that proposition.

## Currentness

For mutable project state, the adapter must distinguish:

- retrieval time;
- event time;
- record time;
- effective/current state when known.

An old exact source can remain valid historical evidence while being invalid evidence
of current state.

## Authority

Adapters may report current assignment or authority evidence.

Adapters may not manufacture authority from:

- role name;
- branch ownership;
- history;
- capability;
- review status;
- prior assignment.

## Failure behavior

If a required source is inaccessible, contradictory, or cannot be bound to the claimed
subject, the adapter must return bounded unavailable/conflict evidence rather than
invent a substitute.

## Self-review boundary

When Voss authored a project change, an adapter must mark that provenance.

A later Voss session can inspect it, but the result cannot be described as independent
review unless an actually independent reviewer/evidence path exists.

## Base Python interface

The candidate interface lives in:

`voss_core/adapter.py`

Project adapters may extend it without changing the core evidence/verdict semantics.
