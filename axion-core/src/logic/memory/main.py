"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `LOG-MEM-MAI-001`             | The Sovereign ID. |
| **Official Name**   | `main.py`                     | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `LOG-MEM`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Systemic Orchestration (Law 00)**
> Implemented from Blueprint `GVRN.REG.MemoryMain.md`.
> Ethos: Coherence through integration.
"""

import logging
import sys
from pathlib import Path

# Configure OMEGA logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [COG-MEM] - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Fix pathing to ensure src is in sys.path
root_path = Path(__file__).parents[3]
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

try:
    from src.logic.memory.memory_system import MemorySystem
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    # Fallback for alternative pathing or local execution
    try:
        from logic.memory.memory_system import MemorySystem  # type: ignore
        from logic.nlp.nlp_engine import AxionCognition  # type: ignore
    except ImportError:
        logger.exception("Failed to import core logic components. Ensure pathing is correct.")
        sys.exit(1)


def run_cognitive_memory_test() -> None:
    """
    Demonstrates the integration of NLP processing into the Memory Retrieval loop.
    Validates the connection between the NLP engine and the adaptive memory system.
    """
    logger.info("Initializing Sovereign Cognitive Memory Bridge...")

    try:
        # 1. Initialize Engines
        cognition = AxionCognition()
        memory = MemorySystem()

        test_query = "What is the status of the Phoenix Protocol?"
        logger.info(f"Processing Query: {test_query}")

        # 2. Extract Cognitive Metadata (THE CONNECT)
        analysis = cognition.process(test_query)
        logger.info(f"Magician Efficiency: {analysis.get('magician_efficiency', 0)}")

        # 3. Memory Retrieval using NLP vectors/lemmas
        results = memory.retrieve_memories(test_query, limit=3)

        if results:
            logger.info(f"Found {len(results)} matches in Sovereign Memory.")
            for i, res in enumerate(results):
                logger.info(f"Match {i + 1} [Score: {res.get('final_score', 'N/A')}]: {res.get('content')[:100]}...")
        else:
            logger.warning("No direct matches found. Triggering Uncertainty Protocol.")
            fallback = memory.handle_no_information(test_query, analysis)
            logger.info(f"Agent Fallback: {fallback}")

        logger.info("Cognitive Memory Bridge test completed successfully.")

    except Exception as e:
        logger.critical(f"Bridge Failure: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_cognitive_memory_test()
