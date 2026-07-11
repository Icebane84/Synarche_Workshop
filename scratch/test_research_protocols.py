"""
Unit tests for the Research-Grade Law prototypes.
Governed by: TDD Principles, MASTER_CODER_V1.0
"""

import pytest
from unittest.mock import MagicMock

# Assume the prototypes and mocks are in these files in the scratch directory
# In a real project, they would be in a structured `src` directory.
from c.Users.Chris.Synarche_Workspace.scratch.mocks import (
    KnowledgeGraph,
    GenerativeModel,
    InteractionHistoryService,
    HighSpeedCache,
    SystemState,
    Action,
)
from c.Users.Chris.Synarche_Workspace.scratch.UMB_COG_ECP_001_EmpathicCatalystProtocol import (
    EmpathicCatalystProtocol,
    EmpathyProfile,
)
from c.Users.Chris.Synarche_Workspace.scratch.UMB_COG_NSP_001_NovaSparkProtocol import (
    NovaSparkProtocol,
)
from c.Users.Chris.Synarche_Workspace.scratch.UMB_CACHE_PCP_001_PredictiveCoherenceProtocol import (
    PredictiveCoherenceProtocol,
)
from c.Users.Chris.Synarche_Workspace.scratch.UMB_COG_EEC_001_EthosOfEmergentChoice import (
    EthosOfEmergentChoiceProtocol,
)


# --- Fixtures for Dependency Injection ---

@pytest.fixture
def mock_knowledge_graph() -> KnowledgeGraph:
    return KnowledgeGraph()

@pytest.fixture
def mock_generative_model() -> GenerativeModel:
    return GenerativeModel()

@pytest.fixture
def mock_history_service() -> InteractionHistoryService:
    return InteractionHistoryService()

@pytest.fixture
def mock_cache() -> HighSpeedCache:
    return HighSpeedCache()


# --- Test Suite for Law 029: Empathic Catalyst Protocol ---

class TestEmpathicCatalystProtocol:
    @pytest.fixture
    def ecp(self) -> EmpathicCatalystProtocol:
        return EmpathicCatalystProtocol()

    def test_get_user_profile_creates_default(self, ecp: EmpathicCatalystProtocol):
        """Tests that a default profile is created for a new user."""
        profile = ecp.get_user_profile("new_user")
        assert profile.user_id == "new_user"
        assert profile.verbosity == 0.5
        assert profile.empathy == 0.5

    def test_positive_feedback_adjusts_profile(self, ecp: EmpathicCatalystProtocol):
        """Tests that positive feedback increases empathy and verbosity."""
        ecp.record_feedback("test_user", "interaction_1", "positive")
        profile = ecp.get_user_profile("test_user")
        assert profile.empathy == 0.55
        assert profile.verbosity == 0.55

    def test_negative_feedback_adjusts_profile(self, ecp: EmpathicCatalystProtocol):
        """Tests that negative feedback decreases empathy and verbosity."""
        ecp.record_feedback("test_user", "interaction_1", "negative")
        profile = ecp.get_user_profile("test_user")
        assert profile.empathy == 0.45
        assert profile.verbosity == 0.45

    def test_profile_weights_are_bounded(self, ecp: EmpathicCatalystProtocol):
        """Tests that weights do not go above 1.0 or below 0.0."""
        user_id = "bound_test_user"
        # Push empathy to the max
        for _ in range(20):
            ecp.record_feedback(user_id, "int", "positive")

        profile = ecp.get_user_profile(user_id)
        assert profile.empathy == 1.0

        # Push empathy to the min
        for _ in range(40):
            ecp.record_feedback(user_id, "int", "negative")

        profile = ecp.get_user_profile(user_id)
        assert profile.empathy == 0.0

    def test_profile_decays_over_time(self, ecp: EmpathicCatalystProtocol, mocker):
        """Tests that weights slowly revert to the default over time."""
        user_id = "decay_user"
        # Mock time to control the decay trigger
        mock_time = mocker.patch('time.time')

        # Set an initial high-empathy profile
        mock_time.return_value = 1000.0
        profile = EmpathyProfile(user_id=user_id, verbosity=0.9, empathy=0.9, last_updated=mock_time.return_value)
        ecp.USER_PROFILES[user_id] = profile

        # Simulate the passage of more than one day
        mock_time.return_value += ecp.DECAY_THRESHOLD_SECONDS + 1

        decayed_profile = ecp.get_user_profile(user_id)
        assert decayed_profile.empathy < 0.9
        assert decayed_profile.empathy > 0.5 # It should move toward 0.5, but not all at once

    def test_generate_styled_prompt_adapts_to_profile(self, ecp: EmpathicCatalystProtocol):
        """Tests that the prompt injector correctly reflects the profile state."""
        user_id = "prompt_user"
        base_prompt = "Explain quantum computing."

        # Low empathy and verbosity
        profile = EmpathyProfile(user_id=user_id, verbosity=0.2, empathy=0.1)
        ecp.USER_PROFILES[user_id] = profile
        styled_prompt = ecp.generate_styled_prompt(user_id, base_prompt)
        assert "direct and factual tone" in styled_prompt
        assert "be concise" in styled_prompt

        # High empathy and verbosity
        profile = EmpathyProfile(user_id=user_id, verbosity=0.9, empathy=0.8)
        ecp.USER_PROFILES[user_id] = profile
        styled_prompt_2 = ecp.generate_styled_prompt(user_id, base_prompt)
        assert "high degree of empathy" in styled_prompt_2
        assert "be verbose" in styled_prompt_2


# --- Test Suite for Law 036: Nova Spark Protocol ---

class TestNovaSparkProtocol:
    @pytest.fixture
    def nsp(self, mock_knowledge_graph, mock_generative_model) -> NovaSparkProtocol:
        return NovaSparkProtocol(mock_knowledge_graph, mock_generative_model)

    def test_execute_returns_tagged_strings(self, nsp: NovaSparkProtocol):
        """Tests that all outputs are correctly tagged as ungrounded."""
        sparks = nsp.execute("any concept")
        assert isinstance(sparks, list)
        assert len(sparks) > 0
        for spark in sparks:
            assert isinstance(spark, str)
            assert spark.startswith("[UNGROUNDED-SYNTHESIS source:NSP-v2.0]") # Ensure version is updated if logic changes

    def test_execute_logs_audit_trail(self, nsp: NovaSparkProtocol, mocker):
        """Tests that the orthogonal vector and its score are logged."""
        # Spy on the logger to ensure it's called correctly
        mock_logger = mocker.spy(nsp_protocol, 'nsp_logger')

        nsp.execute("any concept")

        mock_logger.info.assert_called_once()
        log_message = mock_logger.info.call_args[0][0]
        assert "CORE:" in log_message
        assert "INJECT:" in log_message
        assert "SIM_SCORE:" in log_message

    def test_select_orthogonal_vector_chooses_low_similarity_concept(self, nsp: NovaSparkProtocol, mocker):
        """Tests that the vector with the lowest cosine similarity is chosen and returned."""
        core_concept = "Distributed Systems Consensus"
        # Mock the embeddings to have predictable similarities
        mocker.patch.object(nsp.knowledge_graph, 'get_embedding', side_effect=[
            [1, 0, 0],  # Core concept vector
            [0.9, 0.1, 0], # High similarity candidate
            [0, 1, 0],  # Orthogonal candidate (similarity = 0)
            [-1, 0, 0], # Anti-correlated candidate (similarity = -1)
        ])
        # Mock random.sample to return a deterministic list of candidates
        mock_candidates = ["High Sim", "Orthogonal", "Anti-Correlated"]
        mocker.patch('random.sample', return_value=mock_candidates)

        orthogonal_concept, similarity_score = nsp._select_orthogonal_vector(core_concept)

        # The most "orthogonal" concept is the one most dissimilar (lowest cosine similarity)
        assert orthogonal_concept == "Anti-Correlated"
        assert similarity_score == -1.0

    def test_invalid_divergence_factor_raises_error(self, nsp: NovaSparkProtocol):
        """Tests input validation for the divergence factor."""
        with pytest.raises(ValueError, match="Divergence factor must be between 0.1 and 1.0"):
            nsp.execute("any concept", divergence_factor=2.0)
        with pytest.raises(ValueError, match="Divergence factor must be between 0.1 and 1.0"):
            nsp.execute("any concept", divergence_factor=0.0)


# --- Test Suite for Law 037: Predictive Coherence Protocol ---

class TestPredictiveCoherenceProtocol:
    @pytest.fixture
    def pcp(self, mock_history_service, mock_cache) -> PredictiveCoherenceProtocol:
        # We manually inject mocks here since the prototype doesn't use a formal DI system
        protocol = PredictiveCoherenceProtocol()
        protocol.history_service = mock_history_service
        protocol.cache = mock_cache
        return protocol

    def test_execute_for_user_flow(self, pcp: PredictiveCoherenceProtocol, mocker):
        """Tests the main execution flow and dependency calls."""
        # Mock the internal methods to check if they are called
        mocker.patch.object(pcp, '_run_arima_forecast', return_value=1)
        mocker.patch.object(pcp, '_map_action_to_data', return_value="ARTIFACT:UMB-CSE-001")
        mocker.spy(pcp.history_service, 'get_user_history')
        mocker.spy(pcp.cache, 'set')

        user_id = "test_user_1"
        pcp.execute_for_user(user_id)

        # Verify that all dependencies were called correctly
        pcp.history_service.get_user_history.assert_called_once_with(user_id)
        pcp._run_arima_forecast.assert_called_once()
        pcp._map_action_to_data.assert_called_once_with(1)
        pcp.cache.set.assert_called_once_with(
            f"user:{user_id}:next_action_data",
            "ARTIFACT:UMB-CSE-001",
            ttl=60
        )


# --- Test Suite for Law 041: Ethos of Emergent Choice Protocol ---

class TestEthosOfEmergentChoiceProtocol:
    @pytest.fixture
    def actions(self) -> list[Action]:
        return [
            Action("Low Reward Action", {"coherence": 0.1, "synergy": 0.1}),
            Action("High Reward Action", {"coherence": 0.3, "synergy": 0.2}),
        ]

    @pytest.fixture
    def eec(self, actions) -> EthosOfEmergentChoiceProtocol:
        return EthosOfEmergentChoiceProtocol(possible_actions=actions)

    def test_select_optimal_action(self, eec: EthosOfEmergentChoiceProtocol, mocker):
        """Tests that the protocol selects the action with the highest projected value."""
        # Mock random.random to make state transitions deterministic for the test
        mocker.patch('random.random', return_value=0.5) # This makes the random noise zero

        initial_state = SystemState(coherence=0.5, synergy=0.5)
        optimal_action = eec.select_optimal_action(initial_state)

        assert optimal_action.name == "High Reward Action"
