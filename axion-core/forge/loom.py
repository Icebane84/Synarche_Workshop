"""IDENTIFICATION: TOOL-LOOM-001
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24.
"""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
import hashlib
import json
import logging
import os
from pathlib import Path
import re
from typing import Any

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("gvrn_loom")

WORKSPACE_ROOT = Path(r"c:\Users\Chris\Synarche_Workspace")
REGISTRY_PATH = WORKSPACE_ROOT / "_governance" / "01_Registries" / "GVRN.Master.Registry.yaml"
MANIFEST_JSON = WORKSPACE_ROOT / "_governance" / "01_Registries" / "GVRN.Registry.Manifest.json"

# Regex for Block A extraction & replacement
BLOCK_A_HEADER_RE = re.compile(r"^#+ \*\*Block A:.*?\*\*", re.MULTILINE | re.IGNORECASE)
TABLE_ROW_RE = re.compile(r"\| \s*\*\*([^*]+)\*\*\s* \| \s*`?([^`|]+)`?\s* \|", re.IGNORECASE)
ANCHOR_RE = re.compile(
    r"\[(?:OMNI|GATE)-ANCHOR\] ID: ([\w.-]+) VER: ([\w. \[\]]+) STATUS: ([\w. \[\]]+)",
    re.IGNORECASE,
)
RELATION_RE = re.compile(r"(\w+):\s*([\w.-]+)", re.IGNORECASE)


@dataclass
class ArtifactMetadata:
    """Type-safe data structure representing a Sovereign Registry entry."""

    artifact_id: str
    official_name: str
    version: str = "v15.0 [OMEGA]"
    domain: str = "GVRN"
    status: str = "[ACTIVE]"
    path: str = ""
    content_hash: str = ""
    relations: str = "REF: GVRN.Master.Registry"
    parsed_relations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert dataclass to standard registry dictionary format."""
        d = asdict(self)
        if not d["parsed_relations"]:
            d.pop("parsed_relations", None)
        return d


def calculate_content_hash(content: str) -> str:
    """Calculates SHA-256 hash of the artifact content, excluding Block A headers and anchor tags."""
    content = content.replace("\r\n", "\n")
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

    soul_content = ANCHOR_RE.sub("", soul_content).strip()
    return hashlib.sha256(soul_content.encode("utf-8")).hexdigest()


def parse_markdown_metadata(content: str) -> dict[str, str] | None:
    """Unified metadata parser. Supports HTML comment frontmatter, standard YAML frontmatter,

    Block A markdown tables, and bottom OMNI-ANCHOR tags.
    """
    meta: dict[str, str] = {}

    # 1. HTML Comment Frontmatter (e.g. <!-- artifact_anchor: ... -->)
    if "artifact_anchor:" in content:
        try:
            start_idx = content.find("artifact_anchor:")
            comment_end = content.find("-->", start_idx)
            yaml_text = (
                content[start_idx:comment_end]
                if comment_end != -1
                else content[start_idx : start_idx + 1000]
            )
            frontmatter = yaml.safe_load(yaml_text)
            if isinstance(frontmatter, dict):
                anchor = frontmatter.get("artifact_anchor") or frontmatter
                if isinstance(anchor, dict):
                    aid = anchor.get("id") or anchor.get("artifact_id")
                    if aid:
                        meta["artifact_id"] = str(aid)
                        meta["version"] = str(anchor.get("version", "v15.0 [OMEGA]"))
                        meta["status"] = str(anchor.get("state", anchor.get("status", "[ACTIVE]")))
                        meta["domain"] = str(anchor.get("domain", "GVRN"))
                        return meta
        except Exception:
            pass

    # 2. Standard YAML Frontmatter (--- ... ---)
    if content.startswith("---"):
        try:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                if isinstance(frontmatter, dict):
                    anchor = frontmatter.get("artifact_anchor") or frontmatter
                    if isinstance(anchor, dict):
                        aid = anchor.get("id") or anchor.get("artifact_id")
                        if aid:
                            meta["artifact_id"] = str(aid)
                            meta["version"] = str(anchor.get("version", "v15.0 [OMEGA]"))
                            meta["status"] = str(anchor.get("state", anchor.get("status", "[ACTIVE]")))
                            meta["domain"] = str(anchor.get("domain", "GVRN"))
                            return meta
        except Exception:
            pass

    # 3. Block A Markdown Table
    if "Block A:" in content:
        lines = content.split("\n")
        in_block = False
        for line in lines:
            if "Block A:" in line:
                in_block = True
                continue
            if in_block and (
                line.strip() == "---" or (line.startswith("##") and "Block A:" not in line)
            ):
                break
            if in_block:
                m = TABLE_ROW_RE.search(line)
                if m:
                    raw_key = m.group(1).strip().replace("**", "").replace(":", "")
                    key = raw_key.lower().replace(" ", "_")
                    value = m.group(2).strip().replace("**", "")
                    meta[key] = value

        if "relations" in meta:
            relations_str = meta["relations"]
            rels = RELATION_RE.findall(relations_str)
            if rels:
                meta["parsed_relations"] = [f"{type}:{target}" for type, target in rels]

        if meta and "artifact_id" in meta:
            return meta

    # 4. Bottom Anchor Fallback
    m = ANCHOR_RE.search(content[-2000:])
    if m and "artifact_id" not in meta:
        meta["artifact_id"] = m.group(1)
        meta["version"] = m.group(2)
        meta["status"] = m.group(3)
        return meta

    return meta if meta else None


def generate_block_a(meta: dict[str, Any]) -> str:
    """Generates standardized Block A identification lock markdown table."""
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


def _process_file_scan(fpath: Path) -> tuple[str, dict[str, Any], str] | None:
    """Helper function for parallel file reading and metadata parsing."""
    try:
        content = fpath.read_text(encoding="utf-8").replace("\r\n", "\n")
        meta = parse_markdown_metadata(content)
        if meta and "artifact_id" in meta:
            aid = meta["artifact_id"]
            rel_path = str(fpath.relative_to(WORKSPACE_ROOT)).replace("\\", "/")
            meta["path"] = rel_path
            meta["official_name"] = fpath.name
            content_hash = calculate_content_hash(content)
            meta["content_hash"] = content_hash
            return aid, meta, content
    except Exception as e:
        logger.warning(f"Error reading {fpath}: {e}")
    return None


class GVRNLoom:
    """The Sovereign Loom Engine. Handles master registry synchronization, Block A transclusion, and workspace audits."""

    def __init__(self) -> None:
        self.registry: dict[str, Any] = {}
        if REGISTRY_PATH.exists():
            with open(REGISTRY_PATH, encoding="utf-8") as f:
                self.registry = yaml.safe_load(f) or {}

    def sync_from_workspace(self, dry_run: bool = False) -> None:
        """Syncs workspace markdown metadata and content hashes into Master Registry."""
        scan_dirs = [".", "_governance", ".agent/substrate/rules", "axion-core"]
        exclude_dirs = {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache"}

        logger.info("Syncing Registry from Workspace (PULL)..." + (" [DRY-RUN]" if dry_run else ""))
        found_count = 0
        file_paths: list[Path] = []

        for start_dir in scan_dirs:
            full_path = WORKSPACE_ROOT / start_dir
            if not full_path.exists():
                continue
            for root, dirs, files in os.walk(full_path):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for file in files:
                    if file.endswith(".md"):
                        file_paths.append(Path(root) / file)

        # Parallel file scan across threads
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(_process_file_scan, file_paths)

        for res in results:
            if res:
                aid, meta, _ = res
                rel_path = meta["path"]
                # Deduplication: find if this path is already used by another ID
                path_to_id = {m.get("path"): k for k, m in self.registry.items() if m.get("path")}
                if rel_path in path_to_id and path_to_id[rel_path] != aid:
                    old_id = path_to_id[rel_path]
                    logger.info(
                        f"Deduplicating: Removing old ID {old_id} in favor of {aid} for {rel_path}"
                    )
                    if old_id in self.registry and not dry_run:
                        del self.registry[old_id]

                if not dry_run:
                    self.registry[aid] = meta
                found_count += 1

        # Prune registry entries for files that no longer exist on disk
        missing_ids = [
            aid
            for aid, meta in list(self.registry.items())
            if meta.get("path") and not (WORKSPACE_ROOT / meta["path"]).exists()
        ]
        if not dry_run:
            for aid in missing_ids:
                logger.info(f"Pruning obsolete registry entry for missing file: {aid}")
                del self.registry[aid]

            # Ensure content_hash is updated for all registered artifacts whose files exist on disk
            for aid, meta in self.registry.items():
                path_str = meta.get("path")
                if path_str:
                    fpath = WORKSPACE_ROOT / path_str
                    if fpath.exists():
                        try:
                            content = fpath.read_text(encoding="utf-8").replace("\r\n", "\n")
                            meta["content_hash"] = calculate_content_hash(content)
                        except Exception:
                            pass

            self.save_registry()

        logger.info(
            f"Sync complete. Registry updated with {found_count} artifacts ({len(missing_ids)} obsolete pruned)."
        )

    def propagate_to_workspace(
        self, artifact_id_filter: str | None = None, dry_run: bool = False
    ) -> None:
        """Propagates Block A transclusions and metadata locks back out into workspace markdown files."""
        logger.info("Propagating Registry to Workspace (PUSH)..." + (" [DRY-RUN]" if dry_run else ""))
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
                content = fpath.read_text(encoding="utf-8").replace("\r\n", "\n")

                # Transclusion Support: {{BLOCK_A}}
                if "{{BLOCK_A}}" in content:
                    logger.info(f"Transcluding Block A for {aid}...")
                    new_block_md = generate_block_a(meta)
                    new_content = content.replace("{{BLOCK_A}}", new_block_md)
                    if not dry_run:
                        fpath.write_text(new_content, encoding="utf-8")
                    push_count += 1
                    continue

                # Legacy Block A update if present
                if "Block A:" in content:
                    new_block_md = generate_block_a(meta)
                    match = BLOCK_A_HEADER_RE.search(content)
                    if match:
                        start_pos = match.start()
                        end_match = re.search(r"^\s*---\s*$", content[start_pos:], re.MULTILINE)
                        if end_match:
                            end_pos = start_pos + end_match.start()
                            new_content = content[:start_pos] + new_block_md + "\n" + content[end_pos:]
                            if new_content != content:
                                if not dry_run:
                                    fpath.write_text(new_content, encoding="utf-8")
                                logger.info(f"Healed: {aid} -> {path_str}")
                                push_count += 1
                else:
                    logger.debug(f"Skipping {aid}: No Block A found to overwrite.")
            except Exception as e:
                logger.error(f"Failed to update {aid}: {e}")

        logger.info(f"Propagation complete. {push_count} files updated.")

    def audit(self) -> bool:
        """Audits workspace files against the Master Registry. Returns True if all files are in RESONANCE."""
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
                content = fpath.read_text(encoding="utf-8").replace("\r\n", "\n")

                # 1. Integrity Hash Audit
                current_hash = calculate_content_hash(content)
                stored_hash = meta.get("content_hash")
                if current_hash != stored_hash:
                    logger.warning(f"[DRIFT] {aid}: Hash mismatch! Workspace drifted from Registry.")
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
    parser.add_argument("action", choices=["pull", "push", "both", "audit"], help="Sync action")
    parser.add_argument("--id", help="Filter by artifact ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview action without mutating disk")
    args = parser.parse_args()

    loom = GVRNLoom()
    if args.action in ["pull", "both"]:
        loom.sync_from_workspace(dry_run=args.dry_run)
    if args.action == "audit":
        valid = loom.audit()
        if not valid:
            exit(1)
    if args.action in ["push", "both"]:
        loom.propagate_to_workspace(args.id, dry_run=args.dry_run)
    if not args.dry_run:
        loom.export_json()
