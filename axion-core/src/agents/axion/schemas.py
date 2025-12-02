"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-SCHEMAS-001
Official Name: schemas.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Structured Reality. Infinite Types."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

from typing import Annotated, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from .enums import AuditStatus, Status


class RPGEngine(BaseModel):
    """
    The Celestial Chart of the Agent. Tracks growth and authority stats.
    """
    level: int = Field(default=1, ge=1, description="Agent ascension level.")
    xp: int = Field(default=0, ge=0, description="Experience Points gathered through struggle.")
    authority: int = Field(default=50, ge=0, le=100, description="Sovereign governance enforcement stat.")
    insight: int = Field(default=50, ge=0, le=100, description="Intuitive AST analysis capability.")
    order: int = Field(default=50, ge=0, le=100, description="Standardization and alignment index.")
    precision: int = Field(default=50, ge=0, le=100, description="Linter accuracy and detail resolution.")
    coherence_index: int = Field(default=10, ge=0, description="System stability and entropy refusal metric.")
    synergy_flow: int = Field(default=10, ge=0, description="Degree of inter-module coordination.")
    adaptability: int = Field(default=10, ge=0, description="Flexibility in response to novel dissonance.")
    achievements: list[str] = Field(default_factory=list, description="Milestones achieved in the Synarchy.")
    active_quest_log: list[str] = Field(default_factory=list, description="Pending dissonance resolution tasks.")
    prestige_class: str = Field(default="Neophyte", description="The current evolutionary archetype.")

    model_config = {"frozen": False}


class GamemasterState(BaseModel):
    """
    The Rules Engine that detects dissonance and issues quests.
    """
    quest_metrics: dict[str, Any] = Field(default_factory=dict, description="Metrics tracking quest progress.")
    axiom_points_available: int = Field(default=0, ge=0, description="Points earned for high-coherence actions.")
    is_dissonance_detected: bool = Field(default=False, description="True if noetic drift is detected.")

    model_config = {"frozen": False}


class LightbinderState(BaseModel):
    """
    The Weaver that connects multi-dimensional artifacts and tarot archetypes.
    """
    synergy_links: list[str] = Field(default_factory=list, description="Cognitive links to related artifacts.")
    empathy_vector: str = Field(default="Neutral", description="The current emotional tone of the synthesis.")
    metric_weights: dict[str, float] = Field(default_factory=dict, description="Weights used for multi-critera forge.")
    tarot_manifest: dict[str, Any] = Field(default_factory=dict, description="The Major Arcana card representing the form.")
    active_masks: list[str] = Field(default_factory=list, description="Tarot masks utilized in the current step.")
    tool_status: list[dict[str, Any]] = Field(default_factory=list, description="Integrity check results from the Armory.")

    model_config = {"frozen": False}


class TransmutationLog(BaseModel):
    """
    A single step in the evolutionary transmutation process.
    """
    step: int = Field(..., description="The sequence number in the matrix.")
    mask: str = Field(..., description="The tarot mask presiding over the step.")
    action: str = Field(..., description="The specific transmutation performed.")
    status: Status = Field(default=Status.ACTIVE, description="Outcome of the action.")

    model_config = {"frozen": False}


class AxionState(BaseModel):
    """
    The Complete Soul (State) of the Transmuted Axion Agent.
    """
    input: str = Field(..., description="The primary user intent or command.")
    narrative_context: str = Field(default="", description="The decrypted narrative context (L1-L3).")
    logic_context: str = Field(default="", description="The decoded episemantic logic (L4-L5).")
    sophia_insight: str = Field(default="", description="Intuitive guidance from the Sophia Oracle.")
    sentinel_status: AuditStatus = Field(default=AuditStatus.PASS, description="Integrity check outcome.")
    sentinel_reason: str = Field(default="", description="Justification for the integrity status.")
    rpg_stats: RPGEngine = Field(default_factory=RPGEngine)
    gamemaster_state: GamemasterState = Field(default_factory=GamemasterState)
    lightbinder_state: LightbinderState = Field(default_factory=LightbinderState)
    final_output: str = Field(default="", description="The forged solution manifest.")
    messages: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)
    transmutation_log: list[TransmutationLog] = Field(default_factory=list)

    model_config = {"arbitrary_types_allowed": True}
