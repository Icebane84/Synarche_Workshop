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

## Deduplicated Domains

The 42 laws are grouped into six operational domains:

- `identity-and-traceability`: identity, graph linkage, tombstones, relational integrity, chronicle, fractal governance.
- `resilience-and-remediation`: fault tolerance, preemption, fuzzing, rollback, DLQ, CRDT convergence.
- `grounded-intelligence`: consensus, RAG grounding, confidence, controlled novelty, predictive caching, decision reward.
- `policy-and-access`: schema validation, zero trust, OPA, canonization, RBAC.
- `evolution-and-operations`: refactoring, CQRS, hooks, executable docs, gardening, scaling, GitOps, streaming.
- `experience-and-modularity`: gamification, language, visualization, persona, feedback, bounded contexts, data-driven UI.

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
