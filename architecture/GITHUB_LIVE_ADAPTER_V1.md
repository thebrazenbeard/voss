# GitHub Live Evidence Adapter V1

Status: REAL-PROJECT GENERALIZATION / READ-ONLY ADAPTER

## Purpose

Voss needs to audit mutable GitHub state without confusing a branch name with an immutable subject.

The live adapter therefore binds every file observation to an exact commit SHA and blob SHA.

## Read protocol

For a file requested through mutable ref R:

1. read R and record exact head A;
2. request the file at exact commit A, not through mutable R;
3. record exact Git blob SHA;
4. reread R and record head B;
5. if A == B, the evidence may support a current-ref claim at that read frontier;
6. if A != B, the bytes remain valid evidence for A but are marked stale for current-ref claims.

This closes a race where a branch moves between the head read and file read.

## Comparison protocol

Comparisons use exact commit SHAs rather than two mutable branch names.

The resulting relation is evidence of those exact commits only.

## Mutation boundary

This adapter is read-only.

It does not create branches, update files, merge, deploy, or infer authority from credentials.

Mutation primitives remain separately governed.

## Authentication

Public repositories can be read without a token.

Private repositories require an externally supplied GitHub token. Token possession is transport capability, not project authority.

## Evidence typing

Exact repository source:
- origin: PRIMARY_SOURCE
- fidelity: EXACT_UTF8_SPAN
- immutable binding: Git blob SHA

Mutable branch currentness:
- obtained from direct ref read
- remains current only to the verified read frontier

A branch movement after the bound file read does not invalidate the historical exact bytes. It invalidates using those bytes as evidence of the mutable branch's current state.
