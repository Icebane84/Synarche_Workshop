# ARTIFACT_ID: SENTINEL.KPITracker
# VERSION: v1.0
# STATUS: [ACTIVE]

import json
import threading
from typing import Any, Dict, cast

from .models import EpistemicVerdict


class KPITracker:
    """Manages Key Performance Indicators for Sentinel operations."""

    def __init__(self) -> None:
        self._kpi_lock = threading.Lock()
        self.kpis: Dict[str, Any] = {
            "epistemic_delta_count": 0,
            "verification_coverage": {},
        }

    def update_kpis(self, verdict: EpistemicVerdict) -> None:
        """Updates KPIs based on a single verification verdict."""
        with self._kpi_lock:
            if verdict.delta in ("CRITICAL", "DEGRADED"):
                self.kpis["epistemic_delta_count"] += 1
            for evidence_line in verdict.evidence:
                verifier_name = evidence_line.split(":")[0].strip()
                self.kpis["verification_coverage"][verifier_name] = (
                    self.kpis["verification_coverage"].get(verifier_name, 0) + 1
                )

    def get_kpis(self) -> Dict[str, Any]:
        """Returns a thread-safe, deep copy of the current KPIs."""
        with self._kpi_lock:
            return cast(Dict[str, Any], json.loads(json.dumps(self.kpis)))
