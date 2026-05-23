#!/usr/bin/env python3
"""IDENTIFICATION: FORGE.BeaconGenerator
VERSION: v1.0.0 [OMEGA]
STATUS: KINETIC
TIMESTAMP: 2026-04-24.

Automatically generates or regenerates index.ts Nexus Beacons for every
directory under a given root. Scans directory contents to produce accurate
docblock comments and determines whether the directory has a TypeScript
surface to export or is a Python-boundary directory.

Usage:
    python generate_beacons.py [root_dir]
    python generate_beacons.py                    # defaults to axion-core/
    python generate_beacons.py src/logic          # target a sub-tree
    python generate_beacons.py --dry-run          # preview without writing
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

AXION_ROOT = Path(__file__).parent.parent  # axion-core/
TIMESTAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Directories to skip entirely
SKIP_DIRS = {
    "__pycache__",
    ".mypy_cache",
    ".venv_prs",
    ".venv",
    "node_modules",
    ".git",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def artifact_id_from_path(rel_path: Path) -> str:
    """Derive a canonical artifact ID from a relative directory path."""
    parts = [p.upper().replace("-", "_").replace(".", "_") for p in rel_path.parts]
    # Drop common noise tokens
    parts = [p for p in parts if p not in {"SRC", "03_FABRIC", "02_DOMAIN"}]
    return ".".join(parts) + ".Gateway" if parts else "ROOT.Gateway"


def describe_files(directory: Path) -> tuple[list[str], list[str], list[str]]:
    """Return (py_files, ts_files, other_files) in the directory (non-recursive)."""
    py, ts, other = [], [], []
    for f in sorted(directory.iterdir()):
        if f.is_file() and f.name != "index.ts":
            if f.suffix == ".py" and not f.name.startswith("__"):
                py.append(f.name)
            elif f.suffix in {".ts", ".tsx"} and not f.name.startswith("__"):
                ts.append(f.name)
            elif f.suffix in {".md", ".json", ".yaml", ".yml", ".js", ".css", ".html"}:
                other.append(f.name)
    return py, ts, other


def sub_index_dirs(directory: Path) -> list[str]:
    """Return sub-directory names that contain an index.ts."""
    return [
        d.name
        for d in sorted(directory.iterdir())
        if d.is_dir() and d.name not in SKIP_DIRS and (d / "index.ts").exists()
    ]


def generate_beacon(directory: Path, rel_path: Path, dry_run: bool = False) -> bool:
    """Generate or update the index.ts beacon for a directory. Returns True if written."""
    py_files, ts_files, other_files = describe_files(directory)
    sub_dirs = sub_index_dirs(directory)

    art_id = artifact_id_from_path(rel_path)
    dir_label = str(rel_path).replace("\\", "/") + "/"

    # Build docblock
    lines: list[str] = [
        "/**",
        f" * {dir_label} — Nexus Beacon",
        f" * {'=' * max(1, 60 - len(dir_label))}",
    ]

    if py_files:
        py_list = ", ".join(py_files[:6])
        if len(py_files) > 6:
            py_list += f", +{len(py_files) - 6} more"
        lines.append(f" * Python modules: {py_list}")

    if ts_files:
        ts_list = ", ".join(ts_files[:6])
        lines.append(f" * TypeScript modules: {ts_list}")

    if other_files:
        other_list = ", ".join(other_files[:5])
        if len(other_files) > 5:
            other_list += f", +{len(other_files) - 5} more"
        lines.append(f" * Other files: {other_list}")

    lines += [
        " *",
        f" * [OMNI-ARTIFACT-ANCHOR] ID: {art_id} VER: v15.0 [OMEGA]"
        f" STATUS: CANONIZED TS: {TIMESTAMP}",
        " */",
        "",
    ]

    # Determine export strategy
    export_lines: list[str] = []

    if ts_files:
        # Has real TypeScript — export each module
        for ts_file in ts_files:
            stem = Path(ts_file).stem
            export_lines.append(f"export * from './{stem}';")

    if sub_dirs:
        for sub in sub_dirs:
            export_lines.append(f"export * from './{sub}';")

    if not export_lines:
        # Python-only boundary
        if py_files:
            export_lines = [
                "// Pure Python layer — no TypeScript exports.",
                "// Accessible via the @nexus/ WebSocket bridge.",
                "export {};",
            ]
        else:
            export_lines = ["export {};"]

    content = "\n".join(lines) + "\n".join(export_lines) + "\n"

    target = directory / "index.ts"

    if dry_run:
        print(f"\n[DRY-RUN] Would write: {target}")
        print(content)
        return False

    target.write_text(content, encoding="utf-8")
    print(f"[BEACON] [DONE] {target.relative_to(AXION_ROOT)}")
    return True


def walk_and_generate(root: Path, dry_run: bool = False) -> int:
    """Recursively generate beacons for directories with a module surface only."""
    count = 0
    for dirpath, dirnames, _ in os.walk(root):
        # Prune skipped dirs in-place so os.walk doesn't recurse into them
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        directory = Path(dirpath)
        rel_path = directory.relative_to(AXION_ROOT)

        py, ts, _ = describe_files(directory)

        # A beacon is only meaningful when there is an importable module surface.
        # Markdown-only, YAML-only, JSON-only, or empty directories get no beacon —
        # they have no TypeScript surface and no Python boundary to document.
        has_module_content = bool(py or ts)
        if not has_module_content:
            continue

        if generate_beacon(directory, rel_path, dry_run):
            count += 1

    return count


def clean_orphan_beacons(root: Path, dry_run: bool = False) -> int:
    """Remove index.ts files from directories with no importable module content."""
    removed = 0
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        directory = Path(dirpath)
        beacon = directory / "index.ts"
        if not beacon.exists():
            continue
        py, ts, _ = describe_files(directory)
        if not py and not ts:
            if dry_run:
                print(
                    f"[DRY-RUN] Would remove orphan beacon: {beacon.relative_to(AXION_ROOT)}"
                )
            else:
                beacon.unlink()
                print(f"[CLEAN] [X] Removed orphan: {beacon.relative_to(AXION_ROOT)}")
            removed += 1
    return removed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Nexus Beacon index.ts files for Axion Core directories."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(AXION_ROOT),
        help="Root directory to scan (default: axion-core/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview generated content without writing files.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove index.ts beacons from directories with no .py or .ts files.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[ERROR] Directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"[FORGE] Scanning: {root}")
    print(
        f"[FORGE] Mode: {'DRY-RUN ' if args.dry_run else ''}{'CLEAN' if args.clean else 'WRITE'}"
    )
    print("-" * 60)

    if args.clean:
        count = clean_orphan_beacons(root, dry_run=args.dry_run)
        print("-" * 60)
        print(
            f"[FORGE] {'Would remove' if args.dry_run else 'Removed'} {count} orphan beacon(s)."
        )
    else:
        count = walk_and_generate(root, dry_run=args.dry_run)
        print("-" * 60)
        print(
            f"[FORGE] {'Previewed' if args.dry_run else 'Generated'} {count} beacon(s)."
        )


if __name__ == "__main__":
    main()
