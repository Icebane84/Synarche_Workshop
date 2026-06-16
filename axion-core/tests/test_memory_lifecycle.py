import datetime
import os
import sys
import unittest

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from logic.memory.memory_system import MemoryEntry, MemoryProtocols


class TestMemoryLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.entry = MemoryEntry(
            id=1,
            content="Testing lifecycle",
            activation_score=1.0,
            relevance=0.9,
            usage_count=0,
            layer=MemoryProtocols.LAYER_KINETIC,
        )

    def test_decay_logic(self) -> None:
        # 1. Immediate retrieval (no decay)
        self.entry.last_retrieved = datetime.datetime.now(datetime.timezone.utc)
        self.entry.decay(base_rate=0.1)
        self.assertAlmostEqual(self.entry.activation_score, 1.0)

        # 2. Simulated decay (10 days)
        self.entry.last_retrieved = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=10)
        self.entry.decay(base_rate=0.1)
        self.assertLess(self.entry.activation_score, 1.0)
        self.assertGreater(self.entry.activation_score, 0.5)

    def test_transitions(self) -> None:
        # Active -> Fading
        self.entry.activation_score = 0.1  # Below THRESHOLD_FADING (0.2)
        self.entry.transition()
        self.assertEqual(self.entry.state, "Fading")

        # Fading -> Archived
        self.entry.activation_score = 0.02  # Below THRESHOLD_ARCHIVED (0.05)
        self.entry.transition()
        self.assertEqual(self.entry.state, "Archived")

        # Archived -> Active (Reactivation)
        self.entry.activation_score = 0.4  # Above THRESHOLD_REACTIVATE (0.3)
        self.entry.transition()
        self.assertEqual(self.entry.state, "Active")

    def test_elevation(self) -> None:
        # Consolidation & Elevation (L2 -> L3)
        self.entry.activation_score = 0.9  # Above THRESHOLD_CONSOLIDATED (0.8)
        self.entry.usage_count = 15  # Above MIN_USAGE_CONSOLIDATED (10)
        self.entry.layer = MemoryProtocols.LAYER_KINETIC
        self.entry.transition()
        self.assertEqual(self.entry.state, "Consolidated")
        self.assertEqual(self.entry.layer, MemoryProtocols.LAYER_SEMANTIC)


if __name__ == "__main__":
    unittest.main()
