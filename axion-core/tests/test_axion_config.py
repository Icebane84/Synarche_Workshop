"""
Unified Test: Axion Config Ascension (v15.0)
Verifies that AxionConfig correctly ingests Sovereign YAML settings.
"""

import logging
import sys
from pathlib import Path

# Add project src to sys.path
root = Path(__file__).resolve().parents[1]
sys.path.append(str(root / "src"))

# pylint: disable=wrong-import-position
from agents.axion.config import settings  # noqa: E402

# Configuration for logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def test_config_ingestion() -> None:
    """Verifies that the configuration ingestion is functioning correctly."""
    logger.info("--- [VERIFY] AXION CONFIG INGESTION ---")
    
    # Check basic paths
    logger.info("Workspace Root: %s", settings.WORKSPACE_ROOT)
    assert settings.WORKSPACE_ROOT.exists()
    
    # Check Sovereign Configs (Security, Network, Knowledge)
    logger.info("Security Config: %s", settings.SECURITY)
    logger.info("Network Config: %s", settings.NETWORK)
    logger.info("Knowledge Config: %s", settings.KNOWLEDGE)
    
    # Verify Block A identification presence (should be in the YAML keys if parsed correctly, 
    # but more importantly, the values should not be empty if files exist)
    if (settings.WORKSPACE_ROOT / ".agent" / "security.yaml").exists():
        assert settings.SECURITY is not None
        logger.info("Success: Security config ingested.")
    
    # Check Constants
    assert settings.XP_THRESHOLD_MULTIPLIER == 1000
    assert settings.LEVEL_CHRONOS == 100
    logger.info("Success: OMEGA v15.0 constants verified.")

if __name__ == "__main__":
    try:
        test_config_ingestion()
        logger.info("\n[TRANSCENDENCE] AXION CONFIG VERIFIED.")
    except Exception as e:
        logger.error("\n[DISSONANCE] VERIFICATION FAILED: %s", e)
        sys.exit(1)
