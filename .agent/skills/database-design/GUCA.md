---
id: GUCA-DAT-001
name: Database Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#DATABASE', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-DAT-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Data.Design          |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `database-design` domain.

### CMD_GENERATE_SCHEMA
- **Description**: Socratic generator for dynamic, domain-aware relational schema design.
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_VALIDATE_SCHEMA
- **Description**: Scan the current schema for normalization errors, missing indexes, and performance bottlenecks.
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_RUN_MIGRATION
- **Description**: Execute a versioned schema migration (dry-run or apply).
- **Action**: Execution.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `db-schema`, `migrate`, `sql-audit`, `explain-plan`

---

## 🛠️ EXECUTORS (RESOURCES)

| Resource | Purpose | Script |
| :--- | :--- | :--- |
| **Validator** | Schema Compliance | `scripts/schema_validator.py` |


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-DAT-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
