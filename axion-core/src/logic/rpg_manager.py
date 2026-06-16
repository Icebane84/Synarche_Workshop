"""
artifact_anchor:
  id: CORE.RPG_MANAGER.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

# ## **[ARTIFACT START]**.
#
# ## **Block A: The Identification Lock (UIP-V15)**
#
# | Key               | Value                             | Description       |
# | :---------------- | :-------------------------------- | :---------------- |
# | **Artifact ID**   | `CORE.logic.rpg_manager`          | The Sovereign ID. |
# | **Official Name** | `rpg_manager.py`                   | The Filename.     |
# | **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
# | **Domain**        | `CORE`                            | The Subject.      |
# | **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
# | **Relations**     | `GOVERNED_BY: CORE.Codex.RPG`     | The Network.      |
#
# ---
#
# ## **Block B: Sovereign Identity (The Tarot Mask)**
#
# | Mask ID | Name | Role |
# | :--- | :--- | :--- |
# | VIII | **Justice** | The Arbiter of Economy and Achievement Balance. |
#
# ---
#
# ## **Block C: State Vector (AGP-001)**
#
# | State Field   | Value     |
# | :------------ | :-------- |
# | **Economy**    | `Stardust` |
# | **Persistence**| `Supabase` |
# | **Stability**  | `Stable`   |
#
# ## **[ARTIFACT END]**

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, TypedDict
from dotenv import load_dotenv

try:
    from supabase import Client, create_client
    _SUPABASE_AVAILABLE = True
except ImportError:
    _SUPABASE_AVAILABLE = False


class RPGEngine(TypedDict):
    user_id: str
    level: int
    xp: int
    prestige_score: int
    stardust_available: int
    coherence_index: float
    synergy: float
    adaptability: float
    transparency: float
    semantic_friction_resonance: float
    form_ascension_state: float
    creative_spark: float
    achievements: list[str]
    active_quest_log: list[str]
    prestige_class: str
    updated_at: str


class RPGManager:
    """Manages the RPG state and Stardust economy locally via SQLite.
    Implements AOP-AXIOM-INVEST-001 and conforms to OMEGA v15.0.
    """

    def __init__(self, db_path: str | None = None) -> None:
        """Initializes the RPG Manager with local SQLite store."""
        if not db_path:
            # Resolve relative to workspace root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
            db_path = os.path.join(base_dir, ".agent", "rpg_state.db")
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(db_path))))

        self.db_path = db_path
        # Fixed UUID for local development player
        self.default_user_id: str = "f0f0f0f0-f0f0-4f0f-af0f-f0f0f0f0f0f0"

        # Initialize SQLite database schema
        self._init_sqlite_db()

        # Load environment variables in correct cascading order
        # 1. Base workspace env
        load_dotenv(os.path.join(base_dir, ".env"))
        # 2. Workspace local overrides
        load_dotenv(os.path.join(base_dir, ".env.local"), override=True)
        # 3. Base subproject env
        subproject_dir = os.path.join(base_dir, "axion-core")
        load_dotenv(os.path.join(subproject_dir, ".env"), override=True)
        # 4. Subproject local overrides
        load_dotenv(os.path.join(subproject_dir, ".env.local"), override=True)

        # Initialize Supabase client if configured
        self.use_supabase: bool = False
        self.supabase_client: Any = None

        if _SUPABASE_AVAILABLE:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
            if url and key and "YOUR-SERVICE-ROLE-KEY" not in key and "your-supabase" not in key:
                try:
                    self.supabase_client = create_client(url, key)
                    self.use_supabase = True
                    print(f"[RPG] Supabase remote connection active for: {url}")
                except Exception as e:
                    print(f"[RPG] Failed to initialize Supabase client: {e}")

    def _init_sqlite_db(self) -> None:
        """Initializes the local SQLite database schema if missing."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()

            # Create player_state table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_state (
                    user_id TEXT PRIMARY KEY,
                    xp INTEGER NOT NULL DEFAULT 0,
                    level INTEGER NOT NULL DEFAULT 1,
                    prestige_score INTEGER NOT NULL DEFAULT 0
                )
            """)

            # Create rpg_stats table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rpg_stats (
                    user_id TEXT PRIMARY KEY,
                    stardust_available INTEGER NOT NULL DEFAULT 0,
                    coherence_index REAL NOT NULL DEFAULT 1.0,
                    synergy REAL NOT NULL DEFAULT 1.0,
                    adaptability REAL NOT NULL DEFAULT 1.0,
                    transparency REAL NOT NULL DEFAULT 1.0,
                    semantic_friction_resonance REAL NOT NULL DEFAULT 1.0,
                    form_ascension_state REAL NOT NULL DEFAULT 1.0,
                    creative_spark REAL NOT NULL DEFAULT 1.0,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES player_state(user_id)
                )
            """)

            # Create stardust_ledger table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stardust_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    target_stat TEXT NOT NULL,
                    reference_impact_id TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES player_state(user_id)
                )
            """)

            # Create player_achievements table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_achievements (
                    user_id TEXT NOT NULL,
                    achievement_id TEXT NOT NULL,
                    PRIMARY KEY (user_id, achievement_id),
                    FOREIGN KEY(user_id) REFERENCES player_state(user_id)
                )
            """)

            conn.commit()
        finally:
            conn.close()

    def ensure_player_exists(self, user_id: str | None = None) -> str | None:
        """Verifies that a player entry exists in SQLite, creating one if missing.

        Args:
            user_id: The UUID of the player. Defaults to the system default user.

        Returns:
            The user_id if successful, None otherwise.

        """
        uid: str = user_id or self.default_user_id
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()

            # Check player_state
            cursor.execute("SELECT user_id FROM player_state WHERE user_id = ?", (uid,))
            row = cursor.fetchone()

            if not row:
                print(f"[RPG] Initializing new player state for {uid}...")
                cursor.execute(
                    "INSERT INTO player_state (user_id, xp, level, prestige_score) VALUES (?, 0, 1, 0)",
                    (uid,),
                )

                now_str = datetime.now().isoformat()
                cursor.execute(
                    """INSERT INTO rpg_stats (
                        user_id, stardust_available, coherence_index, synergy, adaptability,
                        transparency, semantic_friction_resonance, form_ascension_state,
                        creative_spark, updated_at
                    ) VALUES (?, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, ?)""",
                    (uid, now_str),
                )
                conn.commit()
            return uid
        except Exception as e:
            print(f"[RPG] Error ensuring player exists: {e}")
            return None
        finally:
            conn.close()

    def _ensure_remote_player_exists(self, uid: str) -> None:
        """Helper to ensure a player profile exists in the remote database."""
        if not self.use_supabase or not self.supabase_client:
            return

        try:
            res = self.supabase_client.table("player_state").select("user_id").eq("user_id", uid).execute()
            if not res.data:
                print(f"[RPG] Initializing remote player state for {uid}...")
                self.supabase_client.table("player_state").insert({
                    "user_id": uid,
                    "xp": 0,
                    "level": 1,
                    "prestige_score": 0
                }).execute()

                self.supabase_client.table("rpg_stats").insert({
                    "user_id": uid,
                    "stardust_available": 0,
                    "coherence_index": 1.0,
                    "synergy": 1.0,
                    "adaptability": 1.0,
                    "transparency": 1.0,
                    "semantic_friction_resonance": 1.0,
                    "form_ascension_state": 1.0,
                    "creative_spark": 1.0,
                    "updated_at": datetime.now().isoformat()
                }).execute()
        except Exception as e:
            print(f"[RPG] Error ensuring remote player exists: {e}")
            raise e

    def get_status(self, user_id: str | None = None) -> RPGEngine | dict[str, Any]:
        """Retrieves the complete status aligned with the RPGEngine TypedDict.

        Args:
            user_id: The UUID of the player.

        Returns:
            A dictionary conforming to the RPGEngine schema.

        """
        uid: str | None = self.ensure_player_exists(user_id)
        if not uid:
            return {"error": "Database unavailable"}

        # Attempt to pull from Supabase first if enabled
        if self.use_supabase and self.supabase_client:
            try:
                self._ensure_remote_player_exists(uid)
                res_player = self.supabase_client.table("player_state").select("*").eq("user_id", uid).execute()
                res_stats = self.supabase_client.table("rpg_stats").select("*").eq("user_id", uid).execute()
                if res_player.data and res_stats.data:
                    player = res_player.data[0]
                    stats = res_stats.data[0]
                    ach_status = self.get_achievements(uid)
                    completed_achievements = [a["id"] for a in ach_status if a.get("completed")]
                    
                    return {
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
                        "creative_spark": stats.get("creative_spark", 1.0),
                        "achievements": completed_achievements,
                        "active_quest_log": [],
                        "prestige_class": player.get("prestige_class", "Novice"),
                        "updated_at": stats.get("updated_at", ""),
                    }
            except Exception as e:
                print(f"[RPG] Supabase error in get_status: {e}. Falling back to SQLite.")

        # Fall back to local SQLite
        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM player_state WHERE user_id = ?", (uid,))
            player_row = cursor.fetchone()

            cursor.execute("SELECT * FROM rpg_stats WHERE user_id = ?", (uid,))
            stats_row = cursor.fetchone()

            if not player_row or not stats_row:
                return {"error": "Player state or stats not found"}

            player = dict(player_row)
            stats = dict(stats_row)

            # Fetch achievements
            achievements = self.get_achievements(uid)
            completed_achievements = [
                a["id"] for a in achievements if a.get("completed")
            ]

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
                "semantic_friction_resonance": stats.get(
                    "semantic_friction_resonance", 1.0
                ),
                "form_ascension_state": stats.get("form_ascension_state", 1.0),
                "creative_spark": stats.get("creative_spark", 1.0),
                "achievements": completed_achievements,
                "active_quest_log": [],  # To be implemented
                "prestige_class": "Novice",  # Default
                "updated_at": stats.get("updated_at", ""),
            }

            return engine_state
        except Exception as e:
            return {"error": str(e)}
        finally:
            conn.close()

    def award_stardust(
        self, amount: int, impact_id: str, user_id: str | None = None
    ) -> int:
        """Awards Stardust to a player and logs the transaction in the ledger.

        Args:
            amount: Amount of Stardust to award.
            impact_id: The reference ID of the action/impact that triggered the reward.
            user_id: The UUID of the player.

        Returns:
            The new total Stardust balance.

        """
        uid: str | None = self.ensure_player_exists(user_id)
        if not uid:
            return 0

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()

            # 1. Update stats
            cursor.execute(
                "SELECT stardust_available FROM rpg_stats WHERE user_id = ?", (uid,)
            )
            row = cursor.fetchone()
            current_stardust = row[0] if row else 0
            new_total: int = current_stardust + amount

            cursor.execute(
                "UPDATE rpg_stats SET stardust_available = ?, updated_at = ? WHERE user_id = ?",
                (new_total, datetime.now().isoformat(), uid),
            )

            # 2. Log in ledger
            cursor.execute(
                """INSERT INTO stardust_ledger (
                    user_id, transaction_type, amount, target_stat, reference_impact_id, created_at
                ) VALUES (?, 'EARNED', ?, 'STARDUST', ?, ?)""",
                (uid, amount, impact_id, datetime.now().isoformat()),
            )

            conn.commit()

            # 3. Mirror to Supabase if enabled
            if self.use_supabase and self.supabase_client:
                try:
                    self._ensure_remote_player_exists(uid)
                    
                    # Update stats remotely
                    self.supabase_client.table("rpg_stats").update({
                        "stardust_available": new_total,
                        "updated_at": datetime.now().isoformat()
                    }).eq("user_id", uid).execute()

                    # Log remotely
                    self.supabase_client.table("stardust_ledger").insert({
                        "user_id": uid,
                        "transaction_type": "EARNED",
                        "amount": amount,
                        "target_stat": "STARDUST",
                        "reference_impact_id": impact_id
                    }).execute()
                except Exception as e:
                    print(f"[RPG] Supabase error mirroring award_stardust: {e}")

            return new_total
        except Exception as e:
            print(f"[RPG] Error awarding stardust: {e}")
            return 0
        finally:
            conn.close()

    def invest_stardust(
        self, stat_name: str, stardust_amount: int, user_id: str | None = None
    ) -> dict[str, Any]:
        """Invests Stardust into a specific stat to increase its value.

        Args:
            stat_name: The internal name of the stat to boost.
            stardust_amount: Amount of Stardust to spend.
            user_id: The UUID of the player.

        Returns:
            A status dictionary indicating success or failure.

        """
        uid: str | None = self.ensure_player_exists(user_id)
        if not uid:
            return {"success": False, "error": "Database unavailable"}

        # Validate stat name
        valid_stats: list[str] = [
            "coherence_index",
            "synergy",
            "adaptability",
            "transparency",
            "semantic_friction_resonance",
            "form_ascension_state",
            "creative_spark",
        ]
        if stat_name not in valid_stats:
            raise ValueError(f"Invalid stat: {stat_name}. Must be one of {valid_stats}")

        conn = sqlite3.connect(self.db_path)
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 1. Check availability
            cursor.execute("SELECT * FROM rpg_stats WHERE user_id = ?", (uid,))
            row = cursor.fetchone()
            if not row:
                return {"success": False, "error": "Player stats not found"}
            stats = dict(row)

            available: int = stats.get("stardust_available", 0)

            if available < stardust_amount:
                return {
                    "success": False,
                    "error": "Insufficient Stardust",
                    "available": available,
                }

            # 2. Calculate increment (100 stardust = 0.1 stat boost)
            increment: float = (stardust_amount / 100.0) * 0.1
            current_val: float = stats.get(stat_name, 1.0)
            new_val: float = current_val + increment

            # 3. Apply updates
            cursor.execute(
                f"UPDATE rpg_stats SET {stat_name} = ?, stardust_available = ?, updated_at = ? WHERE user_id = ?",
                (new_val, available - stardust_amount, datetime.now().isoformat(), uid),
            )

            # 4. Log in ledger
            cursor.execute(
                """INSERT INTO stardust_ledger (
                    user_id, transaction_type, amount, target_stat, reference_impact_id, created_at
                ) VALUES (?, 'SPENT', ?, ?, NULL, ?)""",
                (uid, stardust_amount, stat_name, datetime.now().isoformat()),
            )

            conn.commit()

            # 5. Mirror to Supabase if enabled
            if self.use_supabase and self.supabase_client:
                try:
                    self._ensure_remote_player_exists(uid)

                    # Update stats remotely
                    self.supabase_client.table("rpg_stats").update({
                        stat_name: new_val,
                        "stardust_available": available - stardust_amount,
                        "updated_at": datetime.now().isoformat()
                    }).eq("user_id", uid).execute()

                    # Log ledger remotely
                    self.supabase_client.table("stardust_ledger").insert({
                        "user_id": uid,
                        "transaction_type": "SPENT",
                        "amount": stardust_amount,
                        "target_stat": stat_name,
                        "reference_impact_id": None
                    }).execute()
                except Exception as e:
                    print(f"[RPG] Supabase error mirroring invest_stardust: {e}")

            return {
                "success": True,
                "new_value": round(new_val, 2),
                "stardust_remaining": available - stardust_amount,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()

    def get_achievements(self, user_id: str | None = None) -> list[dict[str, Any]]:
        """Retrieves all achievements and marks those completed by the user.

        Args:
            user_id: The UUID of the player.

        Returns:
            A list of achievement dictionaries with 'completed' status.

        """
        uid: str = user_id or self.ensure_player_exists(user_id) or self.default_user_id

        all_achievements: list[dict[str, Any]] = []
        earned_ids: set = set()

        # 1. Load Achievement Definitions
        ach_def_path: str = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "achievements.json"
        )
        try:
            with open(ach_def_path) as f:
                all_achievements = json.load(f)
        except Exception as e:
            print(f"[RPG] Error loading achievements.json: {e}")

        # 2. Query Supabase or SQLite for earned achievements
        fetched_from_supabase = False
        if self.use_supabase and self.supabase_client:
            try:
                self._ensure_remote_player_exists(uid)
                res = self.supabase_client.table("player_achievements").select("achievement_id").eq("user_id", uid).execute()
                earned_ids = {row["achievement_id"] for row in res.data} if res.data else set()
                fetched_from_supabase = True
            except Exception as e:
                print(f"[RPG] Supabase error checking achievements: {e}. Falling back to SQLite.")

        if not fetched_from_supabase:
            conn = sqlite3.connect(self.db_path)
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT achievement_id FROM player_achievements WHERE user_id = ?",
                    (uid,),
                )
                rows = cursor.fetchall()
                earned_ids = {row[0] for row in rows}
            except Exception as e:
                print(f"[RPG] SQLite error checking achievements: {e}")
            finally:
                conn.close()

        # Merge status
        for a in all_achievements:
            a["completed"] = a["id"] in earned_ids

        return all_achievements

    def query_lore(self, query: str) -> str:
        """Queries the local knowledge base.

        Args:
            query: The search query for the lore.

        Returns:
            A string response containing relevant lore or a failure message.

        """
        return f"The Oracle is currently operating offline. Knowledge regarding '{query}' is kept locally within your governance chronicles."

    def claim_achievement(
        self, achievement_id: str, user_id: str | None = None
    ) -> dict[str, Any]:
        """Claims an achievement reward for a player in SQLite.

        Args:
            achievement_id: The ID of the achievement to claim.
            user_id: The UUID of the player.

        Returns:
            A status dictionary indicating the rewards awarded.

        """
        uid: str = user_id or self.default_user_id

        # 1. Get achievement info (from local JSON for rewards)
        all_ach: list[dict[str, Any]] = self.get_achievements(uid)
        achievement: dict[str, Any] | None = next(
            (a for a in all_ach if a["id"] == achievement_id), None
        )

        if not achievement:
            return {"success": False, "error": "Achievement not found"}

        if achievement.get("completed"):
            return {"success": False, "error": "Already earned"}

        stardust: int = achievement.get("stardust_reward", 0)
        xp: int = achievement.get("xp_reward", 0)

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()

            # Award rewards (stardust)
            if stardust > 0:
                # Get current stardust
                cursor.execute(
                    "SELECT stardust_available FROM rpg_stats WHERE user_id = ?", (uid,)
                )
                row = cursor.fetchone()
                current_stardust = row[0] if row else 0
                new_stardust = current_stardust + stardust
                cursor.execute(
                    "UPDATE rpg_stats SET stardust_available = ?, updated_at = ? WHERE user_id = ?",
                    (new_stardust, datetime.now().isoformat(), uid),
                )

                # Log transaction
                cursor.execute(
                    """INSERT INTO stardust_ledger (
                        user_id, transaction_type, amount, target_stat, reference_impact_id, created_at
                    ) VALUES (?, 'EARNED', ?, 'STARDUST', ?, ?)""",
                    (
                        uid,
                        stardust,
                        f"ACHIEVEMENT:{achievement_id}",
                        datetime.now().isoformat(),
                    ),
                )

            # Award rewards (xp)
            if xp > 0:
                cursor.execute("SELECT xp FROM player_state WHERE user_id = ?", (uid,))
                row = cursor.fetchone()
                current_xp = row[0] if row else 0
                new_xp = current_xp + xp
                cursor.execute(
                    "UPDATE player_state SET xp = ? WHERE user_id = ?", (new_xp, uid)
                )

            # Record achievement
            cursor.execute(
                "INSERT INTO player_achievements (user_id, achievement_id) VALUES (?, ?)",
                (uid, achievement_id),
            )

            conn.commit()

            # Mirror to Supabase if enabled
            supabase_success = False
            if self.use_supabase and self.supabase_client:
                try:
                    self._ensure_remote_player_exists(uid)

                    # 1. Update player_state remotely for XP
                    if xp > 0:
                        self.supabase_client.table("player_state").update({
                            "xp": new_xp
                        }).eq("user_id", uid).execute()

                    # 2. Update rpg_stats remotely for Stardust
                    if stardust > 0:
                        self.supabase_client.table("rpg_stats").update({
                            "stardust_available": new_stardust,
                            "updated_at": datetime.now().isoformat()
                        }).eq("user_id", uid).execute()

                        # Log ledger remotely
                        self.supabase_client.table("stardust_ledger").insert({
                            "user_id": uid,
                            "transaction_type": "EARNED",
                            "amount": stardust,
                            "target_stat": "STARDUST",
                            "reference_impact_id": f"ACHIEVEMENT:{achievement_id}"
                        }).execute()

                    # 3. Record achievement remotely
                    self.supabase_client.table("player_achievements").insert({
                        "user_id": uid,
                        "achievement_id": achievement_id
                    }).execute()

                    supabase_success = True
                except Exception as e:
                    print(f"[RPG] Supabase error mirroring claim_achievement: {e}")

            return {
                "success": True,
                "stardust_awarded": stardust,
                "xp_awarded": xp,
                "mode": "SYNCED" if (self.use_supabase and self.supabase_client and supabase_success) else "LOCAL",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()


if __name__ == "__main__":
    # Quick test
    manager = RPGManager()
    print("Testing RPG Manager...")
    status = manager.get_status()
    if "error" not in status:
        print(
            f"Current Level: {status.get('level')} | Stardust: {status.get('stardust_available')}"
        )

        new_total: int = manager.award_stardust(500, "TEST-IMPACT-001")
        print(f"Awarded 500 Stardust. New Total: {new_total}")

        investment: dict[str, Any] = manager.invest_stardust("coherence_index", 200)
        print(f"Investment Result: {investment}")
    else:
        print(f"Test failed: {status['error']}")


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.logic.rpg_manager VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-04-28
# ---
