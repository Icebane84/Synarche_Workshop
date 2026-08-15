import argparse
import difflib
import json
import os
import sys
from datetime import datetime
from typing import Any, Optional, TypedDict, cast

try:
    from supabase import Client, create_client, ClientOptions
    from postgrest.exceptions import APIError
except ImportError:
    print("Error: 'supabase' library not found. Please run 'pip install supabase'.", file=sys.stderr)
    sys.exit(1)

# cspell:ignore tofile lineterm postgrest

from synarche_logger import get_logger

logger = get_logger(__name__)

class SupabaseConnectionError(Exception):
    """Custom exception for Supabase connection issues."""

# --- CONFIGURATION ---
URL = os.environ.get("SUPABASE_URL", "")
KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")


def _build_client() -> Optional[Client]:
    """Builds and returns a Supabase client if credentials are valid."""
    if not URL or not KEY or "YOUR-SERVICE-ROLE-KEY" in KEY.upper():
        logger.warning("Supabase URL or Key is not configured. Database operations will be skipped.")
        return None

    try:
        # Set a timeout to prevent hanging on connection issues
        opts = ClientOptions(postgrest_client_timeout=10)
        return create_client(supabase_url=URL, supabase_key=KEY, options=opts)
    except Exception as e:
        logger.exception("Failed to initialize Supabase client", exc_info=e)
        return None


supabase: Optional[Client] = _build_client()

TARGET_TABLE = "knowledge_base"
HISTORY_TABLE = "knowledge_history"


class KnowledgeRecord(TypedDict):
    """Defines the structure of a record in the knowledge_base table."""
    id: str
    content: str
    title: str
    metadata: dict[str, Any]


class Categorization(TypedDict):
    """Defines the structure for categorization metadata."""
    domain: str
    type: str


def fetch_batch(limit: int = 5) -> list[dict[str, Any]]:
    """Fetches a batch of records that have not been canonized."""
    if supabase is None:
        logger.warning("Supabase client not available. Cannot fetch batch.")
        return []

    try:
        response = (
            supabase.table(TARGET_TABLE)
            .select("*")
            .eq("is_canonized", False)
            .limit(limit)
            .execute()
        )
        return cast(list[dict[str, Any]], response.data) if response.data else []
    except APIError as e:
        logger.exception("API Error fetching batch: %s", e.message)
        return []


def generate_diff(original: str, new: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(),
        new.splitlines(),
        fromfile="Legacy",
        tofile="Canonized",
        lineterm="",
    )
    return "\n".join(diff)


def commit_transmutation(
    record_id: str, new_title: str, new_content: str, categorization: Categorization
) -> dict[str, Any]:
    """Archives an existing record and updates it with new, canonized content."""
    if supabase is None:
        raise SupabaseConnectionError("Supabase client not available. Cannot commit.")

    try:
        # 1. Fetch the current record to archive it.
        current_response = supabase.table(TARGET_TABLE).select("*").eq("id", record_id).single().execute()
        current_data = current_response.data


        if not current_data:
            return {"status": "error", "id": record_id, "message": "Record not found."}


        # 2. Archive the old version.
        payload = cast(KnowledgeRecord, current_data)
        supabase.table(HISTORY_TABLE).insert({
            "original_id": record_id,
            "content": payload.get("content"),
            "metadata": payload.get("metadata"),
            "archived_at": datetime.now().isoformat(),
        }).execute()


        # 3. Prepare and update with the new canonized data.
        new_metadata = {
            "version": "v10.0",
            "state": "CANONIZED",
            "domain": categorization.get("domain"),
            "type": categorization.get("type"),
            "provenance": f"Reforged by Axion on {datetime.now().date()}",
        }

        supabase.table(TARGET_TABLE).update({
            "content": new_content,
            "title": new_title,
            "metadata": new_metadata,
            "is_canonized": True
        }).eq("id", record_id).execute()

        return {"status": "success", "id": record_id}

    except APIError as e:
        logger.exception("API Error committing transmutation for ID %s: %s", record_id, e.message)
        return {"status": "error", "id": record_id, "message": e.message}
    except Exception as e:
        logger.exception("An unexpected error occurred during commit for ID %s", record_id, exc_info=e)
        return {"status": "error", "id": record_id, "message": str(e)}


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Alchemy: Supabase knowledge base refactoring tool.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Fetch Command ---
    fetch_parser = subparsers.add_parser("fetch", help="Fetch a batch of legacy records.")
    fetch_parser.add_argument("--limit", type=int, default=5, help="Number of records to fetch.")

    # --- Diff Command ---
    diff_parser = subparsers.add_parser("diff", help="Generate a diff between two files.")
    diff_parser.add_argument("old_file", help="Path to the original file.")
    diff_parser.add_argument("new_file", help="Path to the new file.")

    # --- Commit Command ---
    commit_parser = subparsers.add_parser("commit", help="Commit a transmuted record to Supabase.")
    commit_parser.add_argument("record_id", help="The UUID of the record to update.")
    commit_parser.add_argument("title", help="The new title for the record.")
    commit_parser.add_argument("content_file", help="Path to the file with the new content.")
    commit_parser.add_argument("meta_json", help="JSON string or path to a file with categorization metadata.")

    args = parser.parse_args()

    if args.command == "fetch":
        print(json.dumps(fetch_batch()))
    elif args.command == "diff":
        try:
            with open(args.old_file, "r", encoding="utf-8") as f1, open(args.new_file, "r", encoding="utf-8") as f2:
                print(generate_diff(f1.read(), f2.read()))
        except FileNotFoundError as e:
            logger.exception("Diff error: %s", e)
            sys.exit(1)
    elif args.command == "commit":
        try:
            with open(args.content_file, "r", encoding="utf-8") as f:
                content = f.read()

            meta_data: Categorization
            if os.path.exists(args.meta_json):
                with open(args.meta_json, "r", encoding="utf-8") as f:
                    meta_data = json.load(f)
            else:
                meta_data = json.loads(args.meta_json)

            print(
                json.dumps(commit_transmutation(args.record_id, args.title, content, meta_data))
            )
        except FileNotFoundError as e:
            logger.exception("Commit error: %s", e)
            sys.exit(1)
        except json.JSONDecodeError:
            logger.exception("Commit error: Invalid JSON provided for metadata.")
            sys.exit(1)
