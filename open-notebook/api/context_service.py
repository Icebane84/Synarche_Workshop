"""
Context service layer using API.
"""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP


from typing import Any, Dict, List, Optional, Union

from loguru import logger

from api.client import api_client


class ContextService:
    """Service layer for context operations using API."""

    def __init__(self):
        logger.info("Using API for context operations")

    def get_notebook_context(
        self, notebook_id: str, context_config: Optional[Dict] = None
    ) -> Union[Dict[Any, Any], List[Dict[Any, Any]]]:
        """Get context for a notebook."""
        result = api_client.get_notebook_context(
            notebook_id=notebook_id, context_config=context_config
        )
        return result


# Global service instance
context_service = ContextService()
