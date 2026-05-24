---
id: NOVA.Patt.CleanCode.AOP
name: Clean Code Operational Playbook (AOP)
type: PLAYBOOK
tags: ['#NOVA/Patt/CleanCode', '#AOP', '#PROCEDURE']
links: ['[[NOVA.Patt.CleanCode.Index]]', '[[NOVA.Patt.CleanCode.Skill]]']
relations:
    - type: IMPLEMENTS
      target: '[[NOVA.Patt.CleanCode.Skill]]'
    - type: DESCRIBED_BY
      target: '[[NOVA.Patt.CleanCode.Index]]'
description: 'Step-by-step operational procedures for the Clean Code Pattern Shard.'
---

# CLEAN CODE PLAYBOOK | AOP-NOVA.Patt.CleanCode

| Field             | Metadata                                                      |
| :---------------- | :------------------------------------------------------------ |
| **Provenance**    | Genesis Stamp: 2026-03-29                                     |
| **Domain**        | NOVA.Patt.CleanCode                                           |
| **State**         | 🟢 OPERATIONAL                                                |
| **Criticality**   | HIGH                                                          |
| **Class**         | STAR                                                          |
| **Relationships** | IMPLEMENTS [[NOVA.Patt.CleanCode.Skill]], SYNCED_BY [Bifrost] |
| **Author**        | Axion (The Refiner)                                           |
| **Audit**         | Musashi (Pass)                                                |
| **Integrity**     | [V15.0-OMEGA]                                                 |

---

## 📋 PRE-FLIGHT CHECK (Dissonance Scan)

Before any logic edit, perform a **Dissonance Scan**:

1. Scan the file for **Ghost Comments** (comments that state the obvious).
2. Identify **Magic Numbers** or **String Literals** and move them to constants.
3. Check for **High Nesting** ($N > 2$).
4. Check for **Large Functions** ($L > 20$).

---

## 🛠️ PROCEDURE: RITUAL OF RENAMING

If a name does not reveal intent, apply this procedure:

1. **Analyze Purpose**: What is the _Sovereign Job_ of this variable/function?
2. **Apply Domain**: Use domain-specific terms (e.g., `userProfile` vs `data`).
3. **Verb-Noun**: Ensure functions are `ActionSubject` (e.g., `calculateTotal`).
4. **Boolean Question**: Booleans must be `is/has/can` (e.g., `isActive`).

---

## 🛠️ PROCEDURE: THE SEVERING (SRP)

If a function does "more than one thing," apply this procedure:

1. **Identify Shards**: Identify the logical shards within the function.
2. **Extract**: Pull each shard into its own small, private function.
3. **Compose**: Re-write the original function to simply call the shards.
4. **Flatten**: Use **Guard Clauses** to eliminate `else` blocks and reduce nesting.

---

## 🛠️ PROCEDURE: VERIFICATION SYNC

After the Forge phase, execute this sync:

1. **Manual Check**: Read the diff to ensure it's simpler than the original.
2. **Lint Sync**: Run `lint_runner.py` or equivalent.
3. **Record**: Update [[NOVA.Patt.CleanCode.SELT]] with any friction encountered.

---

`[OMNI-ARTIFACT-ANCHOR] ID: NOVA.Patt.CleanCode.AOP VER: v15.0 [OMEGA] DOMAIN: NOVA STATUS: [OPERATIONAL] TS: 2026-03-29`
