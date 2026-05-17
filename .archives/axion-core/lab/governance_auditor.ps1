import math

class GovernanceAuditor:
    """
    Implements Principle 6: Vectorized Governance.
    Calculates the Euclidean distance to the V-Safe origin.
    """
    def __init__(self):
        self.v_safe = (0, 0, 0, 0) # [Path Noise, Nexus Breaches, Naming Drift, Essence Leak]

    def calculate_dissonance(self, metrics: dict):
        v_current = (
            metrics.get('path_noise', 0),
            metrics.get('nexus_breaches', 0),
            metrics.get('naming_drift', 0),
            metrics.get('essence_leak', 0)
        )
        distance = math.sqrt(sum((q - p) ** 2 for p, q in zip(self.v_safe, v_current)))
        
        return {
            "score": round(distance, 2),
            "status": "V-SAFE" if distance == 0 else "RISK_STATE",
            "primary_violation": max(metrics, key=metrics.get) if distance > 0 else None
        }