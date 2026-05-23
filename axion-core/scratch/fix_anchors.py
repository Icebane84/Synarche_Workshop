import os
import re


def fix_anchors(root_dir):
    re.compile(r"^`?\[OMNI-ARTIFACT-ANCHOR\]", re.MULTILINE)

    for root, _dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                changed = False

                # Fix unquoted anchors and metadata blocks
                if "[OMNI-ARTIFACT-ANCHOR]" in content or "### **Block G" in content:
                    lines = content.splitlines()
                    in_metadata_block = False
                    for i, line in enumerate(lines):
                        # Detect start of stray metadata block
                        if "### **Block G" in line or line.strip() == "---":
                            if not line.strip().startswith("#"):
                                in_metadata_block = True

                        if in_metadata_block and not line.strip().startswith("#"):
                            if (
                                line.strip()
                            ):  # Don't comment empty lines if they don't matter, but better safe
                                lines[i] = "# " + line.replace("`", "")
                                changed = True

                        if "[OMNI-ARTIFACT-ANCHOR]" in line:
                            if not line.strip().startswith("#"):
                                lines[i] = "# " + line.replace("`", "")
                                changed = True
                            in_metadata_block = False  # End of block

                    content = "\n".join(lines) + "\n"

                # Fix unterminated triple quotes added at the end
                # Look for a single """ followed by comments and the anchor
                if content.count('"""') % 2 != 0:
                    # Find the last triple quote that isn't the start of the file
                    # Or just remove the stray one near the end
                    lines = content.splitlines()
                    for i in range(len(lines) - 1, 0, -1):
                        if lines[i].strip() == '"""':
                            lines[i] = '# """ (Fixing unterminated string)'
                            changed = True
                            break
                    content = "\n".join(lines) + "\n"

                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Fixed: {path}")


if __name__ == "__main__":
    fix_anchors("c:/Users/Chris/Synarche_Workspace/axion-core/src")
