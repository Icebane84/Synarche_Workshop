# Dual Artifact: Error Detector for Self-Improvement

---

## 👤 Human Perspective: The "Black Box Recorder"

**Objective**
Capture every tool or command failure at the moment it happens, before context is lost. The error detector acts as an automatic incident recorder so failures are never ignored or forgotten.

**Impact**

- Errors are captured with full context (command, exit code, timestamp).
- Prevents "silent failures" where something breaks but no one writes it down.
- Feeds directly into the `.learnings/` loop, so bugs become future defenses.

**Analogy**
Like a flight data recorder — it's always running in the background and only matters when something goes wrong, but when it does, it captures exactly what you need.

---

## 🤖 AI Perspective: The "Failure Interceptor"

**Technical Goal**
Accept an exit code and command string as inputs. If exit code is non-zero, write a formatted alert to the terminal and indicate the correct `.learnings/ERRORS.md` logging target.

**Script Location**
`c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/error_detector.ps1`

**Execution**

```powershell
pwsh -File .agent/skills/self-improvement/scripts/error_detector.ps1 -ExitCode <int> -Command <string>
```

**I/O Contract**

| Parameter   | Required | Format              |
| ----------- | -------- | ------------------- |
| `-ExitCode` | Yes      | `int`               |
| `-Command`  | Yes      | `string`            |
| Exit 0      | Always   | Non-blocking always |

**Logic Flow**

```
Input: -ExitCode <n>, -Command <str>
  → If ExitCode == 0 → no-op, exit 0
  → Else → Write-Host alert (Red) with code and command
          → Write-Host logging hint (Yellow) pointing to ERRORS.md
          → Exit 0 (always non-blocking)
```

**Constraints**

- Must **always** exit `0` — never prevent the caller from continuing.
- Output is terminal-only — does **not** auto-write to `.learnings/ERRORS.md`.
- Must be called **after** the failing command, not wrapping it.
