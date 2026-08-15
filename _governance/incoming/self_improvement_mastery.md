# Dual Artifact: Mastering Self-Improvement

This artifact defines the protocol for the "Mastery" phase of the self-improvement loop, bridging human intent with AI technical execution.

---

## 👤 Human Perspective: The "Feedback Synergy"

_Focused on the partnership and evolution of the workspace._

### Objective

Create a collaborative environment where every mistake is a one-time event and every success becomes a reusable pattern. We want the AI to "grow" with the project, becoming more autonomous and aligned with human preferences over time.

### Impact

- **Zero Regression**: Solutions to complex bugs are remembered and applied to similar future issues.
- **Customized Intelligence**: The agent learns project-specific "unwritten rules" and architectural preferences.
- **Efficiency**: Routine tasks are automated into skills, freeing the human to focus on high-level design.

### Analogy

Think of this as building a "Project Nervous System." The `.learnings/` directory is the memory, and the `skills/` directory is the motor control for complex movements.

---

## 🤖 AI Perspective: The "Self-Optimization Protocol"

_Focused on the mechanical triggers and technical integrity._

### Technical Goal

Ensure 100% capture of non-trivial state changes and logic failures through structured logging. Maintain a high "Signal-to-Noise" ratio in the `.learnings/` directory.

### Core Dependencies

- **Persistence**: `c:/Users/Chris/.gemini/.learnings/` (ERRORS.md, LEARNINGS.md, FEATURE_REQUESTS.md).
- **Logic**: `c:/Users/Chris/.gemini/.agent/skills/self-improvement/SKILL.md`.
- **Helpers**: `c:/Users/Chris/.gemini/.agent/skills/self-improvement/scripts/extract_skill.ps1`.

### Constraints & Standards

- **ID Integrity**: All logs must follow `[LRN|ERR|FEAT]-YYYYMMDD-XXX`.
- **Pathing**: Always use absolute paths for related files in metadata.
- **Verification**: Skills extracted from learnings must pass a "dry run" using the template in `assets/SKILL-TEMPLATE.md`.

### Automation Markers

- **Trigger A (Session Resume)**: Check `.learnings/` for pending high-priority items.
- **Trigger B (Post-Tool Error)**: Execute `scripts/error_detector.ps1` if exit code != 0.
- **Trigger C (Session End)**: Execute `scripts/activator.ps1` to prompt for final logging.
