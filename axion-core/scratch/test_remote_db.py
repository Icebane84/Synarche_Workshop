import os
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client


def _build_client() -> Optional[Client]:
    load_dotenv(".env.local")

    url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL", "")
    key = os.environ.get("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY", "")
    if not url or not key or "your-supabase" in key.lower():
        print("[WARN] Supabase credentials are not configured; skipping database check.")
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

    print(f"Connecting to: {os.environ.get('NEXT_PUBLIC_SUPABASE_URL', '')}")
    try:
        res = supabase.table("achievements").select("*").limit(1).execute()
        print("Success! Achievements found.")
        print(getattr(res, "data", None))
    except Exception as exc:
        print(f"Failed: {exc}")


if __name__ == "__main__":
    main()
