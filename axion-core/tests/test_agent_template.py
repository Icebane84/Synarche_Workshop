import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

# Add src to path so we can import as 'agents.axion...'
sys.path.append(str(Path(__file__).parents[1] / "src"))

try:
    from agents.axion.config import AxionConfig
    from agents.axion.runtime import AxionRuntime
    from agents.axion.schemas import (
        AxionState,
        GamemasterState,
        LightbinderState,
        RPGEngine,
    )
except ImportError:
    # Fallback for different environments
    sys.path.append(str(Path(__file__).parents[1] / "src" / "agents"))
    from axion.config import AxionConfig
    from axion.runtime import AxionRuntime
    from axion.schemas import AxionState, GamemasterState, LightbinderState, RPGEngine

# --- FIXTURES ---


@pytest.fixture
def mock_config():
    return AxionConfig(
        WORKSPACE_ROOT=Path("/tmp/workspace"),
        SOPHIA_PATH=Path("/tmp/tools/sophia.py"),
        SENTINEL_PATH=Path("/tmp/tools/sentinel.py"),
        XP_THRESHOLD_MULTIPLIER=100,
    )


@pytest.fixture
def base_state():
    return AxionState(
        input="Test Input",
        rpg_stats=RPGEngine(
            level=1,
            xp=0,
            authority=10,
            insight=10,
            order=10,
            precision=10,
            coherence_index=10,
            synergy_flow=10,
            adaptability=10,
            achievements=[],
            active_quest_log=[],
            prestige_class="Neophyte",
        ),
        gamemaster_state=GamemasterState(),
        lightbinder_state=LightbinderState(),
    )


@pytest.fixture
def runtime():
    return AxionRuntime()


# --- TESTS: MODELS ---


def test_rpg_engine_validation():
    # Valid
    rpg = RPGEngine(
        level=1,
        xp=0,
        authority=50,
        insight=50,
        order=50,
        precision=50,
        coherence_index=50,
        synergy_flow=50,
        adaptability=50,
    )
    assert rpg.level == 1

    # Invalid (Level < 1)
    with pytest.raises(ValueError):
        RPGEngine(
            level=0,
            xp=0,
            authority=50,
            insight=50,
            order=50,
            precision=50,
            coherence_index=50,
            synergy_flow=50,
            adaptability=50,
        )


# --- TESTS: NODES ---


@pytest.mark.asyncio
async def test_node_retrieve_context(runtime, base_state):
    result = await runtime.node_retrieve_context(base_state)
    assert "narrative_context" in result
    assert "logic_context" in result
    assert "Cognitive Loom" in result["narrative_context"]


@pytest.mark.asyncio
async def test_node_lightbinder_weave(runtime, base_state):
    # Mocking filesystem exists checks inside TarotMask
    with patch("pathlib.Path.exists", return_value=True):
        result = await runtime.node_lightbinder_weave(base_state)

    lb_state = result["lightbinder_state"]
    assert len(lb_state.active_masks) > 0
    assert "I. The Magician" in lb_state.active_masks


@pytest.mark.asyncio
async def test_node_sophia_insight_mocked(runtime, base_state):
    # Mock subprocess for Sophia
    with patch("asyncio.create_subprocess_exec") as mock_exec:
        mock_proc = AsyncMock()
        mock_proc.communicate.return_value = (b"Harmony found.", b"")
        mock_proc.returncode = 0
        mock_exec.return_value = mock_proc

        # Ensure SOPHIA_PATH exists mock
        with patch("pathlib.Path.exists", return_value=True):
            result = await runtime.node_sophia_insight(base_state)

        assert "[SYSTEM] Sophia Scan: Harmony found." in result["sophia_insight"]


@pytest.mark.asyncio
async def test_node_sentinel_check_pass(runtime, base_state):
    result = await runtime.node_sentinel_check(base_state)
    assert result["sentinel_status"] == "PASS"
    assert "Law 24" in result["sentinel_reason"]


@pytest.mark.asyncio
async def test_node_rpg_update(runtime, base_state):
    result = await runtime.node_update_rpg_stats(base_state)
    new_stats = result["rpg_stats"]
    assert new_stats.xp == base_state.rpg_stats.xp + 50
    assert new_stats.coherence_index == base_state.rpg_stats.coherence_index + 1


# --- TESTS: SENTINEL GATE ---


@pytest.mark.asyncio
async def test_sentinel_gate_pass(runtime, base_state):
    state = base_state.model_copy(update={"sentinel_status": "PASS"})
    route = await runtime.sentinel_gate(state)
    assert route == "rpg_update"


@pytest.mark.asyncio
async def test_sentinel_gate_fail(runtime, base_state):
    state = base_state.model_copy(
        update={"sentinel_status": "FAIL", "sentinel_reason": "Violation"}
    )
    # Need to check against langgraph.graph.END, but it's a string constant usually
    route = await runtime.sentinel_gate(state)
    from langgraph.graph import END

    assert route == END
