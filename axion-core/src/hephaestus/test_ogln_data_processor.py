"""
artifact_anchor:
  id: TEST.TEST_OGLN_DATA_PROCESSOR.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: TEST
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

import json
import pytest

# Assuming your Python path is configured to find hephaestus
from hephaestus.ogln_data_processor import MemoryWeaverAgent


@pytest.fixture
def weaver_agent():
    """Fixture to provide a clean MemoryWeaverAgent instance."""
    return MemoryWeaverAgent(target_vault="Pytest Mock Vault")


@pytest.mark.asyncio
async def test_weave_log_entry_plain_text_critical(weaver_agent):
    """Validates that plain text critical errors are parsed correctly."""
    log_entry = "2026-04-16 10:00:00,123 - CoreEngine - ERROR - CRITICAL FAILURE in data_pipeline: OOM Error\nTraceback (most recent call last):\n  File 'main.py', line 1"

    result = await weaver_agent.weave_log_entry(log_entry)

    assert result is not None
    assert result["summary"] == "OGLN Detected Critical Failure: data_pipeline"
    assert "Traceback" in result["stack_trace"]
    assert result["status"] == "Awaiting Root Cause Analysis"
    assert result["weaver_id"] == weaver_agent.weaver_id


@pytest.mark.asyncio
async def test_weave_log_entry_json_critical(weaver_agent):
    """Validates that JSON-formatted logs are parsed efficiently via structured extraction."""
    log_data = {
        "asctime": "2026-05-17T11:00:00.000",
        "name": "AuthService",
        "levelname": "CRITICAL",
        "message": "CRITICAL FAILURE in auth_router: JWT Signature expired",
        "exc_info": "Traceback (most recent call last):\n  File 'auth.py', line 42",
    }
    log_entry = json.dumps(log_data)

    result = await weaver_agent.weave_log_entry(log_entry)

    assert result is not None
    assert result["summary"] == "OGLN Detected Critical Failure: auth_router"
    assert "Traceback" in result["stack_trace"]
    assert result["status"] == "Awaiting Root Cause Analysis"


@pytest.mark.asyncio
async def test_weave_log_entry_database_error(weaver_agent):
    """Validates specific routing for database connectivity errors."""
    log_entry = "2026-04-16 10:05:00,000 - DBService - ERROR - Database connection failed: timeout"
    result = await weaver_agent.weave_log_entry(log_entry)

    assert result is not None
    assert result["type"] == "DB_ERROR"
    assert "Database connection failed: timeout" in result["line"]


@pytest.mark.asyncio
async def test_weave_log_entry_info_ignored(weaver_agent):
    """Validates that non-critical logs are ignored and return None."""
    log_entry = "2026-04-16 10:01:00,456 - SystemInit - INFO - System initialized."
    result = await weaver_agent.weave_log_entry(log_entry)
    assert result is None
