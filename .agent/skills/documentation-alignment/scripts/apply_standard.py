"""
## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.apply.standard`                | The Sovereign ID. |
| **Official Name** | `apply_standard.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |


---

## **Block B: State Vector (AGP-001)**

| State Field   | Value     |
| :------------ | :-------- |
| **Coherence** | `1.0`     |
| **Resonance** | `1.0`     |
| **Stability** | `Stable`  |


---

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                |
| :------------------- | :------------------------ |
| **Logic Drift**      | Strict Linter Enforcement |
| **Semantic Decay**   | Axiomatic Compass Audit   |


---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
| :---------------------- | :---------------- | :---------------------------------------------- |
| `CORE.Codex.Phoenix`    | `GOVERNS`         | Provides the supreme law and ethical framework. |


---
"""

import argparse
import os
import shutil
from datetime import date
from pathlib import Path

from governance_utils import (
    UIP_V15_MD_TEMPLATE,
    UIP_V15_PY_TEMPLATE,
    ShadowLogger,
    generate_omni_anchor,
    get_artifact_id,
    is_v15_compliant,
    strip_legacy_headers,
)


def apply_alignment(filepath: Path, dry_run: bool = False):
    """Apply UIP-V15 header and structural alignment to a file."""
    shadow = ShadowLogger("Align")

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return False

    if is_v15_compliant(content):
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would align: {filepath.name}")
        return True

    # Synthesis Phase
    filename = filepath.name
    artifact_id = get_artifact_id(filename)
    domain = "GVRN"
    status = "[CANONIZED]"
    today = date.today().isoformat()

    # Strip legacy
    clean_content = strip_legacy_headers(content)

    # Generate Omni-Anchor (Block G)
    anchor = generate_omni_anchor(artifact_id, domain, status)

    # Choose template
    if filename.endswith(".py"):
        header = UIP_V15_PY_TEMPLATE.format(
            artifact_id=artifact_id,
            filename=filename,
            domain=domain,
            status=status,
            date=today,
        )
        # Note: We don't usually put Block G inside Py docstrings unless requested,
        # but for OMEGA v15.0 consistency, we can append it at the end of the docstring.
        # However, it's typically a separate comment block if needed.
        # For now, let's keep Py simple or follow Codex.
        new_content = header + "\n" + clean_content
    else:
        header = UIP_V15_MD_TEMPLATE.format(
            artifact_id=artifact_id,
            filename=filename,
            domain=domain,
            status=status,
            date=today,
        )
        # Ensure [ARTIFACT START/END] are present for MD
        if "[ARTIFACT START]" not in clean_content:
            clean_content = "\n\n" + clean_content
        if "[ARTIFACT END]" not in clean_content:
            clean_content = clean_content + "\n\n"

        # Inject the anchor after Block D but before Start/End (according to Codex)
        # Or ideally at the end of the metadata block.
        # Following CORE.Codex.Phoenix.md: Block G is the last block BEFORE [ARTIFACT START].
        new_content = header + "\n" + anchor + "\n\n" + clean_content

    # Backup and Write
    shutil.copy2(filepath, filepath.with_suffix(filepath.suffix + ".v13bak"))
    filepath.write_text(new_content, encoding="utf-8")

    shadow.log_synthesis(str(filepath), f"Upgraded to UIP-V15 ({artifact_id})")
    print(f"  [ALIGNED] {filename}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Apply Standard - OMEGA v15.0 Alignment"
    )
    parser.add_argument("target", help="File or directory to align")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without writing"
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if target.is_file():
        apply_alignment(target, args.dry_run)
    elif target.is_dir():
        # Scoped to relevant files
        files = list(target.rglob("*.py")) + list(target.rglob("*.md"))
        print(f"\n>>> SYNERGIZING TARGET: {target}\n")
        for f in files:
            if any(
                skip in str(f) for skip in [".git", "__pycache__", ".v13bak", ".venv"]
            ):
                continue
            apply_alignment(f, args.dry_run)


if __name__ == "__main__":
    main()
