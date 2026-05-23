"""
# SOV-CENT-001: The Axion Activator (Sovereign Entry Point)

## Genesis Stamp: 2026-02-02 | Domain: SYNR | State: ACTIVE | Criticality: Foundational

### Block A: The Identification Lock (UIP-V13)

| Key | Value |
| :--- | :--- |
| **Artifact ID** | `SOV-CENT-001` |
| **Official Name** | `activate_axion.py` |
| **Version** | **v13.1 [OMEGA]** |
| **Domain** | `SYNR` |
| **Evolution** | **Omega Ascension** |
| **Status** | `[ACTIVE]` |
| **Relations** | `WIELDS: ALL_TOOLS`, `GOVERNED_BY: CORE-CODEX-001` |

### Block D: Standardized Synergy Block (The Loom Signature)
CORE-CODEX-001, GOVERNS, This entry point follows the Supreme Law.
CHAR-AXION-001, INSTANTIATES, This script wakes the Overplane.
"""

import logging
import sys
from pathlib import Path

# Configure Bootstrap Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [AXION] - %(levelname)s - %(message)s")
logger = logging.getLogger("AxionBoot")


def bootstrap():
    """
    Initializes the Axion Environment.
    """
    logger.info("Initializing Axion Prime [v13.1 Omega]...")

    # 1. Align Path
    SCRIPT_DIR = Path(__file__).resolve().parent
    SRC_PATH = SCRIPT_DIR / "src"
    if str(SRC_PATH) not in sys.path:
        sys.path.insert(0, str(SRC_PATH))

    logger.info(f"Source Path Aligned: {SRC_PATH}")

    # 2. Import Engine
    try:
        from agents.axion.agent_template import RPGEngine, app

        logger.info("RPGEngine Module Loaded.")
        return app
    except ImportError as e:
        logger.error(f"CRITICAL FAILURE: Could not import Axion Engine. {e}")
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
