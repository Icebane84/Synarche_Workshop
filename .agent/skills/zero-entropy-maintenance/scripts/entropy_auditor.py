"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-ENTROPY-AUDITOR-001`     | The Sovereign ID. |
| **Official Name** | `entropy_auditor.py`           | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                   | Creation Date.    |.
"""

import argparse
import os
import re


def audit_entropy(directory: str) -> None:
    print(f"\n>>> SCANNING ENTROPY IN: {directory}\n")

    total_todos = 0
    total_fixmes = 0
    total_shadow_lines = 0
    files_with_debt = 0
    total_files = 0

    # Patterns that indicate legitimate metadata/structure rather than dead code
    METADATA_PREFIXES = (
        "# |",
        "# ---",
        "# [",
        "# ##",
        "// |",
        "// ---",
        "// [",
        "// ##",
    )

    for root, _, files in os.walk(directory):
        if any(
            x in root
            for x in [
                "node_modules",
                ".git",
                ".venv",
                "__pycache__",
                "out",
                "out_debug",
            ]
        ):
            continue

        for f in files:
            if f.endswith((".py", ".ts", ".tsx", ".js", ".cjs", ".mjs", ".md")):
                total_files += 1
                path = os.path.join(root, f)
                try:
                    with open(path, encoding="utf-8") as file:
                        content = file.read()
                        lines = content.splitlines()
                except Exception:
                    continue

                # Remove multi-line strings from consideration for shadow code in Python/JS/TS
                if f.endswith((".py", ".ts", ".tsx", ".js")):
                    # Simple heuristic: remove everything between triple quotes
                    content_no_strings = re.sub(r'"""[\s\S]*?"""', "", content)
                    content_no_strings = re.sub(
                        r"'''[\s\S]*?'''", "", content_no_strings
                    )
                    # For JS/TS, also handle backticks
                    if f.endswith((".js", ".ts", ".tsx")):
                        content_no_strings = re.sub(
                            r"`[\s\S]*?`", "", content_no_strings
                        )
                    lines_to_check = content_no_strings.splitlines()
                else:
                    lines_to_check = lines

                file_todos = 0
                file_fixmes = 0
                file_shadow = 0
                consecutive_comments = 0

                # Scan for TODO/FIXME in ALL lines (even strings, as they might be relevant)
                for line in lines:
                    line_upper = line.upper()
                    if "TODO" in line_upper:
                        file_todos += 1
                    if "FIXME" in line_upper:
                        file_fixmes += 1

                # Scan for SHADOW CODE only in non-string lines
                for line in lines_to_check:
                    stripped = line.strip()

                    # Check if it's a comment
                    is_comment = stripped.startswith("#") or stripped.startswith("//")

                    # Check if it's a METADATA comment (exclude from shadow count)
                    is_metadata = any(stripped.startswith(p) for p in METADATA_PREFIXES)

                    if is_comment and not is_metadata:
                        consecutive_comments += 1
                    else:
                        if consecutive_comments >= 3:
                            file_shadow += consecutive_comments
                        consecutive_comments = 0

                if consecutive_comments >= 3:
                    file_shadow += consecutive_comments

                if file_todos > 0 or file_fixmes > 0 or file_shadow > 0:
                    print(
                        f"[!] INFECTED: {path} (TODO: {file_todos}, FIXME: {file_fixmes}, SHADOW: {file_shadow})"
                    )
                    files_with_debt += 1
                    total_todos += file_todos
                    total_fixmes += file_fixmes
                    total_shadow_lines += file_shadow

    # Mathematical aggregation for Technical Debt Mass (TDM)
    tdm = (total_todos * 5) + (total_fixmes * 15) + (total_shadow_lines * 2)

    # Calculate System Stability (RPG Stat mapping)
    # A perfect system has 0 TDM -> 100 Stability.
    stability = max(0.0, 100.0 - (tdm / 10.0))  # Relaxed slightly for OMEGA scale

    print("=" * 60)
    print("  ENTROPY BURDEN (TECHNICAL DEBT MASS) REPORT".center(60))
    print("=" * 60)
    print(f" Files Scanned:       {total_files}")
    print(f" Entropy Vectors:     {files_with_debt} infected files")
    print("-" * 60)
    print(f" TODO Markers:        {total_todos} (Mass: x5)")
    print(f" FIXME Markers:       {total_fixmes} (Mass: x15)")
    print(f" Shadow Code Lines:   {total_shadow_lines} (Mass: x2)")
    print("-" * 60)
    print(f" TOTAL DEBT MASS:     {tdm}")
    print(f" SYSTEM STABILITY:    {stability:.1f} / 100.0")
    print("=" * 60)

    if stability < 50:
        print(
            "\n[!] CRITICAL ENTROPY: System is unstable. Immediate Code Scrub required."
        )
    elif stability < 95:
        print(
            "\n[*] MODERATE ENTROPY: Technical debt is accumulating. Plan a refactor soon."
        )
    else:
        print("\n[OK] SYSTEM STABLE: Entropy is within acceptable operational bounds.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Entropy Auditor")
    parser.add_argument("target", help="Directory to scan.")
    args = parser.parse_args()

    target = os.path.abspath(args.target)
    if os.path.isdir(target):
        audit_entropy(target)
    else:
        print(f"Error: {target} is not a directory.")


if __name__ == "__main__":
    main()
