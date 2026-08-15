---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `README` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# README.md

> **Domain**: GVRN **Evolution**: Omega Ascension **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

### **Block A: The Identification Lock (UIP-V13)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `GVRN-README-001`             | The Sovereign ID. |
| **Official Name**   | `README.md`                   | The Filename.     |
| **Version**         | **v13.1 [OMEGA]**             | The Standard.     |
| **Domain**          | `GVRN`                        | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Omega Ascension`             | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

# Scripts Documentation

## export_docs.py

Consolidates markdown documentation files for use with ChatGPT or other platforms with file upload limits.

### What It Does

- Scans all subdirectories in the `docs/` folder
- For each subdirectory, combines all `.md` files (excluding `index.md` files)
- Creates one consolidated markdown file per subdirectory
- Saves all exported files to `doc_exports/` in the project root

### Usage

```bash
# Using Makefile (recommended)
make export-docs

# Or run directly with uv
uv run python scripts/export_docs.py

# Or run with standard Python
python scripts/export_docs.py
```

### Output

The script creates `doc_exports/` directory with consolidated files like:

- `getting-started.md` - All getting-started documentation
- `user-guide.md` - All user guide content
- `features.md` - All feature documentation
- `development.md` - All development documentation
- etc.

Each exported file includes:

- A main header with the folder name
- Section headers for each source file
- Source file attribution
- The complete content from each markdown file
- Visual separators between sections

### Example Output Structure

```markdown
# Getting Started

This document consolidates all content from the getting-started documentation folder.

---

## Installation

_Source: installation.md_

[Full content of installation.md]

---

## Quick Start

_Source: quick-start.md_

[Full content of quick-start.md]

---
```

### Notes

- The `doc_exports/` directory is gitignored and safe to regenerate anytime
- Index files (`index.md`) are automatically excluded
- Files are sorted alphabetically for consistent output
- The script handles subdirectories only (ignores files in the root `docs/` folder)

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact. GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
