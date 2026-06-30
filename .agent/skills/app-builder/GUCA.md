---
id: GUCA-APP-001
name: App Builder Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#ORCHESTRATOR', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-APP-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Sys.AppBuilder       |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `app-builder` domain.

### CMD_SCAFFOLD_PROJECT
- **Description**: Initialize a new project with the target tech-stack and directory structure.
- **Action**: Synthesis & Creation.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_IDENTIFY_STACK
- **Description**: Analyze natural language requirements to determine the optimal stack.
- **Action**: Decision Logic.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_COORDINATE_AGENTS
- **Description**: Orchestrate a sequence of specialist agents to build a specific feature.
- **Action**: Orchestration.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `scaffold`, `build-app`, `orchestrate`, `stack-select`

---

## 🛠️ EXECUTORS (RESOURCES)

| Resource | Purpose | Link |
| :--- | :--- | :--- |
| **Templates** | Quick-start scaffolding | `.agent/skills/app-builder/templates/` |


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-APP-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
