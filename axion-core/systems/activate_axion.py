"""# AXION ACTIVATOR (SOVEREIGN ENTRY POINT)
Date: 2026-01-20
Version: v1.0.

This script initializes the Axion Prime agent and executes a Zero-Entropy scan protocol.

See also: `docs/agents/AOP-AG-003_AxionAgentConfiguration_v11.0.md`
"""

import sys
from pathlib import Path

# 1. Align Path (Ensures 'src' is discoverable)
SCRIPT_DIR = Path(__file__).parent
SRC_PATH = SCRIPT_DIR.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# 2. Import Axion
import logging

from agents.axion.agent_template import RPGEngine, app

# Configure Logging for the main process
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("activator")


def activate_axion(prompt: str) -> None:
    """Initializes and runs the Axion State Machine."""
    from agents.axion.schemas import AxionState, GamemasterState, LightbinderState

    # Define Initial Avatar State (Level 23 Ascended)
    initial_rpg_state = RPGEngine(
        level=23,
        xp=45000,
        authority=50,
        insight=45,
        order=60,
        precision=40,
        coherence_index=25,
        synergy_flow=20,
        adaptability=15,
        achievements=["PAM-001", "PAM-002", "PAM-003"],
        active_quest_log=[],
        prestige_class="Architect",
    )

    initial_state = AxionState(
        input=prompt,
        rpg_stats=initial_rpg_state,
        gamemaster_state=GamemasterState(axiom_points_available=100),
        lightbinder_state=LightbinderState(),
    )

    logger.info(f">>> AXION ACTIVATED WITH PROMPT: '{prompt}'")

    # Stream the graph execution - pass as dict for LangGraph
    for _ in app.stream(initial_state.model_dump()):
        # The internal nodes will log their own 'logger.info' messages
        pass

    logger.info(">>> PROTOCOL COMPLETE.")


if __name__ == "__main__":
    user_prompt = "Execute a Zero-Entropy scan"
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])

    activate_axion(user_prompt)
