# Dual Artifact: Self-Improvement Activator

---

## 👤 Human Perspective: The "Session Conscience"

**Objective**
Ensure that valuable insights never silently disappear at the end of a session. The activator acts as a gentle "closing prompt" — a final checkpoint that asks: _did we learn anything worth keeping?_

**Impact**

- Prevents "knowledge bleed" where good solutions are forgotten between sessions.
- Builds a culture of continuous improvement without requiring manual discipline.
- Keeps the `.learnings/` log healthy and up-to-date over time.

**Analogy**
Like a pilot's pre-flight and post-flight checklist — the activator runs at session boundaries to ensure nothing critical was missed.

---

## 🤖 AI Perspective: The "Boundary Trigger"

**Technical Goal**
Execute `activator.ps1` at defined session lifecycle events to prompt structured reflection and optional logging to `.learnings/`.

**Trigger Points**

| Event                           | Action                                                                 |
| ------------------------------- | ---------------------------------------------------------------------- |
| Session Resume                  | Check `.learnings/*.md` for `Status: pending` + `Priority: high` items |
| Session End / Task Complete     | Run `activator.ps1` to prompt learning evaluation                      |
| Post-Tool Error (exit code ≠ 0) | Chain to `error_detector.ps1` for immediate capture                    |

**Script Location**
`c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/activator.ps1`

**Execution Command**

```powershell
pwsh -File .agent/skills/self-improvement/scripts/activator.ps1
```

**Output Behavior**

- Prints timestamp, reminder message, and category checklist to terminal.
- Does **not** auto-write to `.learnings/` — human decision required.
- Exit code is always `0` (non-blocking).

**Constraints**

- Must never halt the primary workflow.
- Must remain idempotent — safe to run multiple times per session.
