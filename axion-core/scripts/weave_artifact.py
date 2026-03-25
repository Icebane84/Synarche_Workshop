import os
import sys
import json
import re
import requests  # type: ignore
from pathlib import Path
from dotenv import load_dotenv

# Load credentials from .env
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("AXION_INSFORGE_API_KEY")
BASE_URL = os.getenv("AXION_INSFORGE_BASE_URL")
FUNCTION_SLUG = "weaver-v15"


def weave_artifact(file_path: str) -> None:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File {file_path} not found.")
        return

    content = path.read_text(encoding="utf-8")

    # Extract Metadata from Block A
    artifact_id = path.stem
    version = "v15.0"
    domain = "GVRN"
    name = path.name
    status = "CANONIZED"

    id_match = re.search(r"Artifact ID\*\*?\s*\|\s*`?(.*?)`?\s*\|", content)
    if id_match:
        artifact_id = id_match.group(1).strip().replace("`", "")

    ver_match = re.search(r"Version\*\*?\s*\|\s*(\*\*?[^*]+\*\*?)\s*\|", content)
    if ver_match:
        version = ver_match.group(1).strip().replace("*", "")

    dom_match = re.search(r"Domain\*\*?\s*\|\s*`?(.*?)`?\s*\|", content)
    if dom_match:
        domain = dom_match.group(1).strip().replace("`", "")

    print(f"--- INITIATING WEAVE: {artifact_id} ({version}) ---")

    payload = {
        "content": content,
        "artifact_id": artifact_id,
        "domain": domain,
        "name": name,
        "version": version,
        "status": status,
    }

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    url = f"{BASE_URL}/functions/{FUNCTION_SLUG}"

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "SUCCESS":
            print("[OK] The Weave is complete.")
            print(f"Resonance: {result.get('resonance')}")
            print(f"Reflection: {result.get('reflection')}")
        else:
            print(f"[ERROR] Weave Dissonance: {result.get('message')}")

    except Exception as e:
        print(f"[CRITICAL] Weave Failure: {e}")
        if hasattr(e, "response") and e.response is not None:
            try:
                print(f"Full Response: {json.dumps(e.response.json(), indent=2)}")
            except (json.JSONDecodeError, ValueError, AttributeError):
                print(f"Raw Response: {e.response.text}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python weave_artifact.py <file_path>")
        sys.exit(1)

    weave_artifact(sys.argv[1])
