"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.retrieval.engine`                | The Sovereign ID. |
| **Official Name** | `retrieval_engine.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Logic Drift**      | Strict Linter Enforcement |
# | **Semantic Decay**   | Axiomatic Compass Audit   |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**
"""

import datetime
import logging
import math
from typing import Any, Dict, List, Optional, Tuple, Set

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# Configure logging for this module
logger = logging.getLogger(__name__)


class RetrievalEngine:
    """
    Manages memory retrieval ranking and weight optimization.
    Implements a multi-factor ranking algorithm considering semantic similarity,
    keywords, recency, frequency, and user preferences.
    """

    def __init__(self, cognition: Any = None) -> None:
        """
        Initializes the RetrievalEngine.

        Args:
            cognition: The cognitive engine or processor for processing queries and memories.
        """
        self.cognition = cognition
        self.weights: Dict[str, float] = {
            "semantic": 0.3,
            "keyword": 0.2,
            "recency": 0.2,
            "frequency": 0.1,
            "user_pref": 0.1,
            "context_hist": 0.1,
        }
        self.REWARD_THRESHOLD_SEMANTIC = 0.8
        self.REWARD_XP_INSIGHT = 10
        self.REWARD_BUFF_COHERENCE = 0.05
        self.RECENCY_DECAY_HALFLIFE = 2592000  # 30 days
        self.FREQUENCY_LOG_BASE = 10.0
        self.metrics = {"hits": 0, "misses": 0, "weight_history": []}
        self.learning_data: Dict[str, Any] = {
            "query_patterns": {},
            "successful_retrievals": {},
            "failed_retrievals": {},
            "weight_adjustments": [],
        }
        self.embedding_cache: Dict[str, Any] = {}
        logger.info("RetrievalEngine initialized.")

    def score_memories(
        self, 
        query: str, 
        candidates: List[Dict[str, Any]], 
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Ranks and scores a list of memory candidates against a query.

        Args:
            query: The search query string.
            candidates: A list of memory candidates to score.
            conversation_history: Recent conversation history for contextual scoring.

        Returns:
            A tuple containing (ranked_memories, rpg_rewards).
        """
        if not candidates:
            return [], {"insight_xp": 0, "coherence_buff": 0.0}

        try:
            query_analysis = self.cognition.process(query) if self.cognition else {}
            query_vec = query_analysis.get("vector")
            query_lemmas = set(query_analysis.get("lemmas", []))
            scored_memories = []
            now = datetime.datetime.now(datetime.timezone.utc)

            for mem in candidates:
                self._ensure_vector(mem)
                scores = self._calculate_scores(mem, query_vec, query_lemmas, now, conversation_history)
                final_score = sum(self.weights.get(k, 0) * scores.get(k, 0) for k in self.weights)
                
                # Boost for Obsidian sources (Heritage Bonus)
                if mem.get("source") == "Obsidian":
                    final_score += 0.2
                
                mem["final_score"] = float(final_score)
                mem["score_details"] = scores
                scored_memories.append(mem)

            ranked = sorted(scored_memories, key=lambda x: x["final_score"], reverse=True)
            rewards = self._calculate_rpg_rewards(ranked)
            return ranked, rewards

        except Exception:
            logger.exception("Ranking failed during score_memories execution.")
            return candidates, {"insight_xp": 0, "coherence_buff": 0.0}

    def _calculate_rpg_rewards(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates RPG-style rewards based on the quality of retrieved memories.

        Args:
            results: The ranked list of scored memories.

        Returns:
            A dictionary containing 'insight_xp' and 'coherence_buff'.
        """
        rewards = {"insight_xp": 0, "coherence_buff": 0.0}
        for res in results[:3]:
            if res.get("score_details", {}).get("semantic", 0) > self.REWARD_THRESHOLD_SEMANTIC:
                rewards["insight_xp"] += self.REWARD_XP_INSIGHT
            if res.get("activation_score", 0) > 10:
                rewards["coherence_buff"] += self.REWARD_BUFF_COHERENCE
        return rewards

    def _calculate_scores(
        self, 
        mem: Dict[str, Any], 
        query_vec: Optional[List[float]], 
        query_lemmas: Set[str], 
        now: datetime.datetime, 
        history: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, float]:
        """
        Calculates individual factor scores for a memory.

        Args:
            mem: The memory object.
            query_vec: The vector representation of the query.
            query_lemmas: The set of query lemmas.
            now: Current timestamp for recency calculation.
            history: Recent conversation history.

        Returns:
            A dictionary of factor scores.
        """
        return {
            "semantic": self._score_semantic(mem, query_vec),
            "keyword": self._score_keyword(mem, query_lemmas),
            "recency": self._score_recency(mem, now),
            "frequency": self._score_frequency(mem),
            "user_pref": float(mem.get("user_preference_score", 0.1)),
            "context_hist": self._calculate_contextual_bonus(mem, history),
        }

    def _score_semantic(self, mem: Dict[str, Any], query_vec: Optional[List[float]]) -> float:
        """
        Calculates cosine similarity between query and memory vectors.

        Args:
            mem: The memory object.
            query_vec: The query vector.

        Returns:
            Cosine similarity score (0.0 to 1.0).
        """
        if not query_vec or not mem.get("vector"):
            return 0.0
        v1, v2 = query_vec, mem["vector"]
        if HAS_NUMPY:
            n1, n2 = np.array(v1), np.array(v2)
            norm1, norm2 = np.linalg.norm(n1), np.linalg.norm(n2)
            if norm1 > 0 and norm2 > 0:
                return float(np.dot(n1, n2) / (norm1 * norm2))
        else:
            dot = sum(a * b for a, b in zip(v1, v2))
            norm1 = sum(a * a for a in v1) ** 0.5
            norm2 = sum(a * a for a in v2) ** 0.5
            if norm1 > 0 and norm2 > 0:
                return dot / (norm1 * norm2)
        return 0.0

    def _score_keyword(self, mem: Dict[str, Any], query_lemmas: Set[str]) -> float:
        """
        Calculates keyword overlap score.

        Args:
            mem: The memory object.
            query_lemmas: The set of query lemmas.

        Returns:
            Overlap ratio (0.0 to 1.0).
        """
        if not query_lemmas:
            return 0.0
        overlap = query_lemmas.intersection(set(mem.get("tags") or []))
        return len(overlap) / len(query_lemmas)

    def _score_recency(self, mem: Dict[str, Any], now: datetime.datetime) -> float:
        """
        Calculates recency decay score using an exponential decay function.

        Args:
            mem: The memory object.
            now: Current timestamp.

        Returns:
            Recency score (0.0 to 1.0).
        """
        last_time = mem.get("last_retrieved") or mem.get("created_at")
        if not last_time:
            return 0.5
        if isinstance(last_time, str):
            try:
                last_time = datetime.datetime.fromisoformat(last_time.replace("Z", "+00:00"))
            except ValueError:
                return 0.5
        delta = max((now - last_time).total_seconds(), 0)
        return math.exp(-delta / self.RECENCY_DECAY_HALFLIFE)

    def _score_frequency(self, mem: Dict[str, Any]) -> float:
        """
        Calculates frequency score based on usage count.

        Args:
            mem: The memory object.

        Returns:
            Frequency score.
        """
        return math.log1p(mem.get("usage_count", 0)) / self.FREQUENCY_LOG_BASE

    def _calculate_contextual_bonus(self, mem: Dict[str, Any], history: Optional[List[Dict[str, Any]]]) -> float:
        """
        Calculates a bonus based on similarity to recent conversation context.

        Args:
            mem: The memory object.
            history: Recent conversation history.

        Returns:
            Contextual bonus score.
        """
        if not history:
            return 0.1
        try:
            turns = [turn.get("content", turn.get("Input", "")) for turn in history[-3:]]
            recent_text = " ".join([str(t) for t in turns if t is not None]).lower()
            u1, u2 = set(recent_text.split()), set(str(mem.get("content", "")).lower().split())
            if not u1:
                return 0.1
            return min(1.0, 0.1 + (len(u1.intersection(u2)) / len(u1) * 0.5))
        except Exception:
            return 0.1

    def adjust_weights(
        self, 
        success: bool, 
        query: str = "", 
        used_memories: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Dynamically adjusts ranking weights based on retrieval success or failure.

        Args:
            success: Whether the retrieval was considered successful.
            query: The query string that led to the retrieval.
            used_memories: The list of memories that were actually utilized.
        """
        self.learning_data["query_patterns"][query] = self.learning_data["query_patterns"].get(query, 0) + 1
        if success:
            self.metrics["hits"] += 1
            if used_memories:
                for mem in used_memories:
                    mid = str(mem.get("id"))
                    self.learning_data["successful_retrievals"][mid] = self.learning_data["successful_retrievals"].get(mid, 0) + 1
            self.weights["semantic"] = min(0.6, self.weights["semantic"] + 0.005)
            self.weights["keyword"] = max(0.05, self.weights["keyword"] - 0.005)
        else:
            self.metrics["misses"] += 1
            self.learning_data["failed_retrievals"][query] = self.learning_data["failed_retrievals"].get(query, 0) + 1
            self.weights["keyword"] = min(0.4, self.weights["keyword"] + 0.01)
            self.weights["semantic"] = max(0.1, self.weights["semantic"] - 0.01)

        total = sum(self.weights.values())
        if total > 0:
            for k in self.weights:
                self.weights[k] /= total

        self.learning_data["weight_adjustments"].append({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), 
            "weights": self.weights.copy()
        })

    def _ensure_vector(self, mem: Dict[str, Any]) -> None:
        """
        Ensures a memory has a vector representation, calculating it if necessary.

        Args:
            mem: The memory object to check/update.
        """
        if mem.get("vector") or not self.cognition:
            return
        content = mem.get("content", "")
        if not content:
            return
        content_hash = str(hash(content))
        if content_hash in self.embedding_cache:
            mem["vector"] = self.embedding_cache[content_hash]
            return
        try:
            analysis = self.cognition.process(content)
            vec = analysis.get("vector")
            if vec:
                mem["vector"] = vec
                self.embedding_cache[content_hash] = vec
        except Exception:
            pass

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.retrieval.engine VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 114c4f9f10fb7623
# ---
