"""# TOOL-HPRI-005: The Resonance Scanner (High Harmony).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-005`                                          |
| **2. Official Name**   | `resonance_scanner.py`                                   |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `SYNR`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Resonance**                                            |
| **11. Catalyst**       | **Alignment Check**                                      |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess persona uses this tool for resonance checks.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: High Harmony (The High Priestess)
# Synergy Set: The Weaver's Grace
# Primary Stat Buff: Harmony (+15), Perception (+10)
# Passive Ability: The Harmonic Frequency (Alignment Detection)
# Cognitive Load Cost: Medium
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: SCAN_RESONANCE` | Global Alignment Scan | Synergy Measurement |
| `⚡ EXECUTE: ALIGN_CHECK` | Fast Triage of Drift | Coherence Maintenance |

---

Consolidated tool for scanning directories for 'Resonance Markers' and alignment.
Replaces legacy resonance_scan.py and deep_resonance_scan.py.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List, Tuple

# --- Configuration ---
# Markers that indicate a file is "aligned"
RESONANCE_MARKERS = [
    "UMB-",
    "AOP-",
    "GUCA-",
    "CODEX-",
    "Phoenix-Class",
    "Synarche",
]

# File extensions to scan
VALID_EXTENSIONS = {".md", ".json", ".ts", ".tsx", ".py"}

# Directories to ignore
IGNORE_DIRS = {
    "node_modules",
    ".git",
    ".gemini",
    "__pycache__",
    ".pytest_cache",
    "venv",
    "env",
    "dist",
    "build",
    "coverage",
}

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ResonanceScanner")


def is_aligned(file_path: Path) -> bool:
    """Checks if a file is aligned based on Resonance Markers in its name or content."""
    try:
        # 1. Check filename (Fastest)
        if any(marker in file_path.name for marker in RESONANCE_MARKERS):
            return True

        # 2. Check content (Slower)
        # We read as text, ignoring errors for non-text files that slipped through
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in content for marker in RESONANCE_MARKERS):
            return True

    except Exception as e:
        logger.debug(f"Error checking alignment for {file_path}: {e}")
        # If we can't read it, we assume it's neutral/unaligned for now.
        return False

    return False


def scan_directory(root_path: Path) -> Tuple[int, int, List[Path]]:
    """Recursively scans a directory.
    Returns: (total_files, aligned_files_count, list_of_unaligned_paths).
    """
    total_files = 0
    aligned_files = 0
    unaligned_paths: List[Path] = []

    logger.info(f"Scanning: {root_path}")

    for root, dirs, files in os.walk(root_path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

        for file in files:
            file_path = Path(root) / file

            # Filter by extension
            if file_path.suffix not in VALID_EXTENSIONS:
                continue

            total_files += 1
            if is_aligned(file_path):
                aligned_files += 1
            else:
                unaligned_paths.append(file_path)

    return total_files, aligned_files, unaligned_paths


def print_report(
    root_path: Path,
    total: int,
    aligned: int,
    unaligned_paths: List[Path],
    show_unaligned: bool,
) -> None:
    """Prints a formatted report of the scan."""
    score = (aligned / total * 100) if total > 0 else 0.0

    print("-" * 60)
    print(f"TARGET: {root_path.resolve()}")
    print("-" * 60)
    print(f"Total Files Scanned: {total}")
    print(f"Aligned Files:       {aligned}")
    print(f"Resonance Score:     {score:.2f}%")
    print("-" * 60)

    if show_unaligned and unaligned_paths:
        print(f"\n[!] Found {len(unaligned_paths)} Unaligned Files:")
        # Limit output if too many
        limit = 20
        for p in unaligned_paths[:limit]:
            try:
                # print relative path for readability
                rel = p.relative_to(root_path)
                print(f"  - {rel}")
            except ValueError:
                print(f"  - {p}")
        if len(unaligned_paths) > limit:
            print(f"  ... and {len(unaligned_paths) - limit} more.")
    elif total > 0 and aligned == total:
        print("\n[+] PERFECT RESONANCE. All files are aligned.")

    print("=" * 60 + "\n")


def main() -> None:
    """CLI Entrypoint."""
    parser = argparse.ArgumentParser(
        description="Resonance Scanner: Audits codebase for alignment markers."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        default=["."],
        help="Directories to scan (default: current directory)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show verbose debug logs"
    )
    parser.add_argument(
        "--list-unaligned",
        "-l",
        action="store_true",
        help="List all files that failed alignment check",
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    print("\n>>> INITIATING RESONANCE SCAN v3.0")
    print("=" * 60)

    grand_total = 0
    grand_aligned = 0

    for target in args.targets:
        target_path = Path(target)
        if not target_path.exists():
            logger.error(f"[Error] Directory not found: {target}")
            continue

        if target_path.is_file():
            # Quick single file check
            t = 1
            a = 1 if is_aligned(target_path) else 0
            u = [] if a else [target_path]
            print_report(target_path, t, a, u, args.list_unaligned)
            grand_total += t
            grand_aligned += a
            continue

        t, a, u = scan_directory(target_path)
        print_report(target_path, t, a, u, args.list_unaligned)
        grand_total += t
        grand_aligned += a

    if len(args.targets) > 1:
        agg_score = (grand_aligned / grand_total * 100) if grand_total > 0 else 0.0
        print("AGGREGATE SUMMARY")
        print("=" * 60)
        print(f"Total Files:     {grand_total}")
        print(f"Total Aligned:   {grand_aligned}")
        print(f"Aggregate Score: {agg_score:.2f}%")
        print("=" * 60)


if __name__ == "__main__":
    main()
