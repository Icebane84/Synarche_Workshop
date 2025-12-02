"""
CORE-LOGIC-UTIL-SENTINEL-001 (sentinel_utils.py)
Status: [CANONIZED]
Genesis Stamp: 2026-03-07

 SENTINEL-UTIL-001: The Sentinel Gate (Secure Execution)
 v14.0 [OMEGA] - Centralizes all external command execution to ensure compliance with security protocols.
"""

import logging
import subprocess
from typing import Any

logger = logging.getLogger("sentinel")


def safe_run_command(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
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
            logger.error(f"   > FAILURE (Code {result.returncode}): {result.stderr.strip()}")
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
