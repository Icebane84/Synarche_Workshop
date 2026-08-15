# FILE: test_eve_engine.py
# PURPOSE: Regression suite for EVE — original behavior plus fixes for the
# 5 confirmed bugs found in review.

import datetime
import unittest

from eve_engine import (
    Evidence,
    Claim,
    EvidenceValidationEngine,
    EvidenceType,
    Truth,
    Confidence,
    NO_ASSERTION,
)


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)


class TestOriginalBehaviorPreserved(unittest.TestCase):
    """Confirms the hardening didn't change any of the correct original behavior."""

    def setUp(self):
        self.eve = EvidenceValidationEngine()

    def test_missing_evidence_is_unverified(self):
        claim = Claim(
            claim_id="MISSING.001",
            statement="Boss health synced.",
            required_evidence_types=[EvidenceType.TELEMETRY],
            provided_evidence=[],
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.UNVERIFIED.value)
        self.assertEqual(result["CONFIDENCE"], Confidence.NONE.value)
        self.assertIn("TELEMETRY", result["MISSING_PREREQUISITES"])

    def test_matching_value_passes(self):
        ev = Evidence(
            evidence_type=EvidenceType.TELEMETRY,
            timestamp=now_utc(),
            reference_callback=lambda: 42,
            asserted_value=42,
        )
        claim = Claim(
            claim_id="MATCH.001",
            statement="Debris count confirmed.",
            required_evidence_types=[EvidenceType.TELEMETRY],
            provided_evidence=[ev],
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.PASS.value)
        self.assertEqual(result["CONFIDENCE"], Confidence.MEASURED.value)

    def test_conflicting_evidence_is_conflict(self):
        ev_pass = Evidence(EvidenceType.UNIT_TEST, now_utc(), lambda: 10, asserted_value=10)
        ev_fail = Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: 5, asserted_value=10)
        claim = Claim(
            claim_id="CONFLICT.001",
            statement="Value agreed across sources.",
            required_evidence_types=[EvidenceType.UNIT_TEST, EvidenceType.TELEMETRY],
            provided_evidence=[ev_pass, ev_fail],
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.CONFLICT.value)

    def test_stale_evidence_is_stale(self):
        old_ts = now_utc() - datetime.timedelta(days=200)
        ev = Evidence(EvidenceType.TELEMETRY, old_ts, lambda: 42, asserted_value=42)
        claim = Claim(
            claim_id="STALE.001",
            statement="Old confirmed value.",
            required_evidence_types=[EvidenceType.TELEMETRY],
            provided_evidence=[ev],
            expiration_days=90,
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.STALE.value)

    def test_lexical_violations_still_flagged_alongside_pass(self):
        ev = Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: True)
        claim = Claim(
            claim_id="LEX.001",
            statement="The system is flawless and immune to error.",
            required_evidence_types=[EvidenceType.TELEMETRY],
            provided_evidence=[ev],
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.PASS.value)
        self.assertIn("flawless", result["LEXICAL_VIOLATIONS"])
        self.assertIn("immune", result["LEXICAL_VIOLATIONS"])


class TestBugFixes(unittest.TestCase):
    """One regression test per confirmed bug from the review."""

    def setUp(self):
        self.eve = EvidenceValidationEngine()

    def test_fix1_zero_is_a_valid_pass_not_a_falsy_fail(self):
        """Bug 1: error_count == 0 (the GOOD outcome) previously came back FAIL."""
        ev = Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: 0)  # no assertion, existence check
        result = ev.evaluate()
        self.assertEqual(result["STATUS"], Truth.PASS)
        self.assertIn("Existence confirmed", result["REASON"])

    def test_fix1_bool_false_still_correctly_fails(self):
        """Bug 1 fix must not overcorrect: a real boolean check returning
        False (e.g. 'did the test pass') must still FAIL."""
        ev = Evidence(EvidenceType.UNIT_TEST, now_utc(), lambda: False)
        result = ev.evaluate()
        self.assertEqual(result["STATUS"], Truth.FAIL)

    def test_fix2_empty_claim_raises_instead_of_silently_passing(self):
        """Bug 2: a Claim with no required evidence previously certified as
        PASS with nothing behind it."""
        with self.assertRaises(ValueError):
            Claim(
                claim_id="EMPTY.001",
                statement="The system is stable.",
                required_evidence_types=[],
                provided_evidence=[],
            )

    def test_fix3_confidence_not_gameable_by_repeating_cheap_evidence(self):
        """Bug 3: ten stacked UNIT_TEST entries (weight 1 each) previously
        summed to 10 and reached MEASURED — the same tier as one real
        TELEMETRY reading. Now confidence is based on evidence-type
        diversity, so repeating one cheap type stays capped at that type's
        own weight."""
        ten_unit_tests = [
            Evidence(EvidenceType.UNIT_TEST, now_utc(), lambda: True)
            for _ in range(10)
        ]
        claim = Claim(
            claim_id="GAMED.001",
            statement="Boss orchestrator is correct.",
            required_evidence_types=[EvidenceType.UNIT_TEST],
            provided_evidence=ten_unit_tests,
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.PASS.value)
        # UNIT_TEST alone has weight 1 -> LOW, regardless of repetition.
        self.assertEqual(result["CONFIDENCE"], Confidence.LOW.value)

    def test_fix3_real_diversity_still_reaches_measured(self):
        """Confirms the fix didn't just nerf confidence across the board —
        genuine evidence-type diversity should still be able to reach
        MEASURED."""
        evidence = [
            Evidence(EvidenceType.UNIT_TEST, now_utc(), lambda: True),
            Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: True),
        ]
        claim = Claim(
            claim_id="DIVERSE.001",
            statement="Boss orchestrator is correct.",
            required_evidence_types=[EvidenceType.UNIT_TEST, EvidenceType.TELEMETRY],
            provided_evidence=evidence,
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["CONFIDENCE"], Confidence.MEASURED.value)  # 1 + 10 = 11

    def test_fix4_naive_timestamp_rejected_at_construction(self):
        """Bug 4: a naive timestamp previously crashed certify_claim deep
        inside the staleness check with an uncaught TypeError. Now it's
        rejected immediately at Evidence construction."""
        naive_ts = datetime.datetime.now()  # no tzinfo
        with self.assertRaises(ValueError):
            Evidence(EvidenceType.TELEMETRY, naive_ts, lambda: 42, asserted_value=42)

    def test_fix5_none_is_a_real_assertable_value_not_just_the_default(self):
        """Bug 5: asserted_value=None previously meant 'no assertion was
        made,' so you could never legitimately assert the ground truth
        should be None. NO_ASSERTION is now the explicit sentinel for
        that, freeing up None as a real value."""
        # A real assertion of None, evaluated on its own terms:
        ev_explicit_none = Evidence(
            EvidenceType.UNIT_TEST, now_utc(), lambda: "not none", asserted_value=None
        )
        result = ev_explicit_none.evaluate()
        # Type mismatch: asserted None (NoneType) vs a string ground truth.
        self.assertEqual(result["STATUS"], Truth.FAIL)
        self.assertEqual(result["REASON"], "Type Mismatch")

        # Confirm the sentinel itself still means "no assertion":
        ev_no_assertion = Evidence(
            EvidenceType.UNIT_TEST, now_utc(), lambda: "anything", asserted_value=NO_ASSERTION
        )
        result2 = ev_no_assertion.evaluate()
        self.assertEqual(result2["STATUS"], Truth.PASS)
        self.assertIn("Existence confirmed", result2["REASON"])

    def test_strict_veto_policy_default_true(self):
        """One UNVERIFIED evidence item vetoes the whole claim by default,
        even with other evidence passing — documented, not accidental."""
        evidence = [
            Evidence(EvidenceType.UNIT_TEST, now_utc(), lambda: True, asserted_value=True),
            Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: (_ for _ in ()).throw(ConnectionError("down"))),
        ]
        claim = Claim(
            claim_id="VETO.001",
            statement="System is healthy.",
            required_evidence_types=[EvidenceType.UNIT_TEST, EvidenceType.TELEMETRY],
            provided_evidence=evidence,
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.UNVERIFIED.value)

    def test_strict_veto_policy_can_be_disabled(self):
        """With strict_veto_on_unverified=False, the passing evidence is
        still certifiable and the excluded count is reported."""
        evidence = [
            Evidence(EvidenceType.UNIT_TEST, now_utc(), lambda: True, asserted_value=True),
            Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: (_ for _ in ()).throw(ConnectionError("down"))),
        ]
        claim = Claim(
            claim_id="VETO.002",
            statement="System is healthy.",
            required_evidence_types=[EvidenceType.UNIT_TEST],
            provided_evidence=evidence,
            strict_veto_on_unverified=False,
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.PASS.value)
        self.assertEqual(result["EXCLUDED_UNVERIFIED_COUNT"], 1)

    def test_unverified_filtering_rechecks_burden_of_proof(self):
        """Disabling strict veto should still require successful execution
        of required evidence types. If the required type crashes (UNVERIFIED)
        and gets filtered out, the claim must fail certification as UNVERIFIED."""
        evidence = [
            # TELEMETRY is required, but crashes:
            Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: (_ for _ in ()).throw(ConnectionError("down"))),
        ]
        claim = Claim(
            claim_id="POST_FILTER.001",
            statement="System telemetry confirmed.",
            required_evidence_types=[EvidenceType.TELEMETRY],
            provided_evidence=evidence,
            strict_veto_on_unverified=False,
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.UNVERIFIED.value)
        self.assertIn("TELEMETRY", result["MISSING_PREREQUISITES"])
        self.assertIn("Burden of Proof failed", result["REASON"])

    def test_lexical_violation_caps_confidence_to_low(self):
        """Any claim carrying lexical blocklist violations must have its
        computed confidence capped at Confidence.LOW, even if the evidence
        is otherwise sufficient for MEASURED/HIGH."""
        evidence = [
            Evidence(EvidenceType.UNIT_TEST, now_utc(), lambda: True),
            Evidence(EvidenceType.TELEMETRY, now_utc(), lambda: True),
        ]
        claim = Claim(
            claim_id="LEX_CAP.001",
            # Statement contains 'flawless':
            statement="The system has flawless telemetry logs.",
            required_evidence_types=[EvidenceType.UNIT_TEST, EvidenceType.TELEMETRY],
            provided_evidence=evidence,
        )
        result = self.eve.certify_claim(claim)
        self.assertEqual(result["TRUTH_STATUS"], Truth.PASS.value)
        # Normally 1 + 10 = 11 -> MEASURED. Capped here to LOW due to 'flawless'.
        self.assertEqual(result["CONFIDENCE"], Confidence.LOW.value)
        self.assertIn("flawless", result["LEXICAL_VIOLATIONS"])


if __name__ == "__main__":
    unittest.main()
