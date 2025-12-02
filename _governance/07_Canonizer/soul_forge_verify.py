import os
import re
import sys

def verify_file(filepath):
    print(f"Verifying: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []

    # Check for OMEGA v15.0 header
    if "v15.0 [OMEGA]" not in content:
        errors.append("Missing 'v15.0 [OMEGA]' header.")

    # Check for Status Tag
    if not any(status in content for status in ["[CANONIZED]", "[SYNTHESIZED]", "STATUS: SYNTHESIZED", "STATUS: CANONIZED"]):
        errors.append("Missing or invalid Status Tag (CANONIZED/SYNTHESIZED).")

    # Check for IDs (Optional but recommended)
    if not re.search(r"ID: GVRN\.SOUL\.[A-Z]+", content) and not re.search(r"ID: GVRN\.TRIAD", content):
         errors.append("Missing ID tag (e.g., ID: GVRN.SOUL.AXION).")

    if errors:
        print(f"  [FAIL] {len(errors)} errors found:")
        for error in errors:
            print(f"    - {error}")
        return False
    else:
        print("  [PASS] Compliance verified.")
        return True

def verify_directory(directory):
    success_count = 0
    total_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                total_count += 1
                if verify_file(os.path.join(root, file)):
                    success_count += 1
    
    print(f"\nVerification Summary: {success_count}/{total_count} files passed.")
    return success_count == total_count

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    if os.path.isfile(target):
        if verify_file(target):
            sys.exit(0)
        else:
            sys.exit(1)
    elif os.path.isdir(target):
        if verify_directory(target):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print(f"Target {target} not found.")
        sys.exit(1)
