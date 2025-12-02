"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-INGEST-VAULT-001`                | The Sovereign ID. |
| **Official Name** | `ingest_vault.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import argparse
import os
import re

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "dist"}


def extract_field(content: str, field: str) -> str:
    """Extract a metadata field value from an artifact header."""
    pattern = rf"\*\*{field}\*\*\s*\|\s*`?([^`|\n]+)`?"
    match = re.search(pattern, content)
    if match:
        return match.group(1).strip()
    return "N/A"


def ingest_vault(directory: str) -> None:
    """Ingest all artifacts in a directory and report their metadata."""
    print(f"\n>>> INGESTING VAULT: {directory}\n")
    print("=" * 80)
    print(f"  {'FILE':<35} {'ARTIFACT ID':<25} {'STATUS':<15}")
    print("=" * 80)

    total = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not (f.endswith(".md") or f.endswith(".py")):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, encoding="utf-8") as fh:
                    content = fh.read(2000)  # Only read header for speed
            except Exception:
                continue

            artifact_id = extract_field(content, "Artifact ID")
            status = extract_field(content, "Status")
            fname = f if len(f) <= 34 else f[:31] + "..."
            print(f"  {fname:<35} {artifact_id:<25} {status:<15}")
            total += 1

    print("=" * 80)
    print(f"\n  Total Artifacts Ingested: {total}")
    print("=" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(description="Vault Ingestor — The Magician's Eye")
    parser.add_argument("target", help="Directory to ingest.")
    args = parser.parse_args()
    ingest_vault(os.path.abspath(args.target))


if __name__ == "__main__":
    main()
