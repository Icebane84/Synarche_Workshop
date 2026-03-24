"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-LOGIC-MEM-RETR-001`     | The Sovereign ID. |
| **Official Name**   | `retrieval_engine.py`           | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-LOGIC-MEMORY`           | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Adaptive Ranking (Law 28)**
> Implemented from Blueprint `GVRN.REG.AdaptiveRanking.md`.
> Ethos: The Ranking is Many; The Truth is One.
"""

import datetime
import logging
from typing import Any

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

logger = logging.getLogger(__name__)


class RetrievalEngine:
    """Manages memory retrieval ranking and weight optimization.
    Ports GEM's RetrievalEngine logic into the Axion PRS ecosystem.
    """

    def __init__(self, cognition: Any = None) -> None:
        """:param cognition: AxionCognition instance for embeddings and NLP."""
        self.cognition = cognition

        # Initial weights (GGMA XIV Standard)
        self.weights: dict[str, float] = {
            "semantic": 0.3,
            "keyword": 0.2,
            "recency": 0.2,
            "frequency": 0.1,
            "user_pref": 0.1,
            "context_hist": 0.1,
        }

        # Constants for Scoring (OMEGA Standard)
        self.REWARD_THRESHOLD_SEMANTIC = 0.8
        self.REWARD_XP_INSIGHT = 10
        self.REWARD_BUFF_COHERENCE = 0.05
        self.RECENCY_DECAY_HALFLIFE = 2592000  # 30 days in seconds
        self.FREQUENCY_LOG_BASE = 10.0

        # Performance Tracking & Learning Data
        self.metrics = {"hits": 0, "misses": 0, "weight_history": []}
        self.learning_data: dict[str, Any] = {
            "query_patterns": {},
            "successful_retrievals": {},
            "failed_retrievals": {},
            "weight_adjustments": [],
        }

        self.embedding_cache: dict[str, Any] = {}
        logger.info("RetrievalEngine initialized with Adaptive Multi-Factor Weighting.")

    def score_memories(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        conversation_history: list[dict] | None = None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Scores and ranks a list of candidate memories.
        :param query: The user's input query.
        :param candidates: List of memory dictionaries from the database.
        :param conversation_history: Recent interaction turns for context bonus.
        :return: (Ranked memories, Execution metrics).
        """
        if not candidates:
            return [], {"coherence_impact": 0.0}

        try:
            # 1. Prepare Query Data
            query_analysis = self.cognition.process(query) if self.cognition else {}
            query_vec = query_analysis.get("vector")
            query_lemmas = set(query_analysis.get("lemmas", []))

            scored_memories = []
            now = datetime.datetime.now(datetime.timezone.utc)

            # 2. Score Each Candidate (GGMA Batch Logic)
            for mem in candidates:
                # 2.1 Vector Synthesis (Ensure embeddings for external knowledge)
                self._ensure_vector(mem)

                scores = self._calculate_scores(
                    mem, query_vec, query_lemmas, now, conversation_history
                )

                # Apply Weights
                final_score = sum(
                    self.weights.get(k, 0) * scores.get(k, 0) for k in self.weights
                )

                # 2.2 Sovereign Boost (Obsidian Bias)
                if mem.get("source") == "Obsidian":
                    final_score += 0.2  # Insight Bonus for curated wisdom

                mem["final_score"] = float(final_score)
                mem["score_details"] = scores
                scored_memories.append(mem)

            # 3. Rank
            ranked = sorted(
                scored_memories, key=lambda x: x["final_score"], reverse=True
            )

            # 4. Generate Rewards (GGMA Insight/Coherence Standards)
            rewards = self._calculate_rpg_rewards(ranked)

            return ranked, rewards

        except Exception:
            logger.exception("Ranking failed in RetrievalEngine")
            return candidates, {"insight_xp": 0, "coherence_buff": 0.0}

    def _calculate_rpg_rewards(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        """Calculates XP and status rewards based on retrieval quality."""
        rewards = {"insight_xp": 0, "coherence_buff": 0.0}
        if not results:
            return rewards

        # Only consider top 3 matches for rewards
        for res in results[:3]:
            # Insight reward for semantic accuracy
            if (
                res.get("score_details", {}).get("semantic", 0)
                > self.REWARD_THRESHOLD_SEMANTIC
            ):
                rewards["insight_xp"] += self.REWARD_XP_INSIGHT

            # Coherence reward for frequent/stable memory
            if res.get("activation_score", 0) > 10:
                rewards["coherence_buff"] += self.REWARD_BUFF_COHERENCE

        return rewards

    def _calculate_scores(
        self,
        mem: dict[str, Any],
        query_vec: list[float] | None,
        query_lemmas: set[str],
        now: datetime.datetime,
        history: list[dict] | None,
    ) -> dict[str, float]:
        """Calculates all scoring factors for a single memory."""
        scores = {
            "semantic": self._score_semantic(mem, query_vec),
            "keyword": self._score_keyword(mem, query_lemmas),
            "recency": self._score_recency(mem, now),
            "frequency": self._score_frequency(mem),
            "user_pref": mem.get("user_preference_score", 0.1),
            "context_hist": self._calculate_contextual_bonus(mem, history),
        }
        return scores

    def _score_semantic(
        self, mem: dict[str, Any], query_vec: list[float] | None
    ) -> float:
        """Calculates cosine similarity if vectors are available."""
        if not query_vec or not mem.get("vector"):
            return 0.0

        if HAS_NUMPY:
            v1 = np.array(query_vec)
            v2 = np.array(mem["vector"])
            # Handle zero-norm vectors to prevent division by zero
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            if norm_v1 > 0 and norm_v2 > 0:
                return float(np.dot(v1, v2) / (norm_v1 * norm_v2))
            return 0.0

        # Fallback to simple dot product if vectors are normalized (original logic was more robust)
        # Reimplementing original non-numpy logic for robustness
        v1 = query_vec
        v2 = mem["vector"]
        dot = sum(a * b for a, b in zip(v1, v2, strict=False))
        norm_v1 = sum(a * a for a in v1) ** 0.5
        norm_v2 = sum(a * a for a in v2) ** 0.5
        if norm_v1 > 0 and norm_v2 > 0:
            return dot / (norm_v1 * norm_v2)
        return 0.0

    def _score_keyword(self, mem: dict[str, Any], query_lemmas: set[str]) -> float:
        """Calculates lemma overlap score."""
        if not query_lemmas:
            return 0.0

        # Original code used mem.get("tags")
        mem_tags = set(mem.get("tags") or [])
        overlap = query_lemmas.intersection(mem_tags)
        if not query_lemmas:  # Avoid division by zero if query_lemmas is empty
            return 0.0
        return len(overlap) / len(query_lemmas)

    def _score_recency(self, mem: dict[str, Any], now: datetime.datetime) -> float:
        """Calculates exponential decay based on time."""
        # Original code used 'last_retrieved' or 'created_at'
        last_time = mem.get("last_retrieved") or mem.get("created_at")
        if not last_time:
            return 0.5  # Default if no timestamp

        if isinstance(last_time, str):
            try:
                last_time = datetime.datetime.fromisoformat(
                    last_time.replace("Z", "+00:00")
                )
            except ValueError:
                return 0.5  # Default if parsing fails

        delta = (now - last_time).total_seconds()
        # Half-life decay logic
        import math

        # Ensure delta is non-negative for decay calculation
        delta = max(delta, 0)
        return math.exp(-delta / self.RECENCY_DECAY_HALFLIFE)

    def _score_frequency(self, mem: dict[str, Any]) -> float:
        """Calculates logarithmic frequency score."""
        usage = mem.get("usage_count", 0)
        import math

        return math.log1p(usage) / self.FREQUENCY_LOG_BASE

    def _calculate_contextual_bonus(
        self, mem: dict[str, Any], history: list[dict] | None
    ) -> float:
        """Boosts score if memory overlaps with recent conversation topics."""
        if not history:
            return 0.1

        try:
            # Filter out None content and join
            turns = [
                turn.get("content", turn.get("Input", "")) for turn in history[-3:]
            ]
            recent_text = " ".join([str(t) for t in turns if t is not None]).lower()
            mem_content = str(mem.get("content", "")).lower()

            # Simple overlap check
            u1 = set(recent_text.split())
            if not u1:
                return 0.1

            u2 = set(mem_content.split())
            common = u1.intersection(u2)

            bonus = len(common) / len(u1)
            return min(1.0, 0.1 + (bonus * 0.5))
        except Exception:
            return 0.1

    def adjust_weights(
        self, success: bool, query: str = "", used_memories: list[dict] | None = None
    ) -> None:
        """Adaptive learning: Shift Weights based on resonance."""
        self.learning_data["query_patterns"][query] = (
            self.learning_data["query_patterns"].get(query, 0) + 1
        )

        if success:
            self.metrics["hits"] += 1
            if used_memories:
                for mem in used_memories:
                    mid = str(mem.get("id"))
                    self.learning_data["successful_retrievals"][mid] = (
                        self.learning_data["successful_retrievals"].get(mid, 0) + 1
                    )

            self.weights["semantic"] = min(0.6, self.weights["semantic"] + 0.005)
            self.weights["keyword"] = max(0.05, self.weights["keyword"] - 0.005)
        else:
            self.metrics["misses"] += 1
            self.learning_data["failed_retrievals"][query] = (
                self.learning_data["failed_retrievals"].get(query, 0) + 1
            )

            self.weights["keyword"] = min(0.4, self.weights["keyword"] + 0.01)
            self.weights["semantic"] = max(0.1, self.weights["semantic"] - 0.01)

        total = sum(self.weights.values())
        if total > 0:
            for k in self.weights:
                self.weights[k] /= total

        self.learning_data["weight_adjustments"].append(
            {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "weights": self.weights.copy(),
            }
        )

    def _ensure_vector(self, mem: dict[str, Any]) -> None:
        """Synthesizes a vector for candidates missing them (e.g., Obsidian results)."""
        if mem.get("vector") or not self.cognition:
            return

        content = mem.get("content", "")
        if not content:
            return

        # Check cache first
        content_hash = str(hash(content))
        if content_hash in self.embedding_cache:
            mem["vector"] = self.embedding_cache[content_hash]
            return

        try:
            # Generate on-the-fly embedding
            analysis = self.cognition.process(content)
            vec = analysis.get("vector")
            if vec:
                mem["vector"] = vec
                self.embedding_cache[content_hash] = vec
        except Exception as e:
            logger.warning(f"Vector synthesis failed for memory {mem.get('id')}: {e}")
