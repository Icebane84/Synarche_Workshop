"""ID: TEST-NLP-001
Status: DRAFT
Objective: Verify Phase 1 Core Cognition port and Magician Efficiency logic.
"""

import os
import sys
import unittest

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.logic.nlp.nlp_engine import AxionCognition


class TestNLPEngine(unittest.TestCase):
    def setUp(self):
        self.cognition = AxionCognition()

    def test_magician_efficiency_omega(self):
        """Test that 'Omega' intent boosts efficiency."""
        text = "This is an OMEGA level catalyst for the Synarche."
        efficiency = self.cognition.get_magician_efficiency(text)
        self.assertGreaterEqual(efficiency, 1.8)  # 1.0 + 0.5 (omega) + 0.3 (catalyst)

    def test_magician_efficiency_ambiguous(self):
        """Test that short questions penalize efficiency."""
        text = "What is this?"
        efficiency = self.cognition.get_magician_efficiency(text)
        self.assertLess(efficiency, 1.0)

    def test_detection_loop(self):
        """Test the full process loop includes the efficiency stat."""
        text = "Manifest the solution."
        result = self.cognition.process(text)
        self.assertIn("magician_efficiency", result)
        self.assertEqual(
            result["magician_efficiency"], 1.4
        )  # 1.0 + 0.2 (manifest) + 0.2 (solve)


if __name__ == "__main__":
    unittest.main()
