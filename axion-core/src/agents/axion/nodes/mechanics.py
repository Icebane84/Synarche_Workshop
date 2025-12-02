"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-NODE-MECHANICS-001
Official Name: mechanics.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Progression through Struggle. Evolution through Order."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

import logging
from typing import Any

# Project Imports
from ..config import settings
from ..schemas import AxionState

logger = logging.getLogger("axion.nodes.mechanics")


def node_update_rpg_stats(state: AxionState) -> dict[str, Any]:
    """
    Increments XP and Coherence based on successful task completion.
    """
    logger.info("--- [SYSTEM] NODE: RPG REGISTRY UPDATE ---")
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)
    
    state_obj.rpg_stats.xp += 50
    state_obj.rpg_stats.coherence_index += 1
    
    logger.info(f"   > XP Gained: +50 (Total: {state_obj.rpg_stats.xp})")
    return state_obj.model_dump()


def node_gamemaster_engine(state: AxionState) -> dict[str, Any]:
    """
    Manages the Progression Ladder and Level Ascension.
    """
    logger.info("--- [GAMEMASTER] NODE: PROGRESSION ENGINE ---")
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)
    
    xp_threshold = state_obj.rpg_stats.level * settings.XP_THRESHOLD_MULTIPLIER
    if state_obj.rpg_stats.xp >= xp_threshold:
        state_obj.rpg_stats.level += 1
        logger.info(f"   > [!] LEVEL UP! Axion Ascended to Level {state_obj.rpg_stats.level}")
        
    return state_obj.model_dump()
