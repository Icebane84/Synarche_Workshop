# SELT: WebApp Testing Experience Log & Trace [v15.0]

## 📅 Testing Logs

### 🏗️ 2026-03-30 (Batch 5 Rollout)
- **Status**: Canonized Batch 5 (WebApp Testing).
- **Synthesis**: Standardized Playwright and E2E Architecture into `AOP.md`.
- **Integrity**: Enforced **"Playwright-First"** and **"Hydration-Aware Transitions"** as default operational behaviors.
- **Audit**: Registered automated scan signatures in `GUCA.md`.

## 📍 Systemic Discoveries

### 🧪 Automated Verification
- **Discovery**: Widespread dependency on `wait(1000)` in the Tarot-Forge legacy test suite.
- **Remediation**: Injected **Wait Policy**: Use `await expect().toBeVisible()` or `page.waitForSelector()`. NO hardcoded timeouts.
- **Discovery**: Broken auth flows on Firefox specifically due to cross-site cookie restrictions.
- **Remediation**: Implemented **Browser Matrix Mandate**: E2E tests MUST run on Chromium, WebKit, and Firefox.

## 🚧 Historical Dissonance
- **Issue**: Flaky tests failing in CI/CD due to DB migration race conditions.
- **Legacy Pattern**: Non-deterministic data-seeding in E2E runs.
- **Correction**: Prohibited non-deterministic tests. Mandated **Atomic Data Seeding** and cleanup (AOP 3.4).

---
**Protocol**: This log MUST be updated after every E2E test run or major regression to maintain Zero Entropy in stability governance.
