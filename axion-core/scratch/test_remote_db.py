import os

from dotenv import load_dotenv
from supabase import Client, create_client

# Load from .env.local
load_dotenv(".env.local")

url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
key = os.environ.get("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY")

print(f"Connecting to: {url}")
try:
    supabase: Client = create_client(url, key)
    res = supabase.table("achievements").select("*").limit(1).execute()
    print("Success! Achievements found.")
    print(res.data)
except Exception as e:
    print(f"Failed: {e}")
