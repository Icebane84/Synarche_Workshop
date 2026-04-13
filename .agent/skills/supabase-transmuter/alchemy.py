import os
import json
import difflib
from datetime import datetime
from supabase import create_client, Client

# --- CONFIGURATION ---
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
try:
    supabase: Client = create_client(URL, KEY)
except:
    supabase = None

TARGET_TABLE = "knowledge_base"
HISTORY_TABLE = "knowledge_history"

def fetch_batch(limit=5):
    if not supabase: return []
    response = supabase.table(TARGET_TABLE)\
        .select("*")\
        .not_.contains("metadata", '{"version": "v10.0"}')\
        .limit(limit)\
        .execute()
    return response.data

def generate_diff(original: str, new: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(),
        new.splitlines(),
        fromfile='Legacy',
        tofile='Canonized',
        lineterm=''
    )
    return '\n'.join(diff)

def commit_transmutation(id: str, new_content: str, new_title: str, categorization: dict):
    if not supabase: return {"error": "No Connection"}
    
    # 1. Archive
    current = supabase.table(TARGET_TABLE).select("*").eq("id", id).single().execute()
    if current.data:
        supabase.table(HISTORY_TABLE).insert({
            "original_id": id,
            "content": current.data.get('content'),
            "metadata": current.data.get('metadata'),
            "archived_at": datetime.now().isoformat()
        }).execute()

    # 2. Update
    new_metadata = {
        "version": "v10.0",
        "state": "CANONIZED",
        "domain": categorization.get('domain'),
        "type": categorization.get('type'),
        "provenance": f"Reforged by Axion on {datetime.now().date()}"
    }

    data = supabase.table(TARGET_TABLE).update({
        "content": new_content,
        "title": new_title,
        "metadata": new_metadata
    }).eq("id", id).execute()
    
    return {"status": "success", "id": id}

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1]
    
    if cmd == "fetch":
        print(json.dumps(fetch_batch()))
    elif cmd == "diff":
        with open(sys.argv[2], 'r') as f1, open(sys.argv[3], 'r') as f2:
            print(generate_diff(f1.read(), f2.read()))
    elif cmd == "commit":
        # commit <id> <title> <content_file> <meta_json>
        with open(sys.argv[4], 'r') as f: content = f.read()
        print(json.dumps(commit_transmutation(sys.argv[2], sys.argv[3], content, json.loads(sys.argv[5]))))