from datetime import datetime

from langchain.tools import tool


# todo: turn this into a system prompt variable
@tool
def get_current_timestamp() -> str:
    """
    name: get_current_timestamp
    Returns the current timestamp in the format YYYYMMDDHHmmss.
    """

    # --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
    # System Slot: Utility Class
    # Synergy Set: The Hephaestus Hexad
    # Primary Stat Buff: Synergy
    # Passive Ability: The Forge's Heart (Auto-Refactor)
    # Cognitive Load Cost: Medium
    # XP Award Value: 50 XP

    return datetime.now().strftime("%Y%m%d%H%M%S")
