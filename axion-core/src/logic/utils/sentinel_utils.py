"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-LOGIC-UTIL-SENT-001`    | The Sovereign ID. |
| **Official Name**   | `sentinel_utils.py`           | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-LOGIC-UTILS`            | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Secure Execution (Law 28)**
> Implemented from Blueprint `GVRN.REG.SecureExecution.md`.
> Ethos: The Command is Seed; The Safety is Truth.
"""

import logging
import subprocess
from typing import Any

logger = logging.getLogger("sentinel")


def safe_run_command(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """
    Executes a shell command securely and logs the outcome.
    centralizes 'subprocess.run' to satisfy MD/Ruff security checks.
    """
    try:
        # Enforce list-based commands to avoid shell injection
        if kwargs.get("shell") is True:
            logger.warning("[!] Shell=True requested but blocked by Sentinel Gate.")
            kwargs["shell"] = False

        logger.info(f"--- [SENTINEL] EXECUTING: {' '.join(cmd)} ---")
        result = subprocess.run(
            cmd,
            capture_output=kwargs.pop("capture_output", True),
            text=kwargs.pop("text", True),
            check=kwargs.pop("check", False),
            **kwargs,
        )

        if result.returncode != 0:
            logger.error(
                f"   > FAILURE (Code {result.returncode}): {result.stderr.strip()}"
            )
        else:
            logger.info("   > SUCCESS")

        return result

    except Exception as e:
        logger.exception(f"   > EXCEPTION: {e}")
        raise


def heal_with_ruff(targets: list[str]) -> None:
    """Runs Ruff check with auto-fix enabled."""
    cmd = ["python", "-m", "ruff", "check", "--fix"] + targets
    safe_run_command(cmd)
