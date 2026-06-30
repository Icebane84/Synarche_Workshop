---
name: red-team-tactics
description:
    Adversary simulation principles based on MITRE ATT&CK. Attack phases, detection evasion, reporting. Use when
    performing security audits, identifying attack vectors, or documenting detection gaps.
allowed-tools: Read, Glob, Grep, Bash
---

# Red Team Tactics System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **High-Security Governance** through **Adversary Simulation** and **MITRE ATT&CK Alignment**. This skill mandates an "Attack-First" mindset for verification, ensuring that every defense is validated against real-world breach techniques.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | MITRE ATT&CK Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `scripts/recon_scan.sh` - Automated Attack Surface Mapping.
- `scripts/lolbin_checker.py` - LOLBin Compliance Audit.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Assume Breach" Mandate
**MANDATORY**: Design every component assuming the attacker already has initial access. Verification MUST simulate lateral movement and privilege escalation.

### 2. Defense Evasion Protocol
**MANDATORY**: Audit all system logs for "blind spots" where LOLBins or obfuscated scripts could execute without detection.

### 3. Automated Validation
Every security finding **MUST** be reproducible via a `GUCA.md` command or automated script to ensure remediation is permanent.

---
"Understand the breach. Build the Sovereign."
