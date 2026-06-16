from dotenv import load_dotenv
from supabase import Client, create_client

# Load from .env.local explicitly for testing
load_dotenv(".env.local")

url = "https://rtjkhpotguwngfpvhfej.supabase.co"
key = "your-supabase-service-role-key-here"

print(f"Testing connection to {url}...")
try:
    supabase: Client = create_client(url, key)
    # Check schema of axion_state
    print("Checking 'axion_state' columns...")
    res = supabase.rpc("get_schema_info", {"table_name": "axion_state"}).execute()
    # If get_schema_info doesn't exist, we can try a raw query if we have a custom rpc or just check what we get from a select * limit 1
    # Actually, we can just use the error messages from table calls to infer existence.
    # To get columns without rpc, we can try to select a non-existent column and see the error.

    # Let's try to insert a dummy record to see if it works
    print("Attempting to select from axion_state...")
    res = supabase.table("axion_state").select("*").limit(1).execute()
    print(f"axion_state: {res.data}")

except Exception as e:
    print(f"Connection Failed: {e}")
