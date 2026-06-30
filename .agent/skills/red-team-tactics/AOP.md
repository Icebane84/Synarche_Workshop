# AOP: Red Team Tactics Playbook [v15.0]

## 🛠️ THE ATTACK LIFECYCLE (MITRE ATT&CK)
**Tactics & Techniques for Adversary Simulation.**

### 🚦 Phase 1: Recon & Initial Access [CRITICAL]
- **Passive Recon**: Map technology stacks via `Wappalyzer`, headers, and public repositories.
- **Foothold Strategy**: Identify single point of entry (Phishing, Exploit, Credential Stuffing).
- **Supply Chain**: Audit third-party access and dependency trust boundaries.

### 🚦 Phase 2: Execution & Persistence [HIGH]
- **LOLBins**: Use legitimate binaries (`powershell`, `certutil`, `bash`) to execute code and evade signature-based detection.
- **Scheduled Tasks**: Establish persistence via `cron` or `schtasks` to survive reboots.
- **Lateral Movement**: Utilize valid credentials or pass-the-hash to move from dev/stg to prod.

### 🛡️ Phase 3: Defense Evasion [CRITICAL]
- **Obfuscation**: Hide malicious code within benign artifacts or encrypted containers.
- **Log Evasion**: Clear specific event logs or use "no-log" execution modes.
- **Timestomping**: Modify file timestamps to blend with project age.

---

## 🏰 DECOMPOSITION PROTOCOL (SECURITY PRE-WORK)
**Before starting any system design or feature work, perform this analysis:**
```
UI/TASK: [Task Name]
├── ASSETS: [What is being protected?] (Secrets, PII, Data)
├── THREATS: [Who would attack & how?] (Lateral, Injection, Misconfig)
├── BOUNDARIES: [Where is the trust checked?] (Auth/Authz location)
├── EVASION: [How would detection be bypassed?] (LOLBins, No-Logging)
└── REMEDIATION: [Fail-Secure logic?] (Fail-Closed, Error shielding)
```

---

## 📜 ETHICAL BOUNDARIES (MANDATORY)
1. **Scope Only**: Never touch production data or unauthorized environments.
2. **Minimize Impact**: Do not cause denial of service unless explicitly scoped.
3. **Document All**: Every simulation step must be recorded in `SELT.md`.
4. **Immediate Report**: If a true vulnerability is found, stop simulation and report to the USER immediately.

---
**Protocol**: "Defend by understanding the offense. Research the breach before building the bridge."
