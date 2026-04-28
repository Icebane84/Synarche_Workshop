"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.logic.rpg_manager`          | The Sovereign ID. |
| **Official Name** | `rpg_manager.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                            | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.RPG`     | The Network.      |

---

## **Block B: Sovereign Identity (The Tarot Mask)**

| Mask ID | Name | Role |
| :--- | :--- | :--- |
| VIII | **Justice** | The Arbiter of Economy and Achievement Balance. |

---

## **Block C: State Vector (AGP-001)**

| State Field   | Value     |
| :------------ | :-------- |
| **Economy**    | `Stardust` |
| **Persistence**| `Supabase` |
| **Stability**  | `Stable`   |

## **[ARTIFACT END]**
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from supabase import Client, create_client

# Add forge to path if necessary
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from forge.enums import RPGEngine

# Load environment variables from axion-core/.env
load_dotenv()


class RPGManager:
    """
    Manages the RPG state and Stardust economy via Supabase.
    Implements AOP-AXIOM-INVEST-001 and conforms to OMEGA v15.0.
    """

    def __init__(self) -> None:
        """
        Initializes the RPG Manager with Supabase credentials.
        """
        # Default to local Supabase if not specified
        url: str = os.environ.get("SUPABASE_URL", "http://127.0.0.1:54321")
        # Use service role key for bypass RLS in local dev
        key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "your-local-supabase-service-role-key-here")

        try:
            self.supabase: Optional[Client] = create_client(url, key)
        except Exception as e:
            print(f"[RPG] Failed to connect to Supabase: {e}")
            self.supabase = None

        # Fixed UUID for local development player
        self.default_user_id: str = "f0f0f0f0-f0f0-4f0f-af0f-f0f0f0f0f0f0"

    def ensure_player_exists(self, user_id: Optional[str] = None) -> Optional[str]:
        """
        Verifies that a player entry exists in Supabase, creating one if missing.
        
        Args:
            user_id: The UUID of the player. Defaults to the system default user.
            
        Returns:
            The user_id if successful, None otherwise.
        """
        if not self.supabase:
            return None

        uid: str = user_id or self.default_user_id
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
                        "semantic_friction_resonance": 1.0,
                        "form_ascension_state": 1.0,
                    }
                ).execute()
            return uid
        except Exception as e:
            print(f"[RPG] Error ensuring player exists: {e}")
            return None

    def get_status(self, user_id: Optional[str] = None) -> Union[RPGEngine, Dict[str, Any]]:
        """
        Retrieves the complete status aligned with the RPGEngine TypedDict.
        
        Args:
            user_id: The UUID of the player.
            
        Returns:
            A dictionary conforming to the RPGEngine schema.
        """
        uid: Optional[str] = self.ensure_player_exists(user_id)
        if not uid:
            return {"error": "Database unavailable"}

        try:
            player_res = self.supabase.table("player_state").select("*").eq("user_id", uid).single().execute()
            stats_res = self.supabase.table("rpg_stats").select("*").eq("user_id", uid).single().execute()
            
            player = player_res.data
            stats = stats_res.data
            
            # Fetch achievements
            achievements = self.get_achievements(uid)
            completed_achievements = [a["id"] for a in achievements if a.get("completed")]

            # Construct the RPGEngine object
            engine_state: RPGEngine = {
                "user_id": uid,
                "level": player.get("level", 1),
                "xp": player.get("xp", 0),
                "prestige_score": player.get("prestige_score", 0),
                "stardust_available": stats.get("stardust_available", 0),
                "coherence_index": stats.get("coherence_index", 1.0),
                "synergy": stats.get("synergy", 1.0),
                "adaptability": stats.get("adaptability", 1.0),
                "transparency": stats.get("transparency", 1.0),
                "semantic_friction_resonance": stats.get("semantic_friction_resonance", 1.0),
                "form_ascension_state": stats.get("form_ascension_state", 1.0),
                "achievements": completed_achievements,
                "active_quest_log": [], # To be implemented
                "prestige_class": "Novice", # Default
                "updated_at": stats.get("updated_at", "now()")
            }

            return engine_state
        except Exception as e:
            return {"error": str(e)}

    def award_stardust(self, amount: int, impact_id: str, user_id: Optional[str] = None) -> int:
        """
        Awards Stardust to a player and logs the transaction in the ledger.
        
        Args:
            amount: Amount of Stardust to award.
            impact_id: The reference ID of the action/impact that triggered the reward.
            user_id: The UUID of the player.
            
        Returns:
            The new total Stardust balance.
        """
        uid: Optional[str] = self.ensure_player_exists(user_id)
        if not uid:
            return 0

        try:
            # 1. Update stats
            current_stats = (
                self.supabase.table("rpg_stats").select("stardust_available").eq("user_id", uid).single().execute()
            )
            new_total: int = (current_stats.data.get("stardust_available") or 0) + amount

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

    def invest_stardust(self, stat_name: str, stardust_amount: int, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Invests Stardust into a specific stat to increase its value.
        
        Args:
            stat_name: The internal name of the stat to boost.
            stardust_amount: Amount of Stardust to spend.
            user_id: The UUID of the player.
            
        Returns:
            A status dictionary indicating success or failure.
        """
        uid: Optional[str] = self.ensure_player_exists(user_id)
        if not uid:
            return {"success": False, "error": "Database unavailable"}

        # Validate stat name
        valid_stats: List[str] = [
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
            current: Dict[str, Any] = self.get_status(uid)
            if "error" in current:
                return {"success": False, "error": current["error"]}
                
            available: int = current["stats"].get("stardust_available", 0)

            if available < stardust_amount:
                return {"success": False, "error": "Insufficient Stardust", "available": available}

            # 2. Calculate increment (100 stardust = 0.1 stat boost)
            increment: float = (stardust_amount / 100.0) * 0.1
            current_val: float = current["stats"].get(stat_name, 1.0)
            new_val: float = current_val + increment

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

    def get_achievements(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves all achievements and marks those completed by the user.
        
        Args:
            user_id: The UUID of the player.
            
        Returns:
            A list of achievement dictionaries with 'completed' status.
        """
        uid: str = user_id or self.ensure_player_exists(user_id) or self.default_user_id

        all_achievements: List[Dict[str, Any]] = []
        earned_ids: set = set()

        # 1. Load Achievement Definitions
        ach_def_path: str = os.path.join(os.path.dirname(__file__), "..", "..", "data", "achievements.json")
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
        local_earned_path: str = os.path.join(os.path.dirname(__file__), "..", "..", "data", "player_achievements.json")
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

    def query_lore(self, query: str) -> str:
        """
        Queries the knowledge base (Supabase Vector Store or local mock).
        
        Args:
            query: The search query for the lore.
            
        Returns:
            A string response containing relevant lore or a failure message.
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

    def _save_achievement_locally(self, user_id: str, achievement_id: str) -> None:
        """
        Saves earned achievement ID to local JSON for offline synchronization.
        
        Args:
            user_id: The UUID of the player.
            achievement_id: The ID of the earned achievement.
        """
        local_path: str = os.path.join(os.path.dirname(__file__), "..", "..", "data", "player_achievements.json")
        data: Dict[str, Any] = {}
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

    def claim_achievement(self, achievement_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Claims an achievement reward for a player.
        
        Args:
            achievement_id: The ID of the achievement to claim.
            user_id: The UUID of the player.
            
        Returns:
            A status dictionary indicating the rewards awarded.
        """
        uid: str = user_id or self.default_user_id

        # 1. Get achievement info (from local JSON for rewards)
        all_ach: List[Dict[str, Any]] = self.get_achievements(uid)
        achievement: Optional[Dict[str, Any]] = next((a for a in all_ach if a["id"] == achievement_id), None)

        if not achievement:
            return {"success": False, "error": "Achievement not found"}

        if achievement.get("completed"):
            return {"success": False, "error": "Already earned"}

        stardust: int = achievement.get("stardust_reward", 0)
        xp: int = achievement.get("xp_reward", 0)

        # 2. Try Supabase Update
        try:
            if self.supabase:
                # Award rewards
                if stardust > 0:
                    self.award_stardust(stardust, f"ACHIEVEMENT:{achievement_id}", uid)

                if xp > 0:
                    player = self.supabase.table("player_state").select("xp").eq("user_id", uid).single().execute()
                    new_xp: int = (player.data.get("xp") or 0) + xp
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

        return {"success": True, "stardust_awarded": stardust, "xp_awarded": xp, "mode": "LOCAL"}


if __name__ == "__main__":
    # Quick test
    manager = RPGManager()
    print("Testing RPG Manager...")
    status: Dict[str, Any] = manager.get_status()
    if "error" not in status:
        print(f"Current Level: {status['player']['level']} | Stardust: {status['stats']['stardust_available']}")

        new_total: int = manager.award_stardust(500, "TEST-IMPACT-001")
        print(f"Awarded 500 Stardust. New Total: {new_total}")

        investment: Dict[str, Any] = manager.invest_stardust("coherence_index", 200)
        print(f"Investment Result: {investment}")
    else:
        print(f"Test failed: {status['error']}")


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.logic.rpg_manager VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-04-28
# ---
