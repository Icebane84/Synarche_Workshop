"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-AGT-COR-001`            | The Sovereign ID. |
| **Official Name**   | `core.py`                     | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-AGT`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Core Orchestration (Law 37)**
> Implemented from Blueprint `GVRN.REG.AgentCore.md`.
> Ethos: Purpose through Orchestration.
"""

import logging
import time
from typing import Optional

# Absolute imports from the src root
from src.logic.memory.memory_system import MemorySystem
from src.logic.nlp.analytical_tagger import AnalyticalTagger
from src.logic.nlp.nlp_engine import AxionCognition
from src.logic.utils.explanation_generator import ExplanationGenerator

logger = logging.getLogger(__name__)

# --- CONSTANTS ---
MIN_QUERY_LENGTH: int = 10


class AxionAgentCore:
    """The central orchestration engine for Axion Core."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialize the Axion Agent Core Vessel.

        Args:
            db_path (Optional[str]): Path to the memory database.

        """
        self.cognition = AxionCognition()
        self.memory = MemorySystem(db_path=db_path)
        self.explanation = ExplanationGenerator(self.cognition)
        self.tagger = AnalyticalTagger()

        self.session_id = f"AXION-{int(time.time())}"
        logger.info(f"AxionAgentCore initialized. Session: {self.session_id}")

    def process_event(self, user_query: str) -> str:
        """Executes the 'Event Horizon' processing loop.

        Args:
            user_query (str): The raw input from the user.

        Returns:
            str: The generated response or an error message.

        """
        start_time = time.time()
        logger.info(f"Processing Event: {user_query[:50]}...")

        try:
            # 1. ANALYZE
            self.cognition.process(user_query)

            # 2. RETRIEVE
            memories = self.memory.retrieve_memories(user_query, limit=5)

            # 3. SYNTHESIZE
            response = self.explanation.generate_explanation(user_query, memories)

            # 4. TAG
            tags = self.tagger.tag_content(response)

            # 5. LOG
            duration = time.time() - start_time
            self.memory.log_experience(
                event_type="EVENT_HORIZON_COMPLETED",
                module="AxionAgentCore",
                details={
                    "query_length": len(user_query),
                    "match_count": len(memories),
                    "duration_ms": int(duration * 1000),
                    "tags": tags.get("tags", []),
                    "session_id": self.session_id,
                },
                impact=0.1 if memories else 0.05,
            )

            # 6. LEARN
            if len(user_query) > MIN_QUERY_LENGTH:
                self.memory.add_memory(
                    content=f"User asked: {user_query} | Response: {response[:100]}...",
                    domain="InteractionHistory",
                    relevance=0.4,
                    confidence=0.9,
                    tags=tags.get("tags", []),
                    source="AgentCore",
                )

        except Exception as e:
            logger.exception("Event Horizon collapsed")
            return f"I encountered a cognitive dissonance while processing that request: {e}"
        else:
            return response

    def run_maintenance(self) -> None:
        """Triggers the memory decay and transition cycle."""
        logger.info("Starting cognitive maintenance cycle...")
        self.memory.maintenance_cycle()
