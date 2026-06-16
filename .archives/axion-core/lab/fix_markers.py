"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-FIX-MARKERS-001`         | The Sovereign ID. |
| **Official Name** | `fix_markers.py`               | The Filename.     |
| **Version**       | **v1.1**                       | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Status**        | `[ACTIVE]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |.

---

# Fix Markers (The Sentinel's Stitch)
Injects [ARTIFACT START] and [ARTIFACT END] markers into Markdown files
if they are missing, ensuring compliance with analyze_docs_compliance.py.
"""

from pathlib import Path

START_MARKER = "[ARTIFACT START]"
END_MARKER = "[ARTIFACT END]"


def fix_file(filepath: Path) -> bool:
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return False

    content = "".join(lines)
    changed = False

    # Inject START after Block 0 or first H3/H1 if missing
    if START_MARKER not in content:
        # Find the line after the first separator ---
        for i, line in enumerate(lines):
            if "---" in line:
                lines.insert(i + 1, f"\n{START_MARKER}\n")
                changed = True
                break
        else:
            # Fallback: Prepend
            lines.insert(0, f"{START_MARKER}\n")
            changed = True

    # Inject END at the very bottom if missing
    if END_MARKER not in content:
        lines.append(f"\n{END_MARKER}\n")
        changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    return False


def main():
    root = Path("c:/Users/Chris/Synarche_Workspace/axion-core")
    fixed = 0
    scanned = 0
    for md_file in root.glob("**/*.md"):
        if any(p in md_file.parts for p in [".git", "node_modules", "__pycache__"]):
            continue
        scanned += 1
        if fix_file(md_file):
            fixed += 1
            print(f"  [FIXED] {md_file.relative_to(root)}")

    print(f"\nScan Complete: {scanned} files, {fixed} fixed.")


if __name__ == "__main__":
    main()
