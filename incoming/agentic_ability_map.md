# Agentic Ability Map: Phoenix Synarche Operational Environment

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Status**: [ACTIVE]

This document maps the guardrails, linters, and operational protocols that define the **Agentic Abilities** and constraints within the Phoenix Synarche workspace.

---

## I. The Meta-Enforcer (Trunk & Linters)

| Tool                 | Role          | Focus Area                                                                                                                                                    |
| :------------------- | :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Trunk (v1.25.0)**  | Meta-Engine   | Manages lifecycle and versioning of all active linters.                                                                                                       |
| **Ruff (v0.15.0)**   | Python Master | Fast linting and formatting; enforces absolute imports and Google-style docstrings.                                                                           |
| **ESLint (v9.39.2)** | JS/TS Logic   | Enforces strict functional patterns and security best practices.                                                                                              |
| **Markdownlint**     | Structurer    | Custom rules (`PF001-PF026`) enforce the Phoenix Presentation Standard.                                                                                       |
| **Bandit**           | Security      | Scans Python code for common security vulnerabilities.                                                                                                        |
| **TruffleHog**       | Secret Guard  | Prevents accidental commitment of credentials or private keys.                                                                                                |
| **Cspell**           | Semantic SSOT | Standardizes specialized vocabulary (e.g., [ContextWeave](file:///c:/Users/Chris/Synarche_Workspace/nova_forge/src/engine/ContextWeave.ts#11-23), `κ-nexus`). |
| **Reforge.py**       | Auto-Fixer    | Automated structural transmutation and header injection engine.                                                                                               |

---

## II. The Law of the Forge (Style Guide)

### 1. Cognitive Complexity Guardrails

- **Max Complexity**: `15` per function.
- **Protocol**: Exceeding density requires "logic shattering" into single-purpose sub-functions.
- **Documentation**: Scores > 10 require an `Explain:` comment block.

### 2. RNC-v13 Naming (Resource-Naming-Context)

- **Standard**: `DOMAIN.Subsystem.Descriptor.md`
- **Logic**: Projects must be "Subject-Clustered" for efficient retrieval.

### 3. Absolute Sovereignty (Python 3.14)

- **Functional Paradigm**: No side effects; pure functions preferred.
- **Strict Typing**: Mandatory types for all arguments and returns.

---

## III. Phoenix Protocol Linting (PF-Rules)

| Rule ID   | Name               | Enforcement Logic                                                                                                                                             |
| :-------- | :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **PF001** | Doc ID Format      | Ensures [(XXX-YYY-NNN)](file:///c:/Users/Chris/Synarche_Workspace/open-notebook/open_notebook/frontend/src/lib/api/models.ts#10-14) exists in the H1 heading. |
| **PF002** | Episemantic Valid  | Validates `κ-nexus` and `κ-tempus` markers against a vocabulary.                                                                                              |
| **PF010** | Canonical Acronyms | Auto-corrects lowercase acronyms (e.g., `dsl` → `DSL`) using [cspell.json](file:///c:/Users/Chris/Synarche_Workspace/cspell.json).                            |
| **PF015** | Link Integrity     | Validates that file links AND slugs exist; includes path traversal security.                                                                                  |
| **PF016** | Roman Sequence     | Enforces strict `I., II., III.` numbering for H2 sections.                                                                                                    |
| **PF021** | Actionable Packet  | Mandates the inclusion of a "V. Actionable Prompt Packet" (flexible numbering).                                                                               |
| **PF026** | Asterisk Lists     | Enforces the use of `*` for unordered lists (Synarche Standard).                                                                                              |

---

## IV. Operational Workflows

### 1. Refactor Protocol (`GVRN-REFACTOR-PROTOCOL-001`)

A mandatory loop for all cleanup or standardization tasks:

1. **Audit**: Scan for Complexity/Naming/Typing violations.
2. **Snapshot**: Verify Git tracking.
3. **Reforge**: Execute [reforge.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/tools/reforge.py) for automated structural alignment.
4. **Verification**: Validate logic and functionality.
5. **Chronicle**: Document the change in the system log.

### 2. Finalization Gateway (`GVRN-PROTOCOL-FINALIZATION`)

Artifacts must pass the **7 Gates of Ingestion** before becoming "Canonical":

- Verification → Formatting → Naming → Indexing → Linkage → Risk → Canonization.

---

## V. System Environment

- **IDE Settings**: [.vscode/settings.json](file:///c:/Users/Chris/Synarche_Workspace/.vscode/settings.json) is configured for _Format On Save_ and _Fix All on Save_.
- **Workspace**: [Synarche_Workspace.code-workspace](file:///c:/Users/Chris/Synarche_Workspace/Synarche_Workspace.code-workspace) manages multi-root clusters (`Synarche_Workspace` + `_Desktop_Vault`).
- **Type Safety**: [pyrefly.toml](file:///c:/Users/Chris/Synarche_Workspace/pyrefly.toml) forces strict type diagnostics on all project roots.

---

## VI. Semantic Governance (Tarot Shards)

Metadata fields are governed by specific **Tarot Shards** (Agent Personas):

| Shard         | Governance Area   | Field Examples                                                                                                                                                                      |
| :------------ | :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EMPEROR**   | Structure & ID    | `Artifact ID`, `Version`, [Status](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/enums.py#66-77)                                                                   |
| **STAR**      | Tone & Evolution  | [Signal](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/enums.py#79-87), [Evolution](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/enums.py#89-99) |
| **PRIESTESS** | Knowledge Graph   | [Domain](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/enums.py#36-52), `Celestial Class`, `Synergy Vector`                                                        |
| **JUDGEMENT** | Audit & Integrity | `Author`, `Integrity Hash`, `Musashi Audit`                                                                                                                                         |

---

## VII. Elemental Validation (Musashi Rings)

The linting ecosystem maps to the **5 Rings of Validation**:

| Ring      | Validation Focus | Corresponding Rule (Example)  |
| :-------- | :--------------- | :---------------------------- |
| **EARTH** | Lore & Stability | `PF016` (Sequential Sections) |
| **WATER** | Connectivity     | `PF015` (Link Integrity)      |
| **FIRE**  | Actionability    | `PF021` (Prompt Packet)       |
| **WIND**  | Tone & Style     | `PF010` (Canonical Acronyms)  |
| **VOID**  | Prime Alignment  | `PF001` (Doc ID Format)       |

---

## VIII. Future Evolutions (v13.0 Gaps)

1. **AGP Enforcement**: Need strict rules for `AGP-001` (State Vector) and `AGP-002` (Risk) blocks.
2. **Reforge Upgrade**: [reforge.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/tools/reforge.py) must be ascended from v11.0 to v13.0 to handle modern UIP headers.
3. **Consolidation**: Merge `axion-rules (1).cjs` enhancements back into the master [axion-rules.cjs](file:///c:/Users/Chris/Synarche_Workspace/axion-core/tools/rules/axion-rules.cjs).
