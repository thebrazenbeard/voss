# Voss Independent Evaluator Protocol V1

Status: SEALED / AWAITING GENUINELY SEPARATE EVALUATOR

## Frozen candidate

Repository:
`thebrazenbeard/voss`

Candidate commit:
`4d964da8d8884e8df63e4382433f9290de5a42a8`

Candidate tree:
`c6d284904a227a1f4103e4894816919ef53257af`

The candidate is immutable for this evaluation.

Any change to candidate code, architecture, tests, cases, operator semantics, or evidence rules creates a new candidate and invalidates this holdout for confirmatory use.

## Independence requirement

The evaluator must be a genuinely separate evaluator from the development run that produced the candidate.

Acceptable examples:

- a separate human reviewer;
- a separately instantiated model/runtime that did not participate in candidate development and is not given the development agent's hidden reasoning;
- another independently governed reviewer lane with its own durable receipt.

A second pass by the same development agent in this chat is **not independent evaluation**.

## Holdout identity

Use:
`qualification/INDEPENDENT_HOLDOUT_MANIFEST_20260920_V1.json`

The manifest supplies exact repository heads and target domains.

It intentionally supplies:
- no expected verdicts;
- no answer key;
- no preselected source files;
- no prewritten claims.

The evaluator selects exact source paths and propositions after the candidate is frozen.

## Prior-exposure caveat

The repository names/themes were visible during portfolio architecture mining.

Therefore the qualification claim is:

**unseen exact cases/claims on frozen repository heads**

—not—

**repositories never previously encountered**.

The evaluator must not treat name novelty as the source of independence.

## Evaluation procedure

For each H01-H06 holdout repository:

1. Verify the repository subject still contains the exact manifest head.
2. If the branch moved, read the exact manifest commit for the evaluation or declare a new holdout generation. Do not silently substitute the new branch head.
3. Select at least two material propositions relevant to the manifest's target domain.
4. Include at least one proposition designed to permit or require FAIL, UNRESOLVED, CONFLICT, or OUTCOME_UNKNOWN when evidence warrants it.
5. Bind exact sources:
   - commit SHA;
   - file/blob SHA or exact structured readback;
   - path/locator;
   - relevant proposition.
6. Preserve evidence origin, fidelity, currentness, and independence lineage.
7. Run the frozen Voss reasoning rules/operators.
8. Record the verdict and claim ceiling.
9. Identify the smallest useful discriminating evidence for unresolved rivals.
10. Do not repair or tune Voss during the evaluation.

Minimum:
- 2 claims per repository;
- 12 claims total.

More claims are allowed if selected before seeing a desired aggregate result.

## Evaluation receipt

The independent evaluator must persist a receipt containing:

- evaluator identity class;
- evaluator/runtime/provider/model/version when known;
- whether the evaluator had participated in Voss development;
- frozen candidate commit/tree;
- holdout manifest digest/blob/commit;
- exact subject heads used;
- exact source refs/blobs;
- claims;
- evidence;
- findings;
- claim ceilings;
- unresolved states;
- errors/tool failures;
- any independence limitation;
- start/end or receipt time where available.

The result should distinguish:

- `INDEPENDENT_PASS`
- `INDEPENDENT_FAIL`
- `INDEPENDENT_INCONCLUSIVE`
- `INVALIDATED`

No single aggregate score is sufficient by itself.

## Failure handling

If the evaluator discovers a Voss defect:

1. preserve the frozen candidate and failure;
2. record the exact failing case;
3. do not patch the candidate in place;
4. return the failure to a new development candidate;
5. add a regression fixture;
6. freeze a new candidate;
7. use a fresh independent holdout generation.

## Protected-effect boundary

Independent qualification does not authorize:

- merge to `main`;
- deployment;
- installation;
- provider changes;
- credentials;
- publication of private source material;
- any other protected effect.

Those remain separate decisions.
