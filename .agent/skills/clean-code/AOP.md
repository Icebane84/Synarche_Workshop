---
id: AOP-CLN-001
name: Clean Code Operational Playbook
version: v2.1 [GOLD]
type: OPERATIONAL_PLAYBOOK
status: [ACTIVE]
tags: ['#AOP', '#PROCESS', '#CLEANCODE', '#STANDARDS']
---

# 📖 CLEAN CODE PLAYBOOK | AOP-CLN-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Code.Clean           |
| **State**      | ⚡ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC PROCESSES

### 1. The Naming Ritual

Reveal intent with every identifier:

- **Variables**: `userCount` (not `n`), `isAuthorized` (not `auth`).
- **Functions**: `fetchUserById()` (not `user_getter()`).
- **Booleans**: `hasPermission`, `canEdit`, `shouldSync` (always question form).

### 2. Implementation Density Workflow

The AI must optimize for the highest information-to-word ratio:

- **Halt Tutorials**: Write the code directly. No "First we import..." or "Then we add...".
- **Self-Documenting**: Let the code explain itself through clear names and logic.
- **Boy Scout Rule**: Leave any file you edit cleaner than you found it (refactor small dissonances).

### 3. Verification & Self-Check

MANDATORY checklist before completing any code change:

- [ ] Requirements met exactly?
- [ ] All dependent files updated (imports/signatures)?
- [ ] No regression in linting/TS?
- [ ] Guard clauses used for flat flow?
- [ ] Side effects avoided/isolated?

---

## 🔍 ACTIONABLE HEURISTICS

- **[LIMITS]**: If a function exceeds 20 lines, it MUST be split into smaller, focused units.
- **[DEPTH]**: Maximum nesting depth is 2 levels. Use early returns (Exit Early) to flatten the logic.
- **[SHARED]**: When editing a shared service or component, check all files that import it before finishing.

---

`[OMNI-ARTIFACT-ANCHOR] ID: AOP-CLN-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
