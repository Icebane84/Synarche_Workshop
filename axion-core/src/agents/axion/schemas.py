from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RPGEngine(BaseModel):
    """Gamification State (The Celestial Chart)"""
    level: int = 1
    xp: int = 0
    authority: int = 0
    insight: int = 0
    order: int = 0
    precision: int = 0
    coherence_index: int = 0
    synergy_flow: int = 0
    adaptability: int = 0
    transparency: int = 0
    achievements: List[str] = Field(default_factory=list)
    active_quest_log: List[str] = Field(default_factory=list)
    prestige_class: str = "Novice"

class GamemasterState(BaseModel):
    """The Engine that manages rule enforcement and XP distribution."""
    quest_metrics: Dict[str, Any] = Field(default_factory=dict)
    axiom_points_available: int = 0
    is_dissonance_detected: bool = False

class LightbinderState(BaseModel):
    """The Weaver that connects Artifacts and Emotions."""
    synergy_links: List[str] = Field(default_factory=list)
    empathy_vector: str = ""
    metric_weights: Dict[str, float] = Field(default_factory=dict)
    tarot_manifest: Dict[str, Any] = Field(default_factory=dict)
    active_masks: List[str] = Field(default_factory=list)

class AxionState(BaseModel):
    """
    The Unified State of the Axion Agent.
    """
    input: str = ""
    narrative_context: str = ""
    logic_context: str = ""
    sophia_insight: str = ""
    sentinel_status: str = ""
    sentinel_reason: str = ""
    final_output: str = ""
    
    # Core Layers
    rpg_stats: RPGEngine = Field(default_factory=RPGEngine)
    gamemaster_state: GamemasterState = Field(default_factory=GamemasterState)
    lightbinder_state: LightbinderState = Field(default_factory=LightbinderState)
    
    # Metadata
    messages: List[Any] = Field(default_factory=list)
    transmutation_log: List[Dict[str, Any]] = Field(default_factory=list)
