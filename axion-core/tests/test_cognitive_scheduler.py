"""
artifact_anchor:
  id: TEST.COGNITIVE_SCHEDULER.001
  version: v15.0 [OMEGA]
  provenance: '2026-06-09'
  domain: TEST
  celestial_class: SATELLITE
  tier: TEST
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                                | Description       |
| :------------------ | :----------------------------------- | :---------------- |
| **Artifact ID**     | `TEST-COGSCHED-001`                  | The Sovereign ID. |
| **Official Name**   | `test_cognitive_scheduler.py`        | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**                    | The Standard.     |
| **Domain**          | `TEST`                               | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                        | The Weight.       |
| **Evolution**       | `PAD-SIP Integration Verification`  | The Maturity.     |
| **Status**          | `[ACTIVE]`                           | The Lifecycle.    |

**The Spirit Bomb Axiom: Verification Covenant (Law 54)**
> Every system claim must be provable.
> Ethos: Trust is validated, never assumed.
"""

import datetime
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Path resolution — make src importable from tests/
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

# ---------------------------------------------------------------------------
# §1  Type system tests
# ---------------------------------------------------------------------------

class TestCognitiveTypes(unittest.TestCase):
    """Validate the canonical PAD-SIP runtime types in engine/types.py."""

    def setUp(self):
        from engine.types import (
            CognitiveEdge,
            CognitiveEvent,
            CognitiveGraph,
            CognitiveNode,
            CognitivePhase,
            CognitiveState,
            MemoryPressureLevel,
        )
        self.CognitiveState = CognitiveState
        self.CognitiveEvent = CognitiveEvent
        self.CognitiveNode = CognitiveNode
        self.CognitiveEdge = CognitiveEdge
        self.CognitiveGraph = CognitiveGraph
        self.CognitivePhase = CognitivePhase
        self.MemoryPressureLevel = MemoryPressureLevel

    def test_cognitive_state_defaults(self):
        state = self.CognitiveState()
        self.assertEqual(state.active_nodes, 0)
        self.assertAlmostEqual(state.attention_budget, 1.0)
        self.assertAlmostEqual(state.memory_pressure, 0.0)
        self.assertAlmostEqual(state.novelty_score, 0.5)

    def test_pressure_level_nominal(self):
        state = self.CognitiveState(memory_pressure=0.3)
        self.assertEqual(state.pressure_level, self.MemoryPressureLevel.NOMINAL)

    def test_pressure_level_critical(self):
        state = self.CognitiveState(memory_pressure=0.80)
        self.assertEqual(state.pressure_level, self.MemoryPressureLevel.CRITICAL)

    def test_pressure_level_overflow(self):
        state = self.CognitiveState(memory_pressure=0.95)
        self.assertEqual(state.pressure_level, self.MemoryPressureLevel.OVERFLOW)

    def test_consume_attention_floored(self):
        state = self.CognitiveState(attention_budget=0.10)
        state.consume_attention(0.50)
        self.assertEqual(state.attention_budget, 0.0)

    def test_reset_tick_increments_counter(self):
        state = self.CognitiveState()
        state.reset_tick()
        self.assertEqual(state.tick_count, 1)
        state.reset_tick()
        self.assertEqual(state.tick_count, 2)

    def test_cognitive_event_uuid_unique(self):
        e1 = self.CognitiveEvent()
        e2 = self.CognitiveEvent()
        self.assertNotEqual(e1.event_id, e2.event_id)

    def test_cognitive_node_recency_recent(self):
        node = self.CognitiveNode(
            node_id=1,
            last_access=datetime.datetime.now(datetime.timezone.utc),
        )
        self.assertAlmostEqual(node.recency_score(), 1.0, places=1)

    def test_cognitive_node_recency_old(self):
        old_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
        node = self.CognitiveNode(node_id=2, last_access=old_time)
        # After 30 days (= 1 half-life), score should be ≈ 0.5
        self.assertAlmostEqual(node.recency_score(half_life_days=30.0), 0.5, places=2)

    def test_cognitive_node_compute_attention_formula(self):
        """Verify activation = relevance × recency × novelty × importance, quarter-root."""
        node = self.CognitiveNode(
            node_id=3,
            relevance=1.0,
            last_access=datetime.datetime.now(datetime.timezone.utc),  # recency ≈ 1.0
        )
        # With all factors = 1.0, raw = 1.0, score = 1.0
        score = node.compute_attention(novelty=1.0, importance_override=1.0)
        self.assertAlmostEqual(score, 1.0, places=2)

    def test_cognitive_node_compute_attention_zero_novelty(self):
        node = self.CognitiveNode(node_id=4, relevance=1.0)
        score = node.compute_attention(novelty=0.0)
        self.assertEqual(score, 0.0)

    def test_cognitive_graph_pressure(self):
        graph = self.CognitiveGraph()
        for i in range(500):
            graph.add_node(self.CognitiveNode(node_id=i, state="Active"))
        self.assertAlmostEqual(graph.pressure(capacity=1000), 0.5)

    def test_cognitive_graph_top_nodes(self):
        graph = self.CognitiveGraph()
        for i in range(10):
            graph.add_node(self.CognitiveNode(node_id=i, activation=float(i) / 10.0))
        top = graph.top_nodes(k=3)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].node_id, 9)  # highest activation


# ---------------------------------------------------------------------------
# §2  GovernanceEngine tests
# ---------------------------------------------------------------------------

class TestGovernanceEngine(unittest.TestCase):
    """Validate GovernanceEngine rule loading and evaluation."""

    def setUp(self):
        import importlib.util
        # Import governance_engine directly to avoid cse/__init__.py chain
        # (engine_v2 uses relative imports that fail in flat test context)
        gov_spec = importlib.util.spec_from_file_location(
            "governance_engine",
            str(REPO_ROOT / "src" / "cse" / "validators" / "governance_engine.py"),
        )
        gov_mod = importlib.util.module_from_spec(gov_spec)
        gov_spec.loader.exec_module(gov_mod)
        self.GovernanceEngine = gov_mod.GovernanceEngine
        self.GovernanceRule = gov_mod.GovernanceRule

    def test_loads_rules_from_default_path(self):
        engine = self.GovernanceEngine()
        self.assertGreater(len(engine.list_rules()), 0)

    def test_no_verdicts_on_nominal_state(self):
        engine = self.GovernanceEngine()
        ctx = {
            "active_nodes": 500,
            "memory_pressure": 0.3,
            "novelty_score": 0.5,
            "attention_budget": 0.9,
            "action_risk_score": 0.1,
        }
        verdicts = engine.evaluate(ctx)
        # Nominal context should fire no rules
        self.assertEqual(len(verdicts), 0)

    def test_memory_flood_rule_fires(self):
        engine = self.GovernanceEngine()
        ctx = {
            "active_nodes": 150_000,
            "memory_pressure": 0.3,
            "novelty_score": 0.5,
            "attention_budget": 0.9,
            "action_risk_score": 0.0,
        }
        verdicts = engine.evaluate(ctx)
        effects = [v.effect for v in verdicts]
        self.assertIn("reject_memory_write", effects)

    def test_memory_pressure_triggers_maintenance(self):
        engine = self.GovernanceEngine()
        ctx = {
            "active_nodes": 100,
            "memory_pressure": 0.80,
            "novelty_score": 0.5,
            "attention_budget": 0.9,
            "action_risk_score": 0.0,
        }
        verdicts = engine.evaluate(ctx)
        effects = [v.effect for v in verdicts]
        self.assertIn("trigger_maintenance_cycle", effects)

    def test_attention_budget_gate_fires(self):
        engine = self.GovernanceEngine()
        ctx = {
            "active_nodes": 100,
            "memory_pressure": 0.1,
            "novelty_score": 0.5,
            "attention_budget": 0.05,
            "action_risk_score": 0.0,
        }
        verdicts = engine.evaluate(ctx)
        effects = [v.effect for v in verdicts]
        self.assertIn("gate_non_critical_actions", effects)

    def test_unsafe_action_blocked(self):
        engine = self.GovernanceEngine()
        ctx = {
            "active_nodes": 100,
            "memory_pressure": 0.1,
            "novelty_score": 0.5,
            "attention_budget": 0.9,
            "action_risk_score": 0.90,
        }
        verdicts = engine.evaluate(ctx)
        effects = [v.effect for v in verdicts]
        self.assertIn("block_action", effects)

    def test_runtime_rule_registration(self):
        engine = self.GovernanceEngine()
        rule = self.GovernanceRule(
            rule_id="TEST-001",
            name="test_rule",
            description="Test rule",
            field="active_nodes",
            op="gt",
            value=5,
            effect="test_effect",
            priority=1,
        )
        engine.register_rule(rule)
        ctx = {"active_nodes": 10}
        verdicts = engine.evaluate(ctx)
        self.assertTrue(any(v.effect == "test_effect" for v in verdicts))

    def test_effect_handler_binding(self):
        engine = self.GovernanceEngine()
        handler_called = []
        engine.register_effect_handler("test_effect", lambda s: handler_called.append(True))
        handler = engine.get_effect_handler("test_effect")
        self.assertIsNotNone(handler)
        handler(None)
        self.assertTrue(handler_called)


# ---------------------------------------------------------------------------
# §3  CognitiveScheduler tick loop tests
# ---------------------------------------------------------------------------

class TestCognitiveScheduler(unittest.TestCase):
    """Validate the CognitiveScheduler tick mechanics."""

    def setUp(self):
        from engine.cognitive_scheduler import CognitiveScheduler
        from engine.types import CognitiveEvent, CognitivePhase, MemoryPressureLevel
        self.CognitiveScheduler = CognitiveScheduler
        self.CognitiveEvent = CognitiveEvent
        self.CognitivePhase = CognitivePhase
        self.MemoryPressureLevel = MemoryPressureLevel

    def test_tick_increments_count(self):
        scheduler = self.CognitiveScheduler()
        scheduler.run_tick()
        self.assertEqual(scheduler.state.tick_count, 1)
        scheduler.run_tick()
        self.assertEqual(scheduler.state.tick_count, 2)

    def test_tick_records_phase_durations(self):
        scheduler = self.CognitiveScheduler()
        result = scheduler.run_tick()
        # All 9 phase names should have a recorded duration
        self.assertIn("EXPERIENCE", scheduler.state.phase_durations_ms)
        self.assertIn("REMEMBER", scheduler.state.phase_durations_ms)
        self.assertIn("BIAS", scheduler.state.phase_durations_ms)

    def test_event_passes_through_experience_phase(self):
        scheduler = self.CognitiveScheduler()
        event = self.CognitiveEvent(event_type="TEST_EVENT", content="hello world")
        scheduler.run_tick(event)
        self.assertEqual(scheduler.state.last_event.event_type, "TEST_EVENT")

    def test_snapshot_returns_dict(self):
        scheduler = self.CognitiveScheduler()
        snap = scheduler.snapshot()
        self.assertIsInstance(snap, dict)
        self.assertIn("tick", snap)
        self.assertIn("memory_pressure", snap)
        self.assertIn("novelty_score", snap)

    def test_attention_budget_consumed_each_tick(self):
        scheduler = self.CognitiveScheduler()
        scheduler.run_tick(self.CognitiveEvent(content="test"))
        # Each active stage costs attention — budget should be < 1.0
        self.assertLess(scheduler.state.attention_budget, 1.0)

    def test_governance_gating_skips_act_on_low_budget(self):
        """When attention budget < 0.15, the Ω stage should be skipped."""
        scheduler = self.CognitiveScheduler()
        action_called = []

        mock_action = MagicMock()
        mock_action.select_action = lambda s, e: action_called.append(True)
        scheduler.action_engine = mock_action

        # Force attention budget below threshold before Ω runs
        scheduler.state.attention_budget = 0.05
        scheduler.state.tick_count = 1  # prevent reset_tick from restoring it

        # Run just the act stage
        from engine.types import CognitiveGraph
        scheduler._stage_act(scheduler.state, None, CognitiveGraph())
        # Should not have called select_action
        self.assertEqual(len(action_called), 0)

    def test_custom_stage_override(self):
        """A user-registered stage function should replace the built-in."""
        from engine.types import CognitiveGraph, CognitivePhase
        scheduler = self.CognitiveScheduler()
        calls = []

        def custom_experience(state, event, graph):
            calls.append("custom_E")
            return graph

        scheduler.register_stage(CognitivePhase.EXPERIENCE, custom_experience)
        scheduler.run_tick()
        self.assertIn("custom_E", calls)


# ---------------------------------------------------------------------------
# §4  ScaffoldWeaver tests
# ---------------------------------------------------------------------------

class TestScaffoldWeaver(unittest.TestCase):
    """Validate ScaffoldWeaver stub generation and registry management."""

    def setUp(self):
        from hephaestus.lib.scaffold_weaver import ScaffoldWeaver
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.ScaffoldWeaver = ScaffoldWeaver
        self.weaver = ScaffoldWeaver(root_dir=self.tmpdir)

    def test_weave_creates_file(self):
        pointer = self.weaver.weave(
            name="TestComponent",
            target_path="src/test_stub.py",
            artifact_id="TEST.STUB.001",
            description="Test stub",
            stub_type="class",
            domain="TEST",
        )
        stub_path = Path(self.tmpdir) / "src" / "test_stub.py"
        self.assertTrue(stub_path.exists())
        self.assertIn("STUB-TEST-001", pointer.pointer_id)

    def test_registry_persisted_to_disk(self):
        self.weaver.weave(
            name="AnotherComponent",
            target_path="src/another.py",
            artifact_id="TEST.STUB.002",
            stub_type="function",
            domain="LOGIC",
        )
        registry_path = Path(self.tmpdir) / "data" / "scaffold_registry.json"
        self.assertTrue(registry_path.exists())
        with open(registry_path) as f:
            data = json.load(f)
        self.assertEqual(len(data["stubs"]), 1)

    def test_mark_filled(self):
        pointer = self.weaver.weave(
            name="FillableClass",
            target_path="src/fillable.py",
            artifact_id="TEST.STUB.003",
            domain="CORE",
        )
        self.assertEqual(pointer.status, "pending")
        result = self.weaver.mark_filled(pointer.pointer_id)
        self.assertTrue(result)
        self.assertEqual(self.weaver.get_by_id(pointer.pointer_id).status, "filled")

    def test_get_pending_returns_only_pending(self):
        p1 = self.weaver.weave(
            name="P1", target_path="src/p1.py", artifact_id="T.P1", domain="A"
        )
        p2 = self.weaver.weave(
            name="P2", target_path="src/p2.py", artifact_id="T.P2", domain="A"
        )
        self.weaver.mark_filled(p1.pointer_id)
        pending = self.weaver.get_pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].pointer_id, p2.pointer_id)

    def test_registry_report(self):
        self.weaver.weave(
            name="R1", target_path="src/r1.py", artifact_id="T.R1", domain="A"
        )
        self.weaver.weave(
            name="R2", target_path="src/r2.py", artifact_id="T.R2", domain="A"
        )
        self.weaver.mark_filled(self.weaver.get_pending()[0].pointer_id)
        report = self.weaver.registry_report()
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["filled"], 1)
        self.assertAlmostEqual(report["completion_pct"], 50.0)


# ---------------------------------------------------------------------------
# §5  TransclusionBinder tests
# ---------------------------------------------------------------------------

class TestTransclusionBinder(unittest.TestCase):
    """Validate TransclusionBinder token resolution."""

    def setUp(self):
        from hephaestus.lib.transclusion_binder import TransclusionBinder
        from hephaestus.lib.scaffold_weaver import ScaffoldWeaver
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.TransclusionBinder = TransclusionBinder

        # Pre-populate a stub so the pointer resolver has something to find
        weaver = ScaffoldWeaver(root_dir=self.tmpdir)
        self.pointer = weaver.weave(
            name="TestResolvable",
            target_path="src/resolvable.py",
            artifact_id="TEST.RES.001",
            domain="TEST",
        )
        self.binder = TransclusionBinder(root_dir=self.tmpdir)

    def test_bind_document_no_tokens(self):
        text = "No tokens here."
        out, results = self.binder.bind_document(text)
        self.assertEqual(out, text)
        self.assertEqual(len(results), 0)

    def test_bind_alias_token(self):
        """[[alias:...]] should resolve a file relative to root."""
        # Write a file to resolve
        target = Path(self.tmpdir) / "docs" / "sample.md"
        target.parent.mkdir(exist_ok=True)
        target.write_text("# Sample Content")
        text = "[[alias:docs/sample.md]]"
        out, results = self.binder.bind_document(text)
        self.assertTrue(results[0].resolved)
        self.assertIn("Sample Content", out)

    def test_bind_unknown_alias_fails_gracefully(self):
        text = "[[alias:nonexistent/path.py]]"
        out, results = self.binder.bind_document(text)
        self.assertFalse(results[0].resolved)
        # Token kept in output on failure
        self.assertIn("[[alias:", out)

    def test_bind_pointer_token(self):
        """[[pointer:STUB-TEST-001]] should resolve to the stub file contents."""
        text = f"[[pointer:{self.pointer.pointer_id}]]"
        out, results = self.binder.bind_document(text)
        self.assertTrue(results[0].resolved)
        self.assertIn("STUB", out)

    def test_stats_returns_dict(self):
        stats = self.binder.stats()
        self.assertIn("pointer_count", stats)
        self.assertIn("root", stats)


# ---------------------------------------------------------------------------
# §6  MemoryEntry PAD-SIP attention formula tests
# ---------------------------------------------------------------------------

class TestMemoryEntryAttentionFormula(unittest.TestCase):
    """Validate the upgraded PAD-SIP attention formula in MemoryEntry."""

    def setUp(self):
        # Import MemoryEntry directly
        sys.path.insert(0, str(REPO_ROOT / "src" / "logic" / "memory"))
        from logic.memory.memory_system import MemoryEntry
        self.MemoryEntry = MemoryEntry

    def _make_entry(self, relevance=0.8):
        return self.MemoryEntry(
            id=1,
            content="test content",
            relevance=relevance,
            activation_score=0.5,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            last_retrieved=datetime.datetime.now(datetime.timezone.utc),
        )

    def test_decay_produces_score_in_range(self):
        entry = self._make_entry()
        entry.decay()
        self.assertGreaterEqual(entry.activation_score, 0.0)
        self.assertLessEqual(entry.activation_score, 1.0)

    def test_compute_attention_zero_novelty_gives_zero(self):
        entry = self._make_entry(relevance=1.0)
        score = entry.compute_attention(novelty=0.0, importance=1.0)
        self.assertEqual(score, 0.0)

    def test_compute_attention_max_inputs_gives_one(self):
        """All factors at 1.0 → product = 1.0 → score = 1.0."""
        entry = self._make_entry(relevance=1.0)
        score = entry.compute_attention(novelty=1.0, importance=1.0)
        self.assertAlmostEqual(score, 1.0, places=2)

    def test_attention_formula_static(self):
        score = self.MemoryEntry._attention_formula(1.0, 1.0, 1.0, 1.0)
        self.assertAlmostEqual(score, 1.0)

    def test_attention_formula_symmetry(self):
        """Formula is symmetric: swapping factors doesn't change the result."""
        a = self.MemoryEntry._attention_formula(0.8, 0.6, 0.5, 0.7)
        b = self.MemoryEntry._attention_formula(0.6, 0.8, 0.7, 0.5)
        self.assertAlmostEqual(a, b, places=6)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
