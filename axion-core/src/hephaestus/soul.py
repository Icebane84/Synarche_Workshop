"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `METRIC-AES-001`              | The Sovereign ID. |
| **Official Name**   | `soul.py`                     | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ARCH-METRIC`                 | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Operational`                 | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Elegance Axiom: Algorithmic Soul (Law 7)**
> Implemented from Blueprint `GVRN.ARCH.Soul.md`.
> Ethos: Guardian of Elegance.
"""

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

    def calculate_aes(self, content: str | None = None) -> float:
        """Calculates the Algorithmic Elegance Score (AES).
        Uses AST analysis for Python code and heuristics for others.
        """
        if not content:
            return DEFAULT_AES_SCORE

        try:
            # OPTION C: Native AST Analysis
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
                    ),
                ):
                    complexity += 1
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity += 1  # Base complexity for function

            # A complexity of 50 (very high) results in 5.0 score.
            score = 10.0 - (complexity * 0.1)
            return max(0.0, min(10.0, score))

        except (SyntaxError, ValueError):
            # OPTION A: Heuristic Fallback
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
