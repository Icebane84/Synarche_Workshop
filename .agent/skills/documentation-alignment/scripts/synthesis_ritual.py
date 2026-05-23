import os
import re
import sys
from pathlib import Path

# Absolute Path Calibration
# synthesis_ritual.py is in .agent/skills/documentation-alignment/scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Traversal: scripts -> documentation-alignment -> skills -> .agent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
# Sync Root: parent of .agent
SYNC_ROOT = os.path.dirname(BASE_DIR)

# Add governance_utils to path
sys.path.append(SCRIPT_DIR)
import governance_utils as utils

TARGET_ROOT = os.path.join(SYNC_ROOT, "axion-core/src")


def synthesize_file(filepath):
    """Inject Block A and Block G into a file if missing."""
    p = Path(filepath)
    if p.suffix not in [".py", ".md"]:
        return

    with open(p, "r", encoding="utf-8") as f:
        content = f.read()

    # Seal Check: Is it already compliant?
    if utils.is_v15_compliant(content) and "# Block G" in content:
        return

    print(f"[ Synthesis ] Processing: {p.name}...")

    # Extract or generate Artifact ID
    domain = "CORE"
    if "axion-core/src/agents" in str(p):
        domain = "CORE.AGENT"
    elif "axion-core/src/logic" in str(p):
        domain = "CORE.LOGIC"

    artifact_id = utils.get_artifact_id(p.name, domain)
    official_name = p.name

    # Check for Block A + START/END
    if "Block A" not in content or "[ARTIFACT START]" not in content:
        # Strip old v15-ish headers to avoid duplication
        content = utils.strip_legacy_headers(content)

        # Generate Block A block for Python
        if p.suffix == ".py":
            # Remove existing docstring if it exists at the very top
            if content.startswith('"""') or content.startswith("'''"):
                content = re.sub(r"^(\"\"\"|\'\'\')[\s\S]*?\1", "", content).lstrip()

            header = (
                '"""\n'
                + "## **[ARTIFACT START]**\n\n"
                + utils.BLOCK_A_TEMPLATE.format(
                    artifact_id=artifact_id,
                    official_name=official_name,
                    domain=domain,
                    status="[ACTIVE]",
                )
                + "\n"
                + utils.BLOCK_B_TEMPLATE.format(resonance="1.0")
                + "\n"
                + utils.BLOCK_C_TEMPLATE
                + "\n"
                + utils.BLOCK_D_TEMPLATE
                + "\n"
                + "## **[ARTIFACT END]**\n"
                + '"""\n'
            )
            content = header + "\n" + content
        elif p.suffix == ".md":
            header = (
                "## **[ARTIFACT START]**\n\n"
                + utils.BLOCK_A_TEMPLATE.format(
                    artifact_id=artifact_id,
                    official_name=official_name,
                    domain=domain,
                    status="[ACTIVE]",
                )
                + "\n---\n"
            )
            # Ensure markdown also has END marker
            if "## **[ARTIFACT END]**" not in content:
                content = header + content + "\n\n## **[ARTIFACT END]**"
            else:
                content = header + content

    # Check for Block G (Omni-Anchor)
    if "Block G: The Omni-Anchor" not in content or (
        p.suffix == ".py"
        and "### **Block G" in content
        and "# ### **Block G" not in content
    ):
        # Strip un-commented Block G in Python if it exists
        if p.suffix == ".py":
            content = re.sub(
                r"\n---?\n\n?### \*\*Block G:.*", "", content, flags=re.DOTALL
            )

        anchor = utils.generate_omni_anchor(artifact_id, domain, status="[SYNTHESIZED]")
        if p.suffix == ".py":
            # Comment out the anchor for Python files
            anchor = "\n# " + anchor.replace("\n", "\n# ")
            content = content.rstrip() + "\n" + anchor
        elif p.suffix == ".md" and "## **[ARTIFACT END]**" in content:
            # Avoid duplicating END marker
            content = content.replace(
                "## **[ARTIFACT END]**", f"## **[ARTIFACT END]**\n\n{anchor}"
            )
        else:
            content = content.rstrip() + "\n\n" + anchor

    # Write back
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Synthesis Complete: {artifact_id}")


def run_synthesis(target_dir):
    print(f"[*] Starting Structural Synthesis in {target_dir}...")
    for root, _dirs, files in os.walk(target_dir):
        if "__pycache__" in root:
            continue
        for file in files:
            synthesize_file(os.path.join(root, file))


if __name__ == "__main__":
    run_synthesis(TARGET_ROOT)
