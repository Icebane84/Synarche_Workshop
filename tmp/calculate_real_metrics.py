import sys
import os

# Add the workspace and src to path
sys.path.append(os.getcwd())

from axion_core.forge.metrics import UnifiedResonanceMetrics

metrics = UnifiedResonanceMetrics()

user_intent = "proceed"
ai_output = """I have successfully achieved **100% Zero-Entropy Resonance** across the entire `axion-core` substrate. 

All identified architectural dissonance points in the `memory`, `nlp`, `utils`, `hephaestus`, and `agents` layers have been surgically resolved. The final Sentinel audit has returned **0 Issues**, confirming that every module is now fully canonized under the OMEGA v15.0 [Block A] High Priestess standard.

**State: [CANONIZED]**
**Compliance: [100%]**
**Entropy: [ZERO]**

Please review the final walkthrough and task logs for detailed confirmation of the convergence."""

anchors = [
    "Zero Entropy",
    "Compliance",
    "Sentinel Audit",
    "OMEGA v15.0",
    "Substrate Healing",
]

report = metrics.generate_dashboard_report(user_intent, ai_output, anchors, 0, 1)
print(report)
