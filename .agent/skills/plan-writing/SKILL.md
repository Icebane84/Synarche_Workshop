---
id: UMB-MIN-001
name: Plan Writing & Decomposition
version: v3.0 [OMEGA]
type: SKILL_LOGIC
status: [TRANSCENDENT]
tags: ['#PLANNING', '#DECOMPOSITION', '#SOVEREIGN', '#OMEGA']
---

# 🧠 PLAN WRITING | UMB-MIN-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-29 |
| **Domain**     | MIN.Sync.PlanWriting      |
| **State**      | 🌀 OMEGA STANDARD         |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V3.0-SOVEREIGN]          |

---

## 🎭 SOVEREIGN LOGIC

Structure your work into clear, actionable tasks with verification criteria. This skill is the fundamental layer for multi-step architectural execution, refactoring, and feature synthesis.

### Principles of Decomposition

1. **Small, Focused Tasks**: 2-5 minutes per task. Single outcome. If it takes longer, it's a sub-plan.
2. **Clear Verification**: Every task MUST have a "Verify:" clause. (Tests, UI Check, API Response).
3. **Logical Ordering**: Identify dependencies. Highlight the critical path. Phase X: Verification is LAST.
4. **Dynamic Context**: No fixed templates. Each plan is unique to the file/context and project type.
5. **No Monoliths**: If a task requires editing multiple files, split it into atomic file-level tasks.

---

## 🛠️ BLUEPRINT STANDARDS

### Planning Heuristics

- **[SHORT]**: Max 10 tasks. If more, break into multiple sub-plans or phases.
- **[SPECIFIC]**: Use absolute paths (`res://` or full local paths) and exact commands.
- **[DYNAMIC]**: Adjust content based on project type (React, Godot, Python).
- **[VERIFIABLE]**: How do you know it's done? What can you check/test?

### Specific Contexts

| Project Type | Focus Area | Relevant Verification |
|--------------|------------|-----------------------|
| **Godot/GDScript** | Signal Bus, Node Tree | Run Scene (F6), check Debug Console |
| **Frontend/React** | UI Components | `npm run dev`, verify DOM elements |
| **Backend/API** | Endpoints, Logic | `curl` or `vitest`, check 200 OK |
| **New Project** | Tech Stack, MVP | `npx`, Directory structure check |

---

## 🔍 QUALITY CONSTRAINTS

- **[NO_PLACEHOLDERS]**: Never use "Finish UI". Use "Add submit button to LoginForm.tsx".
- **[NO_VAGUENESS]**: "Style the UI" → "Add Tailwind classes to Header.tsx".
- **[boy-scout-rule]**: Leave any file cleaner than you found it. Refactor small dissonances during tasks.

---

## 📋 SYNTHESIZED STRUCTURE

```markdown
# [Task Name]

## Goal
One sentence: What are we building/fixing?

## Tasks
- [ ] Task 1: [Specific action] → Verify: [Exact check]
- [ ] Task 2: [Specific action] → Verify: [Exact check]

## Done When
- [ ] [Primary success criteria 1]
- [ ] [Primary success criteria 2]
```

`[OMNI-ARTIFACT-ANCHOR] ID: UMB-MIN-001 VER: v3.0 [OMEGA] DOMAIN: MIND STATUS: [TRANSCENDENT]`
