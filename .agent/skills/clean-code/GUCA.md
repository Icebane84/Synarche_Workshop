---
id: GUCA-CLN-001
name: Clean Code Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#CLEANCODE', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-CLN-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Code.Clean           |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `clean-code` domain.

### CMD_REFACTOR_FILE
- **Description**: Automatically refactor a file to adhere to SRP, DRY, and KISS principles.
- **Action**: Refactor.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_AUDIT_CLEANLINESS
- **Description**: Scan the project for "Code Smells" and pragmatic standard violations.
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_APPLY_BOY_SCOUT
- **Description**: Identify and apply small, non-breaking improvements to the current file.
- **Action**: Refactor.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `refactor`, `clean`, `audit-code`, `boy-scout`


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-CLN-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
