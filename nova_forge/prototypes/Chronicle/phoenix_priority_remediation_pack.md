# Phoenix Priority Remediation Pack

This pack operationalizes the seven priority fixes from the review.

## 1. LAW-031 CRDT Severity

Status: applied in `phoenix_schema.normalized.json` and `phoenix_gcdb.registry.json`.

Decision: `LAW-031` remains part of the 42-law canon and is now `MUST`.

Runtime requirement:

```text
Fork or graph merge functions must be commutative, associative, and idempotent.
Timestamp/lexicographic last-writer-wins is not compliant for distributed graph state.
```

Verification:

```text
Apply concurrent graph edits in multiple orders. The derived merged state must be identical.
Apply the same merge twice. The second application must not change state.
```

## 2. FINALIZE_PROPOSAL Reverse Edge

Status: specified as mandatory remediation.

Runtime requirement:

```text
FINALIZE_PROPOSAL must create the forward edge and reverse edge in the same transaction.
```

Minimum `compiled_block` graph shape:

```json
{
    "entry_id": "entry_...",
    "parent_hash": "sha256:...",
    "edges": [
        {
            "from": "entry_...",
            "to": "sha256:parent",
            "type": "DERIVES_FROM"
        },
        {
            "from": "sha256:parent",
            "to": "entry_...",
            "type": "HAS_DERIVATION"
        }
    ]
}
```

## 3. LAW-022 AI Signature Custody

Status: applied.

Decision:

```text
The AI signature is a SENTINEL service-account Ed25519 signature.
The SENTINEL public key must be registered in AUTHORIZED_PUBLIC_KEYS.
The signature must record key_id, role, algorithm, and signature payload.
```

## 4. Key Rotation

Status: implemented as `CTRL-001`, not canonical `LAW-043`.

Reasoning:

The Phoenix canon has exactly 42 laws. Key rotation is mandatory, but it is a security control extension rather than a
new axiom. Treating it as `CTRL-001` gives it `MUST` force without destabilizing the canonical law index.

Minimum key record:

```json
{
    "key_id": "sentinel-2026-q3",
    "owner": "SENTINEL",
    "role": "SENTINEL",
    "algorithm": "Ed25519",
    "public_key": "...",
    "created_at": "2026-06-26T00:00:00Z",
    "expires_at": "2026-09-26T00:00:00Z",
    "status": "ACTIVE"
}
```

## 5. LAW-023 Rename

Status: applied.

Decision:

```text
Dijkstra Garbage Collection -> SFR Threshold Pruning
```

Reason:

The described behavior is threshold-based graph maintenance, not shortest-path search.

## 6. CMD Version Pins

Status: applied.

Pinned dependencies:

```text
CMD.RequestClarification@^1.0.0
CMD.Deprecate@^1.0.0
CMD.Approve@^1.0.0
CMD.Refine@^1.0.0
CMD.EnactTranscendence@^1.0.0
```

## 7. LAW-042 compiled_block Metadata

Status: specified as mandatory remediation.

Minimum `compiled_block` metadata:

```json
{
    "artifact_id": "CORE.CODEX.PhoenixSchema",
    "schema_version": "v16.0",
    "policy_refs": ["LAW-004", "LAW-035", "LAW-042"]
}
```

Runtime requirement:

```text
REGISTER_FORK and FINALIZE_PROPOSAL blocks must carry artifact_id, schema_version, and policy_refs.
```
