"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.explanation.generator`                | The Sovereign ID. |
| **Official Name** | `explanation_generator.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | 0.95     |
# | **Resonance** | 0.92     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Cognitive Overload**| Summary Snippets          |
# | **Template Mismatch**| Fallback Mechanisms       |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Ensures transparency in decision-making.        |

## **[ARTIFACT END]**

Objective: Generates user-facing explanations for the agent's responses.
Conforms to OGLN/AISTF v15.0 governance and documentation standards.
"""

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.explanation.generator VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28

import json
import logging
from typing import Any

log = logging.getLogger(__name__)

DEFAULT_SNIPPET_LENGTH = 150
DEFAULT_TEMPLATES = {
    "factual_question": "My response was based on the following information:\n{memories_formatted}\n",
    "inference": "Based on the following information:\n{memories_formatted}\nI inferred that {inferred_relationship_text}.",
    "character_description": "Here's what I understand about the character based on:\n{memories_formatted}",
    "comparison": "To compare these items, I considered:\n{memories_formatted}",
    "no_memories": "I generated this response based on my general knowledge as I couldn't find specific relevant memories in my operational context.",
    "error_fallback": "I based my answer on the following sources: {memory_ids_list}",
    "action_confirmation": "Understood. Proceeding based on the following context:\n{memories_formatted}",
}


class ExplanationGenerator:
    """
    Generates user-facing explanations for the agent's responses.
    Translates internal cognitive states and memory retrievals into human-readable transparency blocks.
    """

    def __init__(self, templates: dict[str, str] | None = None) -> None:
        """
        Initializes the ExplanationGenerator with optional custom templates.

        Args:
            templates: A dictionary of intent-to-template string mappings.
        """
        self.templates: dict[str, str] = DEFAULT_TEMPLATES.copy()
        if templates:
            self.templates.update(templates)
        log.info("ExplanationGenerator (OMEGA) initialized.")

    def determine_query_type(self, query_analysis: dict[str, Any]) -> str:
        """
        Categorizes the query intent to select the appropriate explanation template.

        Args:
            query_analysis: Dictionary containing processed query metadata (intent, entities, lemmas).

        Returns:
            The identifier string for the selected template.
        """
        intent = query_analysis.get("user_intent_goal", "unknown")
        entities = query_analysis.get("entities", [])
        lemmas = set(query_analysis.get("lemmas", []))

        if any(w in lemmas for w in ["compare", "vs", "difference"]):
            return "comparison"

        if any(label in ["PERSON", "CHARACTER", "ORG"] for _, label in entities):
            return "character_description"

        if intent == "seeking_information":
            return "factual_question"

        if intent == "requesting_action":
            return "action_confirmation"

        return "factual_question"

    def _format_memory_citation(self, memory: dict[str, Any]) -> str:
        """
        Formats a single memory citation block for inclusion in the explanation.

        Args:
            memory: The raw memory dictionary.

        Returns:
            A formatted citation string (e.g., (Resonance: CORE#123)).
        """
        domain = memory.get("domain", "GVRN.NULL")
        mem_id = memory.get("id", "UNK-000")
        return f"(Resonance: {domain}#{mem_id})"

    def generate(
        self,
        query_analysis: dict[str, Any],
        used_memories: list[dict[str, Any]],
        inferred_relationship: str | None = None,
        snippet_length: int = DEFAULT_SNIPPET_LENGTH,
    ) -> str:
        """
        Orchestrates the generation of a complete explanation block.

        Args:
            query_analysis: Analysis of the user's query.
            used_memories: List of memories used in the response generation.
            inferred_relationship: Optional text describing an inferred link between concepts.
            snippet_length: Maximum length for memory snippets.

        Returns:
            The complete, formatted explanation string.
        """
        if not used_memories:
            return self.templates.get("no_memories", "")

        query_type = self.determine_query_type(query_analysis)
        template_str = self.templates.get(query_type, self.templates["factual_question"])

        formatted_memory_list = []
        for mem in used_memories:
            content = mem.get("content", "")
            content_str = json.dumps(content) if isinstance(content, dict) else str(content)
            snippet = content_str[:snippet_length] + ("..." if len(content_str) > snippet_length else "")
            citation = self._format_memory_citation(mem)
            formatted_memory_list.append(f"* {snippet} {citation}")

        memories_formatted = "\n".join(formatted_memory_list)
        memory_ids = ", ".join([str(m.get("id", "UNK")) for m in used_memories])

        format_kwargs = {
            "memories_formatted": memories_formatted,
            "memory_ids_list": memory_ids,
            "inferred_relationship_text": inferred_relationship or "a conceptual resonance",
        }

        try:
            return template_str.format(**format_kwargs)
        except Exception as e:
            log.exception(f"Explanation formatting error: {e}")
            return f"Aligned with findings: {memory_ids}"


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.explanation.generator VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28
# ---
