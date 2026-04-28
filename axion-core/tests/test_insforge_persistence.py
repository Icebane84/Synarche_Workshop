import os
import sys
from unittest.mock import MagicMock

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.engine.deterministic import DeterministicEngine
from src.system.logging.phoenix_logger import logger


def test_insforge_sync():
    """
    Verifies that the engine can initialize the transmuter
    and call synchronization methods correctly.
    """
    logger.info("--- [START] INSFORGE PERSISTENCE VALIDATION ---")

    # Use a dummy key to initialize
    dummy_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    engine = DeterministicEngine(insforge_key=dummy_key)

    # Inject some simulation data
    e1 = engine.entity_manager.create_entity()
    engine.component_store.add_component(e1, "PositionData")

    # Mock the transmuter's network-heavy methods to avoid real HTTP during tests
    engine.transmuter.transmute_entities = MagicMock()
    engine.transmuter.transmute_components = MagicMock()
    engine.transmuter.save_snapshot = MagicMock()

    logger.info("Triggering Cloud Sync (Simulated)...")
    engine.sync_to_cloud()

    # Verify the transmuter was engaged
    assert engine.transmuter.transmute_entities.called, "transmute_entities was not called"
    assert engine.transmuter.transmute_components.called, "transmute_components was not called"
    assert engine.transmuter.save_snapshot.called, "save_snapshot was not called"

    logger.info(f"Engine State at Frame {engine.clock.frame} synced successfully.")
    logger.info("--- [SUCCESS] Insforge Persistence Logic Validated. ---")


if __name__ == "__main__":
    try:
        test_insforge_sync()
    except Exception as e:
        logger.error(f"Insforge Persistence Validation Failed: {e}")
        sys.exit(1)
