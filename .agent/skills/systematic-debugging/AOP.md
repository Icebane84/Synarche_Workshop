# AOP: Systematic Debugging Playbook [v15.0]

## 🏗️ THE 4-PHASE SCIENTIFIC METHOD
**Fixed Causes, Not Observed Symptoms.**

### 🚦 Phase 1: Reliable Reproduction [CRITICAL]
- **Scripted Failure**: No bug is considered "reproduced" until it can be triggered by a single script or command.
- **Trace Analysis**: Collect stack traces, logs, and network payloads *before* postulating a cause.
- **Environment Parity**: Verify if the failure happens in `dev`, `stage`, or `prod`.

### 🚦 Phase 2: Isolation & Tree Trimming [CRITICAL]
- **Binary Search**: Use `git bisect` to find the commit that introduced the fault.
- **Dependency Isolation**: Disable non-essential services/components to see if the bug persists.
- **Minimal Case**: Strip the failing code down to the bare minimum (The "Minimal Reproducible Example").

### 🚦 Phase 3: Root Cause (The 5 Whys) [CRITICAL]
- **Why 1**: [Symptom] (e.g., The form crashes).
- **Why 2**: [Immediate reason] (e.g., Validation error).
- **Why 3**: [Logic flaw] (e.g., Regex is too strict).
- **Why 4**: [Design flaw] (e.g., Input type is ambiguous).
- **Why 5**: [Process flaw] (e.g., Missing unit test for edge cases).

### 🚦 Phase 4: Fix & Verify [CRITICAL]
- **Regression Test**: First, write a test that fails due to the bug.
- **Implement Fix**: Apply the fix until the test passes.
- **Global Verify**: Run `/omega_audit` to ensure no side-effects were introduced.

---

## 🏰 DECOMPOSITION PROTOCOL (DEBUGGING PRE-WORK)
**Before touching any code during a debug session, perform this scan:**
```
UI/TASK: [Bug Name]
├── REPRODUCE: [Is there a script/command to trigger this?] (Phase 1)
├── SYMPTOMS: [What are the specific error logs?] (Evidence check)
├── ISOLATION: [What is the minimal failing case?] (Phase 2)
└── REGRESSION: [Which test will guard this after the fix?] (Verification check)
```

---

## 📜 ANTI-PATTERNS (PROHIBITED)
1. **"Maybe" Fixing**: Changing code without understanding why it might fix the bug.
2. **Ignoring Evidence**: Discounting a log because "that code hasn't changed."
3. **Stopping at Symptoms**: Fixing the crash but leaving the data-integrity issue that caused it.

---
**Protocol**: "In the absence of data, there is no fix. Trust the trace."
