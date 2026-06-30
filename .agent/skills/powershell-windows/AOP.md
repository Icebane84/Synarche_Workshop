# AOP: PowerShell & Windows Operator Playbook [v15.0]

## 🏗️ SHELL SOVEREIGNTY & SECURITY
**The Shell is the Direct Command Interface of the Sovereign.**

### 🚦 Cmdlet Security [CRITICAL]
- **Execution Policy**: Mandate `RemoteSigned` for local script execution. Never use `Bypass` in production.
- **Error Handling**: Every complex script MUST use `try { ... } catch { ... }` blocks with explicit error logging.
- **Strict Mode**: ALWAYS include `Set-StrictMode -Version Latest` at the start of any `.ps1` script to prevent uninitialized variable usage.
- **Credential Safety**: PROHIBITED: Plain-text passwords in scripts. Use `Get-Credential` or `Export-Clixml`.

### 🚦 Automation & Paths [CRITICAL]
- **Path Sovereignty**: Always use absolute paths or resolve relative paths via `$PSScriptRoot`.
- **Operator Selection**: Use `pwsh` (Core) for cross-platform compatibility where possible, or `powershell.exe` for Windows-specific modules.
- **Process Management**: Use `Start-Job` and `Stop-Job` for background task automation.

### 🛡️ ENVIRONMENT & MODULES [HIGH]
- **Module Auditing**: Only use verified modules from the PowerShell Gallery.
- **History Privacy**: Regularly purge or audit the PSReadline history to ensure no secrets were typed.
- **Encoding**: Use `UTF-8` for all file reads/writes to ensure cross-buffer compatibility with OMEGA v15.0.

---

## 🏰 DECOMPOSITION PROTOCOL (SHELL PRE-WORK)
**Before any complex command or script execution, perform this scan:**
```
UI/TASK: [Shell Task]
├── SECURITY: [Is Strict Mode enabled?] (Safety check)
├── PATHS: [Are paths resolved via $PSScriptRoot?] (Context check)
├── ERRORS: [Is there a try-catch-finally block?] (Resilience check)
└── HISTORY: [Will this leak secrets into PSReadline?] (Privacy check)
```

---

## 📜 SCRIPTING STANDARDS (MANDATORY)
1. **Verbs**: Use standard Cmdlet verbs (Get, Set, New, Remove, Invoke).
2. **Pipelines**: Use the pipeline `|` for data transformations, but avoid deep nesting (max 3 levels).
3. **Immutability**: Treat the environment state as immutable; always restore state in the `finally` block if a script changes registry or env vars.

---
**Protocol**: "Command with precision. Execute with safety. Trust the Shell of the Sovereign."
