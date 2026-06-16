"""
artifact_anchor:
  id: CORE.COGNITIVE_SCHEDULER.001
  version: v15.0 [OMEGA]
  provenance: '2026-06-09'
  domain: CORE
  celestial_class: STAR
  tier: SCHEDULING
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-COGSCHED-001`            | The Sovereign ID. |
| **Official Name**   | `cognitive_scheduler.py`      | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG`                         | The Subject.      |
| **Celestial Class** | `[STAR]`                      | The Weight.       |
| **Evolution**       | `PAD-SIP Layer D`             | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |
# Cognitive Load Cost: High

**The Spirit Bomb Axiom: The Eternal Loop (Law 07)**
> Implemented from Blueprint `PAD-SIP.Layer.D.CognitiveScheduler`.
> Ethos: Every cycle of thought refines the next.
"""

import asyncio
import datetime as _dt
import logging
import time
from typing import Any, Callable, Dict, List, Optional

from .types import (
    CognitiveEdge,
    CognitiveEvent,
    CognitiveGraph,
    CognitiveNode,
    CognitivePhase,
    CognitiveState,
    MemoryPressureLevel,
)

logger = logging.getLogger("PhoenixLogger")

# ---------------------------------------------------------------------------
# §1  Stage type alias
# ---------------------------------------------------------------------------

# A stage function receives (CognitiveState, CognitiveEvent | None, CognitiveGraph)
# and returns an updated CognitiveGraph (may be unchanged).
StageFn = Callable[[CognitiveState, Optional[CognitiveEvent], CognitiveGraph], CognitiveGraph]


# ---------------------------------------------------------------------------
# §2  CognitiveScheduler
# ---------------------------------------------------------------------------


class CognitiveScheduler:
    """The master cognitive tick loop for the Axion PAD-SIP operating system.

    Implements the governed recursive pipeline defined in PAD-SIP Layer D:

        E → Φ → Ψ → G → Π → Ω → τ → Λ → Γ → (back to E)

    Where:
        E  — Experience ingestion (ingest_event)
        Φ  — Metaphor encoding    (MemoryWeaverAgent / encode stage)
        Ψ  — Semantic expansion   (LoomParser / expand stage)
        G  — Governance DSL       (GovernanceEngine.evaluate)
        Π  — Pattern mining       (Synergy / ResonanceAuditor)
        Ω  — Action selection     (CoherentSynthesisEngine)
        τ  — Tool execution       (McpInjector)
        Λ  — Memory loom          (MemorySystem reinforce / decay)
        Γ  — Bias update          (EmotionAnalyzer / novelty feedback)

    Each stage is a pluggable callable (StageFn) wired at initialisation.
    The scheduler can run:
        - synchronously via run_tick(event)  — single-pass execution.
        - as an async background loop via start_loop() / stop_loop().

    Governance verdicts produced in the G phase are stored on CognitiveState
    and can halt or modify later phases (e.g. gate_non_critical_actions prevents
    the Ω phase from executing low-priority actions).

    Memory pressure is computed from the graph at the start of every tick and
    triggers the maintenance cycle automatically at >= 0.75 (PAD-SIP GOV-002).

    Usage::

        scheduler = CognitiveScheduler()
        scheduler.register_stage(CognitivePhase.ENCODE, my_encoder)
        ...
        result = scheduler.run_tick(event)
    """

    # Max active-node capacity used for pressure calculation
    CAPACITY = 10_000

    def __init__(
        self,
        memory_system: Optional[Any] = None,
        governance_engine: Optional[Any] = None,
        loom_parser: Optional[Any] = None,
        mcp_injector: Optional[Any] = None,
        action_engine: Optional[Any] = None,
        emotion_analyzer: Optional[Any] = None,
        memory_weaver: Optional[Any] = None,
        synergy_engine: Optional[Any] = None,
    ) -> None:
        """Initialise the scheduler with pluggable sub-component references.

        All arguments are optional so the scheduler can operate in degraded
        mode (executing only the stages that have registered callables).

        Args:
            memory_system      : MemorySystem instance (Λ phase).
            governance_engine  : GovernanceEngine instance (G phase).
            loom_parser        : LoomParser instance (Ψ phase).
            mcp_injector       : McpInjector instance (τ phase).
            action_engine      : CoherentSynthesisEngine instance (Ω phase).
            emotion_analyzer   : EmotionAnalyzer instance (Γ phase).
            memory_weaver      : MemoryWeaverAgent instance (Φ phase).
            synergy_engine     : Synergy / pattern engine instance (Π phase).
        """
        # Sub-system references
        self.memory_system = memory_system
        self.governance_engine = governance_engine
        self.loom_parser = loom_parser
        self.mcp_injector = mcp_injector
        self.action_engine = action_engine
        self.emotion_analyzer = emotion_analyzer
        self.memory_weaver = memory_weaver
        self.synergy_engine = synergy_engine

        # Live cognitive state
        self.state = CognitiveState()

        # Stage registry: phase → callable
        self._stages: Dict[CognitivePhase, StageFn] = {}

        # Event queue for continuous-loop mode.
        # Constructed lazily inside start_loop() so __init__ stays event-loop-agnostic
        # (asyncio.Queue() in __init__ raises DeprecationWarning in Python 3.10+ and
        # an error in 3.12+ when no running event loop exists at construction time).
        self._event_queue: Optional[asyncio.Queue] = None
        self._running: bool = False

        # Wire built-in stages
        self._register_builtin_stages()

        logger.info("[COG-SCHED] CognitiveScheduler initialised.")

    # ------------------------------------------------------------------
    # §2.1  Stage registration
    # ------------------------------------------------------------------

    def register_stage(self, phase: CognitivePhase, fn: StageFn) -> None:
        """Bind a custom callable to a cognitive phase, overriding any existing one.

        Args:
            phase : the CognitivePhase to bind.
            fn    : a StageFn callable.
        """
        self._stages[phase] = fn
        logger.debug(f"[COG-SCHED] Stage registered for phase {phase.name}: {fn.__name__}")

    def _register_builtin_stages(self) -> None:
        """Wire default stage implementations using injected sub-systems."""
        self._stages[CognitivePhase.EXPERIENCE] = self._stage_experience
        self._stages[CognitivePhase.ENCODE] = self._stage_encode
        self._stages[CognitivePhase.EXPAND] = self._stage_expand
        self._stages[CognitivePhase.GOVERN] = self._stage_govern
        self._stages[CognitivePhase.PATTERN] = self._stage_pattern
        self._stages[CognitivePhase.ACT] = self._stage_act
        self._stages[CognitivePhase.TOOL] = self._stage_tool
        self._stages[CognitivePhase.REMEMBER] = self._stage_remember
        self._stages[CognitivePhase.BIAS] = self._stage_bias

    # ------------------------------------------------------------------
    # §2.2  Graph hydration
    # ------------------------------------------------------------------

    def _build_graph(self) -> CognitiveGraph:
        """Construct a fresh CognitiveGraph from the MemorySystem storage.

        Returns:
            CognitiveGraph: A snapshot of all non-archived memory entries.
        """
        graph = CognitiveGraph(tick_id=self.state.tick_count)
        if not self.memory_system or not self.memory_system.storage:
            return graph

        try:
            rows = self.memory_system.storage.get_all_active()
            for row in rows:
                def _parse_dt(val: Any) -> Optional[_dt.datetime]:
                    if isinstance(val, _dt.datetime):
                        return val
                    if isinstance(val, str):
                        try:
                            return _dt.datetime.fromisoformat(val.replace("Z", "+00:00"))
                        except ValueError:
                            return None
                    return None

                node = CognitiveNode(
                    node_id=row.get("id", -1),
                    content=row.get("content", ""),
                    domain=row.get("domain", "GeneralKnowledge"),
                    relevance=float(row.get("relevance", 0.5)),
                    activation=float(row.get("activation_score", 0.5)),
                    state=row.get("state", "Active"),
                    layer=int(row.get("memory_layer", 2)),
                    tags=row.get("tags") if isinstance(row.get("tags"), list) else [],
                    created_at=_parse_dt(row.get("created_at")),
                    last_access=_parse_dt(row.get("last_retrieved")),
                    usage_count=int(row.get("usage_count", 0)),
                )
                graph.add_node(node)
        except Exception:
            logger.exception("[COG-SCHED] Graph hydration failed — continuing with empty graph")

        return graph

    # ------------------------------------------------------------------
    # §2.3  Built-in stage implementations
    # ------------------------------------------------------------------

    def _stage_experience(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """E — Experience ingestion.  Validates and registers the incoming event."""
        if event is None:
            logger.debug("[E] No event this tick.")
            return graph
        state.last_event = event
        state.consume_attention(0.05)
        logger.info(f"[E] Event ingested: type={event.event_type} source={event.source}")
        return graph

    def _stage_encode(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """Φ — Metaphor encoding.  Structures the raw event via MemoryWeaverAgent."""
        if not event or not self.memory_weaver:
            return graph
        try:
            # Run async encoder synchronously if we're in a sync context
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.memory_weaver.weave_log_entry(event.content))
            else:
                loop.run_until_complete(self.memory_weaver.weave_log_entry(event.content))
            state.consume_attention(0.10)
            logger.debug("[Φ] Metaphor encoding complete.")
        except Exception:
            logger.exception("[Φ] Metaphor encoding failed — continuing.")
        return graph

    def _stage_expand(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """Ψ — Semantic loom expansion.  Enriches the event in the ontology graph."""
        if not event or not self.loom_parser:
            return graph
        try:
            # LoomParser may expose parse_file or parse_content; use whatever is available
            if hasattr(self.loom_parser, "parse_content"):
                self.loom_parser.parse_content(event.content)
            state.consume_attention(0.10)
            logger.debug("[Ψ] Semantic expansion complete.")
        except Exception:
            logger.exception("[Ψ] Semantic expansion failed — continuing.")
        return graph

    def _stage_govern(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """G — Governance DSL evaluation.  Fires rules against the current state."""
        if not self.governance_engine:
            return graph
        try:
            ctx = state.to_dict()
            # Add event-level fields for rule evaluation
            if event:
                ctx["event_type"] = event.event_type
                ctx["action_risk_score"] = event.metadata.get("risk_score", 0.0)
            verdicts = self.governance_engine.evaluate(ctx)
            state.governance_verdicts = [v.to_dict() for v in verdicts]

            # Apply governance effects inline
            for verdict in verdicts:
                effect = verdict.effect
                if effect == "trigger_maintenance_cycle" and self.memory_system:
                    logger.info("[G] GOV triggered maintenance cycle.")
                    self.memory_system.maintenance_cycle()
                elif effect == "trigger_pattern_mine":
                    state.pattern_hits.append({"trigger": "overflow_pressure"})
                    logger.info("[G] GOV triggered pattern mine.")
                elif effect in ("flag_contradiction", "flag_dissonance"):
                    logger.warning(f"[G] GOV flag: {effect} | novelty={state.novelty_score:.3f}")
                elif effect == "gate_non_critical_actions":
                    logger.info("[G] Attention budget gate: non-critical actions blocked.")
                elif effect == "block_action":
                    logger.warning("[G] GOV blocked action due to high risk score.")

            state.consume_attention(0.05)
        except Exception:
            logger.exception("[G] Governance evaluation failed — continuing.")
        return graph

    def _stage_pattern(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """Π — Pattern mining.  Runs synergy detection on the active graph.

        Automatically triggered when memory pressure >= CRITICAL (0.75).
        """
        # Only run pattern mining if pressure is elevated or GOV requested it
        should_mine = (
            state.pressure_level in (MemoryPressureLevel.CRITICAL, MemoryPressureLevel.OVERFLOW)
            or any(h.get("trigger") == "overflow_pressure" for h in state.pattern_hits)
        )
        if not should_mine:
            logger.debug("[Π] Pattern mine skipped (pressure nominal).")
            return graph

        if not self.synergy_engine:
            logger.debug("[Π] No synergy engine registered.")
            return graph

        try:
            if hasattr(self.synergy_engine, "detect"):
                hits = self.synergy_engine.detect(graph.nodes)
                if hits:
                    state.pattern_hits.extend(hits)
                    logger.info(f"[Π] {len(hits)} synergy pattern(s) found.")
            state.consume_attention(0.15)
        except Exception:
            logger.exception("[Π] Pattern mining failed — continuing.")
        return graph

    def _stage_act(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """Ω — Action selection & execution."""
        # Governance gate: skip if budget too low
        if state.attention_budget < 0.15:
            logger.info("[Ω] Attention budget exhausted — action skipped.")
            return graph

        if not self.action_engine:
            return graph
        try:
            if hasattr(self.action_engine, "select_action"):
                self.action_engine.select_action(state, event)
            state.consume_attention(0.20)
            logger.debug("[Ω] Action stage complete.")
        except Exception:
            logger.exception("[Ω] Action stage failed — continuing.")
        return graph

    def _stage_tool(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """τ — Tool / environment interaction via MCP injector."""
        if not self.mcp_injector or not event:
            return graph
        try:
            if hasattr(self.mcp_injector, "dispatch"):
                self.mcp_injector.dispatch(event.event_type, event.metadata)
            state.consume_attention(0.10)
            logger.debug("[τ] Tool stage complete.")
        except Exception:
            logger.exception("[τ] Tool stage failed — continuing.")
        return graph

    def _stage_remember(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """Λ — Memory loom: recompute attention scores, reinforce hot nodes, persist.

        Applies the full PAD-SIP attention formula:
            activation = relevance × recency × novelty × importance
        """
        # Recompute attention for all nodes in graph
        for node in graph.nodes.values():
            node.compute_attention(novelty=state.novelty_score)

        # Persist updated activation scores back to memory storage
        if self.memory_system and self.memory_system.storage:
            top = graph.top_nodes(k=20)
            try:
                ids = [n.node_id for n in top if n.node_id >= 0]
                if ids:
                    self.memory_system.storage.boost_access(ids)
                    logger.debug(f"[Λ] Reinforced {len(ids)} hot nodes.")
            except Exception:
                logger.exception("[Λ] Failed to reinforce nodes.")

        # Update active_nodes and pressure on state
        state.active_nodes = graph.active_count()
        state.memory_pressure = graph.pressure(capacity=self.CAPACITY)

        state.consume_attention(0.10)
        logger.debug(
            f"[Λ] Memory loom complete. active={state.active_nodes} "
            f"pressure={state.memory_pressure:.3f}"
        )
        return graph

    def _stage_bias(
        self,
        state: CognitiveState,
        event: Optional[CognitiveEvent],
        graph: CognitiveGraph,
    ) -> CognitiveGraph:
        """Γ — Metaphor bias generator: update novelty_score from emotional/semantic signal."""
        if not event:
            return graph
        try:
            if self.emotion_analyzer and hasattr(self.emotion_analyzer, "score_novelty"):
                novelty = self.emotion_analyzer.score_novelty(event.content, state.last_event)
                state.novelty_score = novelty
                logger.debug(f"[Γ] Novelty updated: {novelty:.3f}")
            else:
                # Default: decay novelty slightly each tick without fresh signal
                state.novelty_score = max(0.1, state.novelty_score * 0.95)
            state.consume_attention(0.05)
        except Exception:
            logger.exception("[Γ] Bias stage failed — continuing.")
        return graph

    # ------------------------------------------------------------------
    # §2.4  Tick execution
    # ------------------------------------------------------------------

    def run_tick(self, event: Optional[CognitiveEvent] = None) -> Dict[str, Any]:
        """Execute a single complete cognitive tick.

        Runs all 9 phases in sequence:  E → Φ → Ψ → G → Π → Ω → τ → Λ → Γ

        Args:
            event: The CognitiveEvent entering the pipeline this tick, or None.

        Returns:
            Dict: A snapshot of the CognitiveState after the tick completes.
        """
        self.state.reset_tick()
        graph = self._build_graph()

        phase_order = [
            CognitivePhase.EXPERIENCE,
            CognitivePhase.ENCODE,
            CognitivePhase.EXPAND,
            CognitivePhase.GOVERN,
            CognitivePhase.PATTERN,
            CognitivePhase.ACT,
            CognitivePhase.TOOL,
            CognitivePhase.REMEMBER,
            CognitivePhase.BIAS,
        ]

        for phase in phase_order:
            self.state.current_phase = phase
            stage_fn = self._stages.get(phase)
            if not stage_fn:
                continue
            t0 = time.perf_counter()
            try:
                graph = stage_fn(self.state, event, graph)
            except Exception:
                logger.exception(f"[COG-SCHED] Phase {phase.name} raised an unhandled exception.")
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self.state.phase_durations_ms[phase.name] = round(elapsed_ms, 2)

        snapshot = self.state.to_dict()
        logger.info(
            f"[COG-SCHED] Tick {self.state.tick_count} complete. "
            f"pressure={self.state.memory_pressure:.3f} "
            f"attention_remaining={self.state.attention_budget:.3f}"
        )
        return snapshot

    # ------------------------------------------------------------------
    # §2.5  Async continuous loop
    # ------------------------------------------------------------------

    async def start_loop(self, tick_interval_s: float = 1.0) -> None:
        """Run the cognitive scheduler as a continuous async background loop.

        Events can be pushed to the scheduler via push_event() while the loop
        is running.  If no event is available at tick time, the scheduler runs
        a maintenance-only tick (event=None).

        Args:
            tick_interval_s: seconds between ticks (default 1.0).
        """
        self._event_queue = asyncio.Queue()  # safe: we're inside an async context
        self._running = True
        logger.info(f"[COG-SCHED] Async loop started (interval={tick_interval_s}s).")
        while self._running:
            event: Optional[CognitiveEvent] = None
            if self._event_queue is not None:
                try:
                    event = self._event_queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass

            try:
                self.run_tick(event)
            except Exception:
                logger.exception("[COG-SCHED] Unhandled error in tick loop — continuing.")

            await asyncio.sleep(tick_interval_s)

        logger.info("[COG-SCHED] Async loop stopped.")

    def stop_loop(self) -> None:
        """Signal the async loop to stop after the current tick."""
        self._running = False

    async def push_event(self, event: CognitiveEvent) -> None:
        """Enqueue a CognitiveEvent for processing on the next available tick.

        Args:
            event: The CognitiveEvent to enqueue.

        Raises:
            RuntimeError: If called before :meth:`start_loop` has initialised the queue.
        """
        if self._event_queue is None:
            raise RuntimeError(
                "[COG-SCHED] push_event() called before start_loop() — "
                "the event queue has not been initialised."
            )
        await self._event_queue.put(event)
        logger.debug(f"[COG-SCHED] Event enqueued: {event.event_type}")

    # ------------------------------------------------------------------
    # §2.6  Introspection
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        """Return the current CognitiveState snapshot without advancing the tick."""
        return self.state.to_dict()

    def __repr__(self) -> str:
        return (
            f"<CognitiveScheduler tick={self.state.tick_count} "
            f"pressure={self.state.memory_pressure:.3f} "
            f"running={self._running}>"
        )
