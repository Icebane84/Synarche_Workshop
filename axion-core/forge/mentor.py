"""CORE-HEPH-MENTOR-001 (mentor.py)
Status: [CANONIZED]
Genesis Stamp: 2026-03-07.

**The Spirit Bomb Axiom: Didactic Manifestation (Law 28)**
> Implemented from Blueprint `GVRN.REG.DidacticModuleGenerator.md`.
> Ethos: Synergistic Partner, Continuous Evolution.
> Generates educational Lesson Modules automatically from Dissonance Quests,
> transforming the Coding Agent from a passive critic into an active Mentor.
"""

from typing import Any

# Map of error codes to Phoenix Principles
PRINCIPLE_MAP = {
    "Complexity": "Clarity Over Obfuscation. Code should be self-evident.",
    "UIP_Missing": "The Identification Lock (Law 1). Knowledge does not exist until it is woven with proper metadata.",
    "Geometry": "The Presentation Mandate (Law 7). Strict Structural Hierarchy is required for coherent parsing.",
    "Imports": "The Relational Mandate. Dependencies must be explicit and sorted for systemic predictability.",
    "Documentation": "Documentation as Cognition. An undocumented function is a missing synapse in the Loom.",
    "General": "Algorithmic Elegance. Every line of code is fuel; bad code is toxic fuel.",
}


class MentorDidactic:
    """Generates structured lessons explaining *why* a fix is required."""

    def __init__(self) -> None:
        """Initialize the didactic lesson generator."""
        self.lessons_generated = 0

    def generate_lesson(
        self,
        violation_type: str,
        context: str,
        before_code: str = "",
        after_code: str = "",
    ) -> dict[str, Any]:
        """Create a structured Didactic Module explaining a code fix."""
        principle = PRINCIPLE_MAP.get(violation_type, PRINCIPLE_MAP["General"])

        # Simple Rationale generator (in a full AGI this would call the NLP engine)
        rationale = (
            f"By addressing this {violation_type} violation in {context}, we elevate the Coherence Index. "
            f"This structurally prevents systemic entropy and improves readability for all Phoenix Agents."
        )

        self.lessons_generated += 1

        lesson_markup = (
            f"## 🎓 Phoenix Lesson Module: {violation_type}\n\n"
            f"> **The Principle:** {principle}\n\n"
            f"### The Rationale\n{rationale}\n\n"
            f"### The Demonstration\n```diff\n{self._format_diff(before_code, after_code)}\n```\n"
        )
        return {
            "violation": violation_type,
            "principle": principle,
            "rationale": rationale,
            "markdown": lesson_markup.strip(),
        }

    def _format_diff(self, before: str, after: str) -> str:
        """Format a simple diff."""
        if not before and not after:
            return "No specific code diff available."

        diff_lines = []
        if before:
            for line in before.splitlines():
                diff_lines.append(f"- {line}")
        if after:
            for line in after.splitlines():
                diff_lines.append(f"+ {line}")

        return "\n".join(diff_lines)
