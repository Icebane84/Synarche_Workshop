# ARTIFACT_ID: SENTINEL.VerdictPublisher
# VERSION: v1.0
# STATUS: [ACTIVE]

from typing import Any, Dict

from .models import DeclaredState, EpistemicVerdict


class VerdictPublisher:
    """SP-VERDICT-004: Issues a final, structured Epistemic Verdict."""

    _DELTA_TO_VERDICT = {
        "CRITICAL": "CLAIM_CONTRADICTED",
        "DEGRADED": "CLAIM_CONTRADICTED",
        "NONE": "CLAIM_SUPPORTED",
        "UNVERIFIED": "CLAIM_UNVERIFIED",
    }

    def publish_verdict(self, declared_state: DeclaredState, delta_details: Dict[str, Any]) -> EpistemicVerdict:
        """Generates a structured EpistemicVerdict based on the delta."""
        overall_delta = delta_details["overall_delta"]
        verdict_status = self._DELTA_TO_VERDICT.get(overall_delta, "CLAIM_UNKNOWN")

        return EpistemicVerdict(
            claim=declared_state.status,
            observed="FAIL" if overall_delta in ("CRITICAL", "DEGRADED") else "PASS",
            evidence=delta_details.get("evidence", []),
            delta=delta_details["overall_delta"],
            verdict=verdict_status,
            reason=delta_details.get("reason"),
            confidence=delta_details.get("confidence", 1.0),
        )
