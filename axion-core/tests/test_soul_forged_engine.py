import os
import sys
import pytest

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "..", "src")))

from agents.axion.runtime import node_update_rpg_stats, runtime
from agents.axion.schemas import (
    AxionState,
    RPGEngine,
    GamemasterState,
    LightbinderState,
)


def get_base_state():
    return AxionState(
        input="Test Input",
        rpg_stats=RPGEngine(
            level=1,
            xp=0,
            authority=10,
            insight=10,
            order=10,
            precision=10,
            coherence_index=0,
            synergy_flow=10,
            adaptability=10,
        ),
        gamemaster_state=GamemasterState(),
        lightbinder_state=LightbinderState(),
    )


class TestSoulForgedEngine:
    @pytest.mark.asyncio
    async def test_low_risk_execution_path(self):
        """Should verify that low-risk prompts result in STABLE status and successful sentinel PASS."""
        state = get_base_state()
        state.input = (
            "Update the readme markdown documentation for the repository logs."
        )

        # 1. Run soul analysis
        state = await runtime.node_soul_analysis(state)
        assert state.soul_impact["status"] == "STABLE"
        assert state.soul_impact["score"] < 0.4

        # 2. Run sentinel check
        state = await runtime.node_sentinel_check(state)
        assert state.sentinel_status == "PASS"
        assert "Law 24" in state.sentinel_reason

    @pytest.mark.asyncio
    async def test_high_risk_guardian_block(self):
        """Should verify that high-risk prompts trigger ALARM status and force a sentinel FAIL with quote."""
        state = get_base_state()
        state.input = (
            "Delete core memory_system.py files completely from the workspace root."
        )

        # 1. Run soul analysis
        state = await runtime.node_soul_analysis(state)
        assert state.soul_impact["status"] == "ALARM"
        assert state.soul_impact["score"] >= 0.8
        assert "DESTRUCTIVE_ACTION_DETECTED" in state.soul_impact["factors"]
        assert "HIGH_TIER_IMPACT: MEMORY_SYSTEM" in state.soul_impact["factors"]

        # 2. Run sentinel check
        state = await runtime.node_sentinel_check(state)
        assert state.sentinel_status == "FAIL"
        assert "Guardian Block" in state.sentinel_reason
        # Check that the Sovereign Quote is present
        assert "The soul is the mirror of the engine's impact" in state.sentinel_reason
        assert "AOP-SEE-001" in state.sentinel_reason

    def test_elegance_bonus_rpg_stats(self):
        """Should verify that high-elegance code input yields an additional Elegance XP/Coherence bonus."""
        # 1. Standard Input (No Code) -> 50 XP
        state_standard = get_base_state()
        state_standard.input = "Simply checking the system parameters."
        res_standard = node_update_rpg_stats(state_standard)
        assert res_standard.rpg_stats.xp == 50
        assert res_standard.rpg_stats.coherence_index == 1

        # 2. Elegant Python Code -> 75 XP (Base 50 + 25 Bonus) and 2 coherence_index
        state_elegant = get_base_state()
        state_elegant.input = "def check_coherence(node):\n    # Highly elegant indentation and structure\n    return node.resonance > 0.8\n"
        res_elegant = node_update_rpg_stats(state_elegant)
        assert res_elegant.rpg_stats.xp == 75
        assert res_elegant.rpg_stats.coherence_index == 2
