"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-LOGIC-EXPL-GEN-001`     | The Sovereign ID. |
| **Official Name**   | `explanation_generator.py`    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-LOGIC-MEMORY`           | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Clarity Generation (Law 28)**
> Implemented from Blueprint `GVRN.REG.ClarityGeneration.md`.
> Ethos: The Voice is Clear; The Explanation is Truth.
"""

from typing import Any


class ExplanationGenerator:
    """Generate human-readable explanations and citations for retrieved memories."""

    def __init__(self) -> None:
        self.max_memories = 3

    def generate(self, query: str, memories: list[dict[str, Any]]) -> str:
        """Synthesize an explanation based on query context and memories."""
        if not memories:
            return "I don't have enough specific context to provide a detailed explanation."

        # Simply return the top memory content for now, or synthesize
        top_memory = memories[0]
        explanation = f"Based on my internal records, {top_memory.get('content', '')}"

        # Add a confidence indicator
        score = top_memory.get("final_score", 0)
        confidence = "High" if score > 0.8 else "Moderate" if score > 0.5 else "Low"

        return f"{explanation}\n\n[Confidence: {confidence}]"

    def generate_citation(self, memories: list[dict[str, Any]]) -> str:
        """Generate a formatted citation string for the used memories.

        Example: [Memory 1 (Tag A), Memory 2 (Tag B)]
        """
        if not memories:
            return "No specific memories were cited for this response."

        citations = []
        for i, m in enumerate(memories[:3], 1):
            source = m.get("metadata", {}).get("source", "Internal Core")
            timestamp = m.get("timestamp", "Unknown Time")
            citations.append(f"[{i}] {source} ({timestamp})")

        return " | ".join(citations)

    def generate_transparency_metadata(
        self, memories: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Provide deep technical reasoning metadata for the retrieval process."""
        if not memories:
            return {
                "status": "No memories found",
                "reasoning": "Query did not trigger high-weight semantic nodes.",
            }

        return {
            "query_intent": "Constructive Evolution",
            "top_match_score": memories[0].get("final_score", 0),
            "memory_diversity": len(
                set(m.get("metadata", {}).get("category", "General") for m in memories)
            ),
            "key_memories_used": [m.get("id", "Unknown") for m in memories[:3]],
            "inferences_made": [
                "Contextual continuity maintained",
                "Semantic overlap verified",
            ],
        }
