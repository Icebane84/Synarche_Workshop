# GUCA: Testing Command Registry [v15.0]

## 🛠️ Testing & Quality Commands

### 🔍 Unit & Integration
- `/run_unit_tests` - Execute all Vitest unit tests.
  - **Automation**: `npx vitest run --dir src/utils src/services`
- `/verify_service_mocks` - Test that mocks match the current API shape.
- `/check_test_coverage` - Show coverage metrics for the current module.
  - **Automation**: `npx vitest run --coverage`

### ⚡ Performance & Health
- `/audit_memory_leak` - Scan for uncleaned event listeners/timers.
- `/check_bundle_size` - Verify component size against the 50kB limit.
  - **Automation**: `npx source-map-explorer dist/assets/*.js`
- `/verify_execution_speed` - Run targeted benchmarks on critical logic.

### 🛡️ Final Verification
- `/run_all_suites` - Execute Unit, Integration, and E2E in sequence.
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

### 🚀 Reporting
- `/generate_health_report` - Pass/Fail/Coverage/Perf metrics for the project.
- `/audit_regression_rate` - Identify the flakiest tests in the system.

---
**Usage**: Testing commands must be executed as part of the commit hook or CI/CD loop. No code is Sovereign without a passing Health Audit.
