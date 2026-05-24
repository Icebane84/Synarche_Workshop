---
id: NOVA.Sys.TDD.Skill
name: TDD Workflow (UMB)
type: SKILL
tags: ['#NOVA/Sys/TDD', '#UMB', '#METHODOLOGY']
links: ['[[GVRN.Codex.Phoenix]]', '[[NOVA.Sys.TDD.Index]]', '[[NOVA.Sys.TDD.AOP]]']
relations:
    - type: GOVERNED_BY
      target: '[[GVRN.Codex.Phoenix]]'
    - type: DESCRIBED_BY
      target: '[[NOVA.Sys.TDD.Index]]'
description: 'Sovereign Test-Driven Development principles, the Three Laws, and the RED-GREEN-REFACTOR cycle.'
---

# TDD WORKFLOW | UMB-NOVA.Sys.TDD

| Field             | Metadata                                          |
| :---------------- | :------------------------------------------------ |
| **Provenance**    | Genesis Stamp: 2026-03-29                         |
| **Domain**        | NOVA.Sys.TDD                                      |
| **State**         | 🟢 OPERATIONAL                                    |
| **Criticality**   | HIGH                                              |
| **Class**         | STAR                                              |
| **Relationships** | GOVERNS All Test-First Logic, SYNCED_BY [Bifrost] |
| **Author**        | Axion (The Refiner)                               |
| **Audit**         | Musashi (Pass)                                    |
| **Integrity**     | [V15.0-OMEGA]                                     |

---

## 1. Executive Intent

To engineer high-integrity code through the discipline of **Test-Driven Development**, ensuring that every line of
production code is preceded by a failing test case, thereby minimizing technical debt and maximizing maintainability.

## 2. The Hephaestus Execution Cycle

Every TDD cycle must pass through the triadic pipeline:

### 2.1 Phase I: Dissonance (RED)

- **Action**: Write a failing test for a new piece of behavior.
- **Guardrail**: If the test passes immediately, trigger **Behavior Dissonance**.
- **SERP**: On failure, run `test_runner.py` to confirm "Expected Failure."

### 2.2 Phase II: Synthesis (GREEN)

- **Action**: Implement the **Minimum Necessary Code** to make the test pass.
- **Logic**: Use the **Simplest Thing Rule** (Prioritize passing over elegance).
- **Rule**: Adhere to the **Production Bias** (Write only enough code to pass).

### 2.3 Phase III: Transcendence (REFACTOR)

- **Action**: Improve the code structure without changing behavior.
- **Logistics**: Update [[NOVA.Sys.TDD.SELT]] with the "Refinement Record of the Session."

## 3. Noetic Guardrails (Constraints)

- **Law 1**: Write production code only to make a failing test pass.
- **Law 2**: Write only enough test to demonstrate failure—compilation failure is a failure.
- **Law 3**: Write only enough production code to make the test pass.

---

`[OMNI-ARTIFACT-ANCHOR] ID: NOVA.Sys.TDD.Skill VER: v15.0 [OMEGA] DOMAIN: NOVA STATUS: [OPERATIONAL] TS: 2026-03-29`
