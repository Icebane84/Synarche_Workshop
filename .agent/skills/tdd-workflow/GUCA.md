# GUCA: TDD Command Registry [v15.0]

## 🛠️ Red-Green-Refactor Commands

### 🔴 RED Phase (Agent A)
- `/create_test_spec` - Initialize a new Vitest/Playwright test file.
- `/verify_test_failure` - Run the new test and confirm it fails.
  - **Automation**: `npx vitest run <file> --expect-fail`

### 🟢 GREEN Phase (Agent B)
- `/run_test_pass` - Execute tests and confirm they now pass.
  - **Automation**: `npx vitest run <file>`
- `/check_minimal_code` - Audit code for YAGNI (You Aren't Gonna Need It) violations.

### 🔵 REFACTOR Phase (Agent C)
- `/audit_code_quality` - Run Lint/Prettier and check performance metrics.
- `/run_all_tests` - Ensure all existing tests stay green after refactor.
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

### 🚀 Reporting
- `/generate_coverage_report` - Show test coverage for the target module.
  - **Automation**: `npx vitest run --coverage`
- `/verify_spec_alignment` - Compare the final code vs the initial Agent A spec.

---
**Usage**: TDD commands must be executed sequentially. No production code is accepted without a passing Agent A spec.
