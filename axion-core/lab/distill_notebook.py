"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-DISTILL-NOTE-001`                | The Sovereign ID. |
| **Official Name** | `distill_notebook.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-28`                       | Creation Date.    |.

Objective: The High Priestess's Transmutation Pipeline — From Chaos to Order.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from typing import Any

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    AxionCognition = None

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("distiller")


class DistillNotebook:
    """The High Priestess's knowledge synthesis pipeline."""

    def __init__(self):
        self.cognition = AxionCognition() if AxionCognition else None
        self.assembler_path = os.path.join(os.path.dirname(__file__), "assembler.py")

    def analyze_note(self, content: str) -> dict[str, Any]:
        """Uses NLP to determine the best Synarchy archetype for a note."""
        if not self.cognition:
            return {"type": "SELT", "intent": "Generic Note"}

        analysis = self.cognition.process(content)
        intent = analysis.get("user_intent_goal", "unknown").lower()
        entities = [ent[0].lower() for ent in analysis.get("entities", [])]

        # Archetype logic
        if "policy" in content.lower() or "governance" in content.lower():
            archetype = "UMB"  # Blueprint
        elif "how to" in content.lower() or intent == "requesting_action":
            archetype = "AOP"  # Playbook
        elif "observation" in content.lower() or "lore" in content.lower():
            archetype = "CSL"  # Collaborative Synthesis
        else:
            archetype = "SELT"  # Standard Block

        return {
            "type": archetype,
            "intent": intent,
            "entities": entities,
            "efficiency": analysis.get("magician_efficiency", 1.0),
        }

    def distill(self, note_path: str, output_id: str):
        """Processes a note and invokes assembler.py to nucleate it."""
        logger.info(f"--- [DISTILL] PROCESSING: {os.path.basename(note_path)} ---")

        try:
            with open(note_path, encoding="utf-8") as f:
                content = f.read()

            prediction = self.analyze_note(content)
            logger.info(f"> Predicted Archetype: {prediction['type']} (Intent: {prediction['intent']})")

            # Prepare metadata for assembler
            meta = {
                "artifact_id": output_id,
                "domain": "GVRN" if prediction["type"] == "UMB" else "ACT",
                "evolution": "Distilled from Open-Notebook",
                "empathy_vector": f"Focused on {', '.join(prediction['entities'][:3])}",
                "magician_efficiency": prediction["efficiency"],
            }

            meta_path = f"{output_id}_meta.json"
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f)

            # Invoke Assembler
            cmd = [
                sys.executable,
                self.assembler_path,
                "--id",
                output_id,
                "--type",
                prediction["type"],
                "--meta",
                meta_path,
                "--cognition",
                "--out",
                f"{output_id}.md",
            ]

            logger.info(f"> Invoking Forge Engine: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"--- [SUCCESS] ARTIFACT NUCLEATED: {output_id}.md ---")
                os.remove(meta_path)
            else:
                logger.error(f"Forge failed: {result.stderr}")

        except Exception as e:
            logger.error(f"Distillation failed for {note_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Distill Notebook — Knowledge Physicalization")
    parser.add_argument("note", help="Path to raw note file")
    parser.add_argument("--id", required=True, help="Target Artifact ID")
    args = parser.parse_args()

    distiller = DistillNotebook()
    distiller.distill(os.path.abspath(args.note), args.id)


if __name__ == "__main__":
    main()
