---
id: GUCA-I18-001
name: i18n & Localization Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#I18N', '#L10N', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-I18-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Engineering.i18n     |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `i18n-localization` domain.

### CMD_I18N_AUDIT
- **Description**: Audit the project for hardcoded strings and missing translations based on [AOP.md](file:///c:/Users/Chris/_Desktop_Vault/dev/rosetta-stone_-the-phoenix-protocol-(cast)/.agent/skills/i18n-localization/AOP.md).
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/auditCommands.ts`
- **Script**: `scripts/i18n_checker.py`

### CMD_EXTRACT_STRINGS
- **Description**: Automatically extract hardcoded strings from source into `common.json` schema.
- **Action**: Creation.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_SYNC_LOCALES
- **Description**: Synchronize structure across all locale JSON files to ensure key parity.
- **Action**: Sync.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `i18n-audit`, `i18n-extract`, `i18n-sync`


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-I18-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
