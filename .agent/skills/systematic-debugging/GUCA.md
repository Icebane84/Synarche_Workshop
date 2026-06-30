# GUCA: Debugging Command Registry [v15.0]

## 🛠️ Diagnostics & Repair Commands

### 🔍 Reproduction & Logs
- `/run_reproduction_script` - Execute the script to trigger the failure.
- `/tail_system_logs` - Show the last 100 lines of application logs.
  - **Automation**: `pm2 logs <name> --err --lines 100`
- `/check_git_history` - Audit the last 5 commits for potential regressions.
  - **Automation**: `git log --oneline -5`

### ⚡ Isolation & Test
- `/run_bisect_scan` - Automate finding the breaking commit.
  - **Automation**: `git bisect start; git bisect run <test_script>`
- `/verify_minimal_case` - Run the stripped-down reproduction code.
- `/clear_build_cache` - Purge caches that may hide bugs.

### 🛡️ Post-Correction
- `/verify_fix_regression` - Run the new test that guards against this bug.
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

### 🚀 Reporting
- `/generate_rca_report` - Auto-generation of Root Cause Analysis (AOP Phase 3).
- `/audit_similar_patterns` - Search the codebase for similar bug signatures.

---
**Usage**: Debugging commands must be executed within the context of an active incident. No commit is allowed without a verified Fix & Verify (Phase 4).
