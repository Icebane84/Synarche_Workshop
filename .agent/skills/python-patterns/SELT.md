# SELT: Python Experience Log & Trace [v15.0]

## 📅 Session Logs

### 🏗️ 2026-03-30 (Batch 4 Rollout)
- **Status**: Canonized Batch 4 (Python).
- **Synthesis**: Standardized Django vs FastAPI selection matrix in `AOP.md`.
- **Integrity**: Enforced **Pydantic v2** and **Async Hygiene** as top-level governance.
- **Audit**: Updated command registry in `GUCA.md`.

## 📍 Systemic Discoveries

### 🧠 Performance Expansion
- **Discovery**: Widespread use of `requests` (blocking) within `async` FastAPI routes.
- **Remediation**: Injected **Async Hygiene** mandate: Blocking libraries are prohibited in `async def` code.
- **Discovery**: Undiagnosed N+1 query performance hits in Django ORM.
- **Remediation**: Implemented the **Query Optimization Rule**: `select_related()` and `prefetch_related()` are mandatory for related data access.

## 🚧 Historical Dissonance
- **Issue**: Type Hinting ignored in large service layers, leading to runtime `NoneType` errors.
- **Legacy Pattern**: Relying on docstrings instead of actual type hints.
- **Correction**: Prohibited untyped public APIs. Mandated Pydantic models for all input/output structures.

---
**Protocol**: This log MUST be updated after every backend audit or implementation task to maintain Zero Entropy in Python governance.
