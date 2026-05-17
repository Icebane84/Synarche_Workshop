#!/usr/bin/env python3
"""
# TOOL-HPRI-001: The Silver Thread (Graph Integrity)

## I. Universal Identification & Provenance
| Attribute | Value |
| :--- | :--- |
| **Artifact ID** | `TOOL-HPRI-001` |
| **Official Name** | `silver_thread.py` |
| **Version** | **v11.0** |
| **Domain** | `SYNG` |
| **Evolution** | **Cognitive Ascension** |
| **Signal (ESF)** | `ESF-BETA` |
| **Status (State)** | `[ACTIVE]` |
| **Tier** | **Strategic** |
| **Celestial Class** | `[STAR]` |
| **Governance** | `GVRN-SYNERGY-001` |
| **Upstream** | `N/A` |
| **Downstream** | `Assessment Report` |
| **Provenance** | `Genesis Stamp: 2026-01-25` |
| **Relations** | `Governed by GVRN-SYNERGY-001` |

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Connection Engine (The High Priestess)
# Synergy Set: The Oracle's Eye
# Primary Stat Buff: Synergy (+20)
# Passive Ability: Spirit Web (Detects broken links)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: SCAN_WEAVE` | Analyze Link Graph | Identify Orphans & Dead Links |
| `⚡ EXECUTE: MEND` | Auto-Suggest Links | Restore Connectivity |
"""

import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def scan_weave(target_dir: Path) -> None:
    """
    Scans a directory for Markdown files and builds a link graph.
    Reports:
    1. Dead Links (Outgoing links to non-existent files)
    2. Orphans (Files with no incoming links)
    """
    if not target_dir.exists():
        logger.error(f"Target directory not found: {target_dir}")
        return

    logger.info(f"Scanning Weave at: {target_dir.resolve()}")

    # 1. Map all existing files (Nodes)
    # Store as {filename_stem: full_path} for simple matching
    # Note: Obsidian links often just use the filename without extension
    nodes = {f.stem: f for f in target_dir.rglob("*.md")}
    logger.info(f"Nodes Found: {len(nodes)}")

    # 2. Extract Links (Edges)
    # adjacency_list: {source: [destinations]}
    # incoming_count: {node: count}
    adjacency_list = defaultdict(list)
    incoming_count = defaultdict(int)
    dead_links = []

    link_pattern = re.compile(r"\[\[(.*?)(?:\|.*?)?\]\]")

    for node_name, file_path in nodes.items():
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            links = link_pattern.findall(content)

            for link in links:
                # Basic normalization: link might point to "Folder/File", we just want "File"
                # This is a heuristic for Obsidian-style fluid linking.
                link_target = Path(link).stem

                adjacency_list[node_name].append(link_target)

                if link_target in nodes:
                    incoming_count[link_target] += 1
                else:
                    dead_links.append((node_name, link))

        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")

    # 3. Report Results
    orphans = [n for n in nodes if incoming_count[n] == 0]

    logger.info("\n" + "=" * 40)
    logger.info("       SILVER THREAD REPORT       ")
    logger.info("=" * 40)

    logger.info(f"\n[!] ORPHANS DETECTED ({len(orphans)}):")
    if orphans:
        for o in orphans[:10]:  # Limit output
            logger.info(f"  - {o}")
        if len(orphans) > 10:
            logger.info(f"  ...and {len(orphans) - 10} more.")
    else:
        logger.info("  None. The Weave is tight.")

    logger.info(f"\n[!] DEAD LINKS DETECTED ({len(dead_links)}):")
    if dead_links:
        for source, target in dead_links[:10]:
            logger.info(f"  - In '{source}': [[{target}]] -> ?")
        if len(dead_links) > 10:
            logger.info(f"  ...and {len(dead_links) - 10} more.")
    else:
        logger.info("  None. All threads connect.")

    connectivity_score = ((len(nodes) - len(orphans)) / len(nodes) * 100) if nodes else 0
    logger.info("\n" + "-" * 40)
    logger.info(f"NETWORK DENSITY SCORE: {connectivity_score:.2f}%")
    logger.info("-" * 40)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python silver_thread.py <target_directory>")
        sys.exit(1)

    scan_weave(Path(sys.argv[1]))
