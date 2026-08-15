#!/usr/bin/env python3
# Copyright Phoenix Protocol. All rights reserved.
# GVRN.Engine.EpistemicLinter.PY — SPELL-001
#
# Implements the "Self-Report Tagging" gate: every claim about a metric gets
# checked against a live reference (if one exists) and explicitly tagged
# with how it was verified, rather than being allowed to assert a clean
# number with no indication of whether anything was actually measured.
#
# STATUS values: PASS | FAIL | UNVERIFIED
# TAG values:    [MEASURED] | [SELF-REPORTED] | [ATTEMPTED MEASUREMENT]
#
# Numeric comparisons use a tolerance (math.isclose) rather than bare `==`,
# because exact float equality produces false "Silent Drift" failures for
# values that are the output of real computation (e.g. a phase multiplier
# computed on both a Python and a C++ side will rarely be bit-identical
# even when both implementations are correct).

import math

LEXICAL_BLOCKLIST = [
    "flawless",
    "immune",
    "perfect",
    "infallible",
    "bulletproof",
    "foolproof",
    "guaranteed",
    "impossible to fail",
    "never fails",
    "100% reliable",
    "always works",
    "unbreakable",
]


class EpistemicLinter:
    def __init__(self, rel_tol: float = 1e-6, abs_tol: float = 1e-9):
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def _scan_lexicon(self, text: str) -> list[str]:
        if not text:
            return []
        lower = text.lower()
        return [term for term in LEXICAL_BLOCKLIST if term in lower]

    @staticmethod
    def _is_numeric(value) -> bool:
        # bool is a subclass of int in Python; treat it as non-numeric here
        # so True/False compare by identity/equality, not by isclose(1/0).
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def execute_spell(self, metric_name, asserted_value, log_context, reference_callback=None):
        base = {
            "METRIC": metric_name,
            "ASSERTED": asserted_value,
            "LOG_CONTEXT": log_context,
            "LEXICAL_VIOLATIONS": self._scan_lexicon(log_context),
        }

        # --- No reference at all: pure self-report ---
        if reference_callback is None:
            return {
                **base,
                "STATUS": "UNVERIFIED",
                "TAG": "[SELF-REPORTED]",
                "GROUND_TRUTH": None,
                "REASON": "No reference callback provided; claim is an unverified self-report.",
            }

        # --- Reference exists, but the bridge to it failed ---
        try:
            ground_truth = reference_callback()
        except Exception as e:
            return {
                **base,
                "STATUS": "UNVERIFIED",
                "TAG": "[ATTEMPTED MEASUREMENT]",
                "GROUND_TRUTH": None,
                "REASON": f"Reference pointer execution failed: {type(e).__name__}: {e}",
            }

        # --- Bridge ran, but returned nothing usable ---
        if ground_truth is None:
            return {
                **base,
                "STATUS": "UNVERIFIED",
                "TAG": "[ATTEMPTED MEASUREMENT]",
                "GROUND_TRUTH": None,
                "REASON": "Reference callback executed successfully but returned no data (None).",
            }

        asserted_numeric = self._is_numeric(asserted_value)
        truth_numeric = self._is_numeric(ground_truth)

        # --- Type mismatch: not the same kind of claim at all ---
        if asserted_numeric != truth_numeric or (
            not asserted_numeric and not truth_numeric and type(asserted_value) is not type(ground_truth)
        ):
            return {
                **base,
                "STATUS": "FAIL",
                "TAG": "[MEASURED]",
                "GROUND_TRUTH": ground_truth,
                "REASON": (
                    f"Type Mismatch Detected: asserted value is {type(asserted_value).__name__}, "
                    f"ground truth is {type(ground_truth).__name__}."
                ),
            }

        if asserted_numeric and truth_numeric:
            matches = math.isclose(
                asserted_value, ground_truth, rel_tol=self.rel_tol, abs_tol=self.abs_tol
            )
        else:
            matches = asserted_value == ground_truth

        if matches:
            return {
                **base,
                "STATUS": "PASS",
                "TAG": "[MEASURED]",
                "GROUND_TRUTH": ground_truth,
                "REASON": "Asserted value confirmed against live reference.",
            }
        else:
            return {
                **base,
                "STATUS": "FAIL",
                "TAG": "[MEASURED]",
                "GROUND_TRUTH": ground_truth,
                "REASON": "Silent Drift Detected: asserted value does not match measured ground truth.",
            }
