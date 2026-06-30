---
id: GUCA-BRN-001
name: Brainstorming Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#BRAINSTORMING', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-BRN-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Sync.Brainstorm      |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `brainstorming` domain.

### CMD_GENERATE_QUESTIONS
- **Description**: Socratic generator for dynamic, domain-aware user clarification.
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_STATUS_BOARD
- **Description**: Display a real-time status tracker for all active operations.
- **Action**: UI/Status.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_SYNC_MENTAL_MODEL
- **Description**: Synthesize the "Mental Model" summary to preserve context across turns.
- **Action**: Context Preservation.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `brainstorm`, `ask`, `status`, `sync-context`


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-BRN-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
