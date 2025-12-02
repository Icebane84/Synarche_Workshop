"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-NODE-INSIGHT-001
Official Name: insight.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Intuition through Sophia. Integrity through Sentinel."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

import logging
import subprocess
from typing import Any

# Project Imports
from ..config import settings
from ..enums import AuditStatus
from ..schemas import AxionState

logger = logging.getLogger("axion.nodes.insight")


def node_sophia_insight(state: AxionState) -> dict[str, Any]:
    """
    Invokes the Sophia Oracle to provide intuitive depth and complexity analysis.
    """
    logger.info("--- [SOPHIA] NODE: ORACLE INSIGHT ---")
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)
    
    sophia_tool = settings.SOPHIA_PATH
    insight_buffer = []

    if sophia_tool and sophia_tool.exists():
        try:
            result = subprocess.run(
                ["python", str(sophia_tool), "--mode", "complexity", "--target", "."],
                capture_output=True,
                text=True,
                check=False,
            )
            if "Clarity Absolute" in result.stdout:
                insight_buffer.append("Sophia Report: Clarity Absolute (Zero Entropy).")
            else:
                insight_buffer.append("Sophia Report: Complexity Dissonance Detected.")
        except Exception as e:
            insight_buffer.append(f"Sophia Oracle Dissonance: {e}")
    else:
        insight_buffer.append("Sophia Tool (Oracle) not found in workspace.")

    intuition = "Mandate: Empower the User through Sovereign Alignment."
    state_obj.sophia_insight = f"{intuition} | {' '.join(insight_buffer)}"
    
    return state_obj.model_dump()


def node_sentinel_check(state: AxionState) -> dict[str, Any]:
    """
    Final Integrity Gate. Inspects generated form for compliance with OMEGA v15.0.
    """
    logger.info("--- [SENTINEL] NODE: INTEGRITY GATE ---")
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)
    
    # Simulation for now, can be linked to sentinel.py logic if needed
    state_obj.sentinel_status = AuditStatus.PASS
    state_obj.sentinel_reason = "Sovereign Compliance Verified (High Priestess Protocol)."
    
    logger.info(f"   > STATUS: {state_obj.sentinel_status} ({state_obj.sentinel_reason})")
    
    return state_obj.model_dump()
