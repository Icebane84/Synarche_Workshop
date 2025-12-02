"""
Verification script for Supabase connection.
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from backend.config import settings
    from backend.supabase_client import get_supabase

    print(f"Checking Supabase configuration...")
    if not settings.is_supabase_configured:
        print("[WARNING] Supabase credentials not found in .env")
        print("Please set SUPABASE_URL and SUPABASE_KEY")
        sys.exit(1)

    print("Initializing Supabase client...")
    client = get_supabase()
    print("[SUCCESS] Supabase client initialized successfully.")
    print(f"Supabase URL: {settings.SUPABASE_URL}")

except Exception as e:
    print(f"[ERROR] Failed to initialize Supabase client: {e}")
    sys.exit(1)
