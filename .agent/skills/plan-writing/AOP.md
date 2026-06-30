---
id: AISTF-MIN-001
name: Plan Writing Operational Playbook
version: v2.1 [GOLD]
type: PROCESS_GUIDE
status: [ACTIVE]
tags: ['#PROCESS', '#PLANNING', '#WORKFLOW']
---

# 📋 OPERATIONAL PLAYBOOK | AISTF-MIN-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-29 |
| **Domain**     | MIN.Sync.PlanWriting      |
| **State**      | ⚙️ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V2.0-SOVEREIGN]          |

---

## 🏗️ EXECUTION WORKFLOW

Follow this sequence to generate a high-fidelity plan.

### Step 1: Context Analysis

- Review current directory structure and affected files.
- Identify dependencies (libraries, other services).
- **Verify**: List the specific files that WILL be edited.

### Step 2: Goal Definition

- Write a single sentence: "Goal: [What we are building/fixing]".
- Identify the **main success criteria**.

### Step 3: Decompose Tasks

- Break goal into 5-10 discrete tasks.
- For each task, add a **Verify** clause (e.g., `Verify: npm run build passes`).
- Ensure every task is **atomic** (one file or one logical change).

### Step 4: Final Validation

- Check that all tasks are in logical order.
- Ensure the critical path is identified.
- **Verification**: Run a final "mental simulation" to check for missed dependencies.

---

## 🛠️ OPERATIONAL STANDARDS

- **[FORMAT]**: Use standard Markdown checkboxes `[ ]`.
- **[PATHS]**: Always use absolute paths within the workspace.
- **[SLUGS]**: Save the plan in the root as `{task-slug}.md`.

---

`[OMNI-ARTIFACT-ANCHOR] ID: AISTF-MIN-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
