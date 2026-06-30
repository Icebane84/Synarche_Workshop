---
name: python-patterns
description:
    Python development principles and decision-making. Framework selection, async patterns, type hints, project
    structure. Teaches thinking, not copying.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Python Governance System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Type-Safe**, **Concurrency-Aware**, and **Sovereign-Architecture** development across the Python ecosystem. This skill prevents the use of legacy blocking patterns and mandates modern (2025) decision-making for frameworks and async performance.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Global Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. Framework Decision Tree
**DO NOT** default to Django. Use **FastAPI** for API-first and microservices. Use **Django** only for full-stack with built-in admin. Refer to `AOP.md`.

### 2. Async Hygiene Mandate
Any blocking I/O (e.g., `requests`, `time.sleep`) is **PROHIBITED** in `async def` code. Use `httpx` or `aiohttp` to maintain concurrency.

### 3. Type-Safe Interface Control
All public APIs and function boundaries **MUST** be explicitly typed. Use **Pydantic v2** for validation and serialization.

### 4. Query Optimization Guardrail
N+1 queries are failures. Mandate `select_related()` and `prefetch_related()` for all relational database access in Django/SQLAlchemy.

---
"Implicit is better than explicit, but typed is better than guessed."
