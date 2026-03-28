import os
import re
import sys
import json
from pathlib import Path

import requests  # type: ignore
from dotenv import load_dotenv

# Load credentials from .env
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("AXION_INSFORGE_API_KEY")
BASE_URL = os.getenv("AXION_INSFORGE_BASE_URL")
FUNCTION_SLUG = "weaver-v15"


def weave_artifact(target_path: str) -> None:
    path = Path(target_path)
    if not path.exists():
        print(f"Error: Path {target_path} not found.")
        return

    if path.is_dir():
        for file in path.glob("**/*.md"):
            if "_archive" in str(file).lower():
                continue
            weave_artifact(str(file))
        return

    content = path.read_text(encoding="utf-8")

    # Extract Metadata from Block A
    artifact_id = path.stem
    version = "v15.0"
    domain = "GVRN"
    name = path.name
    status = "CANONIZED"
    celestial_class = "[MOON]"

    id_match = re.search(r"Artifact ID\*\*?\s*\|\s*`?(.*?)`?\s*\|", content)
    if id_match:
        artifact_id = id_match.group(1).strip().replace("`", "")

    ver_match = re.search(r"Version\*\*?\s*\|\s*(\*\*?[^*]+\*\*?)\s*\|", content)
    if ver_match:
        version = ver_match.group(1).strip().replace("*", "")

    dom_match = re.search(r"Domain\*\*?\s*\|\s*`?(.*?)`?\s*\|", content)
    if dom_match:
        domain = dom_match.group(1).strip().replace("`", "")

    stat_match = re.search(r"Status\*\*?\s*\|\s*`?(.*?)`?\s*\|", content)
    if stat_match:
        status = stat_match.group(1).strip().replace("`", "")

    cel_match = re.search(r"Celestial Class\*\*?\s*\|\s*`?(.*?)`?\s*\|", content)
    if cel_match:
        celestial_class = cel_match.group(1).strip().replace("`", "")

    print(f"--- INITIATING WEAVE: {artifact_id} ({version}) [{celestial_class}] ---")

    payload = {
        "content": content,
        "artifact_id": artifact_id,
        "domain": domain,
        "name": name,
        "version": version,
        "status": status,
        "celestial_class": celestial_class,
    }

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    url = f"{BASE_URL}/functions/{FUNCTION_SLUG}"

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "SUCCESS":
            print(f"[OK] {artifact_id} - Resonance: {result.get('resonance')}")
            if result.get("reflection"):
                print(f"Reflection: {result.get('reflection')}")
        else:
            print(f"[ERROR] {artifact_id} - Dissonance: {result.get('message')}")

    except Exception as e:
        print(f"[CRITICAL] {artifact_id} - Failure: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python weave_artifact.py <file_or_dir_path> ...")
        sys.exit(1)

    for target in sys.argv[1:]:
        weave_artifact(target)
