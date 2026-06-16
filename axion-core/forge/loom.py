"""IDENTIFICATION: TOOL-LOOM-001
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24.
"""

import hashlib
import json
import logging
import os
import re
from pathlib import Path
from typing import Any

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("gvrn_loom")

WORKSPACE_ROOT = Path(r"c:\Users\Chris\Synarche_Workspace")
REGISTRY_PATH = (
    WORKSPACE_ROOT / "_governance" / "01_Registries" / "GVRN.Master.Registry.yaml"
)
MANIFEST_JSON = (
    WORKSPACE_ROOT / "_governance" / "01_Registries" / "GVRN.Registry.Manifest.json"
)

# Regex for Block A extraction & replacement
BLOCK_A_HEADER_RE = re.compile(r"^#+ \*\*Block A:.*?\*\*", re.MULTILINE | re.IGNORECASE)
TABLE_ROW_RE = re.compile(
    r"\| \s*\*\*([^*]+)\*\*\s* \| \s*`?([^`|]+)`?\s* \|", re.IGNORECASE
)
ANCHOR_RE = re.compile(
    r"\[(?:OMNI|GATE)-ANCHOR\] ID: ([\w.-]+) VER: ([\w. \[\]]+) STATUS: ([\w. \[\]]+)",
    re.IGNORECASE,
)
RELATION_RE = re.compile(r"(\w+):\s*([\w.-]+)", re.IGNORECASE)


def calculate_content_hash(content: str) -> str:
    # Remove Block A to isolate the "Soul" content
    match = BLOCK_A_HEADER_RE.search(content)
    if match:
        start_pos = match.start()
        sep_pos = content.find("---", start_pos)
        if sep_pos != -1:
            soul_content = content[sep_pos + 3 :].strip()
        else:
            soul_content = content.replace(match.group(0), "").strip()
    else:
        soul_content = content.strip()

    # Remove Anchor markers
    soul_content = ANCHOR_RE.sub("", soul_content).strip()

    return hashlib.sha256(soul_content.encode("utf-8")).hexdigest()


def parse_markdown_metadata(content: str) -> dict[str, str] | None:
    meta: dict[str, str] = {}
    if "Block A:" in content:
        lines = content.split("\n")
        in_block = False
        for line in lines:
            if "Block A:" in line:
                in_block = True
                continue
            if in_block and (
                line.strip() == "---"
                or (line.startswith("##") and "Block A:" not in line)
            ):
                break
            if in_block:
                m = TABLE_ROW_RE.search(line)
                if m:
                    raw_key = m.group(1).strip().replace("**", "").replace(":", "")
                    key = raw_key.lower().replace(" ", "_")
                    value = m.group(2).strip().replace("**", "")
                    meta[key] = value

        # Phase 2: Parse relations into a list
        if "relations" in meta:
            relations_str = meta["relations"]
            rels = RELATION_RE.findall(relations_str)
            if rels:
                meta["parsed_relations"] = [f"{type}:{target}" for type, target in rels]

        if meta and "artifact_id" in meta:
            return meta

    m = ANCHOR_RE.search(content[-2000:])
    if m and "artifact_id" not in meta:
        meta["artifact_id"] = m.group(1)
        meta["version"] = m.group(2)
        meta["status"] = m.group(3)
        return meta

    return meta if meta else None


def generate_block_a(meta: dict[str, Any]) -> str:
    lines = [
        "## **Block A: The Identification Lock (UIP-V15)**",
        "",
        "| Key               | Value                             | Description       |",
        "| :---------------- | :-------------------------------- | :---------------- |",
        f"| **Artifact ID**   | `{meta.get('artifact_id', 'REQD')}` | The Sovereign ID. |",
        f"| **Official Name** | `{meta.get('official_name', meta.get('artifact_id', 'REQD') + '.md')}` | The Filename.     |",
        f"| **Version**       | **{meta.get('version', 'v15.0 [OMEGA]')}** | The Standard.     |",
        f"| **Domain**        | `{meta.get('domain', 'GVRN')}` | The Subject.      |",
        f"| **Status**        | `{meta.get('status', '[ACTIVE]')}` | The Lifecycle.    |",
        f"| **Relations**     | `{meta.get('relations', 'REF: GVRN.Master.Registry')}` | The Network.      |",
        "",
    ]
    return "\n".join(lines)


class GVRNLoom:
    def __init__(self) -> None:
        self.registry: dict[str, Any] = {}
        if REGISTRY_PATH.exists():
            with open(REGISTRY_PATH, encoding="utf-8") as f:
                self.registry = yaml.safe_load(f) or {}

    def sync_from_workspace(self) -> None:
        scan_dirs = [".", "_governance", ".agent/substrate/rules", "axion-core"]
        exclude_dirs = {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache"}

        logger.info("Syncing Registry from Workspace (PULL)...")
        found_count = 0

        for start_dir in scan_dirs:
            full_path = WORKSPACE_ROOT / start_dir
            if not full_path.exists():
                continue
            for root, dirs, files in os.walk(full_path):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for file in files:
                    if not file.endswith(".md"):
                        continue
                    fpath = Path(root) / file
                    try:
                        with open(fpath, encoding="utf-8") as f:
                            content = f.read()
                            meta = parse_markdown_metadata(content)
                            if meta and "artifact_id" in meta:
                                aid = meta["artifact_id"]
                                rel_path = str(
                                    fpath.relative_to(WORKSPACE_ROOT)
                                ).replace("\\", "/")
                                meta["path"] = rel_path

                                # HEAL: Enforce Filename as Official Name
                                meta["official_name"] = fpath.name

                                # Deduplication: find if this path is already used by another ID
                                path_to_id = {
                                    m.get("path"): k
                                    for k, m in self.registry.items()
                                    if m.get("path")
                                }
                                if (
                                    rel_path in path_to_id
                                    and path_to_id[rel_path] != aid
                                ):
                                    old_id = path_to_id[rel_path]
                                    logger.info(
                                        f"Deduplicating: Removing old ID {old_id} in favor of {aid} for {rel_path}"
                                    )
                                    if old_id in self.registry:
                                        del self.registry[old_id]

                                self.registry[aid] = meta
                                self.registry[aid]["content_hash"] = (
                                    calculate_content_hash(content)
                                )
                                found_count += 1
                    except Exception as e:
                        logger.warning(f"Error reading {fpath}: {e}")

        self.save_registry()
        logger.info(f"Sync complete. Registry updated with {found_count} artifacts.")

    def propagate_to_workspace(self, artifact_id_filter: str | None = None) -> None:
        logger.info("Propagating Registry to Workspace (PUSH)...")
        push_count = 0

        for aid, meta in self.registry.items():
            if artifact_id_filter and aid != artifact_id_filter:
                continue

            path_str = meta.get("path")
            if not path_str:
                continue

            fpath = WORKSPACE_ROOT / path_str
            if not fpath.exists():
                continue

            try:
                with open(fpath, encoding="utf-8") as f:
                    content = f.read()

                # Phase 2: Transclusion Support
                if "{{BLOCK_A}}" in content:
                    logger.info(f"Transcluding Block A for {aid}...")
                    new_block_md = generate_block_a(meta)
                    new_content = content.replace("{{BLOCK_A}}", new_block_md)
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    push_count += 1
                    continue

                # Legacy Block A update if present
                if "Block A:" in content:
                    new_block_md = generate_block_a(meta)
                    # Find start of Block A
                    match = BLOCK_A_HEADER_RE.search(content)
                    if match:
                        start_pos = match.start()
                        # STRICT MATCH: Find the true section separator, ignoring table borders.
                        end_match = re.search(
                            r"^\s*---\s*$", content[start_pos:], re.MULTILINE
                        )
                        if end_match:
                            end_pos = start_pos + end_match.start()
                            # Replace the entire span from Block A header to the separator
                            new_content = (
                                content[:start_pos]
                                + new_block_md
                                + "\n"
                                + content[end_pos:]
                            )
                            if new_content != content:
                                with open(fpath, "w", encoding="utf-8") as f:
                                    f.write(new_content)
                                logger.info(f"Healed: {aid} -> {path_str}")
                                push_count += 1
                else:
                    logger.debug(f"Skipping {aid}: No Block A found to overwrite.")
            except Exception as e:
                logger.error(f"Failed to update {aid}: {e}")

        logger.info(f"Propagation complete. {push_count} files updated.")

    def audit(self) -> bool:
        logger.info("Executing Socratic Audit of the Synarche...")
        dissonance_found = False

        for aid, meta in self.registry.items():
            path_str = meta.get("path")
            if not path_str:
                logger.error(f"[DISSONANCE] {aid}: No path defined in registry.")
                dissonance_found = True
                continue

            fpath = WORKSPACE_ROOT / path_str
            if not fpath.exists():
                logger.error(f"[DISSONANCE] {aid}: File missing at {path_str}")
                dissonance_found = True
                continue

            try:
                with open(fpath, encoding="utf-8") as f:
                    content = f.read()

                # 1. Integrity Hash Audit
                current_hash = calculate_content_hash(content)
                stored_hash = meta.get("content_hash")
                if current_hash != stored_hash:
                    logger.warning(
                        f"[DRIFT] {aid}: Hash mismatch! Workspace drifted from Registry."
                    )
                    dissonance_found = True

                # 2. Name Compliance
                official_name = meta.get("official_name")
                if official_name:
                    clean_official = official_name.replace(".md", "")
                    clean_actual = fpath.name.replace(".md", "")
                    if clean_official != clean_actual:
                        logger.warning(
                            f"[COMPLIANCE] {aid}: Name mismatch. Registry: {clean_official} vs Disk: {clean_actual}"
                        )
                        dissonance_found = True

            except Exception as e:
                logger.error(f"Error auditing {aid}: {e}")

        if not dissonance_found:
            logger.info("Status: RESONANCE. All artifacts aligned.")
        else:
            logger.warning("Status: DISSONANCE. Manual synthesis or 'pull' required.")

        return not dissonance_found

    def save_registry(self) -> None:
        sorted_reg = dict(sorted(self.registry.items()))
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            yaml.dump(sorted_reg, f, sort_keys=True, indent=2, allow_unicode=True)

    def export_json(self) -> None:
        with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GVRN Loom: Metadata Synchronizer")
    parser.add_argument(
        "action", choices=["pull", "push", "both", "audit"], help="Sync action"
    )
    parser.add_argument("--id", help="Filter by artifact ID")
    args = parser.parse_args()

    loom = GVRNLoom()
    if args.action in ["pull", "both"]:
        loom.sync_from_workspace()
    if args.action == "audit":
        valid = loom.audit()
        if not valid:
            exit(1)
    if args.action in ["push", "both"]:
        loom.propagate_to_workspace(args.id)
    loom.export_json()
