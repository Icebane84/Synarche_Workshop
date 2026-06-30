# Dual Artifact: Skill Extraction Helper

---

## 👤 Human Perspective: The "Skill Factory"

**Objective**
Make it trivially easy to turn a verified solution into a permanent, reusable skill. One command scaffolds everything needed so the agent can focus on writing the logic, not the boilerplate.

**Impact**

- Reduces the friction of skill creation to near zero.
- Ensures all new skills share a consistent, discoverable structure.
- Accelerates the growth of the agent's capability library over time.

**Analogy**
Like a "File → New Project" wizard in an IDE — it sets up the right folder, the right template, and gets out of your way.

---

## 🤖 AI Perspective: The "Scaffold Engine"

**Technical Goal**
Given a skill name, create a valid skill directory containing a pre-populated `SKILL.md` derived from the standard template. Halt safely if the skill already exists.

**Script Location**
`c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/extract_skill.ps1`

**Execution**

```powershell
pwsh -File .agent/skills/self-improvement/scripts/extract_skill.ps1 -SkillName <skill-name>
```

**Logic Flow**

```
Input: -SkillName <name>
  → Validate: name is lowercase-with-hyphens
  → Guard: if skills/<name> exists → Write-Error, return
  → New-Item -ItemType Directory → skills/<name>/
  → Copy-Item SKILL-TEMPLATE.md → skills/<name>/SKILL.md
  → Print success path to stdout
  → Exit 0
```

**I/O Contract**

| Parameter    | Required | Format                   |
| ------------ | -------- | ------------------------ |
| `-SkillName` | Yes      | `lowercase-with-hyphens` |
| Exit 0       | Success  | Path printed to stdout   |
| Exit 1       | Failure  | Error written to stderr  |

**Constraints**

- Template source: `assets/SKILL-TEMPLATE.md` (relative to skill dir).
- Target: `.agent/skills/<name>/SKILL.md`.
- Must **not** create `README.md` (Agent Skills spec prohibition).
- After scaffolding, the human or agent **must** customize the `SKILL.md` before the skill is usable.
