---
id: GUCA-GAM-001
name: Game Development Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#GAMEDEV', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-GAM-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Game.Dev             |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `game-development` domain.

### CMD_GEN_GDD

- **Description**: Socratic generator for standardized Game Design Documents based on [AOP.md](file:///c:/Users/Chris/_Desktop_Vault/dev/rosetta-stone_-the-phoenix-protocol-(cast)/.agent/skills/game-development/AOP.md).
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_SCAFFOLD_ENGINE

- **Description**: Scaffold a new game engine project (Phaser, Three.js, PixiJS) with standardized Phoenix structure.
- **Action**: Creation.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_AUDIT_PROFILER

- **Description**: Performance audit for frame budget (16.67ms), draw calls, and memory leaks.
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `gdd`, `scaffold-game`, `profile-game`

### 🛡️ Final Verification

- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-GAM-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
