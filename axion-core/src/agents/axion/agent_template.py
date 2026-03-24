"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-AGENT-TEMPLATE-001`     | The Sovereign ID. |
| **Official Name**   | `agent_template.py`           | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-AGENTS`                 | The Subject.      |
| **Celestial Class** | `[VESSEL]`                    | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Agentic Vessel (Law 28)**
> Implemented from Blueprint `GVRN.REG.AgenticVessel.md`.
> Ethos: The Vessel is Hollow; The Will is Truth.
"""

import asyncio

import structlog

# Core Package Imports
from .config import settings
from .core import AxionAgentCore
from .enums import AuditStatus, LogType
from .runtime import AxionRuntime, app
from .schemas import AxionState, GamemasterState, LightbinderState, RPGEngine

# Legacy/External Logic Imports
try:
    from ...logic.memory.memory_system import MemorySystem
    from ...logic.nlp.nlp_engine import AxionCognition
    from ...utils.experience_logger import ExperienceLogger
except ImportError:
    # Resilience for different execution environments
    MemorySystem = None
    AxionCognition = None
    ExperienceLogger = None

# --- LOGGING SETUP ---
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)
logger = structlog.get_logger()

# Re-export key components for backward compatibility
__all__ = [
    "AuditStatus",
    "AxionAgentCore",
    "AxionRuntime",
    "AxionState",
    "LogType",
    "RPGEngine",
    "app",
    "settings",
]

if __name__ == "__main__":
    # Test execution of the consolidated loop
    async def run_test() -> None:
        """Execute a cognitive loop test for the Axion Agent Vessel."""
        runtime = AxionRuntime()
        instance = runtime.app

        rpg = RPGEngine(
            level=23,
            xp=45000,
            authority=50,
            insight=45,
            order=60,
            precision=40,
            coherence_index=25,
            synergy_flow=20,
            adaptability=15,
            transparency=10,
            prestige_class="Architect",
        )

        state = AxionState(
            input="Review the Synarchy Protocol for Zero Entropy.",
            rpg_stats=rpg,
            gamemaster_state=GamemasterState(),
            lightbinder_state=LightbinderState(),
        )

        logger.info("axion.template.test", status="invoked")
        async for event in instance.astream(state.model_dump()):
            print(event)

    asyncio.run(run_test())
