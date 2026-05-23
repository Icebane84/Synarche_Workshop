"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.sentinel.utils`                | The Sovereign ID. |
| **Official Name** | `sentinel_utils.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Logic Drift**      | Strict Linter Enforcement |
# | **Semantic Decay**   | Axiomatic Compass Audit   |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**
"""

import logging
import subprocess
from typing import Any

# Configure logging for this module
logger = logging.getLogger("sentinel")


def safe_run_command(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
    """Executes a shell command securely and logs the outcome.
    Centralizes 'subprocess.run' to satisfy security checks and logging requirements.

    Args:
        cmd: The command list to execute.
        **kwargs: Additional arguments for subprocess.run.

    Returns:
        The result of the command execution.

    """
    try:
        # Enforce list-based commands to avoid shell injection
        if kwargs.get("shell") is True:
            logger.warning("[!] Shell=True requested but blocked by Sentinel Gate.")
            kwargs["shell"] = False

        logger.info(f"--- [SENTINEL] EXECUTING: {' '.join(cmd)} ---")

        # Extract common flags with defaults
        capture_output = kwargs.pop("capture_output", True)
        text = kwargs.pop("text", True)
        check = kwargs.pop("check", False)

        result = subprocess.run(
            cmd, capture_output=capture_output, text=text, check=check, **kwargs
        )

        if result.returncode != 0:
            stderr_output = (
                result.stderr.strip() if result.stderr else "No stderr output."
            )
            logger.error(f"   > FAILURE (Code {result.returncode}): {stderr_output}")
        else:
            logger.info("   > SUCCESS")

        return result

    except Exception as e:
        logger.exception(f"   > EXCEPTION during safe_run_command: {e}")
        raise


def heal_with_ruff(targets: list[str]) -> None:
    """Runs Ruff check with auto-fix enabled for the specified targets.

    Args:
        targets: List of file paths or directories to fix.

    """
    cmd = ["python", "-m", "ruff", "check", "--fix"] + targets
    safe_run_command(cmd)


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.sentinel.utils VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 0a90931b57f2f549
# ---
