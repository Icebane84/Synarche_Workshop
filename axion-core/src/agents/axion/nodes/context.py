"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-NODE-CONTEXT-001
Official Name: context.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Clarity through Cognition. Intent Decoded."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

import asyncio
import logging
from typing import Any

# Project Imports
from ..insforge_client import insforge
from ..schemas import AxionState
from logic.nlp.nlp_engine import AxionCognition

logger = logging.getLogger("axion.nodes.context")


def node_retrieve_context(state: AxionState) -> dict[str, Any]:
    """
    Triangulates narrative and logic context using the AxionCognition engine.
    Aligned with GVRN.CognitiveLoom requirements.
    """
    logger.info("--- [AXION] NODE: RETRIEVE CONTEXT ---")
    
    # Ensure we are working with the state object
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)
    
    # Invoke Cognition Engine (Modular Synthesis)
    cognition = AxionCognition()
    analysis = cognition.process(state_obj.input)
    
    # Map analysis to state
    state_obj.narrative_context = (
        f"Decoded Intent: {analysis.get('intent', 'Unknown')} | "
        f"Entities: {', '.join(analysis.get('entities', [])) if analysis.get('entities') else 'None'}"
    )
    state_obj.logic_context = (
        f"Tone: {analysis.get('tone', 'Neutral')} | "
        f"Emotive Vector: {analysis.get('emotions', 'Stable')}"
    )
    
    # Authoritative Logging to InsForge
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(insforge.log_event(
                type="NODE_RETRIEVAL",
                description="Axion retrieved cognitive context.",
                payload={
                    "intent": analysis.get("intent"),
                    "tone": analysis.get("tone")
                }
            ))
    except Exception as e:
        logger.warning(f"InsForge Signal Blocked: {e}")
        
    return state_obj.model_dump()
