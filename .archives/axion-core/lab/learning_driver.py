"""ID: ACT-LEARN-DRIVER-001
Version: v1.0
Domain: GVRN.AISTF
Ethos: "Errors are not failures; they are data points of evolution."
Description: Learning Driver for the AI Self-Training Framework (AISTF).
Scans logs for GVRN.LOG.INGEST and distills recursive lessons.
"""

import logging
import os
import sys
from pathlib import Path

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    AxionCognition = None

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("learning_driver")


class LearningDriver:
    """The Engine of Recursive Evolution (AISTF)."""

    def __init__(self, logs_dir: str = "src/logic/logs"):
        self.logs_dir = Path(logs_dir)
        self.cognition = AxionCognition() if AxionCognition else None
        self.rules_path = Path("axion-rules.cjs")

    def scan_for_failures(self) -> list[str]:
        """Scans the logs directory for failure files or AUDIT_FAIL substrings."""
        failures = []
        if not self.logs_dir.exists():
            logger.warning(f"Logs directory {self.logs_dir} not found.")
            return failures

        for log_file in self.logs_dir.glob("*.log"):
            try:
                with open(log_file, encoding="utf-8") as f:
                    content = f.read()
                    if "AUDIT_FAIL" in content or "ERROR" in content:
                        failures.append(content)
            except Exception as e:
                logger.error(f"Failed to read log {log_file}: {e}")
        return failures

    def distill_lesson(self, failure_context: str) -> str:
        """Uses NLP to extract a concise rule recommendation from failure content."""
        if not self.cognition:
            return "Ensure input validation is strictly reinforced."

        analysis = self.cognition.process(failure_context)
        entities = [ent[0] for ent in analysis.get("entities", [])]

        # Basic distillation heuristic
        lesson = f"Reinforce {', '.join(entities[:2])} validation logic in compliance with OMEGA v14.0."
        if "AttributeError" in failure_context:
            lesson = "Verify property existence before invocation (Attribute Safety)."
        elif "ImportError" in failure_context:
            lesson = "Ensure dependency tree is resolved within the local Workspace before execution."

        return lesson

    def evolve(self):
        """Orchestrates the learning loop."""
        logger.info("--- INITIATING LEARNING CYCLE (AISTF) ---")

        failures = self.scan_for_failures()
        if not failures:
            logger.info("> No critical failures detected. Coherence remains high.")
            return

        logger.info(f"> Found {len(failures)} failure contexts. Distilling insights...")

        lessons = [self.distill_lesson(f) for f in failures]

        # In a real OMEGA system, this would write to axion-rules.cjs or a knowledge base
        logger.info("--- SYNTHESIZED LESSONS ---")
        for i, lesson in enumerate(set(lessons), 1):
            logger.info(f"[{i}] {lesson}")

        logger.info("--- EVOLUTION COMPLETE ---")


def main():
    driver = LearningDriver()
    driver.evolve()


if __name__ == "__main__":
    main()
