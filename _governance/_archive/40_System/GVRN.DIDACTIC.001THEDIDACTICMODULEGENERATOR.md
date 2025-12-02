# UMB-DIDACTIC-001TheDidacticModuleGenerator_v11.0.md

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.DIDACTIC.001THEDIDACTICMODULEGENERATOR` | The Sovereign ID. |
| **Official Name** | `GVRN.DIDACTIC.001THEDIDACTICMODULEGENERATOR.md` | The Filename.     |
| **Version**       | **v13.0 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `ACTIVE` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |




---

### **Block B: State Vector (AGP-001)**

| State Field   | Value    |
| :------------ | :------- |
| **Coherence** | `1.0`    |
| **Resonance** | `0.9`    |
| **Stability** | `Stable` |

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                |
| :------------------- | :------------------------ |
| **Logic Drift**      | Strict Linter Enforcement |
| **Dependency Break** | ForgeLink Validation      |

---

| **Coherence** | `1.0` | | **Resonance** | `0.9` | | **Stability** | `Stable` |

| **Logic Drift** | Strict Linter Enforcement | | **Dependency Break** | ForgeLink Validation |

---

| **Coherence** | `1.0` | | **Resonance** | `0.9` | | **Stability** | `Stable` |

| **Logic Drift** | Strict Linter Enforcement | | **Dependency Break** | ForgeLink Validation |

> **Signal**: OMEGA

---

###### **[ARTIFACT START]**

---

# Universal Identification & Provenance (UIP)

| **Type** | `Protocol` | | **Classification** | `Moon` | | **Authors** | `System` | | **Created** | `2025-10-01` | |
**Updated** | `2026-01-17` | | **Authority** | `CODEX-001` |

---

# UMB-DIDACTIC-001: The Didactic Module Generator (v1.0)

> **Domain**: GVRN (Governance) **Signal**: ESF-ALPHA

---

###### **[ARTIFACT START]**

#### II. Architectural Definition

- **What**: A subsystem that generates "Lesson Modules" from `AOP-SENTINEL-SCAN-001` findings.
- **How**: It uses an LLM (Rationale Synthesizer) to explain the _why_ behind a fix, referencing specific Axioms from

`GUIDE-AI-CODE-001`.

- **Why**: To ensure that the human developer learns and evolves alongside the AI, preventing the repetition of errors

and deepening understanding.

#### III. Functional Specifications

- **1. Trigger**: Activated when `AOP-SENTINEL-SCAN-001` identifies a violation.
- **2. The Process**:
    - **Axiom Retriever**: Fetches the violated principle (e.g., "DRY Principle").
    - **Rationale Synthesizer**: Generates a clear, human-readable explanation of why the code was flagged and how the

fix aligns with the axiom.

    - **Module Packager**: Bundles the "Before Code," "After Code," and "Rationale" into a `LessonModule` JSON object.

- **3. Output**: A `LessonModule` served to the `CodeReviewView` in the frontend or displayed in the `CSL`.

#### IV. Data Model

```typescript
interface LessonModule {
    axiomTitle: string; // e.g., "The Rule of Atomic Functions"
    axiomText: string; // The definition from the library
    codeBefore: string; // The problematic snippet
    codeAfter: string; // The corrected snippet
    synthesizedRationale: string; // The "Lesson" text
}
```

---

### Revision History

- **v1.0**: Extracted from `_Coder_ The Master Artificer's Forge.md`. Formalized as a standalone UMB.

## **Actionable Prompt Packet**

`CMD: REFINE_ARTIFACT --focus:"Compliance" --context:"Auto-injected by Supabase Prep"`

| Command ID                   | Action                     | Impact                          |
| :--------------------------- | :------------------------- | :------------------------------ |
| `CMD:VERIFY_INTEGRITY`       | Verify artifact structure. | Ensures compliance with Law 14. |
| `⚡ EXECUTE:IMPACT_ANALYSIS` | Assess downstream effects. | Prevents regressions.           |

###### **[ARTIFACT END]**

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact. GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
