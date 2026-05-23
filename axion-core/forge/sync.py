import json
import logging
import os
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("sync_manifest")

WORKSPACE_ROOT = Path(r"c:\Users\Chris\Synarche_Workspace")
OUTPUT_PATH = (
    WORKSPACE_ROOT / "_governance" / "01_Registries" / "GVRN.Registry.Manifest.json"
)

# Regex for Block A extraction
BLOCK_A_RE = re.compile(
    r"## \*\*Block A:.*?\*\*\n\n(.*?)\n\n", re.DOTALL | re.IGNORECASE
)
TABLE_ROW_RE = re.compile(
    r"\| \s*\*\*([^*]+)\*\*\s* \| \s*`?([^`|]+)`?\s* \|", re.IGNORECASE
)
ANCHOR_RE = re.compile(
    r"\[(?:OMNI|GATE)-ANCHOR\] ID: ([\w.-]+) VER: ([\w. \[\]]+) STATUS: ([\w. \[\]]+)",
    re.IGNORECASE,
)


def parse_metadata(content):
    # 1. Try Block A Table
    meta = {}
    block_a_match = BLOCK_A_RE.search(content)
    if block_a_match:
        table_content = block_a_match.group(1)
        rows = TABLE_ROW_RE.findall(table_content)
        for key, value in rows:
            key = key.strip().lower().replace(" ", "_")
            value = value.strip().replace("**", "")
            meta[key] = value
        if meta and "artifact_id" in meta:
            return meta

    # 2. Try Anchor at bottom (check last 500 chars)
    anchor_match = ANCHOR_RE.search(content[-1000:])
    if anchor_match:
        meta["artifact_id"] = anchor_match.group(1)
        meta["version"] = anchor_match.group(2)
        meta["status"] = anchor_match.group(3)
        return meta

    return None


def sync():
    manifest = {}
    scan_dirs = ["_governance", ".agent/substrate/rules", "axion-core"]
    exclude_dirs = {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache"}

    logger.info("Scanning workspace for metadata locks...")

    for start_dir in scan_dirs:
        full_start_dir = WORKSPACE_ROOT / start_dir
        if not full_start_dir.exists():
            continue

        for root, dirs, files in os.walk(full_start_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if not file.endswith(".md"):
                    continue

                file_path = Path(root) / file
                rel_path = file_path.relative_to(WORKSPACE_ROOT)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        # Read the whole file for anchors at bottom
                        content = f.read()
                        meta = parse_metadata(content)

                        if meta and "artifact_id" in meta:
                            artifact_id = meta["artifact_id"]
                            meta["path"] = str(rel_path).replace("\\", "/")
                            manifest[artifact_id] = meta
                            logger.info(f"Ingested: {artifact_id} -> {rel_path}")
                except Exception as e:
                    logger.warning(f"Failed to parse {rel_path}: {e}")

    logger.info(f"Sync complete. Found {len(manifest)} compliant artifacts.")

    # Sort by ID for readability
    sorted_manifest = dict(sorted(manifest.items()))

    os.makedirs(OUTPUT_PATH.parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_manifest, f, indent=2)

    logger.info(f"Manifest written to {OUTPUT_PATH}")


if __name__ == "__main__":
    sync()
