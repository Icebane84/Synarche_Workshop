# Chronicle Integrity Policy

This deliverable implements the primary OPA Rego policy for `LAW-035`, the Immutable Chronicle.

The policy enforces the Phoenix Schema verification anchor:

```text
State(t) = S(0) + sum(Events)
```

## Files

- `chronicle_integrity.rego`: primary policy package, `phoenix.chronicle.integrity`
- `chronicle_integrity_test.rego`: focused OPA tests for append-only behavior, hash chaining, duplicate rejection, and state derivation

## Enforcement Scope

- Allows only append-style chronicle writes and state derivation.
- Rejects destructive operations such as delete, mutation, truncation, and history rewrite.
- Requires an authorized actor role.
- Requires LAW-035 identity on governed events.
- Requires event identity, content hash, event hash, previous hash, timestamp, and actor-aligned signature.
- Requires each appended event to continue from `chronicle.latest_hash`.
- Rejects duplicate `event_hash` values.
- Validates that existing chronicle events form a hash chain from `genesis_hash`.

## Suggested OPA Command

```powershell
opa test chronicle_integrity.rego chronicle_integrity_test.rego
```

## Integration Note

Wire this policy as the authoritative admission check before any write to the `AISTF_Transactions` table. The application should compute `content_hash` and `event_hash` before policy evaluation, then persist the accepted event as append-only ledger data.
