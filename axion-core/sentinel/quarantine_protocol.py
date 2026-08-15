# ARTIFACT_ID: SENTINEL.QuarantineProtocol
# VERSION: v1.0
# STATUS: [ACTIVE]

import logging
from typing import Callable, Optional

from .models import EpistemicVerdict

logger = logging.getLogger(__name__)


class QuarantineProtocol:
    """SP-QUARANTINE-005: Prevents integration of CRITICAL-delta artifacts."""

    def __init__(self, on_quarantine: Optional[Callable[[str, EpistemicVerdict], None]] = None) -> None:
        self._on_quarantine = on_quarantine

    def enforce_quarantine(self, artifact_id: str, verdict: EpistemicVerdict) -> bool:
        """Checks if an artifact should be quarantined."""
        logger.info("QuarantineProtocol: enforcing for '%s' (delta=%s)", artifact_id, verdict.delta)
        if verdict.delta == "CRITICAL":
            logger.error("ALERT: Artifact '%s' is being QUARANTINED. Reason: %s", artifact_id, verdict.reason)
            if self._on_quarantine:
                self._on_quarantine(artifact_id, verdict)
            return True
        return False
