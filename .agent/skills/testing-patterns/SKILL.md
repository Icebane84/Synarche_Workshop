---
name: testing-patterns
description: Testing patterns and principles. Unit, integration, mocking strategies.
allowed-tools: Read, Glob, Grep, Bash
---

# Testing Patterns System [v15.0]

## 🎯 Axiomatic Purpose

To enforce **Code Health** and **Vitality** through **Unit Testing**, **Performance Auditing**, and **Systemic Isolation**. This skill mandates that every module be verified for correctness and efficiency, ensuring the Sovereign system remains modular and performant.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Global Testing Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts

- `npx vitest run` - Automated Unit & Integration Scan.
- `scripts/omega_audit.py` - Universal Cluster-Wide Health Check.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Isolation-First" Mandate

**MANDATORY**: Test logic in isolation. Use mocks for all external state, APIs, and side-effects to ensure deterministic results.

### 2. Cleanup & Memory Sovereignty

**MANDATORY**: All component/service lifecycle hooks MUST include cleanup logic for listeners, timers, and external state to prevent memory growth.

### 3. Performance Thresholds

No component may exceed **50kB** min+gz. Critical logic must execute in under **10ms**.

### 4. Zero Flaky Tests

PROHIBITED: Non-deterministic tests or "wait-and-hope" timeouts. Tests must be 100% reliable across all environments.

---
"Health is the vitality of the Sovereign. Trust nothing that is not verified."
