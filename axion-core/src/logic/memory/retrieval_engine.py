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
## **[ARTIFACT END]**
"""

import datetime
import logging
import math
from typing import Any

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

logger = logging.getLogger(__name__)

class RetrievalEngine:
    """Manages memory retrieval ranking and weight optimization."""

    def __init__(self, cognition: Any = None) -> None:
        self.cognition = cognition
        self.weights: dict[str, float] = {
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
        self.learning_data: dict[str, Any] = {
            "query_patterns": {},
            "successful_retrievals": {},
            "failed_retrievals": {},
            "weight_adjustments": [],
        }
        self.embedding_cache: dict[str, Any] = {}
        logger.info("RetrievalEngine initialized.")

    def score_memories(self, query: str, candidates: list[dict[str, Any]], conversation_history: list[dict] | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        if not candidates:
            return [], {"coherence_impact": 0.0}
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
                if mem.get("source") == "Obsidian": final_score += 0.2
                mem["final_score"] = float(final_score)
                mem["score_details"] = scores
                scored_memories.append(mem)
            ranked = sorted(scored_memories, key=lambda x: x["final_score"], reverse=True)
            rewards = self._calculate_rpg_rewards(ranked)
            return ranked, rewards
        except Exception:
            logger.exception("Ranking failed")
            return candidates, {"insight_xp": 0, "coherence_buff": 0.0}

    def _calculate_rpg_rewards(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        rewards = {"insight_xp": 0, "coherence_buff": 0.0}
        for res in results[:3]:
            if res.get("score_details", {}).get("semantic", 0) > self.REWARD_THRESHOLD_SEMANTIC:
                rewards["insight_xp"] += self.REWARD_XP_INSIGHT
            if res.get("activation_score", 0) > 10:
                rewards["coherence_buff"] += self.REWARD_BUFF_COHERENCE
        return rewards

    def _calculate_scores(self, mem: dict[str, Any], query_vec: list[float] | None, query_lemmas: set[str], now: datetime.datetime, history: list[dict] | None) -> dict[str, float]:
        return {
            "semantic": self._score_semantic(mem, query_vec),
            "keyword": self._score_keyword(mem, query_lemmas),
            "recency": self._score_recency(mem, now),
            "frequency": self._score_frequency(mem),
            "user_pref": mem.get("user_preference_score", 0.1),
            "context_hist": self._calculate_contextual_bonus(mem, history),
        }

    def _score_semantic(self, mem: dict[str, Any], query_vec: list[float] | None) -> float:
        if not query_vec or not mem.get("vector"): return 0.0
        v1, v2 = query_vec, mem["vector"]
        if HAS_NUMPY:
            n1, n2 = np.array(v1), np.array(v2)
            norm1, norm2 = np.linalg.norm(n1), np.linalg.norm(n2)
            if norm1 > 0 and norm2 > 0: return float(np.dot(n1, n2) / (norm1 * norm2))
        else:
            dot = sum(a * b for a, b in zip(v1, v2))
            norm1 = sum(a * a for a in v1) ** 0.5
            norm2 = sum(a * a for a in v2) ** 0.5
            if norm1 > 0 and norm2 > 0: return dot / (norm1 * norm2)
        return 0.0

    def _score_keyword(self, mem: dict[str, Any], query_lemmas: set[str]) -> float:
        if not query_lemmas: return 0.0
        overlap = query_lemmas.intersection(set(mem.get("tags") or []))
        return len(overlap) / len(query_lemmas)

    def _score_recency(self, mem: dict[str, Any], now: datetime.datetime) -> float:
        last_time = mem.get("last_retrieved") or mem.get("created_at")
        if not last_time: return 0.5
        if isinstance(last_time, str):
            try: last_time = datetime.datetime.fromisoformat(last_time.replace("Z", "+00:00"))
            except ValueError: return 0.5
        delta = max((now - last_time).total_seconds(), 0)
        return math.exp(-delta / self.RECENCY_DECAY_HALFLIFE)

    def _score_frequency(self, mem: dict[str, Any]) -> float:
        return math.log1p(mem.get("usage_count", 0)) / self.FREQUENCY_LOG_BASE

    def _calculate_contextual_bonus(self, mem: dict[str, Any], history: list[dict] | None) -> float:
        if not history: return 0.1
        try:
            turns = [turn.get("content", turn.get("Input", "")) for turn in history[-3:]]
            recent_text = " ".join([str(t) for t in turns if t is not None]).lower()
            u1, u2 = set(recent_text.split()), set(str(mem.get("content", "")).lower().split())
            if not u1: return 0.1
            return min(1.0, 0.1 + (len(u1.intersection(u2)) / len(u1) * 0.5))
        except Exception: return 0.1

    def adjust_weights(self, success: bool, query: str = "", used_memories: list[dict] | None = None) -> None:
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
            for k in self.weights: self.weights[k] /= total
        self.learning_data["weight_adjustments"].append({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "weights": self.weights.copy()})

    def _ensure_vector(self, mem: dict[str, Any]) -> None:
        if mem.get("vector") or not self.cognition: return
        content = mem.get("content", "")
        if not content: return
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
        except Exception: pass

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.retrieval.engine VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 114c4f9f10fb7623
