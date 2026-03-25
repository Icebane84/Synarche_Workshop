"""
IDENTIFICATION: TOOL-MAP-MD-001
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24
"""

import argparse
import os
from typing import Set

#!/usr/bin/env python3
"""
ENTITY-MAP-MD-001: The Structural Alchemist
Domain: ARCH | State: ACTIVE | Version: v15.0 [OMEGA]
Objective: Map markdown hierarchies and ensure structural integrity.
"""

SKIP_DIRS = {".git", "node_modules", ".venv", ".obsidian", "__pycache__"}


def build_tree(
    directory: str, prefix: str = "", depth: int = 0, max_depth: int = 4
) -> list[str]:
    """Recursively build an ASCII directory tree for markdown files."""
    if depth > max_depth:
        return []

    lines = []
    try:
        entries = sorted(os.scandir(directory), key=lambda e: (not e.is_dir(), e.name))
    except PermissionError:
        return []

    md_entries = [
        e
        for e in entries
        if (e.is_dir() and e.name not in SKIP_DIRS) or e.name.endswith(".md")
    ]

    for i, entry in enumerate(md_entries):
        connector = "└── " if i == len(md_entries) - 1 else "├── "
        extension = "    " if i == len(md_entries) - 1 else "│   "

        if entry.is_dir():
            md_count = sum(1 for f in os.listdir(entry.path) if f.endswith(".md"))
            lines.append(f"{prefix}{connector}📁 {entry.name}/ ({md_count} docs)")
            lines.extend(
                build_tree(entry.path, prefix + extension, depth + 1, max_depth)
            )
        else:
            lines.append(f"{prefix}{connector}📄 {entry.name}")

    return lines


def map_markdown_structure(directory: str, output: str | None = None) -> None:
    """Generate and print the markdown directory tree."""
    print(f"\n>>> MAP MARKDOWN STRUCTURE: {directory}\n")

    total_files = sum(
        1 for _, _, files in os.walk(directory) for f in files if f.endswith(".md")
    )

    tree_lines = [f"📚 {os.path.basename(directory)}/"] + build_tree(directory)
    tree_output = "\n".join(tree_lines)

    print("=" * 70)
    print("  MARKDOWN VAULT STRUCTURE MAP".center(70))
    print("=" * 70)
    print(tree_output)
    print("=" * 70)
    print(f"\n  Total Markdown Files: {total_files}")

    if output:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(
                f"# Vault Structure Map\n\n```\n{tree_output}\n```\n\nTotal Files: {total_files}\n"
            )
        print(f"  Saved to: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Map Markdown Structure — Vault Tree Generator"
    )
    parser.add_argument("target", help="Directory to map.")
    parser.add_argument("--out", help="Optional output .md file path.")
    parser.add_argument(
        "--depth", type=int, default=4, help="Max tree depth (default: 4)."
    )
    args = parser.parse_args()
    map_markdown_structure(os.path.abspath(args.target), args.out)


if __name__ == "__main__":
    main()
