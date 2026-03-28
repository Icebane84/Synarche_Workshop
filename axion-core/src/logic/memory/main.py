"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.main`                | The Sovereign ID. |
| **Official Name** | `main.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

---

## **Block B: State Vector (AGP-001)**

| State Field   | Value     |
| :------------ | :-------- |
| **Coherence** | `{resonance}`     |
| **Resonance** | `{resonance}`     |
| **Stability** | `Stable`  |

---

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                |
| :------------------- | :------------------------ |
| **Logic Drift**      | Strict Linter Enforcement |
| **Semantic Decay**   | Axiomatic Compass Audit   |

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
| :---------------------- | :---------------- | :---------------------------------------------- |
| `CORE.Codex.Phoenix`    | `GOVERNS`         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**
"""

import logging
import sys
from pathlib import Path

# Fix pathing
# Path of this file: axion-core/src/logic/memory/main.py
# src root is 3 levels up: axion-core/src/
sys.path.append(str(Path(__file__).parents[3]))

try:
    from src.logic.memory.memory_system import MemorySystem
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    # Fallback for alternative pathing
    try:
        from logic.memory.memory_system import MemorySystem  # type: ignore
        from logic.nlp.nlp_engine import AxionCognition  # type: ignore
    except ImportError:
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        logger.error(
            "Failed to import core logic components. Ensure pathing is correct."
        )
        sys.exit(1)

# Configure OMEGA logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [COG-MEM] - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_cognitive_memory_test() -> None:
    """Demonstrates the integration of NLP processing into the Memory Retrieval loop."""
    logger.info("Initializing Sovereign Cognitive Memory Bridge...")

    try:
        # 1. Initialize Engines
        cognition = AxionCognition()
        memory = MemorySystem()

        test_query = "What is the status of the Phoenix Protocol?"
        logger.info(f"Processing Query: {test_query}")

        # 2. Extract Cognitive Metadata (THE CONNECT)
        analysis = cognition.process(test_query)
        logger.info(f"Magician Efficiency: {analysis['magician_efficiency']}")

        # 3. Memory Retrieval using NLP vectors/lemmas
        results = memory.retrieve_memories(test_query, limit=3)

        if results:
            logger.info(f"Found {len(results)} matches in Sovereign Memory.")
            for i, res in enumerate(results):
                logger.info(
                    f"Match {i + 1} [Score: {res.get('final_score', 'N/A')}]: {res.get('content')[:100]}..."
                )
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

# ---
# 
# ---

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: CORE.main VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 508ca40a88396121`
