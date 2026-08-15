---
name: session-bootstrap
description: "Loads project context at the start of every session. Reads .agent/knowledge/, scans .learnings/ for pending items, and inventories available skills. Provides a structured SESSION BRIEF so the agent is instantly oriented. Use at the start of any new conversation or major task."
---

# Session Bootstrap Skill

Orient the agent at the start of every session. Run `bootstrap.ps1` once and receive a structured briefing covering active protocols, pending learnings, outstanding errors, and available skills.

## Usage

```powershell
pwsh -File .agent/skills/session-bootstrap/scripts/bootstrap.ps1
```

## Output

```
╔══════════════════════════════════╗
║  SESSION BRIEF — YYYY-MM-DD      ║
╠══════════════════════════════════╣
║  Protocols : N active            ║
║  Learnings : N pending           ║
║  Errors    : N pending [HIGH: N] ║
║  Skills    : skill-name          ║
║              ...                 ║
╚══════════════════════════════════╝
```

## What It Reads

| Source                     | Purpose                          |
| -------------------------- | -------------------------------- |
| `.agent/knowledge/*.md`    | Active protocols and conventions |
| `.learnings/LEARNINGS.md`  | Pending learning items           |
| `.learnings/ERRORS.md`     | Pending errors (high-priority)   |
| `.agent/skills/*/SKILL.md` | Available capabilities inventory |

## Constraints

- **Read-only** — never writes to any file.
- **Terminal-only** — output is not logged automatically.
- **Non-blocking** — always exits `0`.
- Target runtime: < 2 seconds.
