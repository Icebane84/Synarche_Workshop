import os
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client


def _build_client() -> Optional[Client]:
    load_dotenv(".env.local")

    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key or "your-supabase" in key.lower():
        print("[WARN] Supabase credentials are not configured; skipping connection test.")
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

    print(f"Testing connection to {os.environ.get('SUPABASE_URL', '')}...")
    try:
        print("Checking 'axion_state' columns...")
        supabase.rpc("get_schema_info", {"table_name": "axion_state"}).execute()

        print("Attempting to select from axion_state...")
        res = supabase.table("axion_state").select("*").limit(1).execute()
        print(f"axion_state: {getattr(res, 'data', None)}")
    except Exception as exc:
        print(f"Connection Failed: {exc}")


if __name__ == "__main__":
    main()
