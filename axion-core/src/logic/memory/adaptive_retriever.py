"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-LOGIC-ADAPT-RETR-001`   | The Sovereign ID. |
| **Official Name**   | `adaptive_retriever.py`       | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-LOGIC-MEMORY`           | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Adaptive Scoring (Law 28)**
> Implemented from Blueprint `GVRN.REG.AdaptiveScoring.md`.
> Ethos: The Factors are Many; The Score is Truth.
"""

import logging
import math
import time
from typing import Any

log = logging.getLogger(__name__)


class AdaptiveRetriever:
    """Handles multi-factor scoring for memory retrieval.
    Factors: Semantic, Keyword, Recency, Frequency (Activation).
    """

    # Scoring Configuration (The High Priestess balance)
    SIMILARITY_THRESHOLD = 0.8
    ACTIVATION_THRESHOLD = 10
    RECENCY_HALFLIFE = 2592000  # 30 days in seconds

    def __init__(self, cognition_engine: Any = None) -> None:
        """Initialize the AdaptiveRetriever."""
        self.cognition = cognition_engine
        self.weights = {
            "semantic": 0.4,
            "keyword": 0.3,
            "recency": 0.2,
            "frequency": 0.1,
        }

    def score_memories(
        self, query: str, memories: list[dict]
    ) -> tuple[list[dict], dict[str, Any]]:
        """Score a list of memories against a query.

        Each memory is expected to have: content, relevance, timestamp, activation_score, vector.
        """
        if not memories:
            return ([], {"insight_xp": 0, "coherence_buff": 0.0})

        # Prepare query data
        query_analysis = self.cognition.process(query) if self.cognition else {}
        query_vector = query_analysis.get("vector")
        query_lemmas = set(query_analysis.get("lemmas", []))

        scored_results = []
        current_time = time.time()

        for mem in memories:
            scores = self._calculate_all_scores(
                mem, query_vector, query_lemmas, current_time
            )

            # Final Weighted Score
            mem["final_score"] = sum(scores[f] * self.weights[f] for f in self.weights)
            mem["scores_detail"] = scores
            scored_results.append(mem)

        # Sort by final score
        scored_results.sort(key=lambda x: x["final_score"], reverse=True)

        # Calculate RPG Rewards
        rewards = self.calculate_rpg_rewards(scored_results)
        return scored_results, rewards

    def _calculate_all_scores(
        self,
        mem: dict,
        query_vector: list[float] | None,
        query_lemmas: set[str],
        current_time: float,
    ) -> dict[str, float]:
        """Calculate local scores for a single memory entry."""
        scores = {"semantic": 0.0, "keyword": 0.0, "recency": 0.0, "frequency": 0.0}

        # 1. Semantic Score
        if query_vector and mem.get("vector") and self.cognition:
            scores["semantic"] = self._calculate_similarity(query_vector, mem["vector"])

        # 2. Keyword Score
        if query_lemmas and self.cognition:
            mem_text = mem.get("content", "")
            mem_lemmas = set(self.cognition.nlp.lemmatize(mem_text))
            if query_lemmas:
                overlap = query_lemmas.intersection(mem_lemmas)
                scores["keyword"] = len(overlap) / len(query_lemmas)

        # 3. Recency Score (Exponential Decay)
        created_at = mem.get("timestamp", current_time)
        time_diff = current_time - created_at
        scores["recency"] = math.exp(-time_diff / self.RECENCY_HALFLIFE)

        # 4. Frequency Score (Logarithmic Scaling)
        activation = mem.get("activation_score", 0)
        scores["frequency"] = math.log1p(activation) / 10.0

        return scores

    def calculate_rpg_rewards(self, results: list[dict]) -> dict[str, Any]:
        """Calculate XP and Stat buffs based on retrieval performance.

        - High semantic similarity awards 'Insight XP'.
        - Frequent reactivation awards 'Coherence'.
        """
        rewards = {"insight_xp": 0, "coherence_buff": 0.0}
        if not results:
            return rewards

        for res in results[:3]:  # Top 3 matches
            detail = res.get("scores_detail", {})
            if detail.get("semantic", 0) > self.SIMILARITY_THRESHOLD:
                rewards["insight_xp"] += 10

            if res.get("activation_score", 0) > self.ACTIVATION_THRESHOLD:
                rewards["coherence_buff"] += 0.05

        return rewards

    def _calculate_similarity(self, v1: list[float], v2: list[float]) -> float:
        """Calculate Cosine Similarity between two vectors."""
        try:
            dot_product = sum(a * b for a, b in zip(v1, v2, strict=True))
            magnitude1 = math.sqrt(sum(a * a for a in v1))
            magnitude2 = math.sqrt(sum(b * b for b in v2))
            if not magnitude1 or not magnitude2:
                return 0.0
            return dot_product / (magnitude1 * magnitude2)
        except Exception:
            return 0.0
