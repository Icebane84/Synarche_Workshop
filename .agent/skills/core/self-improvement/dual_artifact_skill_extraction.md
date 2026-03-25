# Dual Artifact: Automatic Skill Extraction

---

## 👤 Human Perspective: The "Pattern Library"

**Objective**
Automatically convert proven solutions into reusable skills so the agent never has to solve the same problem twice. The goal is to make good ideas permanent.

**Impact**

- Hard-won solutions stop being "lost" when a conversation ends.
- The agent becomes measurably smarter with every complex task it resolves.
- Future sessions inherit the expertise of all past sessions.

**Analogy**
Think of it like a craftsman's toolbox: when a one-off jig works perfectly, you keep it for the next build. Skill extraction turns one-time fixes into permanent tools.

---

## 🤖 AI Perspective: The "Extraction Protocol"

**Technical Goal**
Detect qualifying learnings from `.learnings/LEARNINGS.md` and execute `extract_skill.ps1` to scaffold a new, self-contained skill directory.

**Trigger Criteria (ANY one qualifies)**
| Signal | Source |
| --- | --- |
| `See Also` links to 2+ prior entries | `.learnings/LEARNINGS.md` |
| Status is `resolved` + priority `high` | `.learnings/LEARNINGS.md` |
| User says "save this as a skill" | Conversation |
| Category is `best_practice` with broad applicability | `.learnings/LEARNINGS.md` |

**Execution Steps**

1. Confirm learning status = `resolved`.
2. Run: `pwsh -File .agent/skills/self-improvement/scripts/extract_skill.ps1 -SkillName <name>`
3. Populate the generated `SKILL.md` from `assets/SKILL-TEMPLATE.md`.
4. Verify: no project-specific hardcoded paths, self-contained examples.
5. Update learning entry: set `Status: promoted_to_skill`, add `Skill-Path`.

**Core Dependencies**

- `c:/Users/Chris/.gemini/.learnings/LEARNINGS.md`
- `c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/extract_skill.ps1`
- `c:/Users/Chris/.gemini/.agent/skills/self-improvement/assets/SKILL-TEMPLATE.md`

**Constraints**

- Skill folder name: `lowercase-with-hyphens`.
- No `README.md` inside a skill folder (spec requirement).
- No project-specific absolute paths inside the new `SKILL.md`.
