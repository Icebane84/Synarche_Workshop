"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-WLF-LINTER-001`                | The Sovereign ID. |
| **Official Name** | `wlf_lore_linter.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `NARR`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-28`                       | Creation Date.    |.

Objective: The Star's Narrative Auditor — Ensuring the Soul of Where Light Fades.
"""

import argparse
import logging
import os
import sys

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    AxionCognition = None

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("wlf_linter")


class WLFLoreLinter:
    """The Star's specialized auditor for narrative consistency."""

    PILLARS = [
        "Moral Ambiguity",
        "Corruption",
        "Faith vs. Doubt",
        "Free Will vs. Destiny",
    ]
    TONE_KEYWORDS = [
        "oppressive",
        "gritty",
        "introspective",
        "dread",
        "haunted",
        "shadow",
    ]

    def __init__(self):
        self.cognition = AxionCognition() if AxionCognition else None

    def audit_file(self, file_path: str) -> bool:
        """Audits a single markdown draft for lore and thematic compliance."""
        logger.info(f"--- [WLF AUDIT] INITIATING: {os.path.basename(file_path)} ---")

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            issues = []

            # 1. NLP Tone Analysis
            if self.cognition:
                analysis = self.cognition.process(content)
                emotions = analysis.get("emotions", {})

                # Check for "Dread" or "Sadness" dominance
                if not any(k in ["sadness", "fear", "anger"] for k in emotions):
                    issues.append(
                        "[Tone] Lacks sufficient 'Oppressive/Dread' frequency (Low EQ resonance)."
                    )

                # Check for Magician Efficiency (as a proxy for coherence)
                if analysis.get("magician_efficiency", 0) < 0.8:
                    issues.append(
                        "[Coherence] Narrative intent is ambiguous or disjointed."
                    )

            # 2. Keyword/Pillar Presence
            missing_pillars = [
                p for p in self.PILLARS if p.lower() not in content.lower()
            ]
            if len(missing_pillars) > 2:
                issues.append(
                    f"[Pillars] Critical missing thematic links: {', '.join(missing_pillars)}"
                )

            # 3. POV and Character Checks
            if "I " in content and "POV: Kaelen" in content:
                issues.append(
                    "[POV] 1st Person detected in Kaelen's 3rd Person Limited POV."
                )

            if "Shadow" in content and not any(
                k in content.lower() for k in ["whisper", "voice", "internal"]
            ):
                issues.append(
                    "[Character] Shadow Self described as external/static rather than internal/psychic."
                )

            if issues:
                for issue in issues:
                    logger.error(f"> {issue}")
                return False

            logger.info(f"> SUCCESS: {os.path.basename(file_path)} is CANON-READY.")
            return True

        except Exception as e:
            logger.error(f"Audit failed for {file_path}: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="WLF Lore Linter — Narrative Consistency Auditor"
    )
    parser.add_argument("target", help="Markdown file or directory to audit")
    args = parser.parse_args()

    linter = WLFLoreLinter()
    target = os.path.abspath(args.target)

    if os.path.isfile(target):
        linter.audit_file(target)
    elif os.path.isdir(target):
        for f in os.listdir(target):
            if f.endswith(".md"):
                linter.audit_file(os.path.join(target, f))


if __name__ == "__main__":
    main()
