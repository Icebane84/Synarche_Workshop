"""
artifact_anchor:
  id: CORE.ENGINE_TYPES.001
  version: v15.0 [OMEGA]
  provenance: '2026-06-09'
  domain: CORE
  celestial_class: STAR
  tier: FOUNDATION
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []

### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-TYPES-001`               | The Sovereign ID. |
| **Official Name**   | `types.py`                    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG`                         | The Subject.      |
| **Celestial Class** | `[STAR]`                      | The Weight.       |
| **Evolution**       | `PAD-SIP Foundation`          | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Systemic Synthesis (Law 01)**
> Implemented from Blueprint `PAD-SIP.Layer.B.RuntimePrototype`.
> Ethos: A unified type system is the bedrock of cognitive coherence.
"""

from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

# ---------------------------------------------------------------------------
# §1  Enumerations
# ---------------------------------------------------------------------------


class CognitivePhase(Enum):
    """The eight phases of the cognitive tick loop (PAD-SIP Layer D)."""

    EXPERIENCE = auto()  # E  — raw event ingestion
    ENCODE = auto()  # Φ  — metaphor encoding
    EXPAND = auto()  # Ψ  — semantic loom expansion
    GOVERN = auto()  # G  — governance DSL evaluation
    PATTERN = auto()  # Π  — pattern engine / synergy mining
    ACT = auto()  # Ω  — action engine selection & execution
    TOOL = auto()  # τ  — tool/environment interaction
    REMEMBER = auto()  # Λ  — memory loom reinforcement / decay
    BIAS = auto()  # Γ  — metaphor bias update (closes the loop)


class MemoryPressureLevel(Enum):
    """Operational thresholds for memory pressure."""

    NOMINAL = "nominal"  # 0.0 - 0.49   — no action required
    ELEVATED = "elevated"  # 0.50 - 0.74  — soft warnings
    CRITICAL = "critical"  # 0.75 - 0.89  — pattern mine triggered
    OVERFLOW = "overflow"  # 0.90+         — forced consolidation


# ---------------------------------------------------------------------------
# §2  CognitiveState  (the heart of Layer D)
# ---------------------------------------------------------------------------


@dataclass
class CognitiveState:
    """Live snapshot of the cognitive operating system's current condition.

    This is the single authoritative object read and written by the
    CognitiveScheduler on every tick.  All stage functions (Φ, Ψ, Ω …)
    receive a reference to this object so they share state without coupling.

    Attributes:
        active_nodes        : count of non-archived memory entries currently in play.
        attention_budget    : normalized float [0, 1] - how much focus remains this tick.
        memory_pressure     : normalized float [0, 1] - proportion of active slots used.
        novelty_score       : rolling novelty of the most recent event (cosine distance
                              to prior event vector, or 0.5 default).
        tick_count          : monotonic counter incremented each scheduler cycle.
        current_phase       : which phase of the cognitive loop is executing now.
        last_event          : the most recently ingested CognitiveEvent (or None).
        governance_verdicts : list of verdicts from the last Governance evaluation.
        pattern_hits        : patterns/synergies found in the last Π phase.
        phase_durations_ms  : per-phase timing from the last completed tick (for telemetry).
    """

    active_nodes: int = 0
    attention_budget: float = 1.0
    memory_pressure: float = 0.0
    novelty_score: float = 0.5

    tick_count: int = 0
    current_phase: CognitivePhase = CognitivePhase.EXPERIENCE

    last_event: CognitiveEvent | None = None
    governance_verdicts: list[dict[str, Any]] = field(default_factory=list)
    pattern_hits: list[dict[str, Any]] = field(default_factory=list)
    phase_durations_ms: dict[str, float] = field(default_factory=dict)

    # Derived convenience properties
    @property
    def pressure_level(self) -> MemoryPressureLevel:
        """Returns the categorical pressure level based on the numeric score."""
        overflow_threshold = 0.90
        critical_threshold = 0.75
        elevated_threshold = 0.50

        if self.memory_pressure >= overflow_threshold:
            return MemoryPressureLevel.OVERFLOW
        if self.memory_pressure >= critical_threshold:
            return MemoryPressureLevel.CRITICAL
        if self.memory_pressure >= elevated_threshold:
            return MemoryPressureLevel.ELEVATED
        return MemoryPressureLevel.NOMINAL

    def consume_attention(self, cost: float) -> None:
        """Reduce the attention budget by a given cost, floored at 0."""
        self.attention_budget = max(0.0, self.attention_budget - cost)

    def reset_tick(self) -> None:
        """Prepare state for the next scheduler tick."""
        self.tick_count += 1
        self.attention_budget = 1.0
        self.governance_verdicts = []
        self.pattern_hits = []
        self.phase_durations_ms = {}
        self.current_phase = CognitivePhase.EXPERIENCE

    def to_dict(self) -> dict[str, Any]:
        """Serialize state to a plain dictionary (for telemetry / logging)."""
        return {
            "tick": self.tick_count,
            "phase": self.current_phase.name,
            "active_nodes": self.active_nodes,
            "attention_budget": round(self.attention_budget, 4),
            "memory_pressure": round(self.memory_pressure, 4),
            "pressure_level": self.pressure_level.value,
            "novelty_score": round(self.novelty_score, 4),
            "governance_verdicts": self.governance_verdicts,
            "pattern_hits": len(self.pattern_hits),
        }


# ---------------------------------------------------------------------------
# §3  CognitiveEvent  (Layer A — Experience Stream input)
# ---------------------------------------------------------------------------


@dataclass
class CognitiveEvent:
    """A single unit of experience entering the cognitive pipeline.

    Attributes:
        event_id    : globally unique identifier for this event.
        event_type  : categorical label (e.g. "MEMORY_ADD", "USER_INPUT", "SENSOR_READ").
        content     : the raw textual or structured payload.
        source      : originating module / agent ID.
        timestamp   : UTC time of event creation.
        vector      : optional embedding vector for semantic comparison.
        metadata    : arbitrary extra fields.
        importance  : static importance score [0, 1] assigned at creation time.
    """

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "GENERIC"
    content: str = ""
    source: str = "Unknown"
    timestamp: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    vector: list[float] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        """Serialize event to a plain dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "content": self.content[:200],
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "importance": self.importance,
            "metadata": self.metadata,
        }


# ---------------------------------------------------------------------------
# §4  CognitiveNode  (Layer B — Runtime Prototype: unified Node)
# ---------------------------------------------------------------------------


@dataclass
class CognitiveNode:
    """Canonical representation of a node in the cognitive graph.

    Maps to a MemoryEntry in memory_system.py — the scheduler constructs
    these lightweight objects from DB rows to avoid pulling full ORM objects
    into the scheduling loop.

    Attributes:
        node_id     : matches the integer primary key of the memory_entries table.
        content     : text content of this memory / concept.
        domain      : semantic domain label.
        relevance   : static relevance [0, 1] assigned at creation.
        activation  : live activation score computed by the attention formula.
        state       : memory lifecycle state (Active / Fading / Consolidated / Archived).
        layer       : memory layer (L1-Gems … L5-Meta).
        tags        : classification tags.
        created_at  : UTC creation timestamp.
        last_access : most recent retrieval timestamp (used for recency score).
        usage_count : number of times this node has been accessed.
    """

    node_id: int = -1
    content: str = ""
    domain: str = "GeneralKnowledge"
    relevance: float = 0.5
    activation: float = 0.5
    state: str = "Active"
    layer: int = 2
    tags: list[str] = field(default_factory=list)
    created_at: datetime.datetime | None = None
    last_access: datetime.datetime | None = None
    usage_count: int = 0

    def compute_attention(
        self,
        novelty: float = 0.5,
        importance_override: float | None = None,
    ) -> float:
        """PAD-SIP attention formula: activation = relevance x recency x novelty x importance.

        Args:
            novelty             : novelty score from CognitiveState (0-1).
            importance_override : if provided, overrides self.relevance as importance.

        Returns:
            float: Computed attention score clamped to [0, 1].
        """
        importance = importance_override if importance_override is not None else self.relevance
        recency = self.recency_score()
        raw = self.relevance * recency * novelty * importance
        # Normalize: since each factor is [0,1], product can be tiny - scale by sqrt
        # to keep scores in a usable range without distorting the ranking order.
        normalized = float(min(1.0, raw**0.25))
        self.activation = normalized
        return normalized

    def recency_score(self, half_life_days: float = 30.0) -> float:
        """Exponential decay recency: 1.0 = just accessed, ~0.5 at half_life_days.

        Returns:
            float: Recency score in [0, 1].
        """
        ref = self.last_access or self.created_at
        if ref is None:
            return 0.5
        if ref.tzinfo is None:
            ref = ref.replace(tzinfo=datetime.UTC)
        delta = datetime.datetime.now(datetime.UTC) - ref
        days = delta.days + delta.seconds / 86_400.0
        return float(max(0.0, 0.5 ** (days / half_life_days)))


# ---------------------------------------------------------------------------
# §5  CognitiveEdge  (Layer B — Runtime Prototype: unified Edge)
# ---------------------------------------------------------------------------


@dataclass
class CognitiveEdge:
    """Canonical representation of a directed edge in the cognitive graph.

    Maps to an association / soft-link between two memory entries.

    Attributes:
        edge_id     : unique identifier.
        source_id   : node_id of the source CognitiveNode.
        target_id   : node_id of the target CognitiveNode.
        rel_type    : relationship type label (e.g. "SIMILAR_TO", "CAUSED_BY").
        strength    : edge weight [0, 1].
        created_at  : UTC creation timestamp.
        metadata    : arbitrary extra fields.
    """

    edge_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_id: int = -1
    target_id: int = -1
    rel_type: str = "RELATED"
    strength: float = 0.5
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "rel_type": self.rel_type,
            "strength": self.strength,
        }


# ---------------------------------------------------------------------------
# §6  CognitiveGraph  (Layer B — Runtime Prototype: unified graph)
# ---------------------------------------------------------------------------


@dataclass
class CognitiveGraph:
    """In-memory working set of active nodes and edges for a single scheduler tick.

    The CognitiveScheduler rebuilds this from the storage layer at the start
    of each tick's Λ phase, so it is always a fresh projection of persistent
    memory state.

    Attributes:
        nodes   : mapping of node_id → CognitiveNode.
        edges   : list of CognitiveEdge objects connecting nodes.
        tick_id : tick counter at graph construction time.
    """

    nodes: dict[int, CognitiveNode] = field(default_factory=dict)
    edges: list[CognitiveEdge] = field(default_factory=list)
    tick_id: int = 0

    def add_node(self, node: CognitiveNode) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, edge: CognitiveEdge) -> None:
        self.edges.append(edge)

    def get_node(self, node_id: int) -> CognitiveNode | None:
        return self.nodes.get(node_id)

    def active_count(self) -> int:
        return sum(1 for n in self.nodes.values() if n.state not in ["Archived"])

    def pressure(self, capacity: int = 10_000) -> float:
        """Returns memory pressure as active_count / capacity, capped at 1.0."""
        return min(1.0, self.active_count() / max(1, capacity))

    def top_nodes(self, k: int = 10) -> list[CognitiveNode]:
        """Returns the k nodes with the highest current activation scores."""
        return sorted(self.nodes.values(), key=lambda n: n.activation, reverse=True)[:k]


# ---------------------------------------------------------------------------
# §7  Public re-exports
# ---------------------------------------------------------------------------

__all__ = [
    "CognitiveEdge",
    "CognitiveEvent",
    "CognitiveGraph",
    "CognitiveNode",
    "CognitivePhase",
    "CognitiveState",
    "MemoryPressureLevel",
]
