---
id: GUCA-API-001
name: API Design Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#API', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-API-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Infra.API            |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `api-patterns` domain.

### CMD_DESIGN_RESOURCE
- **Description**: Design a REST-compliant resource structure for a given domain entity.
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_SELECT_API_STYLE
- **Description**: Evaluate requirements and select the optimal API protocol (REST/GraphQL/tRPC).
- **Action**: Decision Architecture.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_AUDIT_API
- **Description**: Perform a security and DX audit on an existing API endpoint schema.
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `api-design`, `endpoint-audit`, `style-select`, `resource-map`

---

## 🛠️ EXECUTORS (SCRIPTS)

| Script | Purpose | Command |
| :--- | :--- | :--- |
| `scripts/api_validator.py` | API endpoint validation | `python scripts/api_validator.py <project_path>` |


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-API-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
