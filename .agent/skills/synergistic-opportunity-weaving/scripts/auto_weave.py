"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-AUTO-WEAVE-001`          | The Sovereign ID. |
| **Official Name** | `auto_weave.py`                | The Filename.     |
| **Version**       | **v15.1 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-07-22`                   | Creation Date.    |.
"""

import argparse
import os
import re
import sys

# Windows console unicode compatibility
sys.stdout.reconfigure(encoding="utf-8")

SKIP_DIRS = {
    ".git", "node_modules", ".venv", ".mypy_cache", ".ruff_cache",
    "_archive", "archive", "99_Archives", "60_Archives", "entropy",
    "incoming", "dist", "out", "playground", "prototypes", "tests", "tools", "_governance"
}

LINK_RE = re.compile(r"\[\[([^\]]+)\]\]|\[([^\]]+)\]\(([^)]+\.md)\)")
ANCHOR_RE = re.compile(r"(\[?(?:OMNI|GATE|RNC|ALIGN|EVOLVE|GOVERN|STABILIZE)-ANCHOR\].*|\[OMNI-ARTIFACT-ANCHOR\].*)", re.IGNORECASE)


def extract_links(content: str) -> set[str]:
    """Extract all internal markdown links from content."""
    links = set()
    for match in LINK_RE.finditer(content):
        target = match.group(1) or os.path.basename(match.group(3) or "")
        if target:
            links.add(target.strip())
    return links


def weave_backlinks(directory: str, dry_run: bool = False) -> None:
    """Scan directory and forge missing reciprocal links using relative paths."""
    nodes = {}

    # Pass 1: Parse all files
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, encoding="utf-8") as fh:
                    content = fh.read()
            except Exception:
                continue
            
            # Clean up old [[wiki-style]] reciprocal links from previous run if any
            # (Matches "- [[something.md]]" or "- [[something]]")
            cleaned_content = re.sub(r"-\s*\[\[[^\]]+\.md\]\]\n?", "", content)
            cleaned_content = re.sub(r"-\s*\[\[[^\]]+\]\]\n?", "", cleaned_content)
            
            if cleaned_content != content:
                content = cleaned_content
                if not dry_run:
                    try:
                        with open(path, "w", encoding="utf-8", newline="\n") as fh:
                            fh.write(content)
                    except Exception:
                        pass

            nodes[f] = {"path": path, "links": extract_links(content), "content": content}

    missing = []
    for fname, data in nodes.items():
        for link in data["links"]:
            # If the linked target is a file we scanned, and it doesn't link back to us
            if link in nodes and fname not in nodes[link]["links"]:
                # Check if the target content already contains references to the source file
                clean_source_name = fname.replace(".md", "")
                target_content = nodes[link]["content"]
                if clean_source_name not in target_content and fname not in target_content:
                    missing.append((fname, link))

    print("\n" + "=" * 70)
    print("  AUTO WEAVE — SYNERGISTIC BACKLINK FORGER (RELATIVE MD)".center(70))
    print("=" * 70)
    print(f"  Files Scanned: {len(nodes)}")
    print(f"  Missing reciprocal links identified: {len(missing)}")
    print("-" * 70)

    if dry_run:
        print("  [DRY RUN] No files will be modified.")
        for src, target in missing[:20]:
            print(f"  Would link [{target}] back to [{src}]")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more.")
        print("=" * 70)
        return

    for src, target in missing:
        target_path = nodes[target]["path"]
        target_content = nodes[target]["content"]
        src_path = nodes[src]["path"]

        # Calculate relative path from target directory to source file
        rel_path = os.path.relpath(src_path, os.path.dirname(target_path)).replace("\\", "/")

        # Form standard markdown link
        backlink_str = f"- [{src}]({rel_path})"

        # Look for existing Relations or Reciprocal Links sections
        if "## Reciprocal Links" in target_content:
            parts = target_content.split("## Reciprocal Links")
            new_content = parts[0] + "## Reciprocal Links\n\n" + backlink_str + "\n" + parts[1].lstrip()
        elif "## Relations" in target_content:
            parts = target_content.split("## Relations")
            new_content = parts[0] + "## Relations\n\n" + backlink_str + "\n" + parts[1].lstrip()
        else:
            # Check for anchor blocks to insert before
            anchor_match = ANCHOR_RE.search(target_content)
            if anchor_match:
                start_pos = anchor_match.start()
                new_content = (
                    target_content[:start_pos].rstrip()
                    + "\n\n## Reciprocal Links\n\n"
                    + backlink_str
                    + "\n\n"
                    + target_content[start_pos:]
                )
            else:
                new_content = target_content.rstrip() + "\n\n## Reciprocal Links\n\n" + backlink_str + "\n"

        # Update in-memory node content to prevent duplicate inserts
        nodes[target]["content"] = new_content
        nodes[target]["links"].add(src)

        # Write to file
        try:
            with open(target_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(new_content)
            print(f"  [FORGED] {target} -> links back to {src}")
        except Exception as e:
            print(f"  [ERROR] Failed to write backlink to {target}: {e}")

    print("-" * 70)
    print("  Weaving operations complete.")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Auto-Weave relative reciprocal backlinks for OGLN/Resonance alignment."
    )
    parser.add_argument("target", help="Directory to scan and weave.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing.")
    args = parser.parse_args()
    
    target = os.path.abspath(args.target)
    weave_backlinks(target, args.dry_run)


if __name__ == "__main__":
    main()
