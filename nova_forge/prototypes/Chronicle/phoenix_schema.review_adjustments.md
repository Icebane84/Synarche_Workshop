# Phoenix Schema Review Adjustment Log

## Adopted

- Escalated `LAW-003` from `SHOULD` to `MUST`.
  Reason: a probabilistic gate that can be bypassed undermines mandatory consensus and canonization controls.

- Escalated `LAW-031` from `SHOULD` to `MUST`.
  Reason: CRDT-style merge semantics are required if distributed graph and chronicle state are mandatory integrity structures.

- Kept `LAW-024` as `SHOULD`.
  Reason: the review is right that emergency process termination is too risky to make mandatory without very high-confidence detection.

- Reframed `LAW-013` as zero-trust mutual identity with a scoped local exception.
  Reason: Ed25519 request signatures are a real identity control, but they are not mTLS. The contract now says so directly.

- Rewrote `LAW-022` AI signature custody.
  Reason: an AI signature must be a concrete signer. The spec now defines it as a registered `SENTINEL` service-account Ed25519 key.

- Renamed `LAW-023` from `Dijkstra Garbage Collection` to `SFR Threshold Pruning`.
  Reason: the described behavior is not Dijkstra's shortest-path algorithm.

- Pinned GUCA command dependencies.
  Reason: cross-artifact commands need semver pins to avoid silent breakage.

- Added explicit `LAW-042` metadata requirements.
  Reason: fork/local blocks need `artifact_id`, `schema_version`, and `policy_refs` to remain governable in isolation.

## Tracked As Gaps

- `LAW-031`: timestamp/lexicographic last-writer-wins fork resolution is not CRDT-compliant.
- `LAW-004`: `FINALIZE_PROPOSAL` needs reverse edge creation.
- `LAW-013`: Ed25519 signatures are a local exception, not mTLS compliance.
- `LAW-017`: JSONL/snapshot storage does not satisfy PostgreSQL foreign key enforcement.
- `LAW-042`: `REGISTER_FORK` compiled blocks need fractal governance metadata.

## Added As Control Extensions

- `CTRL-001`: Key Rotation, `MUST`.
- `CTRL-002`: Voting Period Expiry, `SHOULD`.
- `CTRL-003`: Stake Concentration Limits, `SHOULD`.
- `CTRL-004`: DLQ Size Bounds, `SHOULD`.
- `CTRL-005`: Rate Limiting, `MAY`.
- `CTRL-006`: SELT Audit Log Integrity, `MUST`.

## Not Adopted As Canonical Laws

I did not add `LAW-043+` entries. The Phoenix Schema presents itself as a 42-law canon, so expanding that set casually would create a new versioning problem. The better path is a separate `control_extensions` section: enforceable, schema-validated, and allowed to evolve without rewriting the axiomatic layer.
