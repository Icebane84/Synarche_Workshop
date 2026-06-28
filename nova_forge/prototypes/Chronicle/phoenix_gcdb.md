# Phoenix GCDB Registry

The Phoenix Schema now has a Governance Configuration Database representation. The 42 laws remain canonical policy intent, while controls, exceptions, findings, verifications, evidence, risks, metrics, and graph relationships are first-class objects.

## Object Types

- `POLICY`: canonical `LAW-###` desired behavior.
- `CONTROL`: enforcement mechanism for one or more policies.
- `EXCEPTION`: scoped, temporary policy deviation with approval and risk acceptance metadata.
- `FINDING`: compliance result documenting missing, incorrect, partial, obsolete, or risky implementation state.
- `VERIFICATION`: explicit `TEST-###` procedure proving compliance.
- `EVIDENCE`: artifact, log, policy file, review record, or CI output supporting an assertion.
- `RISK`: business or architectural impact requiring treatment.
- `METRIC`: derived compliance KPI.

## Status Derivation

Policy status is derived rather than hand-assigned:

- No finding and no exception: `COMPLIANT`.
- Finding without exception: `NON_COMPLIANT` for `MUST`, otherwise `PARTIAL`.
- Exception without finding: `EXEMPT`.
- Finding plus exception: `UNDER_REMEDIATION`.

## Files

- `phoenix_gcdb.registry.json`: queryable governance graph.
- `phoenix_gcdb.schema.json`: JSON Schema for the GCDB registry.
- `phoenix_schema.normalized.json`: original normalized policy contract remains the canonical law source.

## Current Metrics

- Policies: 42
- Controls: 48
- Verifications: 48
- Findings: 5
- Exceptions: 2
- Evidence objects: 4
- Relationships: 229

This is the point where Phoenix becomes queryable: `LAW-017` can be traversed to its enforcement controls, verification tests, active findings, exceptions, and evidence without scraping prose.
