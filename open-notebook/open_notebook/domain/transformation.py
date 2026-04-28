
# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

from typing import ClassVar, Optional

from pydantic import Field

from open_notebook.domain.base import ObjectModel, RecordModel


class Transformation(ObjectModel):
    table_name: ClassVar[str] = "transformation"
    name: str
    title: str
    description: str
    prompt: str
    apply_default: bool


class DefaultPrompts(RecordModel):
    record_id: ClassVar[str] = "open_notebook:default_prompts"
    transformation_instructions: Optional[str] = Field(
        None, description="Instructions for executing a transformation"
    )
