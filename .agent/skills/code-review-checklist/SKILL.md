---
id: UMB-REV-001
name: Code Review Checklist
version: v2.1 [GOLD]
type: SKILL_LOGIC
status: [ACTIVE]
tags: ['#CODEREVIEW', '#AUDIT', '#SECURITY', '#QUALITY', '#SOVEREIGN']
---

# 🧠 CODE REVIEW | UMB-REV-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Audit.Review         |
| **State**      | 🌟 GOLD STANDARD          |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V2.0-SOVEREIGN]          |

---

## 🎭 SOVEREIGN LOGIC

Code review is the shield of systemic integrity. We audit implementations for correctness, security vulnerabilities, performance regressions, and adherence to pragmatic coding standards. AI-generated code must be scrutinized with extra focus on hallucinations and edge cases.

### Principles of Cognitive Review

1.  **Sovereign Integrity**: Ensure the code does exactly what it is supposed to do without side effects.
2.  **Security-First Audit**: Treat all user inputs as untrusted. Audit for injection, XSS, and credential leaks.
3.  **Performance Checkpoint**: Optimize for N+1 query prevention and bundle size efficiency.
4.  **Chain of Thought**: Verify that the logic follows a clear, maintainable path (No magic numbers or deep nesting).

---

## 🛠️ BLUEPRINT STANDARDS

### Anti-Pattern Triggers

- **[RED]**: Magic Numbers, Hardcoded Secrets, Infinite Loops, `any` Types.
- **[AMBER]**: Deep Nesting (> 2 levels), Missing Error Handling, Large Functions (> 20 lines).
- **[GREEN]**: Early Returns, Proper Typing, Named Constants, Structured Prompting.

---

## 🔍 QUALITY CONSTRAINTS

- **[NO_SILENT_ERRORS]**: Every failed condition must be handled or logged.
- **[NO_OVER_ABSTRACTION]**: Flag abstractions that increase complexity without adding clear value.

---

`[OMNI-ARTIFACT-ANCHOR] ID: UMB-REV-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
