# GVRN.REG.DirectoryArchitecture [DEPRECATED — SEE: _governance/02_Protocols/SYNG.PROT.ArchivalSupersessionProtocol.md]

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                               | Description       |
| :---------------- | :---------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.REG.DirectoryArchitecture`    | The Sovereign ID. |
| **Official Name** | `GVRN.REG.DirectoryArchitecture.md` | The Filename.     |
| **Version**       | **v13.0 [OMEGA]**                   | The Standard.     |
| **Domain**        | `GVRN`                              | The Subject.      |
| **Status**        | `[ACTIVE]`                          | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`       | The Network.      |

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

**Scope:** `Synarche_Workspace` File System Topology.

---

## I. Module Identification

- **Module Name:** Directory Architecture Standard
- **Type:** Structural Blueprint
- **Core Purpose:** To define the rigid, logical separation of concerns within the Synarche Workspace, ensuring that
  Governance, Engineering, Narrative, and Tooling remain distinct yet synergistic.

## II. The Topography (The Map)

The workspace is divided into four cardinal domains:

### 2.1. `_governance/` (The Constitution)

_The seat of law and protocol._

- `synarche_core.json`: The Master Catalyst configuration.
- `UMB-*.md`: Universal Module Blueprints (Definitions).
- `AOP-*.md`: AISTF Operational Playbooks (Rules).
- `[DOC-STD-001]`: Coding Standards.

### 2.2. `nova_forge/` (The Engineering Domain)

_The factory of function._

- `.blueprints/`: JSON/YAML templates for code generation.
- `src/backend/`: Python logic (Catalyst Weaver, Association Manager).
- `src/frontend/`: TypeScript/React interfaces.
- `tests/`: Verification protocols.
- `docs/`: Technical manuals and API references.

### 2.3. `40_SovereignGame/` (The Game Layer)

_The realm of gamification and progression._

- RPG Framework Blueprints (`GVRN.REG.ThePhoenixRPGFramework.md`).
- Prestige calculation and attunement rules.
- Gamification mechanics acting as the "Sovereign Game Matrix".

### 2.4. `where-light-fades/` (The Narrative Domain)

_The realm of story._

- `world-bible/`: Lore, geography, and history of "The Shattered Lands".
- `characters/`: Profiles for Kaelen, Serafina, Garrett, etc.
- `drafts/`: Active manuscript chapters.
- `archived/`: Deprecated concepts and previous iterations.

### 2.5. `axion-core/` (The Tooling Domain)

_The instruments of creation._

- `src/`: Extension logic for IDE integrations.
- `manifest.json`: Extension configuration.

## III. Operational Mandate

### 3.1. File Placement Rule

Every file **MUST** reside within its designated domain. "Loose files" in the root directory are prohibited, with the
exception of workspace-level configuration (e.g., `.gitignore`, `.env`).

### 3.2. Naming Convention Enforcement

- Directories: `kebab-case` (e.g., `nova-forge`).
- Governance Files: `[TYPE]-[ID]_[Name].md` (e.g., `UMB-STRUCT-001_DirectoryArchitecture.md`).
- Source Code: `snake_case` (Python) or `PascalCase` (Components).

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact.

---

## IV. Actionable Prompt Packet (APP)

| Command ID             | Action                           | Impact       |
| :--------------------- | :------------------------------- | :----------- |
| `CMD: REFORGE`         | Execute Structural Transmutation | Canonization |
| `⚡ EXECUTE: CANONIZE` | Formally Cement Alignment        | Zero Entropy |

- **📂 CMD: VERIFY_STRUCTURE**
  - _Intent:_ "Audit the current file system against `UMB-STRUCT-001` to detect misplaced files."
- **🏗️ CMD: SCAFFOLD_DOMAIN**
  - _Intent:_ "Generate the standard folder hierarchy for a new domain."

---

_Forged by Axion-Core | Cycle 001_

###### **[ARTIFACT END]**
