# WORKSHOP_MAP.md
>
> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## Genesis Stamp: 2026-07-20 Domain: GVRN State: [ACTIVE] Tags: `OGLN_v15, GVRN, Consolidated` Criticality: Operational

---

###### [ARTIFACT START]

### Block A: The Identification Lock (UIP-V15)

---

| Key | Value | Description |
| :--- | :--- | :--- |
| **Artifact ID** | `GVRN-WORKSHOP-MAP-001` | The Sovereign ID. |
| **Official Name** | `WORKSHOP_MAP.md` | The Filename. |
| **Version** | **v15.0 [OMEGA]** | The Standard. |
| **Domain** | `GVRN` | The Subject. |
| **Celestial Class** | `[PLANET]` | The Weight. |
| **Evolution** | `Omega Ascension` | The Maturity. |
| **Status** | `[ACTIVE]` | The Lifecycle. |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001` | The Network. |

# WORKSHOP_MAP.md: The Cartography of the Synarchy

> **Date**: 2026-07-20 | **Domain**: GVRN (Governance) | **Artifact ID**: GVRN-MAP-001 | **Status**: ACTIVE

## I. The Sovereign Root (The Anchors)

---

The root `Synarche_Workspace/` is the **Governance Domain**. It houses the laws, the enforcers, and the configuration anchors for the entire Monorepo.

* 📄 **[Synarche_Workspace.CODE-workspace](file:///C:/Users/Chris/Synarche_Workspace/Synarche_Workspace.code-workspace)**: The Sovereign Anchor. Contains VS CODE settings (Prettier, Ruff, CSpell).
* ⚙️ **[pyproject.toml](file:///C:/Users/Chris/Synarche_Workspace/pyproject.toml)**: The Python Sentinel (Ruff).
* 🛡️ **[.trunk/](file:///C:/Users/Chris/Synarche_Workspace/.trunk)**: The Meta-Enforcer configuration and linter controls.
* 📖 **[cspell.json](file:///C:/Users/Chris/Synarche_Workspace/cspell.json)**: The Dictionary.
* 📐 **[.markdownlint.cjs](file:///C:/Users/Chris/Synarche_Workspace/.markdownlint.cjs)**: The Markdown Standardizer.
* 📡 **[sonar-project.properties](file:///C:/Users/Chris/Synarche_Workspace/sonar-project.properties)**: The All-Seeing Eye.
* ⚡ **[arise.bat](file:///C:/Users/Chris/Synarche_Workspace/arise.bat)**: The active bootstrapper script that runs weavers and updates manifests.
* 📝 **[task.md](file:///C:/Users/Chris/Synarche_Workspace/task.md)**: The active session task list read by agent runloops on onboarding.

---

## II. The Active Cores (The Engines)

---

These are the operational domains where active development and prototyping occur.

| Domain | Description | Path |
| :--- | :--- | :--- |
| **Axion CORE** | The Governance Engine. Contains the Matrix, Rules, and Audit tools. | `[axion-core/](file:///C:/Users/Chris/Synarche_Workspace/axion-core)` |
| **Nova Forge** | The Creative Engine. Python-based generation, logic, and consolidated prototypes (Tarot Forge). | `[nova_forge/](file:///C:/Users/Chris/Synarche_Workspace/nova_forge)` |
| **Open Notebook** | The Knowledge Engine. Streamlit/SurrealDB research interface (Next.js/Python). | `[open-notebook/](file:///C:/Users/Chris/Synarche_Workspace/open-notebook)` |
| **Where Light Fades** | The Creative Narrative (WLF) narrative and lore files. | `[where_light_fades/](file:///C:/Users/Chris/Synarche_Workspace/where_light_fades)` |
| **Phoenix Rosetta Stone** | The main React/Vite-based UI dashboard. | `[phoenix-rosetta-stone/](file:///C:/Users/Chris/Synarche_Workspace/phoenix-rosetta-stone)` |
| **FDE Engine** | Folio Decay Engine runtime, rollback files, and translation layers. | `[fde_engine/](file:///C:/Users/Chris/Synarche_Workspace/fde_engine)` |

---

## III. Monorepo Packages (Shared Subsystems)

---

Shared internal CODE packages residing inside `packages/`:

* 📦 **[nexus-signalbus/](file:///C:/Users/Chris/Synarche_Workspace/packages/nexus-signalbus)**: Shared signal bus architecture.
* 📦 **[supabase/](file:///C:/Users/Chris/Synarche_Workspace/packages/supabase)**: Shared database interfaces.
* 📦 **[synarche_python_logger/](file:///C:/Users/Chris/Synarche_Workspace/packages/synarche_python_logger)**: Standardized logger module.

---

## IV. The Governance Archive (The Library)

---

Where standards, logs, and memories are stored.

* 📜 **[_governance/](file:///C:/Users/Chris/Synarche_Workspace/_governance)**: Protocol documentation, Templates, and Standards.
    * `00_Codex/`: The heart of the system (Phoenix Law).
    * `01_Registries/`: Master Inventory, Artifact Registry, redirects, Scratch Inventory, and path mapping.
    * `02_Protocols/`: Operational playbooks (AOPs), tuning guides (UMBs), and directory standards.
    * `08_Documentation/`: General documentation and analyses.
    * `incoming/`: Inbound documents and raw specification files.
    * `_archive/recovery/`: System backups, recovery submodules, and documentation history.
* 📝 **[_logs/](file:///C:/Users/Chris/Synarche_Workspace/_logs)**: Operational logs and CSL entries.
    * `Sentinel_Reports/`: Cleanly merged logs from the Sentinel audit suite.
    * `refactoring/`: Stashed refactoring logs.
    * `tmp/`: Temporary run logs and TEST outputs.

---

## V. The Legacy Vault (The Shadow)

---

Located outside the workspace to prevent cognitive dissonance:
* `c:/Users/Chris/_Desktop_Vault`
    * **_LEGACY_ARCHIVE**: Where old tools, graphs, and extensions go to rest.

---

## VI. Topology Visual (Clean State)

---

```text
Synarche_Workspace/
├── .agent/                    # 🧠 THE MIND (Agent memory & workflows)
├── .github/                   # CI Actions configuration
├── .vscode/                   # VS Code configuration
├── _governance/               # 📜 THE LAW (Phoenix law, Master Registries, blueprints)
│   ├── _archive/recovery/     # Backups, recovery submodules, and doc history
│   └── incoming/              # Inbound raw specifications
├── _logs/                     # Canonical logs, session records, and manifests
│   ├── Sentinel_Reports/      # Audit reports
│   └── tmp/                   # Temp runs and test scripts
├── axion-core/                # ⚙️ THE ENGINE (Governance core in TypeScript)
│   ├── data/                  # Graph data and JSON nodes
│   ├── supabase/              # Database migrations and schema mappings
│   └── tools/                 # Workspace scripts
├── nova_forge/                # 🧪 THE LAB (Prototypes & Tarot Forge)
│   └── prototypes/            # Consolidated playground and design-system builds
├── open-notebook/             # Knowledge engine (Streamlit & Next.js)
│   └── surreal_data/          # SurrealDB database files (no space in path)
├── packages/                  # Shared monorepo modules
├── phoenix-rosetta-stone/     # Frontend UI app (React/Vite)
├── where_light_fades/         # 📖 THE NARRATIVE (lore, narratives, scripts)
├── arise.bat                  # Root bootstrapper
├── WORKSHOP_MAP.md            # YOU ARE HERE
└── task.md                    # Active task list
```

---

### Block D: Standardized Synergy Block (The Loom Signature)

---

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.

###### [ARTIFACT END]

## Reciprocal Links

- [walkthrough 7.19.2026.md](_logs/walkthrough 7.19.2026.md)
