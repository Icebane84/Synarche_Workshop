---
name: webapp-testing
description:
    Web application testing principles. E2E, Playwright, deep audit strategies. Use when writing tests, executing
    automation, or auditing application stability.
allowed-tools: Read, Glob, Grep, Bash
---

# WebApp Testing System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Automated Truth** and **Regression Resistance** through **Playwright E2E Verification** and **Atomic Component Testing**. This skill mandates a "Test-First" approach for verification, ensuring that every feature is stable and performant before deployment.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Testing Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `npx playwright test` - Automated E2E Security & Behavioral Audit.
- `axe-playwright` (npx) - Automated Accessibility Verification.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Wait-Visibility" Mandate
**MANDATORY**: Never use hardcoded timeouts (`wait()`). Use Playwright's auto-waiting assertions (`toBeVisible`, `toBeEditable`) to ensure test stability.

### 2. Multi-Browser Matrix
**MANDATORY**: All E2E test suites MUST run on Chromium, WebKit, and Firefox to ensure cross-platform compatibility.

### 3. Atomic Data Seeding
Any test requiring persistent state MUST seed its own data at the start of the `test()` block and cleanup at the end.

### 4. Interactive Sanity
All interactive components MUST be tested for keyboard navigation and focus visibility alongside mouse-events.

---
"Trust nothing that is not automated. Verify the Sovereign."
