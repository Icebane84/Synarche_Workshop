---
name: nodejs-best-practices
description:
    Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture.
    Teaches thinking, not copying.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Node.js Governance System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Runtime-Aware**, **Layered-Architecture**, and **Security-First** development across the Node.js ecosystem. This skill prevents the use of outdated legacy patterns and mandates modern (2025) decision-making for frameworks and async performance.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Global Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. Framework Decision Matrix
**DO NOT** default to Express. Use **Hono** for Edge/Serverless and **Fastify** for high-performance APIs. Refer to `AOP.md` for specific criteria.

### 2. Layered Architectural Mandate
Business logic **MUST** be separated into a distinct **Service Layer**. Controllers are for boundary handling only.

### 3. Event Loop Protection
Any synchronous blocking I/O (`fs.readFileSync`, etc.) is **PROHIBITED** in production code. Offload CPU-heavy tasks to worker threads.

### 4. Fail-at-Gate Validation
Input validation using **Zod** or **Valibot** is mandatory at all system boundaries (API, DB, Env).

---
"Node.js design is the fine art of not blocking the event loop."
