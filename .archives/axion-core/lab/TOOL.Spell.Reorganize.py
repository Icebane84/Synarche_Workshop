"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL.Spell.Reorganize`                | The Sovereign ID. |
| **Official Name** | `TOOL.Spell.Reorganize.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-28`                       | Creation Date.    |.

Objective: Structural transmutation of the library with cognitive validation.
"""

import argparse
import logging
import os
import shutil
import sys

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    AxionCognition = None

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("spell_reorganizer")


class SpellReorganizer:
    """The Knight of Swords' Transmutation Spell."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.cognition = AxionCognition() if AxionCognition else None

        # OMEGA RNC Pattern Mappings
        self.domain_map = {
            "GVRN": "src/logic/governance",
            "COG": "src/logic/nlp",
            "ARCH": "src/logic/architecture",
            "SYNG": "src/logic/synergy",
            "COMM": "src/logic/communication",
            "LOGS": "src/logic/logs",
            "ACT": "tools",
            "WLF": "src/narrative/wlf",
        }

    def validate_content(self, file_path: str, target_domain: str) -> bool:
        """Uses NLP to verify if file content matches the target domain."""
        if not self.cognition:
            return True  # Fallback if nlp is missing

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read(2000)  # Read start for metadata

            analysis = self.cognition.process(content)
            entities = [ent[0].upper() for ent in analysis.get("entities", [])]

            # Simple heuristic: Does the target domain appear in entities or keywords?
            if target_domain in entities or target_domain.lower() in content.lower():
                return True

            # Check for efficiency/intent markers
            if analysis.get("magician_efficiency", 0) > 1.2:
                return True  # High confidence manifest

            return False
        except Exception as e:
            logger.warning(f"Cognitive validation failed for {file_path}: {e}")
            return True  # Permissive fallback

    def reorganize(self, source_dir: str):
        """Scans and proposes moves based on RNC prefixes."""
        logger.info(f"--- INITIATING TRANSMUTATION: {source_dir} ---")

        for root, _dirs, files in os.walk(source_dir):
            if ".git" in root or "__pycache__" in root:
                continue

            for f in files:
                if not f.endswith((".py", ".md")):
                    continue

                # Check for RNC prefix (e.g., GVRN.Policy.md)
                prefix = f.split(".")[0] if "." in f else ""

                if prefix in self.domain_map:
                    target_dir = self.domain_map[prefix]
                    source_path = os.path.join(root, f)
                    dest_path = os.path.join(target_dir, f)

                    if os.path.abspath(source_path) == os.path.abspath(dest_path):
                        continue

                    # Cognitive Validation
                    if not self.validate_content(source_path, prefix):
                        logger.warning(
                            f"[Dissonance] {f} failed cognitive alignment for {prefix}. Skipping."
                        )
                        continue

                    if self.dry_run:
                        logger.info(f"[PROPOSAL] Move {f} -> {target_dir}")
                    else:
                        try:
                            os.makedirs(target_dir, exist_ok=True)
                            shutil.move(source_path, dest_path)
                            logger.info(f"[TRANSMUTED] {f} -> {target_dir}")
                        except Exception as e:
                            logger.error(f"Failed to move {f}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Spell Reorganizer — Structural Transmutation"
    )
    parser.add_argument("source", help="Directory to scan")
    parser.add_argument(
        "--execute", action="store_true", help="Actually move the files"
    )
    args = parser.parse_args()

    reorganizer = SpellReorganizer(dry_run=not args.execute)
    reorganizer.reorganize(os.path.abspath(args.source))


if __name__ == "__main__":
    main()
