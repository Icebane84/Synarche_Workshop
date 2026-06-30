# GUCA: WebApp Testing Command Registry [v15.0]

## 🛠️ Execution & Verification Commands

### 🔍 E2E Testing (Playwright)
- `/run_e2e_suite` - Execute all Playwright tests.
  - **Automation**: `npx playwright test`
- `/verify_user_flows` - Targeted test of critical paths (Login, Checkout, Profile).
- `/test_mobile_viewport` - Run E2E tests specifically on mobile emulators.
  - **Automation**: `npx playwright test --project=mobile`

### ⚡ Component & Unit
- `/run_component_tests` - Execute Vitest/Jest component tests.
  - **Automation**: `npm run test:component`
- `/verify_props_validation` - Run Zod/TypeScript sanity checks on component data.

### 🛡️ Automated Audits
- `/run_a11y_suite` - Execute `axe-playwright` accessibility scan.
  - **Automation**: `npx playwright test tests/a11y`
- `/verify_visual_regression` - Compare snapshots vs baseline.
  - **Automation**: `npx playwright test --update-snapshots`

### 🚀 Reporting
- `/generate_test_report` - Auto-generation of pass/fail/coverage metrics.
- `/audit_regression_cause` - Identify the commit that broke the build.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: commands must be executed within the target project context. High-fidelity testing is a blocking requirement for any Production-ready branch.
