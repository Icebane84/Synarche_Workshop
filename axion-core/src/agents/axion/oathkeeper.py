"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AGENT-AXION-PRIME-001
Official Name: oathkeeper.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Zero Entropy. Coherence through Confrontation."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

import asyncio
import logging
from typing import Any, cast

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

# Project Imports
from .enums import AuditStatus
from .nodes import (
    node_gamemaster_engine,
    node_generate_content,
    node_lightbinder_weave,
    node_retrieve_context,
    node_sentinel_check,
    node_sophia_insight,
    node_tarot_render,
    node_update_rpg_stats,
)
from .schemas import AxionState

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("axion")


class AxionOathkeeper:
    """
    The main orchestrator for the Axion Agent (v15.0 [OMEGA]).
    Implements the state machine via LangGraph and manages node transitions.
    """

    def __init__(self) -> None:
        """Initializes the Oathkeeper with a compiled StateGraph."""
        self.graph = self._build_workflow()

    def _build_workflow(self) -> CompiledStateGraph:
        """
        Constructs the LangGraph workflow.
        Defines nodes, edges, and the conditional sentinel gate.
        """
        workflow = StateGraph(AxionState)
        logger.info("   > [OATHKEEPER] Weaving the Seven-Agent Matrix...")
        
        # Add Nodes
        workflow.add_node("retrieve", node_retrieve_context)
        workflow.add_node("lightbinder", node_lightbinder_weave)
        workflow.add_node("sophia", node_sophia_insight)
        workflow.add_node("generate", node_generate_content)
        workflow.add_node("sentinel", node_sentinel_check)
        workflow.add_node("rpg_update", node_update_rpg_stats)
        workflow.add_node("gamemaster", node_gamemaster_engine)
        workflow.add_node("tarot_render", node_tarot_render)

        # Define Edges
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "lightbinder")
        workflow.add_edge("lightbinder", "sophia")
        workflow.add_edge("sophia", "generate")
        workflow.add_edge("generate", "sentinel")

        # Sentinel Gate (Conditional Edge)
        def sentinel_gate(state: dict[str, Any] | AxionState) -> str:
            """Determines if the flow should proceed based on Sentinel status."""
            if isinstance(state, dict):
                status = state.get("sentinel_status", AuditStatus.PASS)
            else:
                status = state.sentinel_status
            return "rpg_update" if status == AuditStatus.PASS else END

        workflow.add_conditional_edges(
            "sentinel", 
            sentinel_gate, 
            {"rpg_update": "rpg_update", END: END}
        )

        workflow.add_edge("rpg_update", "gamemaster")
        workflow.add_edge("gamemaster", "tarot_render")
        workflow.add_edge("tarot_render", END)

        return workflow.compile()

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Executes the agent workflow against the provided input.
        Returns the final state after processing.
        """
        # Initialize session ID if missing
        if "session_id" not in input_data:
            input_data["session_id"] = f"AXION-{int(asyncio.get_event_loop().time())}"
 
        result = await self.graph.ainvoke(input_data)
        return cast(dict[str, Any], result)


# Singleton instance for the High Priestess access
oathkeeper = AxionOathkeeper()
app = oathkeeper.graph
