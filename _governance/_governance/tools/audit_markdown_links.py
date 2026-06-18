import argparse
import collections
import os
import re
from pathlib import Path
from typing import Tuple

def audit_and_strip_links(workspace_root: Path) -> Tuple[int, int]:
def build_file_index(workspace_root: Path) -> dict:
    """Builds a fast lookup dictionary of filename -> list of Paths in the workspace."""
    index = collections.defaultdict(list)
    for p in workspace_root.rglob("*"):
        if p.is_file() and not any(part.startswith('.') for part in p.parts):
            index[p.name].append(p)
    return index

def audit_and_strip_links(workspace_root: Path) -> Tuple[int, int, int]:
    """
    Scans all Markdown files in the workspace. If a link points to a local file
    that does not exist, it strips the markdown link syntax but preserves the text.
    that does not exist, it searches the workspace for a moved file. If a unique
    match is found, it auto-fixes the link. Otherwise, it strips the markdown link syntax.
    """
    # Matches standard Markdown links: [Link Text](target "Optional Title")
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    total_broken_links = 0
    files_modified = 0
    links_fixed = 0

    # Build index for fast lookup of moved files
    file_index = build_file_index(workspace_root)

    # Find all Markdown files in the workspace
    md_files = list(workspace_root.rglob("*.md"))

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue # Skip binary or non-utf-8 files

        original_content = content

        def replace_if_broken(match: re.Match) -> str:
            nonlocal total_broken_links
            nonlocal total_broken_links, links_fixed
            link_text = match.group(1)
            raw_target = match.group(2).strip()

            # Isolate the path from any titles (e.g., "file.md 'My Title'") or anchors
            target_path_str = raw_target.split(' ')[0].split('#')[0]

            # Ignore external URLs, email links, pure anchors, or empty links
            if not target_path_str or target_path_str.startswith(('http://', 'https://', 'mailto:', '#')):
                return match.group(0)

            # Resolve the target relative to the current markdown file's directory
            try:
                target_file = (md_file.parent / target_path_str).resolve()
            except Exception:
                # Malformed paths
                total_broken_links += 1
                return link_text

            # Check if the target exists in the filesystem
            if not target_file.exists():
                print(f"[FIXED] Broken link in {md_file.relative_to(workspace_root)}: -> '{target_path_str}'")
                target_filename = Path(target_path_str).name
                candidates = file_index.get(target_filename, [])

                if len(candidates) == 1:
                    # Unambiguous match found - automatically fix the link
                    correct_file = candidates[0]
                    new_rel_path = os.path.relpath(correct_file, md_file.parent).replace('\\', '/')
                    fixed_target = raw_target.replace(target_path_str, new_rel_path)
                    
                    print(f"[AUTO-FIX] Link updated in {md_file.relative_to(workspace_root)}: '{target_path_str}' -> '{new_rel_path}'")
                    links_fixed += 1
                    return f"[{link_text}]({fixed_target})"
                elif len(candidates) > 1:
                    print(f"[AMBIGUOUS] Broken link in {md_file.relative_to(workspace_root)}: '{target_path_str}'. Found {len(candidates)} candidates. Stripping link.")
                else:
                    print(f"[STRIPPED] Broken link in {md_file.relative_to(workspace_root)}: -> '{target_path_str}' (No candidates found)")

                total_broken_links += 1
                return link_text # Strip the link, return just the text

            # Link is valid, keep original formatting
            return match.group(0)

        # Apply the regex substitution
        new_content = link_pattern.sub(replace_if_broken, content)

        if new_content != original_content:
            md_file.write_text(new_content, encoding='utf-8')
            files_modified += 1

    return total_broken_links, files_modified

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit and sanitize broken Markdown links.")
    parser.add_argument(
        "--dir",
        default=".",
        help="The root directory to scan (defaults to current directory)"
    )
    args = parser.parse_args()

    root_path = Path(args.dir).resolve()
    print(f"Scanning workspace: {root_path}...\n")
    broken_count, modified_count = audit_and_strip_links(root_path)
    print(f"\nAudit Complete. Stripped {broken_count} broken links across {modified_count} files.")