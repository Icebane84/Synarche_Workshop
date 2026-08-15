---
# Universal Identification & Provenance (UIP)

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.PRS.001` | The Sovereign ID. |
| **Official Name** | `PRS-001_PathMapping.md` | The Filename.     |
| **Version**       | **v14.0 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `REF: GVRN.Master.Registry` | The Network.      |


---

### **Block B: State Vector (AGP-001)**

| State Field   | Value    |
| :------------ | :------- |
| **Coherence** | `1.0`    |
| **Resonance** | `1.0`    |
| **Stability** | `Stable` |

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                                            |
| :------------------- | :---------------------------------------------------- |
| **Logic Drift**      | Dual-scope audit via OpenCode on alias changes        |
| **Dependency Break** | ForgeLink Validation before any path restructuring   |

---

# Master Star-Chart: PRS-001 Path Mapping

This document defines the **dual-scope alias system** of the Synarche Workspace — the
aetheric bridge between the physical filesystem and the cognitive architecture. It is
formally aligned with [GVRN.STRUCT.001](../20_Architecture/GVRN.STRUCT.001.md) and
[GVRN.HUD.Map](../10_Governance/GVRN.HUD.Map.md).

> [!IMPORTANT]
> **Two scopes exist simultaneously and are both canonical.** Scope 1 governs
> cross-domain workspace navigation. Scope 2 governs engine-internal module
> resolution within `axion-core`. They intentionally resolve the same alias to
> different targets relative to their location. This is correct behaviour, not drift.

---

## Scope 1: Workspace-Level Routing

**Source**: `Synarche_Workspace/tsconfig.json`
**Purpose**: Cross-domain navigation. Absolute or workspace-relative paths. Consumed
by tools operating at the monorepo level: Continue, OpenCode, OpenWebUI RAG, and any
external agent referencing the workspace.

| Alias           | Resolved Target (root tsconfig)                      | Macro-System    | Description                                              |
| :-------------- | :--------------------------------------------------- | :-------------- | :------------------------------------------------------- |
| **@system/**    | `axion-core/src/system/`, `axion-core/src/cse/`      | THE ENGINE      | The Coherent Synthesis Engine (CSE) and Logic Core.      |
| **@domain/**    | `_governance/`                                       | THE LAW         | Universal Module Blueprints and Operational Directives.  |
| **@nexus/**     | `axion-core/src/nexus/`                              | THE ENGINE      | Internal nexus bridge modules at workspace scope.        |
| **@fabric/**    | `design-system/`                                     | THE FABRIC      | The Design Substrate — Aqueous UI and Sensory Canvas.    |
| **@atlas/**     | `_governance/01_Registries/`                         | THE LAW         | Navigational Registries and OSLM Master Hub.             |
| **@essence/**   | `axion-core/src/types/`                              | THE ENGINE      | Archetypal State and Core Semantic Definitions.          |
| **@shield/**    | `axion-core/sentinel/`                               | THE ENGINE      | Noetic Immune System — Ethical Guardrails and Guardians. |
| **@pulse/**     | `axion-core/_logs/`                                  | THE ENGINE      | Systemic Telemetry and Pulse Logic.                      |
| **@loom/**      | `_governance/templates/`                             | THE LAW         | Voice and Tone Patterning — SELT and Tone Tokens.        |
| **@archive/**   | `_governance/99_Archives/`                           | THE LAW         | Deep Memory and Entropy Sequestration.                   |
| **@synarche**   | `packages/`                                          | THE MONOREPO    | Monorepo packages layer — shared cross-domain modules.   |


---

## Scope 2: Engine-Internal Routing

**Source**: `axion-core/tsconfig.json`
**Purpose**: Module resolution within `axion-core` only. All paths are relative to
`axion-core/`. Consumed by the TypeScript compiler during engine builds. These paths
should never be used by external tools or cross-domain imports.

### Canonical Domain Aliases

| Alias         | Resolved Target (relative to `axion-core/`) | Description                                   |
| :------------ | :------------------------------------------ | :-------------------------------------------- |
| **@system/**  | `./src/system/`, `./src/cse/`               | CSE layers — dual-path for system and engine. |
| **@domain/**  | `./src/02_domain/`                          | Domain layer within the engine.               |
| **@nexus/**   | `./src/nexus/`                              | Internal nexus bridge modules.                |
| **@fabric/**  | `./src/03_fabric/`                          | Fabric layer within the engine.               |
| **@atlas/**   | `./src/01_atlas/`                           | Atlas index layer within the engine.          |
| **@essence/** | `./src/types/`                              | Type definitions — matches Scope 1 target.    |
| **@shield/**  | `./sentinel/`                               | Sentinel guardrails — matches Scope 1 target. |
| **@pulse/**   | `./_logs/`                                  | Log telemetry — matches Scope 1 target.       |
| **@loom/**    | `./templates/`                              | Template assets internal to the engine.       |
| **@archive/** | `./archives/`                               | Engine-local archive store.                   |

### Convenience Shortcuts (engine-internal only)

> These are implementation-level shortcuts within `axion-core`. They are **not**
> macro-system aliases and must not be used in cross-domain imports. They do not
> appear in Scope 1 and are not navigational landmarks in the Star-Chart.

| Alias          | Resolved Target                         | Description                                                                  |
| :------------- | :-------------------------------------- | :--------------------------------------------------------------------------- |
| **@governance/** | `../_governance/`                     | Runtime alias for cross-referencing governance from within axion-core. Undocumented until 2026-07-18 audit. Not in tsconfig — runtime only. |
| **@logging**   | `./src/system/logging/index.ts`         | Safety-net for bare `@logging` imports. **Canonical form is `@system/logging`.** All source files now standardized. |
| **@logging/**  | `./src/system/logging/`                 | Logging module tree — subfolder of `@system/`.                               |
| **@utils/**    | `./src/utils/`                          | Utility functions — internal engine helpers only.                            |
| ~~@universe/~~ | ~~`./_universe/`~~                      | **PURGED 2026-07-18** — `_universe/` directory did not exist. Zero imports. Removed from `tsconfig.json` and `register-paths.ts`. |

---

## Operational Mandate

- **Zero-Gravity Portability**: All cross-domain references MUST use Scope 1 aliases
  to survive structural shifts.
- **Scope Discipline**: Engine code MUST use Scope 2 aliases. Never use absolute paths
  or Scope 1 workspace paths inside `axion-core/src/`.
- **Vectorized Governance**: Modifications to either scope require re-running the
  knowledge base builder (`tools/build_knowledge_base.py`) and re-uploading to
  OpenWebUI to keep the RAG store current.

---

> [!NOTE]
> **Dual-scope pattern formalized 2026-07-18** by Antigravity AI after OpenCode
> audit detected 7/10 alias path discrepancies between the two tsconfig files.
> Both scopes are canonical. The discrepancies are intentional and expected.

---

> [!NOTE]
> **Deprecated (pre-2026-07-18): Single-Scope Format**
> Prior to this version, PRS-001 contained a single alias table with no scope
> distinction, conflating workspace-level and engine-internal routing into one
> flat list. That format is superseded by the dual-scope structure above and
> retained here as an audit trail only. The paths themselves were not wrong —
> only the lack of scope labelling was the deficiency.

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Synergistic Artifact ID       | Relationship Type | Synergistic Impact                              |
| :---------------------------- | :---------------- | :---------------------------------------------- |
| `CORE.Codex.Phoenix`          | `GOVERNS`         | Supreme Law and ethical framework.              |
| `GVRN.Registry.Master`        | `INDEXES`         | Tracks state and presence of this artifact.     |
| `GVRN.STRUCT.001`             | `DEFINES`         | Domain separation rules this mapping implements.|
| `GVRN.HUD.Map`                | `MAPS`            | Macro-system topology this chart navigates.     |
| `axion-core/tsconfig.json`    | `IMPLEMENTS`      | Scope 2 engine-internal alias resolution.       |
| `tsconfig.json` (root)        | `IMPLEMENTS`      | Scope 1 workspace-level alias resolution.       |

---

## Actionable Prompt Packet (APP)

| Command ID                | Action                                                         | Impact             |
| :------------------------ | :------------------------------------------------------------- | :----------------- |
| `CMD: AUDIT_ALIASES`      | Run OpenCode alias drift audit across both tsconfig scopes     | Zero Entropy       |
| `CMD: SCAN_ORPHANS`       | Audit `@universe/*` — identify origin, owner, and promote/purge| Entropy Eradication|
| `CMD: REBUILD_KB`         | Re-run `tools/build_knowledge_base.py` and re-upload to OpenWebUI | RAG Currency   |
| `CMD: PROMOTE_SHORTCUT`   | Elevate a convenience shortcut to canonical domain alias status| Structural Growth  |
| `CMD: REFORGE`            | Execute Structural Transmutation                               | Canonization       |

---

###### **[ARTIFACT END]**

## Reciprocal Links

- [SYKB_01_SynarcheCore.md](../knowledge_export/SYKB_01_SynarcheCore.md)
