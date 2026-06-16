"""[CORE] [SYSTEM] [ACTIVATOR]
Artifact ID: CORE.System.Activator
Official Name: activate_axion.py
Version: v15.0 [OMEGA]
Status: [CANONIZED]
Description: The Sovereign Entry Point for Axion Prime.

[UIP-V15]
| Key | Value |
| :--- | :--- |
| **Artifact ID** | `CORE.System.Activator` |
| **Official Name** | `activate_axion.py` |
| **Version** | **v15.0 [OMEGA]** |
| **Domain** | `CORE` |
| **Status** | `[CANONIZED]` |
| **Relations** | `WIELDS: ALL_TOOLS`, `GOVERNED_BY: CORE-CODEX-001` |

### Block D: Standardized Synergy Block (The Loom Signature)
CORE-CODEX-001, GOVERNS, This entry point follows the Supreme Law.
CHAR-AXION-001, INSTANTIATES, This script wakes the Overplane.
"""

import logging
import sys
from pathlib import Path

# Configure Bootstrap Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [AXION] - %(levelname)s - %(message)s",
)
logger = logging.getLogger("AxionPrime")


def bootstrap() -> None:
    """Initializes the Axion Environment."""
    logger.info("Initializing Axion Prime [v13.1 Omega]...")

    # 1. Align Path (Add project root to allow 'src.' prefix)
    script_dir: Path = Path(__file__).resolve().parent
    workspace_root: Path = script_dir.parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    if str(workspace_root) not in sys.path:
        sys.path.insert(0, str(workspace_root))

    logger.info(f"Project Root Aligned: {script_dir}")

    # 2. Import Engine
    try:
        from src.agents.axion import RPGEngine, app

        logger.info("Axion Engine [agent_template] Loaded.")
        return app
    except ImportError as e:
        logger.exception(f"CRITICAL FAILURE: Could not import Axion Engine. {e}")
        return None


if __name__ == "__main__":
    app_instance = bootstrap()
    if app_instance:
        logger.info(">> AXION IS AWAKE. <<")
        # In a real scenario, this might start a REPL or API server.
        # For now, we confirm awakening.
        print("\n[SYSTEM MESSAGE] Axion Prime is Online. Waiting for input...\n")
        # app_instance.run() # Uncomment if interactive
    else:
        sys.exit(1)

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.System.Activator VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-23
