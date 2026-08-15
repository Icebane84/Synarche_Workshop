#!/usr/bin/env python3
# FILE: test_validate_system.py
# One regression test per confirmed issue, plus a couple of "didn't
# overcorrect" sanity checks.

import json
import os
import tempfile
import unittest
import datetime

from validate_system import SystemValidator


class TestValidateSystemHardening(unittest.TestCase):

    def _mkdir(self, *parts):
        path = os.path.join(self.root, *parts)
        os.makedirs(path, exist_ok=True)
        return path

    def _write(self, rel_path, content):
        full = os.path.join(self.root, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        return full

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    # --- Fix #1: real timestamp ---

    def test_fix1_timestamp_is_live_not_hardcoded(self):
        before = datetime.datetime.now(datetime.timezone.utc)
        validator = SystemValidator(self.root)
        report = validator.run_audit()
        after = datetime.datetime.now(datetime.timezone.utc)

        reported = datetime.datetime.fromisoformat(report["timestamp"])
        self.assertGreaterEqual(reported, before - datetime.timedelta(seconds=1))
        self.assertLessEqual(reported, after + datetime.timedelta(seconds=1))

    # --- Fix #2: empty-scan checks no longer silently PASS ---

    def test_fix2_empty_directory_is_not_65_percent(self):
        validator = SystemValidator(self.root)
        report = validator.run_audit()

        # Every check is UNVERIFIED (nothing at all in the directory) ->
        # score must be undefined, not 65.0 or any other silently-passing value.
        self.assertIsNone(report["evidence_confidence_score"])
        for obs in report["observations"]:
            self.assertEqual(obs["status"], "UNVERIFIED")

    def test_fix2_unverified_excluded_from_denominator(self):
        # Only markdown present -> rnc_lint applies (to the .md file),
        # import_paths and compilation are UNVERIFIED (no code/config),
        # block_integrity applies (one .md file, non-compliant).
        self._write("NOTES.md", "just some notes, no PPL blocks here")
        validator = SystemValidator(self.root)
        report = validator.run_audit()

        by_id = {o["id"]: o for o in report["observations"]}
        self.assertEqual(by_id["compilation"]["status"], "UNVERIFIED")
        self.assertEqual(by_id["import_paths"]["status"], "UNVERIFIED")
        self.assertIn(by_id["rnc_lint"]["status"], ("PASS", "FAIL"))
        self.assertIn(by_id["block_integrity"]["status"], ("PASS", "FAIL"))
        # Score, if defined, must be computed only from rnc_lint + block_integrity's weights.
        if report["evidence_confidence_score"] is not None:
            applicable_weight = by_id["rnc_lint"]["weight"] + by_id["block_integrity"]["weight"]
            self.assertAlmostEqual(applicable_weight, 0.45)

    # --- Fix #3: RNC regex accepts mixed-case segments ---

    def test_fix3_real_gvrn_filenames_are_compliant(self):
        real_names = [
            "GVRN.Master.Registry.yaml",
            "GVRN.Documentation.PromptDSL.md",
            "GVRN.SPEC.VERIFICATION_QUAD.001.md",
            "GVRN.Engine.WorkspaceWalker.PY",
            "LOG.MECS.LEDGER.json",
        ]
        for name in real_names:
            # spread across dirs so RNC's own-name skip-list doesn't interfere
            self._write(os.path.join("docs", name), "content")

        validator = SystemValidator(self.root)
        status, details = validator.check_rnc_compliance()
        self.assertEqual(details["violations"], [],
                          f"Real GVRN filenames flagged as violations: {details['violations']}")

    def test_fix3_genuinely_noncompliant_name_still_flagged(self):
        # Sanity check: the fix must not have become so permissive that
        # nothing fails anymore.
        self._write("readme.md", "content")
        validator = SystemValidator(self.root)
        status, details = validator.check_rnc_compliance()
        self.assertIn("readme.md", details["violations"])

    # --- Fix #4: compilation check recognizes Python and C++/Unreal ---

    def test_fix4_python_project_without_tsconfig_is_not_auto_fail(self):
        self._write("pyproject.toml", "[tool.mypy]\nstrict = true\n")
        self._write("src/GVRN.Engine.Sample.PY", "def add(a: int, b: int) -> int:\n    return a + b\n")

        validator = SystemValidator(self.root)
        status, details = validator.check_compilation()
        self.assertEqual(status, "PASS")
        self.assertIn("python", details["ecosystems_detected"])

    def test_fix4_cpp_unreal_project_is_not_auto_fail(self):
        self._write("MyGame.uproject", "{}")
        validator = SystemValidator(self.root)
        status, details = validator.check_compilation()
        self.assertEqual(status, "PASS")
        self.assertIn("cpp_unreal", details["ecosystems_detected"])

    def test_fix4_nothing_recognized_is_unverified_not_fail(self):
        self._write("random.txt", "nothing relevant here")
        validator = SystemValidator(self.root)
        status, details = validator.check_compilation()
        self.assertEqual(status, "UNVERIFIED")

    # --- Fix #5: case-insensitive extension matching ---

    def test_fix5_uppercase_py_extension_is_scanned(self):
        self._write("GVRN.Engine.Sample.PY", "import os\n")
        validator = SystemValidator(self.root)
        status, details = validator.check_import_paths()
        self.assertEqual(details["total_code_files_scanned"], 1)

    # --- Fix #6: "../" substring in prose no longer flagged ---

    def test_fix6_mention_of_dotdot_in_docstring_is_not_flagged(self):
        self._write("sample.py", '"""See the sibling docs at ../docs/README.md for notes."""\nimport os\n')
        validator = SystemValidator(self.root)
        status, details = validator.check_import_paths()
        self.assertEqual(status, "PASS")
        self.assertEqual(details["path_noise_files_count"], 0)

    def test_fix6_actual_relative_import_is_still_flagged(self):
        self._write("sample.py", "from ..sibling import helper\n")
        validator = SystemValidator(self.root)
        status, details = validator.check_import_paths()
        self.assertEqual(status, "FAIL")
        self.assertEqual(details["path_noise_files_count"], 1)


if __name__ == "__main__":
    unittest.main()
