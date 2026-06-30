---
id: GUCA-DOC-001
name: Documentation Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#DOCUMENTATION', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-DOC-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Doc.Templates        |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `documentation-templates` domain.

### CMD_GENERATE_README
- **Description**: Socratic generator for standardized project README based on [AOP.md](file:///c:/Users/Chris/_Desktop_Vault/dev/rosetta-stone_-the-phoenix-protocol-(cast)/.agent/skills/documentation-templates/AOP.md).
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_GENERATE_ADR
- **Description**: Template generator for standardized Architectural Decision Records (ADR).
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_AUDIT_DOCS
- **Description**: Scan the the project documentation for structure compliance, broken links, and missing sections.
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `readme`, `adr`, `gen-docs`, `audit-docs`


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-DOC-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
