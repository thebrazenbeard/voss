> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# Voss — forensic evidence and review toolkit

Voss is an experimental, project-agnostic Python toolkit for evidence-bound audits. It helps applications describe claims, attach source evidence, keep unresolved findings unresolved, compare rival explanations, and avoid promoting source-code or review results into unproven real-world effects.

**Implemented today:** the `voss_core` Python package, a read-only `voss_adapters` GitHub adapter, structured case/receipt models, validation and reconciliation helpers, tests, and frozen research cases. **Not provided:** an autonomous auditor, authenticated authorization service, provider-identity binding, secure execution sandbox, or deployment/merge controller. A human or embedding host must supply trusted evidence, scope and effect authority, and evaluation decisions.

## Install and try the library

Requires Python **3.11 or newer**. From a checked-out copy of this repository, install in an isolated environment:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

This example is intentionally conservative: repository source can show that code exists; it does not prove that software is installed or active on another machine.

```python
from voss_core import (
    AuditEngine,
    Claim,
    Evidence,
    EvidenceClass,
    VerdictState,
    unresolved_by_default,
)

claim = Claim(
    id="example:deployment",
    proposition="The service is running on the target host",
    required_evidence_classes=(EvidenceClass.DIRECT_READBACK,),
)
source = Evidence(
    id="example:source",
    evidence_class=EvidenceClass.PRIMARY_SOURCE,
    source="repository/tree",
    proposition="The service's source code exists",
    supports=(claim.id,),
)

finding = AuditEngine(unresolved_by_default).run([claim], [source])[0]
assert finding.state is VerdictState.UNRESOLVED
print(finding.state.value)
```

`unresolved_by_default` is a baseline evaluator, not an AI verdict engine. An embedding application may pass its own evaluator; `AuditEngine.run` checks the returned finding's evidence references and declared evidence-class ceiling. It does **not** independently verify whether the evaluator's conclusion is true.

## Reusable components

| Component | What the source implements | Boundary |
| --- | --- | --- |
| `Claim`, `Evidence`, `Finding`, `AuditEngine` | Typed evidence classes, findings, and validation of referenced evidence; default unresolved evaluator | No automatic web research or fact verification |
| `CaseFile`, `EvidenceRecord`, `ClaimRecord` | Structured case-level evidence, subject, fidelity, and currentness distinctions | Caller-supplied records are not authenticated by their dataclass types |
| Provenance, time, currentness, and rival-hypothesis helpers | Deterministic structures for comparing candidate explanations and source timing | No guarantee of complete sources or ground-truth attribution |
| `ReviewBinding`, `mutation_gate`, `GitReadAdapter` | Exact Git-head/blob freshness checks and an injectable read adapter | A passing comparison is not an authenticated write permission |
| `GitHubRESTClient` in `voss_adapters.github_live` | Optional **read-only** REST branch/file/compare evidence, fetched at an exact commit and reread for ref movement | Requires network access and API permission; does not mutate GitHub |
| `AuthorityEvidence`, `effect_authorized` | A deterministic predicate over supplied authority records and exact target/operation/scope | Does **not** authenticate those records, bind them immutably to a host actor/provider, or issue real consent |
| Effect history and `reconcile_operation` | Validates a bounded operation-state transition and classifies ambiguous effect outcomes | Caller must supply independently verified effect presence, absence and authority |
| Influence, privacy and experiment helpers | Source-level policy checks and research-validation structures | No system-wide information-flow isolation, privacy clearance or execution control |

For precise interfaces start with [`voss_core/__init__.py`](voss_core/__init__.py), [`voss_core/engine.py`](voss_core/engine.py), and [`voss_adapters/github_live.py`](voss_adapters/github_live.py). The package metadata is in [`pyproject.toml`](pyproject.toml).

## Evidence and effect boundaries

- **Evidence classes stay distinct.** A schema-valid finding, source file, GitHub receipt, model review, and live host readback establish different facts. `validate_finding` can reject a `PASS` missing declared evidence classes, and runtime/effect states require supplied `DIRECT_READBACK` evidence; it does not authenticate the readback itself.
- **Exact subjects and currentness matter.** A review at an old commit does not automatically qualify a new head. Cross-subject comparisons do not transfer identity, provider bindings, consent, or permissions.
- **Authority is host-owned.** Any model-facing or locally constructed `AuthorityEvidence` is untrusted until the embedding host authenticates and immutably binds its actor, subject, provider, target, operation, scope, and revocation state. The predicate alone is **not** a coherent authorization service.
- **Ambiguous effects are not success.** After an interrupted write or uncertain response, authoritative readback and precondition checks must determine whether to adopt an existing effect, safely retry, stop, or leave the outcome unknown.
- **Private data stays private.** File paths, source extracts, review records and correlation metadata can expose confidential information. Callers must restrict sources and disclosure; a public repository does not authorize publishing private inputs.

The current implementation is a library and research artifact. Its tests do **not** constitute independent model evaluation, host installation verification, provider-attested authorization, or production security certification.

## Architecture and research material

The portable review interfaces and limitations are documented in:

- [System architecture](architecture/VOSS_SYSTEM_ARCHITECTURE_V2.md)
- [Evidence ontology](architecture/AUDIT_MODEL_V1.yaml)
- [Operator registry](architecture/VOSS_OPERATOR_REGISTRY_V1.yaml)
- [Influence firewall design](architecture/VOSS_INFLUENCE_FIREWALL_V1.md)
- [Adapter contract](architecture/PROJECT_ADAPTER_CONTRACT_V1.md)
- [Case-file JSON schema](schemas/VOSS_CASE_FILE_V1.schema.json)
- [Qualification protocol](qualification/VOSS_GENERAL_QUALIFICATION_V1.md)

The earlier blind causal-identifiability/astrology benchmark, historical case files, checkpoints, and project-specific source-cut reports remain **qualification and provenance artifacts**, not automatically current assignments or evidence of independently verified capability. Some research material originated within a wider portfolio that included private sources; this public repository does not grant permission to republish private identities, payloads, or source maps.

## Workspace safety and limits

The current tree has a source-level VS Code startup safety regression check. A concealed workspace `folderOpen` task and executable content disguised as a font asset were removed from current source; automatic workspace tasks are set to `"off"`. The tests cannot establish safety of earlier checkouts, user editor extensions, host processes, or uninspected startup paths. Do not execute historical removed payloads.

Contributions should preserve evidence provenance, exact artifact binding and fail-closed findings; review [CONTRIBUTING.md](CONTRIBUTING.md) and [CLA.md](CLA.md). For use or redistribution rights, consult the license documents above before relying on the public source.
