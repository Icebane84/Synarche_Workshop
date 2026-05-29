import os
import sys
import sqlite3
import unittest
import uuid

# Add src and logic directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "..", "src", "logic")))

from rpg_manager import RPGManager


class TestSQLiteRPGPersistence(unittest.TestCase):
    def setUp(self):
        # We will use a dedicated test database to avoid polluting the development DB
        self.test_db_path = os.path.abspath(os.path.join(current_dir, "..", ".agent", "rpg_state_test.db"))
        # Ensure clean state
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
        self.manager = RPGManager(db_path=self.test_db_path)
        self.test_user_id = str(uuid.uuid4())

    def tearDown(self):
        # Clean up database file after test execution
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception as e:
                print(f"Error cleaning up test DB: {e}")

    def test_database_initialization(self):
        """Should verify that the SQLite database file and required tables are initialized."""
        self.assertTrue(os.path.exists(self.test_db_path))
        
        conn = sqlite3.connect(self.test_db_path)
        try:
            cursor = conn.cursor()
            # Verify tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn("player_state", tables)
            self.assertIn("rpg_stats", tables)
            self.assertIn("stardust_ledger", tables)
            self.assertIn("player_achievements", tables)
        finally:
            conn.close()

    def test_persistence_across_instances(self):
        """Should verify that data persists cleanly across different RPGManager instances."""
        # 1. Initialize player and award stardust
        self.manager.ensure_player_exists(self.test_user_id)
        self.manager.award_stardust(1250, "INITIAL_BOOST", self.test_user_id)
        
        # 2. Re-instantiate a second manager pointing to the same file
        second_manager = RPGManager(db_path=self.test_db_path)
        status = second_manager.get_status(self.test_user_id)
        
        # 3. Assert values are identical
        self.assertEqual(status.get("stardust_available"), 1250)
        self.assertEqual(status.get("level"), 1)

    def test_stardust_ledger_integrity(self):
        """Should verify that all earned and spent transactions are logged correctly in the ledger."""
        self.manager.ensure_player_exists(self.test_user_id)
        self.manager.award_stardust(800, "EARN_1", self.test_user_id)
        self.manager.invest_stardust("coherence_index", 500, self.test_user_id)
        
        # Connect directly to SQLite to check transactions count and details
        conn = sqlite3.connect(self.test_db_path)
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stardust_ledger WHERE user_id = ? ORDER BY id ASC", (self.test_user_id,))
            rows = [dict(r) for r in cursor.fetchall()]
            
            self.assertEqual(len(rows), 2)
            
            # Check Earned transaction
            self.assertEqual(rows[0]["transaction_type"], "EARNED")
            self.assertEqual(rows[0]["amount"], 800)
            self.assertEqual(rows[0]["reference_impact_id"], "EARN_1")
            
            # Check Spent transaction
            self.assertEqual(rows[1]["transaction_type"], "SPENT")
            self.assertEqual(rows[1]["amount"], 500)
            self.assertEqual(rows[1]["target_stat"], "coherence_index")
        finally:
            conn.close()

    def test_stat_investment_scaling(self):
        """Should verify that stardust investment updates stats and decreases balance correctly."""
        self.manager.ensure_player_exists(self.test_user_id)
        self.manager.award_stardust(1000, "START", self.test_user_id)
        
        res = self.manager.invest_stardust("synergy", 300, self.test_user_id)
        self.assertTrue(res["success"])
        # (300 / 100) * 0.1 = 0.3 increase -> 1.0 + 0.3 = 1.3
        self.assertAlmostEqual(res["new_value"], 1.3)
        self.assertEqual(res["stardust_remaining"], 700)
        
        # Verify persistence on disk
        status = self.manager.get_status(self.test_user_id)
        self.assertAlmostEqual(status.get("synergy"), 1.3)
        self.assertEqual(status.get("stardust_available"), 700)


if __name__ == "__main__":
    unittest.main()
