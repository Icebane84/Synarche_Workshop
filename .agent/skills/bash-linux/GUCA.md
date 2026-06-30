---
id: GUCA-BSH-001
name: Bash & Linux Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#BASH', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-BSH-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Infra.Bash           |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `bash-linux` domain.

### CMD_EXECUTE_BATCH
- **Description**: Run a batch of shell commands with comprehensive error trapping.
- **Action**: Execution.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_AUDIT_TERMINAL
- **Description**: Scan the current shell environment for configuration drift or security leaks.
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_PROCESS_TEXT
- **Description**: Apply high-density text transformations (grep/sed/awk) to a stream of data.
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `sh`, `bash`, `shell-exec`, `grep-all`, `find-all`


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-BSH-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
