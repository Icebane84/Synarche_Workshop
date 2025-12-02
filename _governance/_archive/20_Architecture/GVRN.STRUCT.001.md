# UMB-STRUCT-001_DirectoryArchitecture_v11.2.md

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.STRUCT.001` | The Sovereign ID. |
| **Official Name** | `GVRN.STRUCT.001.md` | The Filename.     |
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

> **Signal**: OMEGA

---

###### **[ARTIFACT START]**

---

# Universal Identification & Provenance (UIP)

| **Type** | `Blueprint` | | **Classification** | `Planet` | | **Authors** | `Synarche` | | **Created** | `2026-01-04` |
| **Updated** | `2026-01-21` | | **Authority** | `CODEX-001` |

---

# UMB-STRUCT-001: Directory Architecture & Domain Separation

---

## II. The Topography (The Map)

The workspace is organized into functional domains to ensure zero-entropy information management:

### 2.1. `_governance/` (The Constitution)

> _The seat of law and protocol._

- `UMB-*.md`: Universal Module Blueprints (Definitions).
- `AOP-*.md`: AISTF Operational Playbooks (Rules).
- `DOC-STD-001`: Coding Standards.
- `Project_Credentials.md`: Secrets and Keys.

### 2.2. `nova-forge/` (The Engineering Domain)

> _The factory of function._

- `src/`: Unified source code (Python/TS).
- `infra/`: Infrastructure as Code (Terraform, Supabase).
- `scripts/`: Operational automation.
- `config/`: Environment and application settings.
- **Constraint**: `nova_forge` (snake_case) is deprecated; all engineering efforts must transition to `nova-forge`.

### 2.3. `where-light-fades/` (The Narrative Domain)

> _The realm of story._

- `1-11 Numbered Vault`: Standardized lore directories.
- `Characters/`: Verified character profiles (e.g., `WLF-CHAR-001_Kaelen_v1.3.md`).
- `Unfiltered/`: Raw intake for narrative processing.

### 2.4. `axion-core/` (The Agentic Domain)

> _The inner sanctum of agent intelligence._

- `tools/`: The high-level toolset (e.g., `catalyst_weaver.py`).
- `src/agents/`: Core logic for specialized agents.
- `docs/specs/`: Architectural specifications for agentic tools.

### 2.5. `open-notebook/` & `playground/` (The Research Domain)

> _The laboratory of exploration._

- Used for rapid prototyping, transient notes, and non-governed testing.
- **Rule**: Content intended for production must be migrated to `nova-forge` or `axion-core`.

### 2.6. `_logs/` (The Memory)

- `*_audit.txt`: Compliance and audit records.
- `walkthroughs/`: Immutable records of task completions.
- `agent/`: **Authoritative Agent Brain** (Mirrored). Contains `task.md`, `walkthrough.md`, and operational logs.

---

## III. External Integration

### 3.1. The Crystalline Galaxy (Master Library)

- **Path**: `c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library`
- **Role**: The **Cold Storage** Authority. The immutable source of truth for all Protocols and Modules.
- **Rule**: All "Golden Artifacts" start here.

### 3.2. The Synarche Forge (Runtime Cache)

- **Path**: `Synarche_Workspace/_governance`
- **Role**: The **Hot Runtime**. A "Build Artifact" or projection of the Master Library.
- **Bridge Protocol**: The Workspace is a downstream consumer. Updates in the Galaxy must be synced effectively to the
  Forge.
- **Integration**: `axion-core` tools scan the Galaxy for OSLM discovery.

---

## IV. Operational Mandate

### 4.1. The Zero Entropy Rule

Every file **MUST** reside within its designated domain. "Loose files" in the root directory (Synarche_Workspace) must
be audited and neutralized (moved or deleted) weekly.

### 4.2. Naming Convention Enforcement

- **Directories**: `kebab-case` (Mandatory for all primary domains).
- **Governance**: `DOMAIN.Subsystem.Descriptor.md`.
- **Source Code**: `snake_case` (Python) or `PascalCase` (Frontend Components).

---

## V. Actionable Prompt Packet

### Packet A: Entropy Audit

> "📂 CMD: AUDIT_WORKSPACE --loose-files --root:/"

---

_"Structure is the vessel through which purpose flows."_

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact. GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.

###### **[ARTIFACT END]**
