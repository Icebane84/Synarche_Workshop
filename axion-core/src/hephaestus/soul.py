"""
artifact_anchor:
  id: CORE.SOUL.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

# ### **Block A: The Identification Lock (UIP-V15)**.
#
# | Key                 | Value                         | Description       |
# | :------------------ | :---------------------------- | :---------------- |
# | **Artifact ID**     | `METRIC-AES-001`              | The Sovereign ID. |
# | **Official Name**   | `soul.py`                     | The Filename.     |
# | **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
# | **Domain**          | `ARCH-METRIC`                 | The Subject.      |
# | **Celestial Class** | `[PLANET]`                    | The Weight.       |
# | **Evolution**       | `Operational`                 | The Maturity.     |
# | **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
# | **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |
#
# **The Elegance Axiom: Algorithmic Soul (Law 7)**
# > Implemented from Blueprint `GVRN.ARCH.Soul.md`.
# > Ethos: Guardian of Elegance.

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

import ast

from .lib.emotion_analyzer import EmotionAnalyzer

DEFAULT_AES_SCORE = 7.0
MAX_LINE_COUNT = 50
MAX_INDENT_LEVEL = 3


class ArtificersSoul:
    """The Soul module responsible for calculation the Algorithmic Elegance Score (AES)."""

    def __init__(self) -> None:
        self.emotion_engine = EmotionAnalyzer()

    def calculate_narrative_resonance(self, text: str) -> float:
        """Calculates narrative resonance based on emotional content density and weight."""
        if not text:
            return 1.0
        emotions = self.emotion_engine.detect_emotions(text)
        if not emotions:
            return 0.5  # Neutral default resonance
        total_intensity = sum(emotions.values())
        resonance = min(1.0, total_intensity / len(emotions) * (1.0 + 0.1 * len(emotions)))
        return round(max(0.0, min(1.0, resonance)), 3)

    def _calculate_ast_complexity(self, content: str) -> float:
        """Calculates complexity using AST parsing."""
        tree = ast.parse(content)
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(
                node,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.ExceptHandler,
                    ast.With,
                    ast.AsyncFor,
                    ast.AsyncWith,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                complexity += 1
        score = 10.0 - (complexity * 0.1)
        return max(0.0, min(10.0, score))

    def _calculate_heuristic_score(self, content: str) -> float:
        """Calculates complexity using heuristic fallback."""
        lines = content.splitlines()
        line_count = len(lines)

        # Penalties
        length_penalty = (
            max(0, (line_count - MAX_LINE_COUNT) * 0.05)
            if line_count > MAX_LINE_COUNT
            else 0
        )

        indent_penalty = 0
        keyword_penalty = 0
        keywords = ["if ", "for ", "while ", "switch ", "case ", "catch "]

        for line in lines:
            stripped = line.lstrip()
            if not stripped:
                continue

            # Indentation (approx 4 spaces per level)
            indent_level = (len(line) - len(stripped)) / 4
            if indent_level > MAX_INDENT_LEVEL:
                indent_penalty += 0.5

            # Keywords
            if any(kw in stripped for kw in keywords):
                keyword_penalty += 0.2

        raw_score = 10.0 - length_penalty - indent_penalty - keyword_penalty
        return max(0.0, min(10.0, raw_score))

    def calculate_aes(self, content: str | None = None) -> float:
        """Calculates the Algorithmic Elegance Score (AES).
        Uses AST analysis for Python code and heuristics for others.
        """
        if not content:
            return DEFAULT_AES_SCORE

        try:
            return self._calculate_ast_complexity(content)
        except (SyntaxError, ValueError):
            return self._calculate_heuristic_score(content)
