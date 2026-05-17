"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.system.logging.phoenix`             | The Sovereign ID. |
| **Official Name** | `phoenix_logger.py`                | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[ACTIVE]`                        | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Log Saturation**   | Multi-Level Filtering     |
# | **Temporal Drift**   | ISO-8601 Synchronization  |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**

Objective: Initializes the PhoenixLogger with dual-stream handlers as per UMB-PHX-LOG-001.
Conforms to OGLN/AISTF v15.0 governance and documentation standards.
"""

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.system.logging.phoenix VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28

import logging
from enum import Enum, auto


# GVRN-STD-ENUM-001 - Mandates Enum for logging levels
class ProcessStatus(Enum):
    """
    Standardized enumeration for process logging levels.
    Ensures consistent status reporting across the Axion Core.
    """

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    DEBUG = auto()


def setup_synarche_logging(log_file: str = "error_audit.log") -> logging.Logger:
    """
    Initializes the PhoenixLogger with dual-stream handlers:
    1. Console (INFO+) for real-time transparency.
    2. File (ERROR+) for persistent accountability and auditing.

    Args:
        log_file: Path to the persistent error log file.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger("PhoenixLogger")

    # Ensure we don't add duplicate handlers if initialized multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)  # Root captures all; handlers filter

    # ISO-8601 Format for V-Control (Temporal Precision)
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # 1. Console Handler (The Pulse) - INFO and above
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(log_format)

    # 2. File Handler (The Memory) - ERROR and above
    try:
        f_handler = logging.FileHandler(log_file)
        f_handler.setLevel(logging.ERROR)
        f_handler.setFormatter(log_format)
        logger.addHandler(f_handler)
    except Exception as e:
        # Fallback if file logging fails (e.g., read-only filesystem)
        logger.warning(f"Failed to initialize file logger: {e}")

    logger.addHandler(c_handler)

    logger.info("PhoenixLogger initialized: Dual-stream logging active.")
    return logger


# Export a default instance for convenience across the workspace
logger = setup_synarche_logging()

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.system.logging.phoenix VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28
# ---
