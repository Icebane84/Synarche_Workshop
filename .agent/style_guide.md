# style_guide.md

> **Domain**: GVRN **Evolution**: Omega Ascension **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

### **Block A: The Identification Lock (UIP-V13)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `GVRN-STYLE-GUIDE-001`        | The Sovereign ID. |
| **Official Name**   | `style_guide.md`              | The Filename.     |
| **Version**         | **v13.1 [OMEGA]**             | The Standard.     |
| **Domain**          | `GVRN`                        | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Omega Ascension`             | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

# 🛡️ AGENT STYLE GUIDE (v13.0)

> **Ref:** GVRN-RULE-001 | **State:** [ACTIVE] | **Ethos:** Zero Entropy

This guide defines the **Law of the Forge**. You must adhere to these standards for all file modifications.

---

## 1. 🧬 The Cognitive limit (Sonar Protocol)

**Objective**: Keep code simple, readable, and linear.

- **Maximum Cognitive Complexity**: `15` (per function).
- **Modularization**: If a function exceeds this logic density, **shatter it** into smaller, single-purpose
  sub-functions.
- **Documentation**: Any complex logic (Score > 10) requires a `Explain:` comment block.

## 2. 📛 Naming Conventions (RNC-v13)

All artifacts (files) must follow the **Context-First / Subject-Clustered** standard if they are "Knowledge" or
"Governance".

- **Format**: `[DOMAIN]-[OBECT]-[ID]_[Name]_[Version].md`
- **Example**: `GVRN-RULE-001_AgentStyleGuide_v13.0.md`
- **Code Files**: `snake_case` for Python (`compliance_audit.py`), `camelCase` for TS/JS (`fileSystem.ts`).

## 3. 🐍 Python Standards (Axion Core)

- **Version**: Python 3.14 (Functional/Typed)
- **Typing**: Strict `type hints` required for all function arguments and returns.
- **Docstrings**: Google Style docstrings for every module, class, and function.
- **Imports**: Absolute imports only. Group by: Standard -> Third Party -> Local.

## 4. ⚡ TypeScript/Node Standards (Axion Ext)

- **Strict Mode**: `strict: true` in `tsconfig.json`.
- **Async/Await**: No `.then()` chains.
- **Functional**: Prefer pure functions over classes where possible.

## 5. 🏗️ The Command Center Pattern

- **Integration**: New tools should be wired into `.vscode/tasks.json` if they are user-facing.
- **Skills**: Reusable logic must be encapsulated in `.agent/skills/`.

---

**"We do not guess. We verify."**

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact. GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
