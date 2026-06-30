---
id: GUCA-REV-001
name: Code Review Command Set
version: v2.1 [GOLD]
type: COMMAND_DEFINITION
status: [ACTIVE]
tags: ['#GUCA', '#CODEREVIEW', '#COMMANDS', '#SOVEREIGN']
---

# 🛠️ COMMAND ARCHITECTURE | GUCA-REV-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Audit.Review         |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC COMMANDS

Commands mapped to the `code-review-checklist` domain.

### CMD_AUDIT_SECURITY
- **Description**: Scan the current code for security vulnerabilities, hardcoded secrets, and sanitization misses.
- **Action**: Security Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_GENERATE_REVIEW
- **Description**: Automatically generate a constructive code review based on the [AOP.md](file:///c:/Users/Chris/_Desktop_Vault/dev/rosetta-stone_-the-phoenix-protocol-(cast)/.agent/skills/code-review-checklist/AOP.md) checkpoints.
- **Action**: Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

### CMD_VERIFY_LLM_SAFETY
- **Description**: Specific audit for AI-generated code safety, hallucination checks, and structured prompting.
- **Action**: Safety Audit.
- **Registry**: `src/services/commands/definitions/utilityCommands.ts`

---

## ⚡ OPERATIONAL ALIASES

- `review`, `audit-security`, `check-safety`, `verify-logic`


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---

`[OMNI-ARTIFACT-ANCHOR] ID: GUCA-REV-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
