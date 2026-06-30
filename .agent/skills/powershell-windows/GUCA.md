# GUCA: PowerShell Command Registry [v15.0]

## 🛠️ Shell & System Commands

### 🔍 Cmdlet Execution
- `/run_ps_script` - Execute a verified `.ps1` script.
  - **Automation**: `powershell.exe -ExecutionPolicy RemoteSigned -File <path>`
- `/get_process_tree` - List all active Windows processes and their parents.
- `/verify_strict_mode` - Scan scripts for `Set-StrictMode` compliance.

### ⚡ Automation & Registry
- `/audit_env_vars` - Search for potential secrets in Environment Variables.
- `/check_path_sovereignty` - Verify absolute vs relative pathing in scripts.
- `/run_task_sch_scan` - Audit Windows Task Scheduler for OMEGA automation.

### 🛡️ Final Verification
- `/run_shell_audit` - Execute the master shell-security validation script.
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

### 🚀 Reporting
- `/generate_execution_report` - Pass/Fail/Error-Rate metrics for shell tasks.
- `/audit_history_leaks` - Identify potential secret leaks in PSReadline history.

---
**Usage**: PowerShell commands must be executed within the session context. No shell task is Sovereign without a verified Execution Policy and a valid `try/catch` handler.
