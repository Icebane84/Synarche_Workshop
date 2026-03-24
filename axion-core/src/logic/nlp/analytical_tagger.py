"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-LOGIC-COG-TAGGER-001`   | The Sovereign ID. |
| **Official Name**   | `analytical_tagger.py`        | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-LOGIC-NLP`              | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Analytical Tagging (Law 28)**
> Implemented from Blueprint `GVRN.REG.AnalyticalTagging.md`.
> Ethos: The Tag is precise; The Understating is Truth.
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
    print(
        tagger.tag_content("The Phoenix Protocol is a GVRN standard for OMEGA systems.")
    )
