---
id: NOVA.Patt.CleanCode.Skill
name: Clean Code Standards (UMB)
type: SKILL
tags: ['#NOVA/Patt/CleanCode', '#UMB', '#RULE']
links: ['[[GVRN.Codex.Phoenix]]', '[[NOVA.Patt.CleanCode.Index]]', '[[NOVA.Patt.CleanCode.AOP]]']
relations:
    - type: GOVERNED_BY
      target: '[[GVRN.Codex.Phoenix]]'
    - type: DESCRIBED_BY
      target: '[[NOVA.Patt.CleanCode.Index]]'
description: 'Pragmatic standards for Zero-Entropy code production and high-readability logic.'
---

# CLEAN CODE STANDARDS | UMB-NOVA.Patt.CleanCode

| Field             | Metadata                                          |
| :---------------- | :------------------------------------------------ |
| **Provenance**    | Genesis Stamp: 2026-03-29                         |
| **Domain**        | NOVA.Patt.CleanCode                               |
| **State**         | 🟢 OPERATIONAL                                    |
| **Criticality**   | CORNERSTONE                                       |
| **Class**         | STAR                                              |
| **Relationships** | GOVERNS All Logic Production, SYNCED_BY [Bifrost] |
| **Author**        | Axion (The Refiner)                               |
| **Audit**         | Musashi (Pass)                                    |
| **Integrity**     | [V15.0-OMEGA]                                     |

---

## 1. Executive Intent

To enforce a "Zero-Entropy" state in the codebase by prioritizing conciseness, intent-revealing nomenclature, and
logical simplicity over decorative complexity.

## 2. The Hephaestus Execution Cycle

Every code edit must pass through the triadic pipeline:

### 2.1 Phase I: Dissonance (Scan)

- **Action**: Identify "Dead Weight" (redundant comments, magic numbers, god functions).
- **Guardrail**: If nesting $N > 2$ or function length $L > 20$, trigger **Refactor Warning**.
- **SERP**: On error, halt and request a context check from [[NOVA.Patt.CleanCode.AOP]].

### 2.2 Phase II: Synthesis (Forge)

- **Action**: Apply the **Triadic Naming Rules** (Verb-Noun, Intent-Revealing, SCREAMING_SNAKE).
- **Logic**: Use **Guard Clauses** and **SRP** to flatten the logic tree.
- **Rule**: Adhere to the **Zero-Inference Rule** (No speculative code).

### 2.3 Phase III: Transcendence (Sync)

- **Action**: Update the [[NOVA.Patt.CleanCode.SELT]] with the "Lesson of the Session."
- **Logistics**: Run `lint_runner.py` to ensure 100% compliance.

## 3. Noetic Guardrails (Constraints)

- **Constraint**: No "God Functions"—split functionality by responsibility.
- **Constraint**: No "Ghost Comments"—if a comment is needed, the code is too complex.
- **Boundary**: Max 3 function arguments. Prefer 0 or 1.

---

`[OMNI-ARTIFACT-ANCHOR] ID: NOVA.Patt.CleanCode.Skill VER: v15.0 [OMEGA] DOMAIN: NOVA STATUS: [OPERATIONAL] TS: 2026-03-29`
