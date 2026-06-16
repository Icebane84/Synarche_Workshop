**Location:** .agent/substrate/rules/README.md

# 📜 Sovereign Rules & Compliance (.agent/substrate/rules)

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                       | Description       |
| :---------------- | :-------------------------- | :---------------- |
| **Artifact ID**   | `SYNG.RULES.Sovereign`      | The Sovereign ID. |
| **Official Name** | `README.md`                 | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**           | The Standard.     |
| **Domain**        | `SUBSTRATE`                 | The Subject.      |
| **Status**        | `[ACTIVE]`                  | The Lifecycle.    |
| **Relations**     | `REF: GVRN.Master.Registry` | The Network.      |

---

Authoritative protocols and linter configurations that enforce the Synarche aesthetic and logical standards.

## ⚖️ Rule Books

- **[GEMINI.md](GEMINI.md)**: The High Gate Sovereign Rules (Root Authority).
- **[SOUL.md](SOUL.md)**: The Sovereign Identity and Continuity protocols.
- **[SELF-IMPROVEMENT.md](SELF-IMPROVEMENT.md)**: The "Zero Entropy" learning and evolution protocols.
- **[GVRN-ABILITY-MAP.md](GVRN-ABILITY-MAP.md)**: Mapping of agent abilities to linter and tool configurations.
- **[LEARNING.md](LEARNING.md)**: Standards for the `_governance/06_Learning` subsystem.

## 🔍 Alignment & Linting

> **Canonical Source of Truth:** `axion-core/standards/`
>
> All linting, type-checking, and formatting rules are centralized in the
> `axion-core/standards/` directory. Do NOT create project-local config files.

- **ESLint (All Languages + Markdown)**: [`axion-core/standards/eslint.config.mjs`](../../../axion-core/standards/eslint.config.mjs)
  - Phoenix governance rules (PF001-PF032) via `eslint-plugin-phoenix`
  - TypeScript strict typing rules
  - React/Vite rules for frontend projects
- **Mypy (Python)**: [`axion-core/standards/mypy.ini`](../../../axion-core/standards/mypy.ini)
- **CSpell (Spelling)**: [`axion-core/standards/cspell.jsonc`](../../../axion-core/standards/cspell.jsonc)
- **Prettier (Formatting)**: [`axion-core/standards/.prettierrc`](../../../axion-core/standards/.prettierrc)

---

`[OMNI-ANCHOR] ID: SYNG.RULES.Sovereign VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-03-23`
