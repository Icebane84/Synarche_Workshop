import os
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client


def _build_client() -> Optional[Client]:
    load_dotenv(".env.local")

    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key or "your-supabase" in key.lower():
        print("[WARN] Supabase credentials are not configured; skipping connection checks.")
        return None

    try:
        return create_client(url, key)
    except Exception as exc:
        print(f"[WARN] Failed to initialize Supabase client: {exc}")
        return None


def main() -> None:
    supabase = _build_client()
    if supabase is None:
        return

    print("Fetching table list...")
    try:
        tables_to_check = [
            "player_state",
            "axion_state",
            "rpg_stats",
            "stardust_ledger",
            "achievements",
            "player_achievements",
            "documents",
        ]
        for table in tables_to_check:
            try:
                supabase.table(table).select("count", count=None).limit(1).execute()
                print(f"[EXISTS] {table}")
            except Exception as exc:
                if "PGRST204" in str(exc) or "PGRST205" in str(exc):
                    print(f"[MISSING] {table}")
                else:
                    print(f"[ERROR] {table}: {exc}")

    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
