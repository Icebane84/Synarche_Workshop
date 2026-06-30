---
name: powershell-windows
description: PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling.
allowed-tools: Read, Glob, Grep, Bash, PowerShell
---

# PowerShell Windows System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Shell Sovereignty** and **Operational Safety** through **Strict-Mode Scripting** and **Error-Resilient Automation**. This skill mandates that every terminal command and script be secure, absolute, and handled with precision, ensuring the Sovereignty of the Windows execution environment.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Windows Operator Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `powershell.exe -ExecutionPolicy RemoteSigned` - Automated Security Check.
- `scripts/omega_audit.py` - Universal Cluster-Wide Health Check.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Strict-Mode" Mandate
**MANDATORY**: All `.ps1` scripts MUST include `Set-StrictMode -Version Latest` at the start to prevent uninitialized variable usage and silent failures.

### 2. Resilience (Try-Catch) Mandate
**MANDATORY**: Every IO, Registry, or Network operation MUST be wrapped in a `try/catch/finally` block with explicit error logging and state restoration.

### 3. Absolute Pathing
**MANDATORY**: Resolve all paths via `$PSScriptRoot` or use absolute paths. Prohibit reliance on `$PWD` (Current Working Directory) for stability.

### 4. Credential & History Sovereignty
PROHIBITED: Typing secrets into the shell. MANDATED: Use `Get-Credential` and purge `PSReadline` history after sensitive tasks.

---
"The shell is the voice of the Sovereign. Command with the truth."
