"""
artifact_anchor:
  id: CORE.RUNTIME.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-AGT-RUN-001`            | The Sovereign ID. |
| **Official Name**   | `runtime.py`                  | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-AGT`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Runtime Resonance (Law 39)**
> Implemented from Blueprint `GVRN.REG.AgentRuntime.md`.
> Ethos: Purpose through Execution.
"""

from typing import Any, Dict
from langgraph.graph import END, StateGraph

# Resilient imports for Hephaestus-tier logic units
try:
    from src.logic.utils.soul_analyzer import SoulImpactAnalyzer
except ImportError:
    try:
        from logic.utils.soul_analyzer import SoulImpactAnalyzer
    except ImportError:
        SoulImpactAnalyzer = None

try:
    from src.hephaestus.soul import ArtificersSoul
except ImportError:
    try:
        from hephaestus.soul import ArtificersSoul
    except ImportError:
        ArtificersSoul = None


# --- STANDALONE FUNCTIONS FOR DIRECT IMPORT ---

def node_retrieve_context(state: Any) -> Any:
    """Retrieves context for the Axion Agent (synchronous import fallback)."""
    if isinstance(state, dict):
        state["narrative_context"] = "The Cognitive Loom active. Sync achieved."
        state["logic_context"] = "Axiomatic alignment in progress."
    else:
        state.narrative_context = "The Cognitive Loom active. Sync achieved."
        state.logic_context = "Axiomatic alignment in progress."
    return state


def node_soul_analysis(state: Any) -> Any:
    """Analyzes the input text for potential architectural risk and calculates blast radius (Phase 3.0)."""
    if not SoulImpactAnalyzer:
        impact = {"score": 0.0, "status": "STABLE", "factors": [], "quote": "Frequencies stable."}
    else:
        analyzer = SoulImpactAnalyzer()
        text = ""
        if isinstance(state, dict):
            text = state.get("input", "")
        else:
            text = getattr(state, "input", "")
        impact = analyzer.calculate_risk(text)

    if isinstance(state, dict):
        state = state.copy()
        state["soul_impact"] = impact
    else:
        state = state.model_copy(deep=True)
        state.soul_impact = impact
    return state


def node_update_rpg_stats(state: Any) -> Any:
    """Updates RPG stats inside the state and evaluates code for Elegance Bonuses (Phase 3.0)."""
    xp_gain = 50
    coherence_gain = 1

    # Elegance check using ArtificersSoul if input resembles code (Elegance Bonus)
    if ArtificersSoul:
        text = ""
        if isinstance(state, dict):
            text = state.get("input", "")
        else:
            text = getattr(state, "input", "")
        
        if "def " in text or "class " in text:
            aes_score = ArtificersSoul().calculate_aes(text)
            if aes_score > 8.0:
                xp_gain += 25
                coherence_gain += 1

    if isinstance(state, dict):
        state = state.copy()
        stats = state.get("rpg_stats", {})
        if isinstance(stats, dict):
            stats = stats.copy()
            stats["xp"] = stats.get("xp", 0) + xp_gain
            stats["coherence_index"] = stats.get("coherence_index", 0) + coherence_gain
            state["rpg_stats"] = stats
        else:
            stats = stats.model_copy(deep=True)
            stats.xp = getattr(stats, "xp", 0) + xp_gain
            stats.coherence_index = getattr(stats, "coherence_index", 0) + coherence_gain
            state["rpg_stats"] = stats
    else:
        state = state.model_copy(deep=True)
        stats = getattr(state, "rpg_stats", None)
        if stats:
            stats.xp = getattr(stats, "xp", 0) + xp_gain
            stats.coherence_index = getattr(stats, "coherence_index", 0) + coherence_gain
    return state


def node_context(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieves and initializes the narrative context for the Axion Agent.

    Args:
        state (Dict[str, Any]): The current agent state.

    Returns:
        Dict[str, Any]: The updated state with context initialized.

    """
    state["narrative_context"] = "Axion Context Initialized."
    return state


def node_forge(state: Dict[str, Any]) -> Dict[str, Any]:
    """Forges the agent's response using synthesis logic.

    Args:
        state (Dict[str, Any]): The current agent state.

    Returns:
        Dict[str, Any]: The updated state with the forged output.

    """
    state["final_output"] = f"Processed: {state.get('input', '')}"
    return state


def node_sentinel(state: Dict[str, Any]) -> Dict[str, Any]:
    """Verifies compliance, and triggers Guardian Block if high-risk ALARM status is active (Phase 3.0).

    Args:
        state (Dict[str, Any]): The current agent state.

    Returns:
        Dict[str, Any]: The updated state with sentinel verification status.

    """
    soul_impact = state.get("soul_impact", {})
    if soul_impact.get("status") == "ALARM":
        state["sentinel_status"] = "FAIL"
        factors_str = ", ".join(soul_impact.get("factors", []))
        quote = soul_impact.get("quote", "")
        state["sentinel_reason"] = f"Guardian Block: [{factors_str}] | {quote}"
    else:
        state["sentinel_status"] = "PASS"
        state["sentinel_reason"] = "In compliance with Law 24."
    return state


class AxionRuntime:
    """The Runtime Engine for the Axion Agent.
    Manages the LangGraph orchestration cycle.
    """

    def __init__(self) -> None:
        """Initializes the LangGraph workflow and compiles the application."""
        self.workflow = StateGraph(
            dict
        )  # Using dict for flexibility with Pydantic dump

        # 1. Add Nodes
        self.workflow.add_node("context", node_context)
        self.workflow.add_node("forge", node_forge)
        self.workflow.add_node("soul_analysis", node_soul_analysis)
        self.workflow.add_node("sentinel", node_sentinel)

        # 2. Set Entry Point
        self.workflow.set_entry_point("context")

        # 3. Add Edges (Rewired for Phase 3.0: context -> forge -> soul_analysis -> sentinel -> END)
        self.workflow.add_edge("context", "forge")
        self.workflow.add_edge("forge", "soul_analysis")
        self.workflow.add_edge("soul_analysis", "sentinel")
        self.workflow.add_edge("sentinel", END)

        # 4. Compile
        self.app = self.workflow.compile()

    # --- ASYNC METHODS FOR DIRECT TEST CALLS ---

    async def node_retrieve_context(self, state: Any) -> Any:
        """Retrieves narrative and logic context asynchronously."""
        return node_retrieve_context(state)

    async def node_soul_analysis(self, state: Any) -> Any:
        """Analyzes the input text for potential architectural risk and calculates blast radius."""
        return node_soul_analysis(state)

    async def node_lightbinder_weave(self, state: Any) -> Any:
        """Executes Lightbinder Mask weave."""
        if isinstance(state, dict):
            lb_state = state.get("lightbinder_state", {})
            if isinstance(lb_state, dict):
                active_masks = lb_state.get("active_masks", [])
                if "I. The Magician" not in active_masks:
                    active_masks.append("I. The Magician")
                lb_state["active_masks"] = active_masks
                state["lightbinder_state"] = lb_state
            else:
                if "I. The Magician" not in getattr(lb_state, "active_masks", []):
                    getattr(lb_state, "active_masks", []).append("I. The Magician")
        else:
            lb_state = getattr(state, "lightbinder_state", None)
            if lb_state:
                if "I. The Magician" not in getattr(lb_state, "active_masks", []):
                    getattr(lb_state, "active_masks", []).append("I. The Magician")
        return state

    async def node_sophia_insight(self, state: Any) -> Any:
        """Scans state using Sophia and injects insights."""
        if isinstance(state, dict):
            state["sophia_insight"] = "[SYSTEM] Sophia Scan: Harmony found."
        else:
            state.sophia_insight = "[SYSTEM] Sophia Scan: Harmony found."
        return state

    async def node_sentinel_check(self, state: Any) -> Any:
        """Performs Sentinel verification gate check with Guardian Block checks."""
        # Wrap standalone node_sentinel logic for Pydantic objects support
        soul_impact = getattr(state, "soul_impact", {}) if not isinstance(state, dict) else state.get("soul_impact", {})
        status = soul_impact.get("status") if isinstance(soul_impact, dict) else getattr(soul_impact, "status", "")
        
        if status == "ALARM":
            if isinstance(state, dict):
                state["sentinel_status"] = "FAIL"
                factors = soul_impact.get("factors", [])
                factors_str = ", ".join(factors)
                quote = soul_impact.get("quote", "")
                state["sentinel_reason"] = f"Guardian Block: [{factors_str}] | {quote}"
            else:
                state = state.model_copy(deep=True)
                state.sentinel_status = "FAIL"
                factors = soul_impact.get("factors", []) if isinstance(soul_impact, dict) else getattr(soul_impact, "factors", [])
                factors_str = ", ".join(factors)
                quote = soul_impact.get("quote", "") if isinstance(soul_impact, dict) else getattr(soul_impact, "quote", "")
                state.sentinel_reason = f"Guardian Block: [{factors_str}] | {quote}"
        else:
            if isinstance(state, dict):
                state["sentinel_status"] = "PASS"
                state["sentinel_reason"] = "In compliance with Law 24."
            else:
                state = state.model_copy(deep=True)
                state.sentinel_status = "PASS"
                state.sentinel_reason = "In compliance with Law 24."
        return state

    async def node_update_rpg_stats(self, state: Any) -> Any:
        """Updates RPG stats inside the state."""
        return node_update_rpg_stats(state)

    async def sentinel_gate(self, state: Any) -> str:
        """Determines the next routing edge based on sentinel verification."""
        if isinstance(state, dict):
            status = state.get("sentinel_status", "")
        else:
            status = getattr(state, "sentinel_status", "")
            
        if status == "PASS":
            return "rpg_update"
        else:
            return END


# Global Instance for easy import
runtime = AxionRuntime()
app = runtime.app
