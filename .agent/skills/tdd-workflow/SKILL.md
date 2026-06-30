---
name: tdd-workflow
description: Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle.
allowed-tools: Read, Glob, Grep, Bash
---

# TDD Workflow System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Spec-First Accuracy** and **Implementation Discipline** through the **Red-Green-Refactor Cycle** and the **Agent A/B/C Triple-Pass Protocol**. This skill mandates that code only exists to satisfy a verified requirement, ensuring the Sovereignty of the codebase.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | TDD & Agent A/B/C Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `npx vitest run --coverage` - Automated Coverage & Behavior Audit.
- `scripts/omega_audit.py` - Universal Cluster-Wide Verification.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Spec-First" (Agent A) Mandate
**MANDATORY**: No production code may be edited until a failing test file is committed and verified by the test runner.

### 2. Triple-Pass Separation
**MANDATORY**: Each feature must go through the Agent A (RED), Agent B (GREEN), and Agent C (REFACTOR) phases as distinct cognitive steps.

### 3. YAGNI Enforcement (Agent B)
**MANDATORY**: In the GREEN phase, write only the minimal code necessary to pass the spec. Do not optimize, refactor, or add "future-proof" logic.

### 4. Zero Entropy Refactor (Agent C)
All refactoring must align with OMEGA v15.0 standards and maintain 100% test passing status across the `/omega_audit`.

---
"The test is the specification. Trust the Sovereign cycle."
