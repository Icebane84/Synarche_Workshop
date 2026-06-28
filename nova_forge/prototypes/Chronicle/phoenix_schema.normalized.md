# Phoenix Schema Normalized Spec

This normalization separates the Phoenix Schema into two layers:

- Poetic layer: philosophical ethos and grouped domains.
- Executable contract: machine-checkable law records with required fields, severity, tests, owners, dependencies, and validation criteria.

## Conflict Resolution

- Version conflict fixed by making `v16.0` the canonical executable version.
- The former `v14.0` value is retained as `legacy_version`.
- Status conflict fixed by separating two dimensions:
  - `lifecycle_state: ACTIVE`
  - `canonization_state: CANONIZED`

## Review Adjustments

The review was incorporated with a distinction between canonical laws and implementation controls.

Accepted changes:

- `LAW-003` is now `MUST` because a consensus gate cannot be optional if downstream promotion controls depend on it.
- `LAW-031` is now `MUST` because distributed merge semantics protect mandatory graph and chronicle integrity guarantees.
- `LAW-022` now defines AI signature custody as a `SENTINEL` service-account Ed25519 key registered in `AUTHORIZED_PUBLIC_KEYS`.
- `LAW-023` was renamed from `Dijkstra Garbage Collection` to `SFR Threshold Pruning` because the described behavior is threshold pruning, not shortest-path search.
- GUCA command dependencies are now version-pinned with semver dependency strings.
- `LAW-042` now names the required fork/local metadata explicitly: `artifact_id`, `schema_version`, and `policy_refs`.

Qualified changes:

- `LAW-013` remains `MUST`, but the contract now distinguishes networked mTLS from a documented local-workstation Ed25519 exception.
- `LAW-032` and `LAW-038` remain conditional deployment controls. Kubernetes/GitOps requirements are not marked compliant on a local workstation unless the deployment profile enables them.
- The six missing areas from the review are not added as `LAW-043+`. They are modeled as `control_extensions` so the Phoenix 42-law canon remains stable while security and operational gaps still become enforceable.

## Deduplicated Domains

The 42 laws are grouped into six operational domains:

- `identity-and-traceability`: identity, graph linkage, tombstones, relational integrity, chronicle, fractal governance.
- `resilience-and-remediation`: fault tolerance, preemption, fuzzing, rollback, DLQ, CRDT convergence.
- `grounded-intelligence`: consensus, RAG grounding, confidence, controlled novelty, predictive caching, decision reward.
- `policy-and-access`: schema validation, zero trust, OPA, canonization, RBAC.
- `evolution-and-operations`: refactoring, CQRS, hooks, executable docs, gardening, scaling, GitOps, streaming.
- `experience-and-modularity`: gamification, language, visualization, persona, feedback, bounded contexts, data-driven UI.

## Implementation Tracking

The normalized JSON now includes:

- `implementation_context`: records the current deployment target and server review context.
- `policy_exceptions`: records explicit, scoped exceptions such as Ed25519 local identity in place of mTLS.
- `implementation_gaps`: records known non-compliance against the target contract.
- `control_extensions`: records enforceable non-canonical controls such as key rotation and SELT audit integrity.

## Deliverables

- `phoenix_schema.normalized.json`: the normalized machine-enforceable contract.
- `phoenix_schema.contract.schema.json`: JSON Schema for validating the contract shape.
- `chronicle_integrity.rego`: primary LAW-035 policy already generated for the Immutable Chronicle.

## Suggested Validation

Use a JSON Schema validator against:

```text
phoenix_schema.normalized.json
phoenix_schema.contract.schema.json
```

The contract is intentionally strict: each law must include `id`, `intent`, `principle`, `enforcement`, `severity`, `test`, `owner`, `dependencies`, and `validation_criteria`.

## GCDB Evolution

The next governance layer is now represented by:

- `phoenix_gcdb.registry.json`: first-class policy, control, exception, finding, verification, evidence, risk, metric, and relationship objects.
- `phoenix_gcdb.schema.json`: JSON Schema for the GCDB registry.
- `phoenix_gcdb.md`: concise explanation of the registry model and status derivation.

In the GCDB layer, `implementation_gaps` are promoted to `compliance_findings`, tests are separated into `VERIFICATION` objects, and policy status is derived from findings and exceptions rather than manually assigned.
