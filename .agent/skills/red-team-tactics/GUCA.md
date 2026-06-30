# GUCA: Red Team Command Registry [v15.0]

## 🛠️ Audit & Simulation Commands

### 🔍 Reconnaissance
- `/simulate_recon` - Automated attack surface mapping.
  - **Automation**: `bash scripts/recon_scan.sh <target_url>`
- `/check_wappalyzer` - Identify tech stack vs known CVEs.
- `/verify_repo_secrets` - Scan for leaked tokens using `trufflehog` or `gitleaks`.

### ⚡ Initial Access & Execution
- `/check_phishing_vectors` - Identification of email/employee entry points.
- `/test_lolbins` - Check for common Living-Off-The-Land binaries misuse.
  - **Automation**: `python scripts/lolbin_checker.py`
- `/verify_persistence` - Scan for unauthorized cron/schtasks entries.

### 🛡️ Defense Evasion
- `/audit_log_evasion` - Check for gaps in security logging or "no-log" flags.
- `/verify_obfuscation` - Scan artifacts for high-entropy obfuscants.
  - **Automation**: `bash scripts/entropy_audit.sh <dir>`

### 🚀 Reporting
- `/generate_attack_narrative` - Auto-generation of finding descriptions (What, Where, Why, Impact, Fix).
- `/audit_remediation_gaps` - Map findings to detection failures.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: Commands must be executed relative to the project root. High-security mandates (OWASP 2025) are the default baseline for all audit outputs.
