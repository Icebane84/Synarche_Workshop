# TRANSCLUDE_BLOCK: governance_auditor.py

import math


class GovernanceAuditor:
    """Implements Principle 6: Vectorized Governance.
    Quantifies architectural compliance as a multi-dimensional distance.
    """

    def __init__(self):
        # The 'Safe State' is the origin point (0, 0, 0, 0)
        self.v_safe = (0, 0, 0, 0)

    def calculate_dissonance(self, metrics: dict):
        """Calculates the Euclidean distance to the V-Safe state.
        Metrics input schema:
        - path_noise: Count of relative (../) imports.
        - nexus_breaches: Imports bypassing index.ts entry points.
        - naming_drift: Count of non-definitive names (data, info, etc).
        - essence_leak: Interfaces/Types not using 'export type'.
        """
        # Dimensions: [Path, Nexus, Naming, Essence]
        v_current = (
            metrics.get("path_noise", 0),
            metrics.get("nexus_breaches", 0),
            metrics.get("naming_drift", 0),
            metrics.get("essence_leak", 0),
        )

        # Vector Distance Calculation: sqrt(sum((q - p)^2))
        distance = math.sqrt(
            sum((q - p) ** 2 for p, q in zip(self.v_safe, v_current, strict=False))
        )

        return {
            "score": round(distance, 2),
            "status": "V-SAFE" if distance == 0 else "RISK_STATE",
            "primary_violation": (
                max(metrics, key=metrics.get) if distance > 0 else None
            ),
        }


# --- EXAMPLE USAGE ---
# auditing a specific module:
# metrics = {
#     "path_noise": 5,      # 5 instances of ../../ found
#     "nexus_breaches": 0,   # All boundaries respected
#     "naming_drift": 2,     # Found 'userData' and 'config'
#     "essence_leak": 1      # One interface leaked into runtime
# }

# auditor = GovernanceAuditor()
# result = auditor.calculate_dissonance(metrics)
# print(f"Architectural Dissonance: {result['score']} ({result['status']})")
