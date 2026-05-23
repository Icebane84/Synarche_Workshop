"""Test for Fused Cognitive Runtime (Axion OMEGA).
Verifies that AxionCognition, AdaptiveRetriever, and ExplanationGenerator
work together and influence RPG stats.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent
sys.path.append(str(root))

from agents.axion.runtime import (
    node_retrieve_context,
    node_update_rpg_stats,
)
from logic.memory.adaptive_retriever import AdaptiveRetriever
from logic.nlp.nlp_engine import AxionCognition
from logic.utils.explanation_generator import ExplanationGenerator


def test_cognitive_fusion():
    print(">>> TESTING COGNITIVE FUSION...")

    # 1. Initialize Components
    cognition = AxionCognition()
    AdaptiveRetriever(cognition_engine=cognition)
    ExplanationGenerator()

    # 2. Setup Initial State
    initial_state = {
        "input": "How does the Phoenix Protocol align with OMEGA?",
        "narrative_context": "",
        "logic_context": "",
        "sophia_insight": "",
        "sentinel_status": "",
        "sentinel_reason": "",
        "final_output": "",
        "messages": [],
        "rpg_stats": {
            "level": 1,
            "xp": 0,
            "authority": 10,
            "insight": 10,
            "order": 10,
            "precision": 10,
            "coherence_index": 0,
            "synergy_flow": 0,
            "adaptability": 0,
            "transparency": 0,
            "achievements": [],
            "active_quest_log": [],
            "prestige_class": "Novice",
        },
        "gamemaster_state": {
            "quest_metrics": {},
            "axiom_points_available": 0,
            "stardust_balance": 0,
            "is_dissonance_detected": False,
            "dissonance_vector": 0.0,
            "v_current": {"x": 100, "y": 100, "z": 100},
            "v_safe": {"x": 100, "y": 100, "z": 100},
        },
        "lightbinder_state": {
            "synergy_links": ["LINK: TEST"],
            "empathy_vector": "Neutral",
            "metric_weights": {},
            "tarot_manifest": {},
            "active_masks": [],
        },
        "transmutation_log": [],
    }

    # 3. Step 1: node_retrieve_context
    print("\n--- [STEP 1] node_retrieve_context ---")
    state = node_retrieve_context(initial_state)

    print(f"Narrative Context Snippet: {state['narrative_context'][:100]}...")

    # 4. Step 2: node_update_rpg_stats
    print("\n--- [STEP 2] node_update_rpg_stats ---")
    pre_xp = state["rpg_stats"]["xp"]
    pre_coherence = state["rpg_stats"]["coherence_index"]

    state = node_update_rpg_stats(state)

    print(f"XP Gained: {state['rpg_stats']['xp'] - pre_xp}")
    print(
        f"Coherence Index Delta: {state['rpg_stats']['coherence_index'] - pre_coherence}"
    )

    print("\n>>> COGNITIVE FUSION TEST PASSED!")


if __name__ == "__main__":
    test_cognitive_fusion()
