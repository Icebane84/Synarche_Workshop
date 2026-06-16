import re
from pathlib import Path

# Patterns to identify hardcoded blocks
BLOCK_F_PATTERN = re.compile(
    r"### \*\*Block F: The Integrity Gate \(CIV-GATE\)\*\*.*?\| Status .*?\| PASS .*?\| SENTINEL \|.*?(?:---|$)",
    re.DOTALL,
)
BLOCK_G_PATTERN = re.compile(
    r"### \*\*Block G: The Omni-Anchor \(System Snapshot\)\*\*.*?\* \[OMNI-ARTIFACT-ANCHOR\],?.*? \[PHOENIX-ARTIFACT-ANCHOR\].*?(?:---|$)",
    re.DOTALL,
)


def refactor_file(file_path: Path) -> bool:
    """Replaces hardcoded blocks with TRANSCLUDE tags."""
    content = file_path.read_text(encoding="utf-8")
    original_content = content

    # 1. Replace Block F
    if "SELT-GATE-CIV-001.md" not in content:
        content = BLOCK_F_PATTERN.sub(
            "\n{{ TRANSCLUDE: SELT-GATE-CIV-001.md }}\n", content
        )

    # 2. Replace Block G
    if "SELT-ANCHOR-OMNI.md" not in content:
        content = BLOCK_G_PATTERN.sub(
            "\n{{ TRANSCLUDE: SELT-ANCHOR-OMNI.md }}\n", content
        )

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False


def grand_weave(target_dir: str) -> None:
    """Recursively refactor the governance substrate."""
    root = Path(target_dir).resolve()
    print(f"\n>>> INITIATING GRAND WEAVE REFACTOR: {root}\n")

    modified_count = 0
    total_count = 0

    for file_path in root.glob("**/*.md"):
        # Skip templates and archives
        if (
            "templates" in str(file_path).lower()
            or "_archive" in str(file_path).lower()
        ):
            continue

        total_count += 1
        if refactor_file(file_path):
            modified_count += 1
            print(f"  [MODIFIED] {file_path.name}")
        else:
            if "TRANSCLUDE" in file_path.read_text(encoding="utf-8"):
                print(f"  [SKIPPED]  {file_path.name} (Already transcluded)")
            else:
                pass  # No target blocks found

    print(f"\n>>> REFACTOR COMPLETE: {modified_count}/{total_count} files updated.")


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "_governance"
    grand_weave(target)
