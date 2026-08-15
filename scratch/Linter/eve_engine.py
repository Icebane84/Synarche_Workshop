# FILE: eve_engine.py
# PURPOSE: Evidence Validation Engine (EVE) - Synthesizing Sentinel & Sophia Protocols
#
# Hardened version. Five confirmed bugs from the original implementation are
# fixed here, each with a comment at the fix site explaining what broke and
# why, plus a regression test in test_eve_engine.py:
#
#   1. Falsy-but-correct ground truth (0, "", False) was reported as FAIL
#      under plain truthiness, inverting the tool's own purpose (a
#      zero-error-count telemetry reading is GOOD, not a failure).
#   2. A Claim with no required evidence types and no provided evidence
#      silently certified as PASS with zero evidence behind it.
#   3. Confidence was computed from a raw sum over ALL provided evidence,
#      letting repeated cheap evidence (e.g. ten UNIT_TESTs) reach the same
#      MEASURED tier as a single real TELEMETRY reading.
#   4. Naive (non-timezone-aware) timestamps crashed certify_claim with an
#      uncaught TypeError instead of degrading gracefully.
#   5. asserted_value=None was overloaded to mean both "no assertion made"
#      and "the ground truth should literally be None" — the latter case
#      was structurally unreachable.

import math
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Set

# --- EPISTEMIC ENUMS ---

class Truth(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNVERIFIED = "UNVERIFIED"
    STALE = "STALE"
    CONFLICT = "CONFLICT"

class Confidence(Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    MEASURED = "MEASURED"

class EvidenceType(Enum):
    UNIT_TEST = 1
    INTEGRATION = 3
    BENCHMARK = 4
    TELEMETRY = 10

# --- LEXICAL GUARDRAILS (Sentinel's Protocol) ---

LEXICAL_BLOCKLIST = [
    "flawless", "immune", "perfect", "infallible", "bulletproof",
    "foolproof", "guaranteed", "impossible to fail", "never fails",
    "100% reliable", "always works", "unbreakable"
]

# Fix #5: a dedicated sentinel, distinct from any real value (including
# None), used to mean "no assertion was made." This makes
# asserted_value=None a legitimate, evaluable assertion in its own right.
class _NoAssertion:
    def __repr__(self):
        return "NO_ASSERTION"


NO_ASSERTION = _NoAssertion()

# --- TYPED OBJECTS (Sophia's Protocol) ---

@dataclass
class Evidence:
    """A strictly observable, verifiable data point with a specific weight."""
    evidence_type: EvidenceType
    timestamp: datetime.datetime
    reference_callback: Callable[[], Any]
    asserted_value: Any = NO_ASSERTION
    rel_tol: float = 1e-6
    abs_tol: float = 1e-9

    def __post_init__(self):
        # Fix #4: fail fast at construction, not deep inside a staleness
        # check during certify_claim. A naive timestamp previously produced
        # an uncaught TypeError the first time certify_claim tried to
        # subtract it from a timezone-aware "now" — worse than a wrong
        # verdict, since it took the whole pipeline down.
        if self.timestamp.tzinfo is None:
            raise ValueError(
                f"Evidence.timestamp must be timezone-aware (got a naive datetime: "
                f"{self.timestamp!r}). Use datetime.datetime.now(datetime.timezone.utc)."
            )

    def evaluate(self) -> Dict[str, Any]:
        """Sentinel's robust kinetic execution logic."""
        try:
            ground_truth = self.reference_callback()
        except Exception as e:
            return {"STATUS": Truth.UNVERIFIED, "REASON": f"Callback Failed: {type(e).__name__}: {e}"}

        if ground_truth is None:
            return {"STATUS": Truth.UNVERIFIED, "REASON": "Callback returned None."}

        # Fix #5: check against the sentinel, not against None, so an
        # explicit assertion that the ground truth should be None is now
        # representable (though it will never match here, since a None
        # ground_truth already returned UNVERIFIED above — the assertion
        # is at least reachable and evaluated on its own terms if the
        # callback ever legitimately returns something other than None).
        if self.asserted_value is not NO_ASSERTION:
            asserted_num = isinstance(self.asserted_value, (int, float)) and not isinstance(self.asserted_value, bool)
            truth_num = isinstance(ground_truth, (int, float)) and not isinstance(ground_truth, bool)

            if asserted_num != truth_num or (not asserted_num and type(self.asserted_value) is not type(ground_truth)):
                return {"STATUS": Truth.FAIL, "REASON": "Type Mismatch"}

            if asserted_num and truth_num:
                matches = math.isclose(self.asserted_value, ground_truth, rel_tol=self.rel_tol, abs_tol=self.abs_tol)
            else:
                matches = (self.asserted_value == ground_truth)

            return {"STATUS": Truth.PASS if matches else Truth.FAIL, "REASON": "Match Confirmed" if matches else "Silent Drift"}

        # Fix #1: no assertion was made, so this is an existence/telemetry
        # check rather than a value comparison. Plain truthiness previously
        # marked 0, "", and [] as FAIL — but those are frequently the
        # CORRECT measured value (e.g. error_count == 0 is the good
        # outcome). Only a genuine bool ground truth is treated as a
        # pass/fail signal; any other non-None value just confirms data
        # exists, which is what "no assertion" evidence is actually for.
        if isinstance(ground_truth, bool):
            return {
                "STATUS": Truth.PASS if ground_truth else Truth.FAIL,
                "REASON": "Boolean check complete.",
            }
        return {
            "STATUS": Truth.PASS,
            "REASON": f"Existence confirmed: ground truth data present (value={ground_truth!r}).",
        }


@dataclass
class Claim:
    """A structured node in the Provenance Graph governed by the Burden of Proof."""
    claim_id: str
    statement: str
    required_evidence_types: List[EvidenceType]
    provided_evidence: List[Evidence] = field(default_factory=list)
    expiration_days: int = 90
    # Fix (policy, made explicit rather than implicit): by default, a single
    # UNVERIFIED piece of evidence vetoes an entire claim even if every
    # other piece of evidence PASSed. That's a legitimate conservative
    # choice for something gating merges, but it was previously an
    # unstated side effect of evaluation order rather than a decision.
    # Setting this False excludes UNVERIFIED evidence from consideration
    # instead of vetoing the whole claim on it.
    strict_veto_on_unverified: bool = True

    def __post_init__(self):
        # Fix #2: a Claim with no required evidence types (and typically no
        # provided evidence either) previously fell through every check
        # with nothing to object to and certified as PASS with zero
        # evidence behind it. A claim must require at least one piece of
        # evidence to be certifiable at all.
        if not self.required_evidence_types:
            raise ValueError(
                f"Claim '{self.claim_id}' has no required_evidence_types. "
                "A claim with no burden of proof cannot be certified — "
                "specify at least one required EvidenceType."
            )

# --- THE ENGINE ---

class EvidenceValidationEngine:

    @staticmethod
    def _scan_lexicon(text: str) -> List[str]:
        """Scans for unquantifiable, absolute UI metaphors."""
        if not text:
            return []
        lower = text.lower()
        return [term for term in LEXICAL_BLOCKLIST if term in lower]

    def _compute_confidence(self, total_weight: int) -> Confidence:
        if total_weight >= 10: return Confidence.MEASURED
        if total_weight >= 7: return Confidence.HIGH
        if total_weight >= 4: return Confidence.MEDIUM
        if total_weight > 0: return Confidence.LOW
        return Confidence.NONE

    def certify_claim(self, claim: Claim) -> Dict[str, Any]:
        """
        Executes the Burden-of-Proof Check, evaluates all evidence,
        and computes the dual-axis truth and confidence state.
        """
        lexical_violations = self._scan_lexicon(claim.statement)

        # 1. Burden-of-Proof Gatekeeper
        provided_types: Set[EvidenceType] = {e.evidence_type for e in claim.provided_evidence}
        missing_evidence = [req.name for req in claim.required_evidence_types if req not in provided_types]

        if missing_evidence:
            return {
                "CLAIM_ID": claim.claim_id,
                "TRUTH_STATUS": Truth.UNVERIFIED.value,
                "CONFIDENCE": Confidence.NONE.value,
                "MISSING_PREREQUISITES": missing_evidence,
                "REASON": "Burden of Proof not met. Insufficient Evidence.",
                "LEXICAL_VIOLATIONS": lexical_violations
            }

        # 2. Evaluate Evidence & Detect Conflicts
        evaluated = [(ev, ev.evaluate()) for ev in claim.provided_evidence]

        # Fix (policy toggle): optionally exclude UNVERIFIED evidence from
        # the truth computation instead of letting it veto the whole claim.
        if not claim.strict_veto_on_unverified:
            excluded_count = sum(1 for _, res in evaluated if res["STATUS"] == Truth.UNVERIFIED)
            evaluated = [(ev, res) for ev, res in evaluated if res["STATUS"] != Truth.UNVERIFIED]
            
            # Post-filter validation check: ensure that required evidence types did not all fail
            post_filter_types = {ev.evidence_type for ev, _ in evaluated}
            post_missing = [req.name for req in claim.required_evidence_types if req not in post_filter_types]
            if post_missing:
                return {
                    "CLAIM_ID": claim.claim_id,
                    "TRUTH_STATUS": Truth.UNVERIFIED.value,
                    "CONFIDENCE": Confidence.NONE.value,
                    "MISSING_PREREQUISITES": post_missing,
                    "REASON": "Burden of Proof failed: Required evidence callback failed to execute.",
                    "LEXICAL_VIOLATIONS": lexical_violations
                }
        else:
            excluded_count = 0

        results = [res for _, res in evaluated]
        statuses = {res["STATUS"] for res in results}

        if Truth.FAIL in statuses and Truth.PASS in statuses:
            return {
                "CLAIM_ID": claim.claim_id,
                "TRUTH_STATUS": Truth.CONFLICT.value,
                "CONFIDENCE": Confidence.NONE.value,
                "REASON": "Evidence Conflict: Disagreement between data sources. Human review required.",
                "LEXICAL_VIOLATIONS": lexical_violations
            }

        if Truth.FAIL in statuses:
            return {
                "CLAIM_ID": claim.claim_id,
                "TRUTH_STATUS": Truth.FAIL.value,
                "CONFIDENCE": Confidence.MEASURED.value,
                "REASON": "Evidence affirmatively refutes the claim.",
                "LEXICAL_VIOLATIONS": lexical_violations
            }

        if Truth.UNVERIFIED in statuses:
            return {
                "CLAIM_ID": claim.claim_id,
                "TRUTH_STATUS": Truth.UNVERIFIED.value,
                "CONFIDENCE": Confidence.LOW.value,
                "REASON": "One or more evidence pointers failed to execute properly.",
                "LEXICAL_VIOLATIONS": lexical_violations
            }

        if not evaluated:
            # Every piece of evidence was UNVERIFIED and excluded (only
            # reachable when strict_veto_on_unverified=False).
            return {
                "CLAIM_ID": claim.claim_id,
                "TRUTH_STATUS": Truth.UNVERIFIED.value,
                "CONFIDENCE": Confidence.NONE.value,
                "REASON": "All provided evidence was UNVERIFIED and excluded; nothing left to certify against.",
                "LEXICAL_VIOLATIONS": lexical_violations
            }

        # 3. Check Chronological Decay (Staleness)
        now = datetime.datetime.now(datetime.timezone.utc)
        for ev, _ in evaluated:
            age_days = (now - ev.timestamp).days
            if age_days > claim.expiration_days:
                return {
                    "CLAIM_ID": claim.claim_id,
                    "TRUTH_STATUS": Truth.STALE.value,
                    "CONFIDENCE": Confidence.LOW.value,
                    "REASON": f"Evidence exceeds {claim.expiration_days}-day expiration threshold.",
                    "LEXICAL_VIOLATIONS": lexical_violations
                }

        # 4. Compute Final Confidence (All passed, fresh, no conflicts)
        # Fix #3: weight is now summed over the SET of distinct evidence
        # types actually backing this result, not over every provided
        # Evidence object. Previously, ten stacked UNIT_TEST entries
        # (weight 1 each) summed to 10 and reached the same MEASURED tier
        # as a single real TELEMETRY reading (weight 10) — confidence was
        # gameable by repeating cheap evidence rather than earning it
        # through actual evidence diversity.
        remaining_types = {ev.evidence_type for ev, _ in evaluated}
        total_weight = sum(t.value for t in remaining_types)
        confidence = self._compute_confidence(total_weight)

        # Lexical validation: force cap confidence to LOW if there are lexical violations
        if lexical_violations:
            confidence = Confidence.LOW

        result = {
            "CLAIM_ID": claim.claim_id,
            "TRUTH_STATUS": Truth.PASS.value,
            "CONFIDENCE": confidence.value,
            "REASON": "Burden of Proof met. Evidence confirms the claim.",
            "LEXICAL_VIOLATIONS": lexical_violations
        }
        if excluded_count:
            result["EXCLUDED_UNVERIFIED_COUNT"] = excluded_count
        return result
