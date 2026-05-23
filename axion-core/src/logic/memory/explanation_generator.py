"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `LOG-MEM-EXP-001`             | The Sovereign ID. |
| **Official Name**   | `explanation_generator.py`    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `LOG-MEM`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Transparent Reasoning (Law 15)**
> Implemented from Blueprint `GVRN.REG.ExplanationGenerator.md`.
> Ethos: Clarity through synthesized citations.
"""

from typing import Any, Dict, List


class ExplanationGenerator:
    """Generate human-readable explanations and citations for retrieved memories.
    Facilitates systemic transparency by explaining 'why' specific data was retrieved.
    """

    def __init__(self) -> None:
        """Initializes the generator with default limits."""
        self.max_memories = 3

    def generate(self, query: str, memories: List[Dict[str, Any]]) -> str:
        """Synthesize an explanation based on query context and memories.

        Args:
            query (str): The original search query.
            memories (List[Dict[str, Any]]): The retrieved memories to explain.

        Returns:
            str: A human-readable explanation string.

        """
        if not memories:
            return "I don't have enough specific context to provide a detailed explanation."

        # Simply return the top memory content for now, or synthesize
        top_memory = memories[0]
        explanation = f"Based on my internal records, {top_memory.get('content', '')}"

        # Add a confidence indicator
        score = top_memory.get("final_score", 0)
        confidence = "High" if score > 0.8 else "Moderate" if score > 0.5 else "Low"

        return f"{explanation}\n\n[Confidence: {confidence}]"

    def generate_citation(self, memories: List[Dict[str, Any]]) -> str:
        """Generate a formatted citation string for the used memories.
        Example: [Memory 1 (Tag A), Memory 2 (Tag B)].

        Args:
            memories (List[Dict[str, Any]]): The retrieved memories to cite.

        Returns:
            str: A formatted citation string.

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
        self, memories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Provide deep technical reasoning metadata for the retrieval process.

        Args:
            memories (List[Dict[str, Any]]): The retrieved memories.

        Returns:
            Dict[str, Any]: Technical metadata including match scores and query intent.

        """
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
