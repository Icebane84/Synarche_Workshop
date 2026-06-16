import os
import sys
import unittest
import uuid
from unittest.mock import MagicMock, patch

# Add src to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "..", "src", "logic")))

from rpg_manager import RPGManager


class TestRPGAchievements(unittest.TestCase):
    def setUp(self):
        self.test_db_path = os.path.abspath(
            os.path.join(current_dir, "..", ".agent", "rpg_state_test.db")
        )
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception:
                pass
        self.manager = RPGManager(db_path=self.test_db_path)
        self.manager.use_supabase = False  # Disable remote writes for base tests
        self.test_user_id = str(uuid.uuid4())
        self.manager.ensure_player_exists(self.test_user_id)

    def tearDown(self):
        if hasattr(self, "test_db_path") and os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception:
                pass

    def test_get_achievements_empty(self):
        """Should return all available achievements with completed=False status initially."""
        achievements = self.manager.get_achievements(self.test_user_id)
        self.assertGreater(len(achievements), 0)
        for a in achievements:
            self.assertFalse(a["completed"])

    def test_claim_valid_achievement(self):
        """Should successfully claim an achievement and award rewards."""
        # Assuming "FIRST_GENESIS" is a seeded achievement
        res = self.manager.claim_achievement("FIRST_GENESIS", self.test_user_id)
        self.assertTrue(res["success"])
        self.assertIn("stardust_awarded", res)

        # Verify status update
        achievements = self.manager.get_achievements(self.test_user_id)
        claimed = next(a for a in achievements if a["id"] == "FIRST_GENESIS")
        self.assertTrue(claimed["completed"])

    def test_claim_already_earned(self):
        """Should fail to claim an achievement that was already earned."""
        self.manager.claim_achievement("FIRST_GENESIS", self.test_user_id)
        res = self.manager.claim_achievement("FIRST_GENESIS", self.test_user_id)
        self.assertFalse(res["success"])
        self.assertEqual(res["error"], "Already earned")

    def test_claim_invalid_achievement(self):
        """Should fail to claim a non-existent achievement."""
        res = self.manager.claim_achievement("NON_EXISTENT", self.test_user_id)
        self.assertFalse(res["success"])
        self.assertEqual(res["error"], "Achievement not found")


class MockSupabaseResponse:
    def __init__(self, data, error=None):
        self.data = data
        self.error = error


class TestRPGDualWrite(unittest.TestCase):
    def setUp(self):
        self.test_db_path = os.path.abspath(
            os.path.join(current_dir, "..", ".agent", "rpg_state_test_dual.db")
        )
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception:
                pass

        self.manager = RPGManager(db_path=self.test_db_path)
        self.manager.use_supabase = True
        self.mock_client = MagicMock()
        self.manager.supabase_client = self.mock_client
        self.test_user_id = str(uuid.uuid4())

        # Set up default mock return values for tables
        self.mock_tables = {}
        def get_mock_table(name):
            if name not in self.mock_tables:
                tb = MagicMock()
                # Chain default values
                tb.select.return_value.eq.return_value.execute.return_value = MockSupabaseResponse([])
                tb.insert.return_value.execute.return_value = MockSupabaseResponse([])
                tb.update.return_value.eq.return_value.execute.return_value = MockSupabaseResponse([])
                self.mock_tables[name] = tb
            return self.mock_tables[name]

        self.mock_client.table.side_effect = get_mock_table

        # Pre-initialize all expected tables to prevent KeyErrors during setup and test runs
        for name in ["player_state", "rpg_stats", "stardust_ledger", "player_achievements"]:
            get_mock_table(name)

        # Call local setup
        self.manager.ensure_player_exists(self.test_user_id)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception:
                pass

    def test_get_status_sync(self):
        """Should fetch from Supabase if available."""
        # Setup mock returns for player_state and rpg_stats
        self.mock_tables["player_state"].select.return_value.eq.return_value.execute.return_value = MockSupabaseResponse([
            {"user_id": self.test_user_id, "level": 5, "xp": 1500, "prestige_score": 10, "prestige_class": "Acolyte"}
        ])
        self.mock_tables["rpg_stats"].select.return_value.eq.return_value.execute.return_value = MockSupabaseResponse([
            {
                "user_id": self.test_user_id,
                "stardust_available": 3500,
                "coherence_index": 1.5,
                "synergy": 1.2,
                "adaptability": 1.3,
                "transparency": 1.4,
                "semantic_friction_resonance": 1.0,
                "form_ascension_state": 1.1,
                "creative_spark": 1.6,
                "updated_at": "2026-06-06T12:00:00"
            }
        ])

        status = self.manager.get_status(self.test_user_id)
        self.assertEqual(status["level"], 5)
        self.assertEqual(status["xp"], 1500)
        self.assertEqual(status["stardust_available"], 3500)
        self.assertEqual(status["coherence_index"], 1.5)
        self.assertEqual(status["synergy"], 1.2)
        self.assertEqual(status["prestige_class"], "Acolyte")

    def test_get_status_fallback(self):
        """Should fall back to local SQLite if Supabase fetch throws an exception."""
        # SQLite state has 0 stardust, level 1, xp 0 initially. Let's award some locally
        self.manager.use_supabase = False
        self.manager.award_stardust(800, "LOCAL_BOOST", self.test_user_id)
        self.manager.use_supabase = True

        # Make Supabase query throw exception
        self.mock_tables["player_state"].select.side_effect = Exception("Supabase Offline")

        status = self.manager.get_status(self.test_user_id)
        # Should fall back to SQLite stats
        self.assertEqual(status["stardust_available"], 800)
        self.assertEqual(status["level"], 1)

    def test_award_stardust_dual_write(self):
        """Should write to both SQLite and Supabase."""
        new_total = self.manager.award_stardust(1200, "QUEST_1", self.test_user_id)
        self.assertEqual(new_total, 1200)

        # Verify Supabase was called to update stats and insert ledger row
        self.mock_client.table.assert_any_call("rpg_stats")
        self.mock_client.table.assert_any_call("stardust_ledger")
        self.mock_tables["rpg_stats"].update.assert_called_once()
        self.mock_tables["stardust_ledger"].insert.assert_called_once()

    def test_invest_stardust_dual_write(self):
        """Should spend stardust and update stats on both SQLite and Supabase."""
        self.manager.use_supabase = False
        self.manager.award_stardust(1000, "INIT", self.test_user_id)
        self.manager.use_supabase = True

        res = self.manager.invest_stardust("synergy", 300, self.test_user_id)
        self.assertTrue(res["success"])
        self.assertEqual(res["stardust_remaining"], 700)

        # Verify Supabase updates
        self.mock_client.table.assert_any_call("rpg_stats")
        self.mock_client.table.assert_any_call("stardust_ledger")
        
        # Verify update content has Synergy incremented (1.0 + 0.3 = 1.3)
        self.mock_tables["rpg_stats"].update.assert_called_with({
            "synergy": 1.3,
            "stardust_available": 700,
            "updated_at": unittest.mock.ANY
        })

    def test_claim_achievement_dual_write(self):
        """Should claim achievement and mirror rewards to Supabase."""
        # Verify FIRST_GENESIS claim
        res = self.manager.claim_achievement("FIRST_GENESIS", self.test_user_id)
        self.assertTrue(res["success"])
        self.assertEqual(res["mode"], "SYNCED")

        # Verify remote tables were updated/inserted
        self.mock_client.table.assert_any_call("player_state")
        self.mock_client.table.assert_any_call("rpg_stats")
        self.mock_client.table.assert_any_call("stardust_ledger")
        self.mock_client.table.assert_any_call("player_achievements")

        # player_state should update XP (FIRST_GENESIS rewards 100 XP)
        self.mock_tables["player_state"].update.assert_called_once_with({"xp": 100})
        # rpg_stats should update stardust (FIRST_GENESIS rewards 500 Stardust)
        self.mock_tables["rpg_stats"].update.assert_called_once_with({
            "stardust_available": 500,
            "updated_at": unittest.mock.ANY
        })
        # player_achievements should record completion
        self.mock_tables["player_achievements"].insert.assert_called_once_with({
            "user_id": self.test_user_id,
            "achievement_id": "FIRST_GENESIS"
        })

    def test_get_achievements_from_supabase(self):
        """Should retrieve achievements from Supabase if available."""
        self.mock_tables["player_achievements"].select.return_value.eq.return_value.execute.return_value = MockSupabaseResponse([
            {"achievement_id": "FIRST_GENESIS"}
        ])

        achievements = self.manager.get_achievements(self.test_user_id)
        genesis = next(a for a in achievements if a["id"] == "FIRST_GENESIS")
        self.assertTrue(genesis["completed"])


if __name__ == "__main__":
    unittest.main()
