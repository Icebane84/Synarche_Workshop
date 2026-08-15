# ARTIFACT_ID: SENTINEL.DeltaEngine
# VERSION: v1.0
# STATUS: [ACTIVE]

from typing import Any, Dict, List

from .models import DeclaredState, ObservedState


class DeltaEngine:
    """SP-DELTA-003: Compares Declared State against Observed State."""

    STRICT_STATUSES = {"[CANONIZED]"}

    def _determine_overall_delta(
        self, issues: list[str], is_strict: bool, definitive_count: int, total_count: int
    ) -> str:
        """Helper to determine the final delta status."""
        if issues:
            return "CRITICAL" if is_strict else "DEGRADED"
        elif definitive_count < total_count:
            return "UNVERIFIED"
        else:
            return "NONE"

    def calculate_delta(self, declared_state: DeclaredState, observed_state: ObservedState) -> Dict[str, Any]:
        """
        Calculates the delta between declared and observed states.
        """
        issues: List[str] = []
        evidence: List[str] = []
        reasons: List[str] = []
        definitive_count = 0
        total_count = 0
        is_strict = declared_state.status in self.STRICT_STATUSES

        for verifier_name, result in observed_state.verifier_results.items():
            status = result.get("status", "UNKNOWN")
            message = result.get("message", "")
            evidence.append(f"{verifier_name}: {status}")
            total_count += 1
            if status in ("PASS", "FAIL"):
                definitive_count += 1
            if status == "FAIL":
                issues.append(f"{verifier_name} failed: {message}")
                reasons.append(f"[{verifier_name}] {message}")
            elif status == "VERIFIER_FAILURE":
                issues.append(f"{verifier_name} crashed: {message}")
                reasons.append(f"[{verifier_name} CRASHED] {message}")

        confidence = (definitive_count / total_count) if total_count else 0.0
        overall_delta = self._determine_overall_delta(issues, is_strict, definitive_count, total_count)
        reason = (
            "; ".join(reasons)
            if reasons
            else (
                "All checks passed."
                if overall_delta == "NONE"
                else "Some verifiers did not produce a definitive result."
            )
        )

        return {
            "overall_delta": overall_delta,
            "issues": issues,
            "evidence": evidence,
            "reason": reason,
            "confidence": confidence,
        }
