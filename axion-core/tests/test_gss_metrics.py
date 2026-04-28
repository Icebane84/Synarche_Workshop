import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.deterministic import DeterministicEngine
from src.system.logging.phoenix_logger import logger

def test_gss_calculation():
    """
    Validates that the SynergySystem correctly identifies state complexity 
    and calculates a non-zero Coherence Index (CI).
    """
    logger.info("--- [START] GSS SYNERGY VALIDATION ---")
    
    engine = DeterministicEngine()
    engine.initialize()

    # Phase 1: Zero State
    engine.step()
    logger.info(f"Initial CI (Zero State): {engine.synergy_metrics.coherence_index:.4f}")
    assert engine.synergy_metrics.coherence_index == 0.0, "Initial CI should be 0.0"

    # Phase 2: Building Coherence
    logger.info("Injecting Entities and Components...")
    e1 = engine.entity_manager.create_entity()
    engine.component_store.add_component(e1, "PositionData")
    engine.component_store.add_component(e1, "VelocityData")
    
    engine.step()
    ci_level_1 = engine.synergy_metrics.coherence_index
    logger.info(f"CI Level 1 (Single Entity, 2 Components): {ci_level_1:.4f}")
    assert ci_level_1 > 0.0, "CI should be greater than 0 after data injection"

    # Phase 3: Increasing Diversity (Resonance)
    e2 = engine.entity_manager.create_entity()
    engine.component_store.add_component(e2, 100) # Numeric component type
    
    engine.step()
    ci_level_2 = engine.synergy_metrics.coherence_index
    logger.info(f"CI Level 2 (Diverse Types): {ci_level_2:.4f}")
    
    # Diversity should increase CI based on our CR (Coupling Resonance) formula
    assert ci_level_2 > ci_level_1, f"Diversity CI ({ci_level_2}) should be > Baseline CI ({ci_level_1})"

    logger.info(f"Final Synergy Metrics: {engine.synergy_metrics}")
    logger.info("--- [SUCCESS] GSS Metrics validated. ---")

if __name__ == "__main__":
    try:
        test_gss_calculation()
    except Exception as e:
        logger.error(f"GSS Validation Failed: {e}")
        sys.exit(1)
