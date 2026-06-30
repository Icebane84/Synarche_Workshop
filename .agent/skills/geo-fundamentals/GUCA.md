---
id: GUCA-GEO-001
name: GEO Fundamentals Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#GEO', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-GEO-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Engineering.GEO      |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `geo-fundamentals` domain.

### CMD_GEO_AUDIT
- **Description**: Audit the project for AI citation readiness based on [AOP.md](file:///c:/Users/Chris/_Desktop_Vault/dev/rosetta-stone_-the-phoenix-protocol-(cast)/.agent/skills/geo-fundamentals/AOP.md).
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/auditCommands.ts`
- **Script**: `scripts/geo_checker.py`

### CMD_GEN_FAQ
- **Description**: Socratic generator for FAQ sections with JSON-LD schema (FAQPage).
- **Action**: Synthesis.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_ENTITY_SYNC
- **Description**: Verify entity consistency across major brand profiles (LinkedIn, Wikipedia, Homepage).
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `geo-audit`, `gen-faq`, `entity-sync`


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-GEO-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
