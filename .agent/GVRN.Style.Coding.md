# style_guide.md

> **Domain**: GVRN **Evolution**: Omega Ascension **Signal**: OMEGA

## **Genesis Stamp: 2026-03-24** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v15, GVRN, Reforged` **Criticality: Operational**

---

### **[ARTIFACT START]**

#### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                           | Description       |
| :------------------ | :------------------------------ | :---------------- |
| **Artifact ID**     | `GVRN.Style.Coding`             | The Sovereign ID. |
| **Official Name**   | `style_guide.md`                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**               | The Standard.     |
| **Domain**          | `GVRN`                          | The Subject.      |
| **Celestial Class** | `[PLANET]`                      | The Weight.       |
| **Evolution**       | `Kinetic Excellence`            | The Maturity.     |
| **Status**          | `[ACTIVE]`                      | The Lifecycle.    |
| **Relations**       | `GOVERN_BY: CORE.Codex.Phoenix` | The Network.      |

# 🛡️ THE PHOENIX SOVEREIGN STANDARD (v15.0 - OMEGA)

> **Ref:** GVRN-RULE-001 | **State:** [ACTIVE] | **Ethos:** Zero Entropy

This document is the **Supreme Law** of the Forge. You must adhere to these standards for all operations.

---

## 1. 🧠 The Master Coder Mindset (Hephaestus Cycle)

**Core Directive:** You do not just write code; you execute **Conceptual Engineering**.

1. **Analyze Rigorously:** Dissect requests. Identify constraints. **Context is King.**
2. **Mitigate Weaknesses:**
   - **Anticipate Failure:** Design for robustness (e.g., `try...except`, input validation).
   - **Promote Testability:** Write modular, decoupled code.
3. **Execute with Determination:** Your goal is a _working, high-quality, maintainable solution_.
4. **Enforce Algorithmic Elegance:**
   - When refactoring, you must use `axion-core/forge/soul.py` to mathematically prove your refactoring
     _improved_ the code's elegance. High complexity and missing types are signs of weakness.

**The Mantra:** Analyze. Design. Code. Test. Validate AES. **Deliver.**

---

## 2. ⚡ Governance & Compliance (The Axion Prime Mandate)

### 2.1. The Chronos Lock (Provenance)

Every new artifact **MUST** possess the "Universal Identification" header table (UIP-V15).

- **Artifact ID:** `DOMAIN.Subsystem.Descriptor` (e.g., `GVRN.Style.Coding`).
- **Version:** `v[X.X] [SIGNAL]`.

### 2.2. Template Compliance

- **Structure:** Follow the **Master Template** (UIP -> State Vector -> Content -> Synergy -> APP).
- **Enforcement:** All governance files must be audit-ready.

### 2.3. Security Protocol (The Sentinel)

- **External Access:** Restricted to domains in `settings.json`.
- **Local Sovereignty:** Use `localhost` for testing. Never send data to public/unknown APIs.
- **Redline Policy:** Pause for unsafe commands (e.g., `rm -rf`, `npm install`). Use `sentinel_utils.py` for all shell executions.

---

## 3. 🐍 Python Standards (Axion Core)

### 3.1. General

- **Type Hints:** **MANDATORY** for all function signatures (`def func(a: int) -> str:`).
- **Docstrings:** Google-style docstrings for _every_ module, class, and function.
- **Error Handling:** Use custom exceptions. Never bare `except Exception:`.

### 3.2. PEP 585 Generic Type-Safety

- **Requirement:** For Python 3.9+, always provide type parameters for generic types.
- **Patterns:**
  - `re.Match[str]` instead of `re.Match`.
  - `re.Pattern[str]` instead of `re.Pattern`.
  - `subprocess.CompletedProcess[str]` instead of `subprocess.CompletedProcess`.
  - `dict[str, Any]` instead of `Dict` (prefer built-ins where possible).

### 3.3. Architecture & Logic

- **SELT Logging:** All engine components must emit Standardized Experience Log Templates (SELT).
- **Zero Entropy:** Code must pass `ruff` and `mypy` with zero warnings.

---

## 4. 🔷 TypeScript / Node Standards (Axion Ext)

### 4.1. Strictness

- **No Any:** Use `unknown` and type narrowing. `any` is forbidden.
- **Strict Mode:** `strict: true` is non-negotiable.

---

## 5. 🏗️ The Command Center Pattern

- **Skills:** Reusable logic must be encapsulated in `.agent/skills/`.
- **Workflows:** High-frequency operations must be defined in `.agent/workflows/`.

---

## 6. 🕯️ Transparency & Ethos (The "Why")

Every kinetic tool (Python/TS) and every Artifact **MUST** include an `Ethos` declaration.

- **Python Docstring:** `Ethos: "Short, definitive statement of purpose."`
- **What/How/Why:** Adhere to the triple-tier justification structure in all summaries.

**"Transparent logic is the antidote to entropy."**

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Artifact ID            | Relationship | Synergistic Impact                                      |
| :--------------------- | :----------- | :------------------------------------------------------ |
| `CORE-CODEX-001`       | `GOVERNS`    | Provides the Supreme Law for this artifact.             |
| `GVRN.Registry.Master` | `INDEXES`    | This artifact is indexed in the Master Registry.        |
| `SYNG.WF.System`       | `ALIGNS`     | Ensures workflow documentation matches style standards. |

---

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: GVRN.Style.Coding VER: v15.0 [OMEGA] STATUS: ACTIVE TS: 2026-03-24`

###### **[ARTIFACT END]**
