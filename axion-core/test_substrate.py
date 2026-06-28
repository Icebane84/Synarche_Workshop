import os
import shutil
import tempfile
import time
import unittest

from substrate_server import ImmutableKnowledgeSubstrate, SystemCausalEvent


class TestImmutableKnowledgeSubstrate(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory and a fresh substrate instance for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.journal_path = os.path.join(self.test_dir, "test_journal.jsonl")
        self.snapshot_path = os.path.join(self.test_dir, "test_snapshot.json")
        self.substrate = ImmutableKnowledgeSubstrate(journal_path=self.journal_path, snapshot_path=self.snapshot_path)

    def tearDown(self):
        """Remove the temporary directory after each test."""
        shutil.rmtree(self.test_dir)

    def test_initial_state(self):
        """Verify the initial state of a new substrate."""
        self.assertEqual(self.substrate.total_blocks_processed, 0)
        self.assertEqual(len(self.substrate.proposal_registry), 0)
        self.assertEqual(self.substrate.global_state_root, "0x" + "0" * 64)

    def test_handle_submit_proposal(self):
        """Test that submitting a proposal correctly updates the proposal registry."""
        # 1. Define the test event payload
        proposal_payload = {
            "entry_id": "codex.test/item-1",
            "term": "Test Term",
            "assertion": "This is a test assertion.",
            "nonce": "test-nonce-123",
            "timestamp": int(time.time()),
            "lineage": {
                "parent_hash": "ROOT_GENESIS",
                "causal_trigger": "test_suite",
                "justification": "This is required for the test case to pass.",
            },
        }

        # 2. Create the causal event
        event_id = 1
        event = SystemCausalEvent(
            event_id=event_id, action_type="SUBMIT_PROPOSAL", payload=proposal_payload, node_id="TEST_NODE"
        )

        # 3. Commit the event
        self.substrate.commit_validated_event(event)

        # 4. Assert the expected state changes
        self.assertIn(event_id, self.substrate.proposal_registry)
        proposal_entry = self.substrate.proposal_registry[event_id]
        self.assertEqual(proposal_entry["status"], "VOTING")
        self.assertEqual(proposal_entry["node_origin"], "TEST_NODE")
        self.assertEqual(proposal_entry["data_payload"], proposal_payload)
        self.assertEqual(self.substrate.total_blocks_processed, 1)
