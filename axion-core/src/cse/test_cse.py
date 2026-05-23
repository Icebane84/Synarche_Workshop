import sys
import json
import io
import pytest
from cse import main

def test_cse_successful_synthesis(monkeypatch, capsys):
    """
    [Industry Standard: BDD (Behavior Driven Development)]
    Given a valid CollapsedBlock JSON on stdin
    When the CSE main function executes
    Then it should output a valid synthesized JSON to stdout
    """
    # 1. Arrange: Setup the mock input data
    mock_payload = {
        "blockId": "test-uuid-001",
        "data": {"element": "button", "actionType": "CLICK"}
    }
    
    # Mock sys.stdin to return our JSON string automatically
    monkeypatch.setattr('sys.stdin', io.StringIO(json.dumps(mock_payload)))

    # 2. Act: Execute the target function
    main()

    # 3. Assert: Capture standard output and verify it
    captured = capsys.readouterr()
    
    # Ensure no fatal errors were dumped to stderr
    assert not captured.err, "Expected clean execution, but got stderr output"
    
    # Parse the stdout back into a Python dictionary
    result = json.loads(captured.out)
    
    # Validate the structural integrity of the response
    assert result["status"] == "SYNTHESIZED"
    assert result["processedData"]["actionType"] == "CLICK"
    assert "Successfully processed by Python" in result["message"]