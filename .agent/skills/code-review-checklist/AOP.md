---
id: AOP-REV-001
name: Code Review Operational Playbook
version: v2.1 [GOLD]
type: OPERATIONAL_PLAYBOOK
status: [ACTIVE]
tags: ['#AOP', '#PROCESS', '#CODEREVIEW', '#AUDIT']
---

# 📖 CODE REVIEW PLAYBOOK | AOP-REV-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Audit.Review         |
| **State**      | ⚡ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC PROCESSES

### 1. The Audit Ritual (MANDATORY)

Review and verify the code against these checkpoints before completion:

- **Correctness**: Evidence of success (build, tests, or manual logic check).
- **Security**: Input validation and secret scanning.
- **Performance**: No N+1 queries or memory leaks.
- **Standards**: Does it follow the [Clean Code AOP](file:///c:/Users/Chris/_Desktop_Vault/dev/rosetta-stone_-the-phoenix-protocol-(cast)/.agent/skills/clean-code/AOP.md)?

### 2. AI-Specific Verification

Scrutinize AI-generated output for unique failure modes:
- **Hallucinations**: Cross-reference library APIs with fresh documentation.
- **Sanitization**: Ensure structured prompting and output sanitization for critical sinks.
- **Partial Updates**: Check if all dependent files were modified (Ghost Updates).

### 3. Review Feedback Standards

Use visual markers to prioritize feedback:
- 🔴 **BLOCKING**: Security flaws, breaking changes, or critical bugs.
- 🟡 **IMPROVEMENT**: Performance optimizations, best practices.
- 🟢 **NIT**: Style guide violations, minor typos.
- ❓ **QUESTION**: Clarifying logic or intent.

---

## 🔍 ACTIONABLE HEURISTICS

- **[TRACEABILITY]**: If an implementation deviates from the plan, flag it as a risk.
- **[EARLY EXIT]**: Flag deep nesting (>2 levels) for refactoring to early returns.
- **[NAMING]**: Flag generic names (`data`, `item`, `val`) for intent-revealing alternatives.

---

`[OMNI-ARTIFACT-ANCHOR] ID: AOP-REV-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
