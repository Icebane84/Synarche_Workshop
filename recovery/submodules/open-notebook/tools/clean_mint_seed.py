import os

INPUT_FILE = r"c:\Users\Chris\_Desktop_Vault\Phoenix\input_artifacts\mint_seed.py.md"
OUTPUT_FILE = (
    r"c:\Users\Chris\Synarche_Workspace\_governance\40_System\AXION.MINT.SEED.001.md"
)
ARCHIVE_FILE = (
    r"c:\Users\Chris\Synarche_Workspace\_governance\99_Archives\mint_seed.py.md"
)

GOVERNANCE_HEADER = """# AXION.MINT.SEED.001


| Key | Value | Description |
| :--- | :--- | :--- |
| **Artifact ID** | `AXION.MINT.SEED.001` | The Sovereign ID. |
| **Official Name** | `AXION.MINT.SEED.001.md` | The Filename. |
| **Version** | **v1.0 [ALPHA]** | The Standard. |
| **Domain** | `AXION` | The Subject. |
| **Celestial Class** | `[SATELLITE]` | The Weight. |
| **Evolution** | `Emerging` | The Maturity. |
| **Status** | `[ACTIVE]` | The Lifecycle. |
| **Relations** | `GOVERNS: [Nicemind_Seeds], ALIGNS: GVRN.Axiomatic.Lattice` | The Network. |

---

## **Block B: State Vector (AGP-001)**

| State Field | Value |
| :--- | :--- |
| **Coherence** | `1.0` |
| **Resonance** | `0.9` |
| **Stability** | `Stable` |

## **Block C: Risk & Mitigation (AGP-002)**

| Risk | Mitigation |
| :--- | :--- |
| **Logic Drift** | Strict Linter Enforcement |
| **Dependency Break** | ForgeLink Validation |

---

> **Signal**: ALPHA

---

###### **[ARTIFACT START]**

## 1.0 Overview

This artifact contains the `ArtifactTransmuter` utility, designed to convert Synarche Markdown artifacts into a Nicemind-compatible import format.
It parses the Governance Blocks (A, D) and transforms them into a mindmap tree structure.

## 2.0 Source Code (`mint_seed.py`)

```python
"""

GOVERNANCE_FOOTER = """
```

---

###### **[ARTIFACT END]**

---

### **Block F: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: AXION.MINT.SEED.001 VER: v1.0 [ALPHA] HASH: [AUTO] STATE-VECTOR: [Active : Tool : Coherence] ETHOS: Seeds of Cognition. STATUS: ACTIVE`

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---
"""


def clean_and_process():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    clean_lines = []
    for line in lines:
        # Strip backticks at the start and end of lines, common in the source file
        # The file format is `line of code`
        stripped = line.strip()
        if stripped.startswith("`") and stripped.endswith("`"):
            # clean `code` -> code
            # But be careful of indentation.
            # actually, let's look at the raw line content
            # The pattern seems to be: `code`
            # We want to keep indentation if it exists inside the backticks, or outside?
            # Looking at file content: `    def __init__(self, source_dir, output_file):`
            # The backticks wrap the whole line including indentation? No, usually indentation is outside or inside.
            # Let's assume standard markdown code block wasn't used, but inline code for every line.

            # Simple regex to remove leading/trailing backtick
            # Replaces first ` and last `
            # But we must preserve leading whitespace *inside* the backtick if the user put it there?
            # Or is the indentation outside?
            # Sample: `    def __init__(...` -> the backtick is at the start.

            content = stripped[1:-1]  # remove first and last char
            clean_lines.append(content)
        else:
            # If no backticks, just check if it's a normal line or empty
            clean_lines.append(line.rstrip())

    # Write the new artifact
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(GOVERNANCE_HEADER)
        f.write("\n".join(clean_lines))
        f.write(GOVERNANCE_FOOTER)

    print(f"Created {OUTPUT_FILE}")

    # Archive original
    import shutil

    os.makedirs(os.path.dirname(ARCHIVE_FILE), exist_ok=True)
    shutil.move(INPUT_FILE, ARCHIVE_FILE)
    print(f"Archived original to {ARCHIVE_FILE}")


if __name__ == "__main__":
    clean_and_process()
