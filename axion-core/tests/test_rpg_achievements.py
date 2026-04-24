import unittest
import os
import sys
import uuid

# Add src to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "..", "src", "logic"))

from rpg_manager import RPGManager

class TestRPGAchievements(unittest.TestCase):
    def setUp(self):
        self.manager = RPGManager()
        self.test_user_id = str(uuid.uuid4())
        self.manager.ensure_player_exists(self.test_user_id)

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

if __name__ == "__main__":
    unittest.main()
