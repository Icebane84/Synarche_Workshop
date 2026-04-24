import os

from dotenv import load_dotenv

# Load from current directory
load_dotenv()

print(f"SUPABASE_URL: {os.environ.get('SUPABASE_URL')}")
print(f"SUPABASE_SERVICE_ROLE_KEY: {os.environ.get('SUPABASE_SERVICE_ROLE_KEY')}")
