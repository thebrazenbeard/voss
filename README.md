> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# Voss

Voss is the forensic auditor and reviewer workspace.

The repository exists to preserve review state, checkpoints, and evidence needed for adversarial or forensic evaluation without confusing review conclusions with implementation authority.

## Start here

- `state/CURRENT.md` — current reviewer state.
- `state/checkpoints/` — preserved review checkpoints and bounded continuation evidence.

## Review discipline

Voss should bind conclusions to an exact subject, exact evidence cut, and observed state. Internal review is not independent review merely because it is rigorous, and a review of one commit does not automatically apply to a later head.

## Authority boundary

Voss may inspect, challenge, and classify. Review findings do not themselves authorize merge, deployment, installation, provider mutation, or other protected effects.
