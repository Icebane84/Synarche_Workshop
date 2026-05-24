---
id: NOVA.Sys.TDD.GUCA
name: TDD Workflow Command Architecture (GUCA)
type: COMMAND
tags: ['#NOVA/Sys/TDD', '#GUCA', '#TRIGGER']
links: ['[[NOVA.Sys.TDD.Index]]', '[[NOVA.Sys.TDD.Skill]]']
relations:
    - type: IMPLEMENTS
      target: '[[NOVA.Sys.TDD.Skill]]'
    - type: DESCRIBED_BY
      target: '[[NOVA.Sys.TDD.Index]]'
description: 'Command activation and verification triggers for test-driven development workflows.'
---

# TDD COMMANDS | GUCA-NOVA.Sys.TDD

| Field             | Metadata                                               |
| :---------------- | :----------------------------------------------------- |
| **Provenance**    | Genesis Stamp: 2026-03-29                              |
| **Domain**        | NOVA.Sys.TDD                                           |
| **State**         | 🟢 OPERATIONAL                                         |
| **Criticality**   | HIGH                                                   |
| **Class**         | STAR                                                   |
| **Relationships** | IMPLEMENTS [[NOVA.Sys.TDD.Skill]], SYNCED_BY [Bifrost] |
| **Author**        | Axion (The Refiner)                                    |
| **Audit**         | Musashi (Pass)                                         |
| **Integrity**     | [V15.0-OMEGA]                                          |

---

## ⚡ ACTIVATION TRIGGERS

Invoke this skill cluster when:

- **"Develop via TDD"**: Initialized the full Forge cycle for a new requirement.
- **"RED Phase"**: Execute the **Failure Synthesis** ritual.
- **"GREEN Phase"**: Execute the **GREEN Phase Synthesis** ritual.
- **"REFACTOR Phase"**: Execute the **REFACTOR Phase Refinement** procedure.

---

## ✅ VERIFICATION TRIGGERS

Before saying "Task Complete," perform this status check:

1. **Critical Check**: "Did the test fail (RED) before it passed (GREEN)?"
2. **Standard Check**: "Is the code cleaner after the REFACTOR phase?"
3. **Audit Check**: "Is the TDD loop documented in the **Master Registry**?"

---

## 🔄 SELF-CHECK MATRIX

| Step | Action                   | If Failed                          |
| :--- | :----------------------- | :--------------------------------- |
| 1    | Analyze Failure Reasons  | RE-RED the test case.              |
| 2    | Evaluate Code Complexity | RE-FACTOR using cleaner patterns.  |
| 3    | Run Regression Suite     | RE-GREEN before status completion. |

---

`[OMNI-ARTIFACT-ANCHOR] ID: NOVA.Sys.TDD.GUCA VER: v15.0 [OMEGA] DOMAIN: NOVA STATUS: [OPERATIONAL] TS: 2026-03-29`
