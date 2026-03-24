# GUCA-IDE-SENTINEL-001_TheIDEIntegritySentinel_v11.0.md

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                                                          | Description       |
| :---------------- | :------------------------------------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-GUCA-IDE-SENTINEL-001-THEIDEINTEGRITYSENTINEL-V11.0-001` | The Sovereign ID. |
| **Official Name** | `GUCA-IDE-SENTINEL-001_TheIDEIntegritySentinel_v11.0.md`       | The Filename.     |
| **Version**       | **v13.0 [OMEGA]**                                              | The Standard.     |
| **Domain**        | `GVRN`                                                         | The Subject.      |
| **Status**        | `[ACTIVE]`                                                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`                                  | The Network.      |

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

# GUCA-IDE-SENTINEL-001: The IDE Integrity Sentinel

**Tags:** `OGLN_v11`, `Sentinel`, `VSCode`, `Integrity`

---

### I. Universal Identification & Provenance (The Vector Signature)

#### The Chronos Lock & Axiomatic Metadata Layer

| Field | Value |

`axion-core/tools/ide_sentinel.py`

## II. Core Purpose & Objective

**Core Purpose:** To audit and enforce VS Code configuration (Extensions, Settings, Formatters) for Phoenix-Class
coherence. **Module Objective:** Ensure that every developer environment is identical, preventing configuration drift
and ensuring "Zero Entropy" in development workflows.

## III. Operational Mechanism

The Sentinel scans the `.vscode/` directory of the current workspace.

### 3.1. Audit Vectors

1. **Extensions Vector:** Checks `extensions.json` for mandatory extensions (e.g., `charliermarsh.ruff`).
2. **Settings Vector:** Checks `settings.json` for:
   - `editor.formatOnSave`: Must be `true`.
   - `editor.defaultFormatter`: Must be `charliermarsh.ruff`.
   - `python.defaultInterpreterPath`: Must point to local `.venv`.
3. **Code Actions Vector:** Ensures `source.organizeImports` is enabled on save.

## IV. Usage

### 4.1. Audit (Dry Run)

```powershell
python axion-core/tools/ide_sentinel.py
```

Reports system entropy without making changes.

### 4.2. Remediation (Fix)

```powershell
python axion-core/tools/ide_sentinel.py --fix
```

Automatically updates `settings.json` and `extensions.json` to match the standard.

## V. Actionable Prompt Packet

**CMD: AUDIT_IDE_CONFIG**

> "Run the IDE Sentinel to check for configuration drift. Report any entropy."

**CMD: ENFORCE_IDE_CONFIG**

> "Run the IDE Sentinel with `--fix` to strictly enforce the Phoenix standard configuration."

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact. GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.

###### **[ARTIFACT END]**
