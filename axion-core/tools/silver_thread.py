"""# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-001`                                |
| **2. Official Name**   | `silver_thread.py`                             |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `SYNG` (Synergy)                               |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **Spirit Web Connectivity**                    |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `GOVERNED_BY: [CORE-CODEX-001]`                |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |.

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
| CORE-CODEX-001 | GOVERNS | This tool is governed by the Supreme Law. |

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Connection Engine (The High Priestess)
# Synergy Set: The Oracle's Eye
# Primary Stat Buff: Synergy (+20)
# Passive Ability: Spirit Web (Detects broken links)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP
"""

import json
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

# Configure Logging to STDOUT
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SilverThread")


def scan_weave(target_dir: Path) -> None:
    """Scans a directory for Markdown files and builds a link graph.
    Reports:
    1. Dead Links (Outgoing links to non-existent files)
    2. Orphans (Files with no incoming links).
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

    # 3. Compile Results
    orphans = [n for n in nodes if incoming_count[n] == 0]
    report_data = {
        "target": str(target_dir.resolve()),
        "nodes_count": len(nodes),
        "orphans": orphans,
        "dead_links": [{"source": s, "target": t} for s, t in dead_links],
        "connectivity_score": (
            ((len(nodes) - len(orphans)) / len(nodes) * 100) if nodes else 0
        ),
    }

    # 4. Report Results
    logger.info("\n" + "=" * 40)
    logger.info("       SILVER THREAD REPORT       ")
    logger.info("=" * 40)

    logger.info(f"\n[!] ORPHANS DETECTED ({len(orphans)}):")
    if orphans:
        for o in orphans[:10]:
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

    logger.info("\n" + "-" * 40)
    logger.info(f"NETWORK DENSITY SCORE: {report_data['connectivity_score']:.2f}%")
    logger.info("-" * 40)

    # 5. Save Report
    workspace_root = target_dir
    while (
        workspace_root.parent != workspace_root
        and not (workspace_root / "axion-core").exists()
    ):
        workspace_root = workspace_root.parent

    log_dir = workspace_root / "_logs"
    if log_dir.exists():
        log_path = log_dir / "silver_thread_audit.json"
        try:
            with open(log_path, "w") as f:
                json.dump(report_data, f, indent=2)
            logger.info(f"\nAudit saved to {log_path.relative_to(workspace_root)}")
        except Exception as e:
            logger.error(f"Failed to save audit log: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python silver_thread.py <target_directory>")
        sys.exit(1)

    scan_weave(Path(sys.argv[1]))
