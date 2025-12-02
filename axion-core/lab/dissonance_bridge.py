"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-DISSONANCE-BRIDGE-001`                | The Sovereign ID. |
| **Official Name** | `dissonance_bridge.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import json
import logging
import os
import sys
import traceback

# Add current directory to path so we can import internal modules safely
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import the ascended Sentinel class
from src.hephaestus.sentinel import CodeSentinel as Auditor


def run_dissonance_bridge(target_dir: str):
    """Run the compliance audit and serialize the result natively to JSON for the React HUD."""
    # Optional: We could load real Stardust/Prestige values here from the OSML layer or a DB.
    # For now, we will return some hardcoded Genesis state to prove the bridge works,
    # alongside the LIVE dynamic audit results.

    response = {
        "status": "success",
        "genesis_state": {
            "prestige_level": 1,
            "stardust_available": 350,
            "system_coherence": 0.0,  # Will calculate based on audit
            "active_impacts": 0,
        },
        "entities": [],
    }

    try:
        auditor = Auditor(target_dir)
        auditor.run()

        entities = []
        error_id_counter = 1

        # Calculate coherence based on pass/fail ratio
        total_files = len(auditor.report)
        passed_files = len([r for r in auditor.report if r["status"] == "PASS"])

        if total_files > 0:
            response["genesis_state"]["system_coherence"] = round((passed_files / total_files) * 100)
        else:
            response["genesis_state"]["system_coherence"] = 100

        # Map auditor warnings and errors to DissonanceEntity objects
        for result in auditor.report:
            if result["status"] != "PASS":
                # Convert errors
                for err in result["errors"]:
                    entities.append(
                        {
                            "id": f"err-{error_id_counter:03d}",
                            "file": result["file"],
                            "message": err,
                            "severity": "error",
                            "line": 1,  # The auditor doesn't currently provide lines, default to 1
                            "health": 100,  # Represents "Corruption Health"
                        }
                    )
                    error_id_counter += 1

                # Convert warnings
                for warn in result["warnings"]:
                    entities.append(
                        {
                            "id": f"warn-{error_id_counter:03d}",
                            "file": result["file"],
                            "message": warn,
                            "severity": "warning",
                            "line": 1,
                            "health": 50,
                        }
                    )
                    error_id_counter += 1

        response["entities"] = entities
        response["genesis_state"]["active_impacts"] = len(entities)

        # Output strictly as JSON so Express/React can parse it easily
        print(json.dumps(response))

    except Exception as e:
        # Catch unexpected structural errors and return as a bridge error
        error_response = {"status": "error", "message": str(e), "trace": traceback.format_exc()}
        print(json.dumps(error_response))
        sys.exit(1)


if __name__ == "__main__":
    # Ensure no other logging pollutes stdout
    logging.getLogger().setLevel(logging.CRITICAL)

    # Target the primary governance directory
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    target = os.path.join(workspace_root, "_governance")

    run_dissonance_bridge(target)
