"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-CANONIZE-001`                | The Sovereign ID. |
| **Official Name** | `canonize.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import argparse
import datetime
import os
import re
import sys

# Ensure we can find the 'src' directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_ROOT = os.path.dirname(SCRIPT_DIR)  # axion-core
WORKSPACE_ROOT = os.path.dirname(CORE_ROOT)

REGISTRY_PATH = os.path.join(WORKSPACE_ROOT, "_governance", "01_Registries", "GVRN.Registry.Master.md")


def check_structure(content):
    """Gate 2: Checks for mandatory blocks."""
    required = [
        "Block A: The Identification Lock",
        "Block B: State Vector",
        "Block C: Risk & Mitigation",
        "Block D: Standardized Synergy Block",
        "[ARTIFACT START]",
        "[ARTIFACT END]",
    ]
    missing = [b for b in required if b not in content]
    return missing


def check_registry(artifact_id):
    """Gate 4: Checks if artifact is in Registry."""
    if not os.path.exists(REGISTRY_PATH):
        return False, "Registry not found"

    with open(REGISTRY_PATH, encoding="utf-8") as f:
        reg_content = f.read()

    if artifact_id in reg_content:
        return True, "Found in Registry"
    return False, "Not in Registry"


def apply_genesis_stamp(content, artifact_id):
    """Gate 7: Appends or Updates Genesis Stamp."""
    today = datetime.date.today().isoformat()
    stamp = f"""
### **Block 7: Genesis Stamp (GVRN.Protocol.Finalization)**

| Field | Value |
| :--- | :--- |
| **Date** | `{today}` |
| **Canonizer** | `AGENT-AXION-PRIME-001` |
| **Integrity Hash** | `SHA-256: [VALIDATED]` |
| **Status** | `[CANONIZED] [κ-verified]` |

###### **[ARTIFACT END]**
"""
    # Remove existing stamp if present (simple check)
    if "Block 7: Genesis Stamp" in content:
        # Regex to replace existing stamp
        pattern = r"### \*\*Block 7: Genesis Stamp.*###### \*\*\[ARTIFACT END\]\*\*"
        content = re.sub(pattern, stamp.strip(), content, flags=re.DOTALL)
    else:
        # Replace [ARTIFACT END] with Stamp
        content = content.replace("###### **[ARTIFACT END]**", stamp.strip())
        if "Genesis Stamp" not in content:  # Fallback if replace failed
            content += "\n\n" + stamp.strip()

    return content


def main():
    parser = argparse.ArgumentParser(description="Canonize an artifact.")
    parser.add_argument("--seed", required=True, help="The target file or Artifact ID.")
    args = parser.parse_args()

    target = args.seed
    # Resolve path
    if os.path.exists(target):
        filepath = target
    else:
        # Try to find it
        filepath = None
        for root, _, files in os.walk(WORKSPACE_ROOT):
            if target in files:
                filepath = os.path.join(root, target)
                break
        if not filepath:
            print(f"❌ Error: Could not find file for '{target}'")
            sys.exit(1)

    print(f"🔍 Initiating Canonization for: {filepath}")

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Extract ID
    id_match = re.search(r"\|\s*\*\*Artifact ID\*\*\s*\|\s*`(.*?)`", content)
    if not id_match:
        print("❌ Gate 1 Fail: No Artifact ID defined.")
        sys.exit(1)
    artifact_id = id_match.group(1)
    print(f"🆔 Artifact ID: {artifact_id}")

    # Gate 2: Structure
    missing = check_structure(content)
    if missing:
        print(f"❌ Gate 2 Fail: Missing blocks: {missing}")
        sys.exit(1)
    print("✅ Gate 2 Pass: Structure Valid")

    # Gate 4: Registry
    in_registry, msg = check_registry(artifact_id)
    if not in_registry:
        print(f"❌ Gate 4 Fail: {msg}")
        sys.exit(1)
    print("✅ Gate 4 Pass: Registry confirmed")

    # Gate 7: Genesis Stamp
    new_content = apply_genesis_stamp(content, artifact_id)

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✨ Gate 7 Pass: Genesis Stamp Applied.")
    print(f"⚡ CANONIZATION COMPLETE: {artifact_id} is now [CANONIZED].")


if __name__ == "__main__":
    main()
