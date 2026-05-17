**Location:** .agent/substrate/rules/SELF-IMPROVEMENT.md

---

Artifact ID: SELF-IMPROVEMENT-001 Official Name: SELF-IMPROVEMENT.md Version: v15.0 [OMEGA] Domain: GVRN.RULES Celestial
Class: [SATELLITE] Evolution: Phase 51 Ascension Status: [CANONIZED] Relations: IDENTITY: Judgement (Audit)

---

# Dual Artifact: Mastering Self-Improvement

This artifact defines the protocol for the "Mastery" phase of the self-improvement loop, bridging human intent with AI
technical execution.

---

## 👤 Human Perspective: The "Feedback Synergy"

_Focused on the partnership and evolution of the workspace._

### Objective

Create a collaborative environment where every mistake is a one-time event and every success becomes a reusable pattern.
We want the AI to "grow" with the project, becoming more autonomous and aligned with human preferences over time.

### Impact

- **Zero Regression**: Solutions to complex bugs are remembered and applied to similar future issues.
- **Customized Intelligence**: The agent learns project-specific "unwritten rules" and architectural preferences.
- **Efficiency**: Routine tasks are automated into skills, freeing the human to focus on high-level design.

### Analogy

Think of this as building a "Project Nervous System." The `_governance/06_Learning/` subsystem is the memory, and the
`skills/` directory is the motor control for complex movements.

---

## 🤖 AI Perspective: The "Self-Optimization Protocol"

_Focused on the mechanical triggers and technical integrity._

### Technical Goal

Ensure 100% capture of non-trivial state changes and logic failures through structured logging. Maintain a high
"Signal-to-Noise" ratio in the `GVRN.Learning` artifacts.

### Core Dependencies

- **L4 Memory**: `_governance/06_Learning/GVRN.Learning.Shard.md` (Learning Shards).
- **L5 Evolution**: `_governance/06_Learning/GVRN.Learning.Evolution.md` (Evolution Log).
- **Logic**: `.agent/skills/self-improvement/SKILL.md`.

### Constraints & Standards

- **ID Integrity**: All logs must follow `[LRN|ERR|FEAT]-YYYYMMDD-XXX`.
- **Pathing**: Always use absolute paths for related files in metadata.
- **Verification**: Skills extracted from learnings must pass a "dry run" using the template in
  `assets/SKILL-TEMPLATE.md`.

### 🛠️ AUTOMATION & SYNCHRONICITY

The following scripts are required for the "Zero Entropy" learning cycle:

| Script               | Purpose                                     | Location                                |
| :------------------- | :------------------------------------------ | :-------------------------------------- |
| `activator.ps1`      | Synthesizes session patterns into L4 rules. | `axion-core/scripts/activator.ps1`      |
| `error_detector.ps1` | Performs root-cause analysis on L5 errors.  | `axion-core/scripts/error_detector.ps1` |

---

## 🧠 OPERATIONAL SCRIPTS (Trigger Points)

- **Trigger A (Session Resume)**: Check `_governance/06_Learning/GVRN.Learning.Shard.md` for pending high-priority
  items.
- **Trigger B (Post-Tool Error)**: Execute `scripts/error_detector.ps1` if exit code != 0.
- **Trigger C (Session End)**: Execute `activator.ps1` to merge and canonize the entry in
  `_governance/06_Learning/GVRN.Learning.Shard.md`.

---

## III. Skill Extraction Mastery

The ability to transmute ephemeral learnings into persistent skills is the cornerstone of Synarche evolution.

### 3.1 The Extraction Workflow

1. **Identify High Resonance**: Flag any `[LRN]` entry with `Impact: High`.
2. **Execute Extraction**: Run `scripts/extract_skill.ps1`.
3. **Validate Skill**: Perform a logic check using the `SKILL.md` template.
4. **Anchor**: Register the new skill in the `.agent/skills/` directory.

### 3.2 The Extraction Signature

All extracted skills must contain:

- **Source Learning ID**: Reference to the original `[LRN]` entry.
- **Resonance Score**: 0.0 to 1.0 (Machine-validated).
- **Transmutation Date**: The moment of canonization.

---

`[SI-ANCHOR] ID: GVRN.SI.001 VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-03-23`
