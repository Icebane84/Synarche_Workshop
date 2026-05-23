"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `LOG-MEM-ADA-001`             | The Sovereign ID. |
| **Official Name**   | `adaptive_retriever.py`       | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `LOG-MEM`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Adaptive Recall (Law 14)**
> Implemented from Blueprint `GVRN.REG.AdaptiveRetriever.md`.
> Ethos: Contextual relevance through multi-vector weighting.
"""

import logging
import math
import time
from typing import Any, Dict, List, Optional, Set, Tuple

log = logging.getLogger(__name__)


class AdaptiveRetriever:
    """Handles multi-factor scoring for memory retrieval.
    Factors: Semantic, Keyword, Recency, Frequency (Activation).
    """

    # Scoring Configuration (The High Priestess balance)
    SIMILARITY_THRESHOLD: float = 0.8
    ACTIVATION_THRESHOLD: int = 10
    RECENCY_HALFLIFE: int = 2592000  # 30 days in seconds

    def __init__(self, cognition_engine: Any = None) -> None:
        """Initializes the AdaptiveRetriever.

        Args:
            cognition_engine (Any): The engine used for NLP processing and vectorization.

        """
        self.cognition = cognition_engine
        self.weights: Dict[str, float] = {
            "semantic": 0.4,
            "keyword": 0.3,
            "recency": 0.2,
            "frequency": 0.1,
        }

    def score_memories(
        self, query: str, memories: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Scores a list of memories against a query using multi-factor analysis.

        Args:
            query (str): The search query.
            memories (List[Dict[str, Any]]): The list of memory objects to score.

        Returns:
            Tuple[List[Dict[str, Any]], Dict[str, Any]]: The scored and sorted memories, plus RPG rewards.

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
        scored_results.sort(key=lambda x: x.get("final_score", 0), reverse=True)

        # Calculate RPG Rewards
        rewards = self.calculate_rpg_rewards(scored_results)
        return scored_results, rewards

    def _calculate_all_scores(
        self,
        mem: Dict[str, Any],
        query_vector: Optional[List[float]],
        query_lemmas: Set[str],
        current_time: float,
    ) -> Dict[str, float]:
        """Calculates individual factor scores for a single memory entry.

        Args:
            mem (Dict[str, Any]): The memory object.
            query_vector (Optional[List[float]]): The vector representation of the query.
            query_lemmas (Set[str]): The set of lemmas from the query.
            current_time (float): The current system time.

        Returns:
            Dict[str, float]: A dictionary containing scores for semantic, keyword, recency, and frequency.

        """
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

    def calculate_rpg_rewards(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates XP and Stat buffs based on retrieval performance.
        High semantic similarity awards 'Insight XP'.
        Frequent reactivation awards 'Coherence'.

        Args:
            results (List[Dict[str, Any]]): The scored retrieval results.

        Returns:
            Dict[str, Any]: The calculated rewards dictionary.

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

    def _calculate_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Calculates Cosine Similarity between two vectors.

        Args:
            v1 (List[float]): The first vector.
            v2 (List[float]): The second vector.

        Returns:
            float: The cosine similarity score (0.0 to 1.0).

        """
        try:
            dot_product = sum(a * b for a, b in zip(v1, v2, strict=False))
            magnitude1 = math.sqrt(sum(a * a for a in v1))
            magnitude2 = math.sqrt(sum(b * b for b in v2))
            if not magnitude1 or not magnitude2:
                return 0.0
            return dot_product / (magnitude1 * magnitude2)
        except Exception:
            return 0.0
