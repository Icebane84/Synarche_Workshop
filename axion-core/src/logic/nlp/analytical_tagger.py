"""CORE-LOGIC-COG-TAGGER-001 (analytical_tagger.py)
Status: [CANONIZED]
Genesis Stamp: 2026-03-07.

 COG-TAGGER-001: Analytical Tagger (The Hermit's Lantern)
 v14.0 [OMEGA] - Cognitive tagging hub.
 Ethos: "Categorization is the first step of Understanding."
"""

import logging

try:
    from .nlp_engine import AxionCognition
except (ImportError, ValueError):
    try:
        from src.logic.nlp.nlp_engine import AxionCognition
    except ImportError:
        AxionCognition = None

logger = logging.getLogger(__name__)


class AnalyticalTagger:
    """The Hermit's Lantern — Cognitive Tagging Hub."""

    def __init__(self):
        self.cognition = AxionCognition() if AxionCognition else None

    def tag_content(self, content: str) -> dict[str, list[str]]:
        """Unified tagging method for the Event Horizon loop."""
        tags = self.tag_memory(content)
        return {"tags": tags}

    def tag_memory(self, content: str) -> list[str]:
        """Generates semantic tags for a given memory content."""
        if not self.cognition:
            return ["GENERIC"]

        analysis = self.cognition.process(content)
        entities = [ent[0].upper() for ent in analysis.get("entities", [])]
        keywords = [kw.upper() for kw in analysis.get("topic_keywords", [])]

        # Heuristic tagging
        tags = set(entities) | set(keywords)

        if analysis.get("magician_efficiency", 1.0) > 1.2:
            tags.add("HIGH_RESONANCE")

        if "OMEGA" in content.upper():
            tags.add("OMEGA_ALIGNED")

        return list(tags) if tags else ["UNTAGGED"]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tagger = AnalyticalTagger()
    print(tagger.tag_content("The Phoenix Protocol is a GVRN standard for OMEGA systems."))
