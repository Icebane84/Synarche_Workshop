---
name: systematic-debugging
description:
    4-phase systematic debugging methodology with root cause analysis and evidence-based verification. Use when
    debugging complex issues.
allowed-tools: Read, Glob, Grep, Bash
---

# Systematic Debugging System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Root-Cause Analysis (RCA)** and **Scientific Precision** in software repair. This skill mandates that every bug be precisely reproduced, isolated, and understood before a fix is implemented, ensuring that the Sovereign system remains stable and predictable.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | 4-Phase Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `pm2 logs --err` - Automated Log Verification.
- `git bisect` - Automated Regression Isolation.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Evidence-Only" Mandate
**MANDATORY**: Do not fix what is not understood. Every repair must point to a specific stack trace, log, or reproduction script as the primary evidence.

### 2. The 5 Whys
**MANDATORY**: For every critical bug, perform a 5 Whys analysis to reach the architectural or process root cause.

### 3. Fix & Verify (Phase 4)
No fix is complete without a new, failing test that now passes. All fixes must be verified by the `/omega_audit` master validation script.

### 4. Zero Patches
PROHIBITED: "Quick patches" or "monkey-patching" that bypass the core reason for the bug without a long-term architectural resolution.

---
"Fix the cause, not the symptom. Trust the evidence of the Sovereign."
