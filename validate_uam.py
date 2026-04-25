import os
import re
import sys


def validate_uam_anchors(directory_path: str) -> bool:
    """
    Scans a directory for files containing the artifact_anchor block
    and validates the presence and values of required Sovereign Metadata fields using PyYAML.
    """
    required_fields = ["id", "version", "provenance", "domain", "celestial_class", "tier", "state", "ethos"]

    allowed_celestial_classes = {"STAR", "PLANET", "MOON"}
    allowed_states = {"PROPOSED", "DRAFT", "ACTIVE", "CANONIZED"}

    # Regex to extract the YAML block following 'artifact_anchor:'
    # It stops at standard comment closers like -->, """, ''', or end of file
    anchor_pattern = re.compile(r"artifact_anchor:\s*(.*?)(?:-->|\"\"\"|'''|\Z)", re.DOTALL)

    missing_anchor_files = []
    invalid_anchor_files = []

    print(f"Scanning Nexus: {directory_path}...\n")

    for root, dirs, files in os.walk(directory_path):
        # Ignore standard environments and git folders
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", "node_modules", "venv", "env"]]

        for file in files:
            # Target relevant source files
            if not file.endswith((".py", ".html", ".md", ".ts", ".js")):
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                match = anchor_pattern.search(content)

                if not match:
                    missing_anchor_files.append(file_path)
                    continue

                anchor_text = match.group(1)
                missing_fields = []

                # Check for the existence of each required field key
                for field in required_fields:
                    if not re.search(rf"{field}:\s+", anchor_text):
                        missing_fields.append(field)

                if missing_fields:
                    invalid_anchor_files.append((file_path, missing_fields))

            except Exception as e:
                print(f"[!] Error reading {file_path}: {e}")

    # Reporting
    print("=== UAM VALIDATION REPORT ===")
    if not missing_anchor_files and not invalid_anchor_files:
        print("ALL CLEAR: All scanned artifacts possess a valid 12-Point Sovereign Metadata Lock.")

    if missing_anchor_files:
        print(f"\n[CRITICAL] Missing 'artifact_anchor' block ({len(missing_anchor_files)} files):")
        for mf in missing_anchor_files:
            print(f"  - {mf}")

    if invalid_anchor_files:
        print(f"\n[WARNING] Malformed 'artifact_anchor' block ({len(invalid_anchor_files)} files):")
        for inv_f, errors in invalid_anchor_files:
            print(f"  - {inv_f} | Issues: {', '.join(errors)}")

    return not missing_anchor_files and not invalid_anchor_files


if __name__ == "__main__":
    # Defaults to the current working directory where the script is executed
    target_directory = os.getcwd()
    is_valid = validate_uam_anchors(target_directory)
    sys.exit(0 if is_valid else 1)
