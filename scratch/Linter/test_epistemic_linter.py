# FILE: test_epistemic_linter.py
# PURPOSE: Sentinel Audit Array for SPELL-001 (Epistemic Linter)
#
# First 5 tests are Axion's original scenarios, unchanged.
# Tests 6-10 close gaps found in review: float tolerance, FAIL+lexical
# camouflage together, exception breadth, no-data-returned, and type
# mismatch — see the review notes for why each one matters.

import unittest
from epistemic_linter import EpistemicLinter


class TestEpistemicLinter(unittest.TestCase):
    def setUp(self):
        """Initialize the linter before each test."""
        self.linter = EpistemicLinter()

    # --- Axion's original 5 scenarios ---

    def test_unverified_no_reference(self):
        """SCENARIO 1: The system makes a claim without checking external reality."""
        result = self.linter.execute_spell(
            metric_name="phase_multiplier",
            asserted_value=1.05,
            log_context="Calculated phase multiplier.",
            reference_callback=None
        )
        self.assertEqual(result["STATUS"], "UNVERIFIED")
        self.assertEqual(result["TAG"], "[SELF-REPORTED]")
        self.assertEqual(result["METRIC"], "phase_multiplier")

    def test_unverified_callback_exception(self):
        """SCENARIO 2: The system attempts to check reality, but the bridge fails."""
        def broken_bridge_callback():
            raise ConnectionError("Port timeout.")

        result = self.linter.execute_spell(
            metric_name="boss_health_state",
            asserted_value=1000,
            log_context="Checking boss health.",
            reference_callback=broken_bridge_callback
        )
        self.assertEqual(result["STATUS"], "UNVERIFIED")
        self.assertEqual(result["TAG"], "[ATTEMPTED MEASUREMENT]")
        self.assertIn("Reference pointer execution failed", result["REASON"])

    def test_pass_matching_values(self):
        """SCENARIO 3: The system's claim perfectly aligns with physical memory."""
        def active_bridge_callback():
            return 42

        result = self.linter.execute_spell(
            metric_name="integrity_deviation_rate",
            asserted_value=42,
            log_context="Integrity holding steady.",
            reference_callback=active_bridge_callback
        )
        self.assertEqual(result["STATUS"], "PASS")
        self.assertEqual(result["TAG"], "[MEASURED]")
        self.assertEqual(result["ASSERTED"], result["GROUND_TRUTH"])

    def test_fail_silent_drift(self):
        """SCENARIO 4: The system's claim contradicts physical memory (Silent Drift)."""
        def active_bridge_callback():
            return 1.05  # Actual C++ Coefficient

        result = self.linter.execute_spell(
            metric_name="phase_multiplier",
            asserted_value=1.50,  # Hallucinated Python Multiplier
            log_context="Phase multiplier engaged.",
            reference_callback=active_bridge_callback
        )
        self.assertEqual(result["STATUS"], "FAIL")
        self.assertEqual(result["TAG"], "[MEASURED]")
        self.assertNotEqual(result["ASSERTED"], result["GROUND_TRUTH"])
        self.assertIn("Silent Drift Detected", result["REASON"])

    def test_lexical_guardrails(self):
        """SCENARIO 5: The system uses unquantifiable rhetorical armor."""
        def active_bridge_callback():
            return "Stable"

        result = self.linter.execute_spell(
            metric_name="system_state",
            asserted_value="Stable",
            log_context="The architecture is flawless and immune to errors.",
            reference_callback=active_bridge_callback
        )

        # The logic passes, but the lexicon must be flagged.
        self.assertEqual(result["STATUS"], "PASS")
        self.assertTrue(len(result["LEXICAL_VIOLATIONS"]) >= 2)

        violations_text = " ".join(result["LEXICAL_VIOLATIONS"])
        self.assertIn("flawless", violations_text)
        self.assertIn("immune", violations_text)

    # --- New: float tolerance ---

    def test_pass_within_float_tolerance(self):
        """SCENARIO 6: Real computation rarely produces bit-identical floats
        across a Python/C++ boundary. A near-equal value must still PASS,
        or every legitimate phase_multiplier check becomes a false FAIL."""
        def active_bridge_callback():
            return 1.0500000001  # effectively 1.05, differs in the 10th decimal

        result = self.linter.execute_spell(
            metric_name="phase_multiplier",
            asserted_value=1.05,
            log_context="Phase multiplier engaged.",
            reference_callback=active_bridge_callback
        )
        self.assertEqual(result["STATUS"], "PASS")
        self.assertEqual(result["TAG"], "[MEASURED]")

    # --- New: the dangerous combination the original 5 didn't cover ---

    def test_fail_with_lexical_camouflage(self):
        """SCENARIO 7: A genuinely wrong metric wrapped in confident,
        unfalsifiable language — the riskier case than SCENARIO 5's
        PASS+bad-language combination, since this is a real drift hiding
        behind rhetoric rather than just rhetoric on top of a true claim."""
        def active_bridge_callback():
            return 500  # actual measured boss health

        result = self.linter.execute_spell(
            metric_name="boss_health_state",
            asserted_value=1000,  # wrong — doesn't match live state
            log_context="Boss health synchronization is bulletproof and guaranteed accurate.",
            reference_callback=active_bridge_callback
        )
        self.assertEqual(result["STATUS"], "FAIL")
        self.assertIn("Silent Drift Detected", result["REASON"])
        self.assertTrue(len(result["LEXICAL_VIOLATIONS"]) >= 2)
        violations_text = " ".join(result["LEXICAL_VIOLATIONS"])
        self.assertIn("bulletproof", violations_text)
        self.assertIn("guaranteed", violations_text)

    # --- New: exception breadth ---

    def test_unverified_on_non_connection_exception(self):
        """SCENARIO 8: The bridge callback can fail in ways other than a
        ConnectionError. A malformed or unexpected bridge object should
        still degrade to UNVERIFIED, not crash execute_spell."""
        def malformed_bridge_callback():
            raise AttributeError("'NoneType' object has no attribute 'read'")

        result = self.linter.execute_spell(
            metric_name="frame_budget_ms",
            asserted_value=6.94,
            log_context="Checking frame budget.",
            reference_callback=malformed_bridge_callback
        )
        self.assertEqual(result["STATUS"], "UNVERIFIED")
        self.assertEqual(result["TAG"], "[ATTEMPTED MEASUREMENT]")
        self.assertIn("Reference pointer execution failed", result["REASON"])

    # --- New: reference ran but returned nothing ---

    def test_unverified_when_callback_returns_none(self):
        """SCENARIO 9: The bridge itself executes without error but has no
        data to give back. This is distinct from a hard failure and should
        be tagged as such rather than treated as a match or a drift."""
        def empty_bridge_callback():
            return None

        result = self.linter.execute_spell(
            metric_name="geometry_collections_fractured",
            asserted_value=4,
            log_context="Checking destruction telemetry.",
            reference_callback=empty_bridge_callback
        )
        self.assertEqual(result["STATUS"], "UNVERIFIED")
        self.assertEqual(result["TAG"], "[ATTEMPTED MEASUREMENT]")
        self.assertIn("returned no data", result["REASON"])

    # --- New: type mismatch, not just value mismatch ---

    def test_fail_on_type_mismatch(self):
        """SCENARIO 10: The claim and the ground truth aren't even the same
        kind of thing (e.g. a number asserted against a string state) —
        a distinct failure mode from a same-type value drift."""
        def active_bridge_callback():
            return "42"  # string, not int

        result = self.linter.execute_spell(
            metric_name="debris_actors_spawned",
            asserted_value=42,
            log_context="Checking debris count.",
            reference_callback=active_bridge_callback
        )
        self.assertEqual(result["STATUS"], "FAIL")
        self.assertIn("Type Mismatch Detected", result["REASON"])


if __name__ == "__main__":
    unittest.main()
