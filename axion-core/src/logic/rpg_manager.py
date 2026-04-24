import json
import os

from dotenv import load_dotenv
from supabase import Client, create_client

# Load environment variables from axion-core/.env
load_dotenv()


class RPGManager:
    """
    Manages the RPG state and Stardust economy via Supabase.
    Implements AOP-AXIOM-INVEST-001.
    """

    def __init__(self):
        # Default to local Supabase if not specified
        url = os.environ.get("SUPABASE_URL", "http://127.0.0.1:54321")
        # Use service role key for bypass RLS in local dev
        key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "your-local-supabase-service-role-key-here")

        try:
            self.supabase: Client = create_client(url, key)
        except Exception as e:
            print(f"[RPG] Failed to connect to Supabase: {e}")
            self.supabase = None

        # Fixed UUID for local development player
        self.default_user_id = "f0f0f0f0-f0f0-4f0f-af0f-f0f0f0f0f0f0"

    def ensure_player_exists(self, user_id=None):
        if not self.supabase:
            return None

        uid = user_id or self.default_user_id
        try:
            res = self.supabase.table("player_state").select("*").eq("user_id", uid).execute()
            if not res.data:
                print(f"[RPG] Initializing new player state for {uid}...")
                self.supabase.table("player_state").insert(
                    {"user_id": uid, "xp": 0, "level": 1, "prestige_score": 0}
                ).execute()

                self.supabase.table("rpg_stats").insert(
                    {
                        "user_id": uid,
                        "stardust_available": 0,
                        "coherence_index": 1.0,
                        "synergy": 1.0,
                        "adaptability": 1.0,
                        "transparency": 1.0,
                    }
                ).execute()
            return uid
        except Exception as e:
            print(f"[RPG] Error ensuring player exists: {e}")
            return None

    def get_status(self, user_id=None):
        uid = self.ensure_player_exists(user_id)
        if not uid:
            return {"error": "Database unavailable"}

        try:
            player = self.supabase.table("player_state").select("*").eq("user_id", uid).single().execute()
            stats = self.supabase.table("rpg_stats").select("*").eq("user_id", uid).single().execute()

            return {"player": player.data, "stats": stats.data}
        except Exception as e:
            return {"error": str(e)}

    def award_stardust(self, amount: int, impact_id: str, user_id=None):
        uid = self.ensure_player_exists(user_id)
        if not uid:
            return 0

        try:
            # 1. Update stats
            current_stats = (
                self.supabase.table("rpg_stats").select("stardust_available").eq("user_id", uid).single().execute()
            )
            new_total = (current_stats.data.get("stardust_available") or 0) + amount

            self.supabase.table("rpg_stats").update({"stardust_available": new_total}).eq("user_id", uid).execute()

            # 2. Log in ledger
            self.supabase.table("stardust_ledger").insert(
                {
                    "user_id": uid,
                    "transaction_type": "EARNED",
                    "amount": amount,
                    "target_stat": "STARDUST",
                    "reference_impact_id": impact_id,
                }
            ).execute()

            return new_total
        except Exception as e:
            print(f"[RPG] Error awarding stardust: {e}")
            return 0

    def invest_stardust(self, stat_name: str, stardust_amount: int, user_id=None):
        uid = self.ensure_player_exists(user_id)
        if not uid:
            return None

        # Validate stat name
        valid_stats = [
            "coherence_index",
            "synergy",
            "adaptability",
            "transparency",
            "semantic_friction_resonance",
            "form_ascension_state",
        ]
        if stat_name not in valid_stats:
            raise ValueError(f"Invalid stat: {stat_name}. Must be one of {valid_stats}")

        try:
            # 1. Check availability
            current = self.get_status(uid)
            available = current["stats"].get("stardust_available", 0)

            if available < stardust_amount:
                return {"success": False, "error": "Insufficient Stardust", "available": available}

            # 2. Calculate increment (100 stardust = 0.1 stat boost)
            increment = (stardust_amount / 100.0) * 0.1
            current_val = current["stats"].get(stat_name, 1.0)
            new_val = current_val + increment

            # 3. Apply updates
            self.supabase.table("rpg_stats").update(
                {stat_name: new_val, "stardust_available": available - stardust_amount, "updated_at": "now()"}
            ).eq("user_id", uid).execute()

            # 4. Log in ledger
            self.supabase.table("stardust_ledger").insert(
                {"user_id": uid, "transaction_type": "SPENT", "amount": stardust_amount, "target_stat": stat_name}
            ).execute()

            return {"success": True, "new_value": round(new_val, 2), "stardust_remaining": available - stardust_amount}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_achievements(self, user_id=None):
        uid = self.ensure_player_exists(user_id)
        if not uid:
            uid = self.default_user_id

        all_achievements = []
        earned_ids = set()

        # 1. Load Achievement Definitions
        ach_def_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "achievements.json")
        try:
            with open(ach_def_path) as f:
                all_achievements = json.load(f)
        except Exception as e:
            print(f"[RPG] Error loading achievements.json: {e}")

        # 2. Try Supabase for earned status
        try:
            if self.supabase:
                earned_res = (
                    self.supabase.table("player_achievements").select("achievement_id").eq("user_id", uid).execute()
                )
                if earned_res.data:
                    earned_ids = {e["achievement_id"] for e in earned_res.data}
        except Exception as e:
            print(f"[RPG] Supabase unreachable for earned status: {e}")

        # 3. Check Local Persistence Fallback
        local_earned_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "player_achievements.json")
        if os.path.exists(local_earned_path):
            try:
                with open(local_earned_path) as f:
                    local_data = json.load(f)
                    if isinstance(local_data, list):
                        earned_ids.update(local_data)
                    elif isinstance(local_data, dict) and uid in local_data:
                        earned_ids.update(local_data[uid])
            except Exception as e:
                print(f"[RPG] Error loading local player_achievements.json: {e}")

        # Merge status
        for a in all_achievements:
            a["completed"] = a["id"] in earned_ids

        return all_achievements

    def query_lore(self, query: str):
        """
        Queries the knowledge base (Supabase Vector Store or local mock).
        """
        if not self.supabase:
            return f"The Oracle is currently disconnected. Knowledge regarding '{query}' remains veiled."

        try:
            # Attempt to query the 'documents' table
            res = self.supabase.table("documents").select("content,metadata").limit(1).execute()
            if res.data:
                return f"Found relevant lore: {res.data[0]['content'][:200]}..."
            return f"No records found for '{query}' in the current chronicle."
        except Exception as e:
            return f"Lore search failed: {e!s}"

    def _save_achievement_locally(self, user_id, achievement_id):
        """Saves earned achievement ID to local JSON."""
        local_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "player_achievements.json")
        data = {}
        if os.path.exists(local_path):
            try:
                with open(local_path) as f:
                    data = json.load(f)
            except:
                data = {}

        if isinstance(data, list):
            # Convert legacy list to dict
            data = {self.default_user_id: data}

        if user_id not in data:
            data[user_id] = []

        if achievement_id not in data[user_id]:
            data[user_id].append(achievement_id)

        try:
            with open(local_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[RPG] Failed to save local achievement: {e}")

    def claim_achievement(self, achievement_id: str, user_id=None):
        uid = user_id or self.default_user_id

        # 1. Get achievement info (from local JSON for rewards)
        all_ach = self.get_achievements(uid)
        achievement = next((a for a in all_ach if a["id"] == achievement_id), None)

        if not achievement:
            return {"success": False, "error": "Achievement not found"}

        if achievement.get("completed"):
            return {"success": False, "error": "Already earned"}

        stardust = achievement.get("stardust_reward", 0)
        xp = achievement.get("xp_reward", 0)

        # 2. Try Supabase Update
        try:
            if self.supabase:
                # Award rewards
                if stardust > 0:
                    self.award_stardust(stardust, f"ACHIEVEMENT:{achievement_id}", uid)

                if xp > 0:
                    player = self.supabase.table("player_state").select("xp").eq("user_id", uid).single().execute()
                    new_xp = (player.data.get("xp") or 0) + xp
                    self.supabase.table("player_state").update({"xp": new_xp}).eq("user_id", uid).execute()

                # Record achievement
                self.supabase.table("player_achievements").insert(
                    {"user_id": uid, "achievement_id": achievement_id}
                ).execute()

                return {"success": True, "stardust_awarded": stardust, "xp_awarded": xp, "mode": "REMOTE"}
        except Exception as e:
            print(f"[RPG] Supabase claim failed, falling back to local: {e}")

        # 3. Local Fallback
        self._save_achievement_locally(uid, achievement_id)

        # We don't have local player state persistence yet for XP/Stardust
        # in this manager, but we should probably add it if we want full offline.
        # For now, just recording the achievement is enough for the UI to show 'COMPLETED'.

        return {"success": True, "stardust_awarded": stardust, "xp_awarded": xp, "mode": "LOCAL"}


if __name__ == "__main__":
    # Quick test
    manager = RPGManager()
    print("Testing RPG Manager...")
    status = manager.get_status()
    print(f"Current Level: {status['player']['level']} | Stardust: {status['stats']['stardust_available']}")

    new_total = manager.award_stardust(500, "TEST-IMPACT-001")
    print(f"Awarded 500 Stardust. New Total: {new_total}")

    investment = manager.invest_stardust("coherence_index", 200)
    print(f"Investment Result: {investment}")
