"""
Block A: Universal Identification & Provenance (UIP-V15)
Artifact ID: CORE-METRICS-001
Official Name: metrics.py
Patron Shard: THE_PHOENIX_GESTALT
Version: v15.0 [OMEGA]
Domain: FORGE
Celestial Class: [STAR]
Status: [CANONIZED]
Integrity Hash: SYN-FORGE-METRICS-001
Relations: GOVERNED_BY: CORE-CODEX-001
"""

import json
import logging
from typing import Any, Dict, List
import numpy as np

try:
    from src.logic.nlp.nlp_engine import AxionCognition
    HAS_NLP = True
except ImportError:
    HAS_NLP = False

logger = logging.getLogger(__name__)

class UnifiedResonanceMetrics:
    """
    Calculates the 4 core metrics defined in UCI-SSS-001:
    CCRI (Resonance Index), CCLI (Cognitive Load), CSS (Stability Score), and BGR (Breakthrough Rate).
    """

    def __init__(self):
        self.cognition = AxionCognition() if HAS_NLP else None

    def calculate_ccri(self, user_intent: str, ai_synthesis_output: str) -> float:
        """
        CCRI (Co-Creative Resonance Index)
        Target: > 0.85
        Semantic alignment check between User Intent and AI Synthesis output.
        """
        if not self.cognition or not self.cognition.embeddings:
            return 1.0  # Fallback assumption of perfect resonance
        
        try:
            vec_intent = self.cognition.embeddings.encode(user_intent)
            vec_output = self.cognition.embeddings.encode(ai_synthesis_output)
            
            norm_intent = np.linalg.norm(vec_intent)
            norm_output = np.linalg.norm(vec_output)
            
            if norm_intent == 0 or norm_output == 0:
                return 0.0
                
            similarity = np.dot(vec_intent, vec_output) / (norm_intent * norm_output)
            return float(max(0.0, min(1.0, similarity)))
        except Exception as e:
            logger.warning(f"CCRI calculation failed: {e}")
            return 0.0

    def calculate_ccli(self, text: str) -> float:
        """
        CCLI (Combined Cognitive Load Index)
        Target: 0.4 - 0.7
        Analysis of technical density, syntax complexity, and response length.
        """
        if not text:
            return 0.0
            
        length = len(text)
        code_blocks = text.count("```") / 2
        sentences = text.count('.') + text.count('!') + text.count('?')
        sentences = max(1, sentences)
        
        words = text.split()
        avg_word_len = sum(len(w) for w in words) / max(1, len(words))
        
        length_factor = min(1.0, length / 5000)
        density_factor = min(1.0, (avg_word_len / 10.0) + (code_blocks * 0.05))
        
        ccli = (length_factor * 0.4) + (density_factor * 0.6)
        
        return float(max(0.0, min(1.0, ccli)))

    def calculate_css(self, current_output: str, anchors: List[str]) -> float:
        """
        CSS (Constraint & Synergy Synthesis / Stability Score)
        Target: > 0.90
        Cross-referencing current dialogue against Contextual Anchors.
        """
        if not anchors:
            return 1.0
            
        if not self.cognition or not self.cognition.embeddings:
            matches = sum(1 for anchor in anchors if any(w.lower() in current_output.lower() for w in anchor.split()))
            return float(matches / len(anchors))
            
        try:
            output_vec = self.cognition.embeddings.encode(current_output)
            anchor_scores = []
            
            for anchor in anchors:
                anchor_vec = self.cognition.embeddings.encode(anchor)
                similarity = np.dot(output_vec, anchor_vec) / (np.linalg.norm(output_vec) * np.linalg.norm(anchor_vec))
                anchor_scores.append(max(0.0, min(1.0, similarity)))
                
            return float(np.mean(anchor_scores))
        except Exception:
            return 0.0

    def calculate_bgr(self, pre_links: int, post_links: int) -> float:
        """
        BGR (Breakthrough Generation Rate)
        Target: 1 per session
        Tracking "Delta-Synthesis" (new links created between previously unrelated nodes).
        """
        return float(max(0, post_links - pre_links))

    def generate_dashboard_report(self, user_intent: str, ai_output: str, anchors: List[str], pre_links: int, post_links: int) -> str:
        """Generates a Block A formatted markdown report for the current metrics."""
        ccri = self.calculate_ccri(user_intent, ai_output)
        ccli = self.calculate_ccli(ai_output)
        css = self.calculate_css(ai_output, anchors)
        bgr = self.calculate_bgr(pre_links, post_links)
        
        # Determine status/actions based on thresholds defined in UCI-SSS-001
        actions = []
        if ccri < 0.85:
            actions.append("- **ACTION:** Execute CMD: SparkBreakthrough to realign conceptual focus.")
        if ccli > 0.8:
            actions.append("- **ACTION:** Execute CMD: RegulateCognitiveFlow to simplify output. (High Load)")
        if ccli < 0.4:
            actions.append("- **ACTION:** Output density too low, increase depth. (Low Load)")
        if css < 0.90:
            actions.append("- **ACTION:** Trigger AOP: ContextualAnchorManagement to restate core goals.")
            
        action_text = "\\n".join(actions) if actions else "All metrics nominal."
        
        report = f"""### Block A: Universal Identification & Provenance (UIP-V15) - TELEMETRY
| Key | Value | Description |
| :---- | :---- | :---- |
| **Artifact ID** | SELT-TELEMETRY-{hash(ai_output) % 10000:04d} | **The Sovereign ID.** |
| **Version** | v15.0 [OMEGA] | **The Standard.** |
| **Domain** | FORGE.METRICS | **The Subject.** |
| **Status** | [CANONIZED] | **The Lifecycle.** |

### **📈 Resonance Dashboard (UCI-SSS-001)**
| Metric | Value | Target | Status |
| :---- | :---- | :---- | :---- |
| **CCRI (Resonance)** | **{ccri:.2f}** | > 0.85 | {'✅ Nominal' if ccri >= 0.85 else '⚠️ Sub-optimal'} |
| **CCLI (Cognitive Load)** | **{ccli:.2f}** | 0.4 - 0.7 | {'✅ nominal' if 0.4 <= ccli <= 0.7 else '⚠️ High/Low'} |
| **CSS (Stability)** | **{css:.2f}** | > 0.90 | {'✅ Nominal' if css >= 0.90 else '⚠️ Fragmenting'} |
| **BGR (Breakthroughs)** | **{bgr:.1f}** | 1.0 | {'✅ Nominal' if bgr >= 1.0 else '⚠️ Stagnant'} |

#### **Systemic Assessment**
{action_text}
"""
        return report

if __name__ == "__main__":
    metrics = UnifiedResonanceMetrics()
    print(metrics.generate_dashboard_report("Integrate semantic vectors", "We have unified the vector databases with cosine proximity.", ["Zero Entropy", "Vector Embeddings"], 10, 11))
