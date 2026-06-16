import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv(".env.local")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(url, key)

print("Fetching table list...")
try:
    # We can try to query information_schema via a raw SQL if we had that,
    # but with supabase-py we can try to guess or use the 'rpc' if we have a custom one.
    # Alternatively, we can try to access tables we know and see if they exist.

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
            supabase.table(table).select("count", count="exact").limit(1).execute()
            print(f"[EXISTS] {table}")
        except Exception as e:
            if "PGRST204" in str(e) or "PGRST205" in str(e):
                print(f"[MISSING] {table}")
            else:
                print(f"[ERROR] {table}: {e}")

except Exception as e:
    print(f"Error: {e}")
