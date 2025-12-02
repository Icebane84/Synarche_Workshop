# Dual Artifact: Session Bootstrap

---

## 👤 Human Perspective: The "Morning Briefing"

**Objective**
Every new session should start with a clear picture of where we left off — no re-reading history, no context guessing. The agent walks in already oriented.

**Impact**

- Eliminates the "cold start" problem between sessions.
- High-priority pending items surface immediately instead of being forgotten.
- The agent feels like a senior team member who read the notes before the meeting.

**Analogy**
Like a military briefing at the start of a shift — current status, outstanding actions, known risks, and today's priorities. No one has to catch up from scratch.

---

## 🤖 AI Perspective: The "Context Loader"

**Technical Goal**
At the start of every session, read `.agent/knowledge/`, scan `.learnings/` for pending items, and output a structured session brief to orient the agent on current state and priorities.

**Bootstrap Script Location**
`c:/Users/Chris/.gemini/.agent/skills/session-bootstrap/scripts/bootstrap.ps1`

**Execution**

```powershell
pwsh -File .agent/skills/session-bootstrap/scripts/bootstrap.ps1
```

**Logic Flow**

```
1. Read .agent/knowledge/*.md           → index active protocols
2. Scan .learnings/LEARNINGS.md         → extract Status: pending entries
3. Scan .learnings/ERRORS.md            → extract Status: pending, Priority: high
4. List .agent/skills/*/SKILL.md        → inventory available capabilities
5. Print structured SESSION BRIEF:
     - Active Protocols  (from knowledge/)
     - Pending Learnings (count + IDs)
     - Pending Errors    (count + IDs, high-priority highlighted)
     - Available Skills  (names only)
```

**Output Contract**

```
╔══════════════════════════════════╗
║  SESSION BRIEF — 2026-03-10      ║
╠══════════════════════════════════╣
║  Protocols : 6 active            ║
║  Learnings : 2 pending           ║
║  Errors    : 0 pending           ║
║  Skills    : zod-validation      ║
║              self-improvement    ║
╚══════════════════════════════════╝
```

**Constraints**

- Read-only — must not modify any file.
- Output to terminal only — not logged automatically.
- Must complete in under 2 seconds.
- Exit code always `0` (non-blocking).
