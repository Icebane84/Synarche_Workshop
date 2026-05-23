# /standards — The Law Substrate

> **"Standards are not suggestions. They are the immutable grammar of the system."**

---

## Purpose

---

---CORE

This directory is the **single source of truth for all linter, formatter, and type-checker configuration** for Axion
CORE. Every TOOL that enforces CODE quality across the workspace reads its rules from here. There is intentionally no
executable CODE in this directory — only law.

---

## Configuration Files

---

| File                       | TOOL                | What it governs                                    |
| :------------------------- | :------------------ | :------------------------------------------------- |
| `pyproject.toml`           | Ruff, Black, pyTEST | Python formatting, linting, TEST configuration     |
| `pyrefly.toml`             | Pyrefly             | Python type-checking configuration and import root |
| `mypy.ini`                 | mypy                | Static type analysis for Python                    |
| `eslint.config.mjs`        | ESLint              | TypeScript/JavaScript linting rules                |
| `.prettierrc`              | Prettier            | TypeScript/JSON/Markdown formatting                |
| `markdownlint.json`        | markdownlint        | Markdown structure enforcement                     |
| `.markdownlint.cjs`        | markdownlint (CJS)  | Extended markdown rules                            |
| `cspell.jsonc`             | CSpell              | Spell-checking for all file types                  |
| `sonar-project.properties` | SonarQube           | Static analysis and CODE quality gates             |

|

- ***

## Law of Primacy

---

These configuration files take **absolute precedence** over any TOOL defaults. If a TOOL is run anywhere in the
workspace, it must resolve its config to this directory. Any TOOL running without referencing these files is operating
outside governance.

---

## What Does NOT Belong Here

---

- ❌ Python source CODE of any kind
- ❌ TEST files
- ❌ Documentation (`.md` narrative files) — those live in `_governance/08_Documentation/`
- ❌ Per-module `.pylintrc` or local overrides — all rules are centralised here

---

## Governance

---

| Governing artifact                  | Location               |
| :---------------------------------- | :--------------------- |
| `GVRN.Style.001` (Coding Standards) | `_governance/02_GVRN/` |
| `GVRN.Guide.Coding.md`              | `_governance/` (root)  |
| `CODING_HANDBOOK.md`                | `_governance/` (root)  |

---

`[OMNI-ARTIFACT-ANCHOR] ID: GVRN.Standards.SignPost VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-24`
