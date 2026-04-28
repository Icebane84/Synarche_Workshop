# /templates — The Loom Substrate

> **"A blueprint is not a thing. It is the intention that precedes the thing."**

---

## Purpose

This directory holds **inert structural blueprints** — template definitions used by the Substrate Forge
(`forge/substrate_forge.py`) to generate canonical Python modules, governance artifacts, and workflow documents. Nothing
here executes. Nothing here is imported. Templates are raw material, not products.

---

## What Belongs Here

| Type                                 | Example                  | Governance                  |
| :----------------------------------- | :----------------------- | :-------------------------- |
| Universal Module Blueprints (UMBs)   | `UMB-GENSEED-001_*.md`   | `GVRN.Assembler.Core`       |
| Workflow Blueprint Templates (SELTs) | `SELT-UWB-001_*.md`      | `AOP-PGPS-001`              |
| Artifact JSON schemas                | `artifact_template.json` | `GVRN.Style.001`            |
| Emoji/Protocol bundles               | `AOP-EMOJI-001_*.md`     | `GVRN.Protocol.Scaffolding` |

### Sub-directories

- **`blocks/`** — Reusable Markdown transclusion blocks (document fragments, not full templates)
- **`_archive/`** — Retired templates. Read-only. Never delete — only archive.

---

## What Does NOT Belong Here

- ❌ Completed, generated Python modules → they live in `src/` or `forge/engines/`
- ❌ Executable scripts → they live in `forge/` or `lab/`
- ❌ Governance law artifacts → they live in `_governance/`
- ❌ Any file with runtime imports

---

## How Templates Are Used

```
UMB-*.md  →  substrate_forge.py  →  src/[domain]/[module].py
SELT-*.md →  Agent workflow execution (read by AI, not Python)
```

The Substrate Forge reads UMB files, extracts metadata (class name, methods, rationale), and scaffolds the corresponding
Python implementation. The AI agent then fills in the logic.

---

## Governance

| Governing artifact                             | Location                      |
| :--------------------------------------------- | :---------------------------- |
| `GVRN.Assembler.Core`                          | `_governance/05_Assembler/`   |
| `AOP-PGPS-001` (Genesis Presentation Standard) | `_governance/03_AvatarSuite/` |
| `GVRN.Style.001` (Coding Standards)            | `_governance/02_GVRN/`        |

---

`[OMNI-ARTIFACT-ANCHOR] ID: LOOM.Templates.SignPost VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-24`
