import unittest
import os
import json
import tempfile
import yaml
import hashlib
import sys

# Standardize console encoding for Windows Cp1252 console safety
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add tools directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from workspace_walker import WorkspaceWalker

class TestWorkspaceWalker(unittest.TestCase):
    def setUp(self):
        # Create temp directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace_root = self.temp_dir.name
        
        # Setup subdirectories
        os.makedirs(os.path.join(self.workspace_root, "_governance", "01_Registries"), exist_ok=True)
        os.makedirs(os.path.join(self.workspace_root, "_governance", "50_Logs"), exist_ok=True)
        
        self.registry_path = os.path.join(self.workspace_root, "_governance", "01_Registries", "GVRN.Master.Registry.yaml")
        self.ledger_path = os.path.join(self.workspace_root, "_governance", "50_Logs", "LOG.MECS.LEDGER.json")
        
        # Create a mock file
        self.mock_file_path = os.path.join(self.workspace_root, "test_file.cpp")
        with open(self.mock_file_path, "w", encoding="utf-8") as f:
            f.write("int main() { return 0; }")
            
        self.file_hash = hashlib.sha256(b"int main() { return 0; }").hexdigest()
        
        # Create mock registry
        self.mock_registry = {
            "TEST.NODE.001": {
                "artifact_id": "TEST.NODE.001",
                "official_name": "test_file.cpp",
                "path": "test_file.cpp",
                "version": "v1.0",
                "status_(state)": "ACTIVE",
                "relations": "GOVERNED_BY: SPEC-001",
                "parsed_relations": ["GOVERNED_BY:SPEC-001"],
                "specs": {
                    "param": 42
                }
            }
        }
        with open(self.registry_path, "w", encoding="utf-8") as f:
            yaml.dump(self.mock_registry, f)
            
        # Create mock ledger
        self.mock_ledger = {
            "records": [
                {
                    "artifact_path": "test_file.cpp",
                    "content_sha256": self.file_hash,
                    "verified_at": "2026-07-25T00:00:00Z"
                }
            ]
        }
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(self.mock_ledger, f)
            
        # Initialize walker
        self.walker = WorkspaceWalker(workspace_root=self.workspace_root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_data(self):
        self.assertIn("TEST.NODE.001", self.walker.registry)
        self.assertIn("test_file.cpp", self.walker.ledger_records)

    def test_check_waning_seal_valid(self):
        status = self.walker.check_waning_seal("test_file.cpp")
        self.assertEqual(status, "STILL_VALID")

    def test_check_waning_seal_stale(self):
        # Modify file content on disk to invalidate the ledger hash
        with open(self.mock_file_path, "w", encoding="utf-8") as f:
            f.write("int main() { return 1; }")
            
        status = self.walker.check_waning_seal("test_file.cpp")
        self.assertEqual(status, "STALE_VERIFICATION_VOID")

    def test_render_sliding_context(self):
        context = self.walker.render_sliding_context("TEST.NODE.001")
        self.assertIn("Node ID: TEST.NODE.001", context)
        self.assertIn("Waning Seal Status: STILL_VALID", context)
        self.assertIn("[Waning Seal is STILL_VALID. File contents cached", context)

    def test_render_sliding_context_stale_shows_content(self):
        # Modify file content to trigger state decay
        with open(self.mock_file_path, "w", encoding="utf-8") as f:
            f.write("int main() { return 1; }")
            
        context = self.walker.render_sliding_context("TEST.NODE.001")
        self.assertIn("Waning Seal Status: STALE_VERIFICATION_VOID", context)
        self.assertIn("int main() { return 1; }", context)

    def test_render_sliding_context_missing_file_does_not_claim_still_valid(self):
        # Regression test: a node whose backing file has been deleted must
        # never render the "Waning Seal is STILL_VALID... cached" message.
        # That message previously appeared for MISSING nodes because the
        # file-content trigger only checked for STALE_VERIFICATION_VOID and
        # UNVERIFIED, not MISSING, so it fell through to the cached-content
        # else-branch meant for genuinely valid files.
        os.remove(self.mock_file_path)

        status = self.walker.check_waning_seal("test_file.cpp")
        self.assertEqual(status, "MISSING")

        context = self.walker.render_sliding_context("TEST.NODE.001")
        self.assertIn("Waning Seal Status: MISSING", context)
        self.assertNotIn("Waning Seal is STILL_VALID", context)
        self.assertIn("missing on disk", context)

    def test_check_waning_seal_matches_backslash_ledger_path(self):
        # Regression test: a ledger record written with backslash separators
        # (e.g. produced by os.path.join on Windows) must still match a
        # forward-slash rel_path lookup, since the registry itself stores
        # forward-slash paths. Previously this silently returned UNVERIFIED
        # instead of STILL_VALID because only the lookup side was normalized.
        nested_dir = os.path.join(self.workspace_root, "_governance", "08_Documentation")
        os.makedirs(nested_dir, exist_ok=True)
        nested_file = os.path.join(nested_dir, "spec.md")
        with open(nested_file, "w", encoding="utf-8") as f:
            f.write("hello")
        nested_hash = hashlib.sha256(b"hello").hexdigest()

        # Append a ledger record whose artifact_path uses backslashes.
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            ledger_data = json.load(f)
        ledger_data["records"].append({
            "artifact_path": "_governance\\08_Documentation\\spec.md",
            "content_sha256": nested_hash,
            "verified_at": "2026-07-25T00:00:00Z",
        })
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger_data, f)

        walker = WorkspaceWalker(workspace_root=self.workspace_root)
        status = walker.check_waning_seal("_governance/08_Documentation/spec.md")
        self.assertEqual(status, "STILL_VALID")

if __name__ == "__main__":
    unittest.main()
