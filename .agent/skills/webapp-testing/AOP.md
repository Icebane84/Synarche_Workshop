# AOP: Playwright & Verification Playbook [v15.0]

## 🏗️ TESTING ARCHITECTURE & STRATEGY
**Truth is the Structural Property of Execution.**

### 🚦 E2E User Flows [CRITICAL]
- **Playwright First**: Mandate Playwright for all cross-browser E2E testing.
- **Atomic Tests**: Each test must be independent. Use `test.describe()` to group but avoid shared state between tests.
- **Selectors**: Prefer `getByRole`, `getByLabel`, `getByText`. Avoid fragile CSS/XPath selectors.
- **Environment**: Test against a local dev server (`npm run dev`) or a production-identical staging build.

### 🚦 Component Verification [CRITICAL]
- **Interaction**: Verify that components respond correctly to clicks, typing, and mouse-events.
- **Props Validation**: Use TypeScript and Zod to ensure components only receive valid data structures.
- **Hydration Check**: In SSR (Next.js/React), verify that the client-side state matches the server-side markup.

### 🛡️ AUTOMATED AUDITS [HIGH]
- **Accessibility (Axe)**: Integrate `axe-playwright` into the E2E suite to scan every state of the UI.
- **Performance (Lighthouse)**: Run Lighthouse on critical paths to guard against performance regressions.
- **Security (Fuzzing)**: Use Playwright to fuzz-test form inputs with long strings, SQL injections, and script tags.

---

## 🏰 DECOMPOSITION PROTOCOL (TESTING PRE-WORK)
**Before starting any feature implementation, perform this scan:**
```
UI/TASK: [Task Name]
├── FLOWS: [What are the critical user paths?] (E2E check)
├── EDGE: [What happens on bad input / empty states?] (Logic check)
├── AUDIT: [Are we running A11y / Perf checks?] (Audit check)
└── SNAPSHOT: [Do we need visual regression?] (UI check)
```

---

## 📜 ASSERTION STANDARDS (MANDATORY)
1. **Visible**: Ensure elements are visible and stable before interaction.
2. **Behavioral**: Assert on the result of the action (e.g., "Expect count to increment"), not the implementation.
3. **Negative**: Always test that unauthorized actors CANNOT access protected resources.

---
**Protocol**: "A feature is not done until it is tested. A test is not done until it is automated."
