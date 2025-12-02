"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-FIX-MD013-001`                | The Sovereign ID. |
| **Official Name** | `fix_md013.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

#!/usr/bin/env python3
import argparse
import sys
import textwrap


def fix_md013(file_path, line_length=120, dry_run=False):
    """Reads a markdown file and wraps lines longer than line_length,
    preserving code blocks, tables, and frontmatter.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    new_lines = []
    in_code_block = False
    in_frontmatter = False
    frontmatter_separator_count = 0

    # Simple heuristic to detect URL-only lines or similar that shouldn't be wrapped aggressively
    # (Though textwrap usually handles long words by breaking them or keeping them if break_long_words=False)

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        original_line_with_newline = line

        # --- State Management ---

        # Frontmatter detection
        if i == 0 and stripped_line == "---":
            in_frontmatter = True
            frontmatter_separator_count += 1
            new_lines.append(original_line_with_newline)
            continue

        if in_frontmatter:
            new_lines.append(original_line_with_newline)
            if stripped_line == "---":
                frontmatter_separator_count += 1
                if frontmatter_separator_count == 2:
                    in_frontmatter = False
            continue

        # Code block detection
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(original_line_with_newline)
            continue

        if in_code_block:
            new_lines.append(original_line_with_newline)
            continue

        # Table detection (heuristic: line starts with |)
        if stripped_line.startswith("|"):
            new_lines.append(original_line_with_newline)
            continue

        # --- Wrapping Logic ---

        # Don't wrap headings
        if stripped_line.startswith("#"):
            new_lines.append(original_line_with_newline)
            continue

        # Don't wrap if line is short enough
        if len(line.rstrip()) <= line_length:
            new_lines.append(original_line_with_newline)
            continue

        # Handle Blockquotes
        prefix = ""
        content_to_wrap = line.rstrip()

        if stripped_line.startswith("> "):
            prefix = "> "
            content_to_wrap = line.rstrip()[line.find("> ") + 2 :]
        elif stripped_line.startswith(">"):  # Handle ">Text" without space
            prefix = "> "
            content_to_wrap = line.rstrip()[line.find(">") + 1 :]

        # Setup textwrapper
        # break_long_words=False ensures we don't break long URLs
        # break_on_hyphens=False keeps hyphenated words together
        wrapper = textwrap.TextWrapper(
            width=line_length,
            initial_indent=prefix,
            subsequent_indent=prefix,
            break_long_words=False,
            break_on_hyphens=False,
        )

        wrapped_lines = wrapper.wrap(content_to_wrap)

        # Start a new block of lines
        for wl in wrapped_lines:
            new_lines.append(wl + "\n")

    # Write back to file
    # Write back to file or print diff
    if dry_run:
        print(f"[DRY RUN] Would write {len(new_lines)} lines to {file_path}")
        # Could implement a diff here if desired
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Successfully processed {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Autofix MD013 (line length) in Markdown files."
    )
    parser.add_argument("file", help="Path to the markdown file to fix.")
    parser.add_argument(
        "--length", type=int, default=120, help="Maximum line length (default: 120)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without writing."
    )

    args = parser.parse_args()
    fix_md013(args.file, args.length, args.dry_run)
