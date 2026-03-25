import os
import re
import sys
import argparse


def verify_soul_artifact(file_path):
    print(f"[*] Verifying Soul Artifact: {file_path}")

    if not os.path.exists(file_path):
        print(f"[!] Error: File not found at {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # check 1: OMEGA v15.0 Header
    if "v15.0 [OMEGA]" not in content:
        print("[!] Error: Missing OMEGA v15.0 header.")
        return False

    # Check 2: Soul Artifact ID pattern (Check for GVRN.SOUL. prefix)
    if (
        "GVRN.SOUL." not in content
        and "SOUL-" not in content
        and not re.search(r"\[SOUL-.*\]", content)
    ):
        print("[!] Error: Missing SOUL Artifact ID or Anchor ID.")
        return False

    # Check 3: Relationship tokens (Ensure standard Gov headers exist)
    if "Ethical Alignment" not in content and "Governance Anchors" not in content:
        print("[!] Error: Missing Governance Anchors or Ethical Alignment.")
        return False

    print(f"[+] {os.path.basename(file_path)}: Soul Artifact resonance verified.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify Soul Forging Artifacts for OMEGA v15.0 compliance."
    )
    parser.add_argument("file", nargs="?", help="Path to a single file to verify.")
    parser.add_argument("--dir", help="Path to a directory to recursively verify.")

    args = parser.parse_args()

    if args.dir:
        files_to_verify = []
        for root, _, files in os.walk(args.dir):
            for file in files:
                if file.endswith(".md"):
                    files_to_verify.append(os.path.join(root, file))

        results = [verify_soul_artifact(f) for f in files_to_verify]
        if all(results):
            print(f"\n[SUCCESS] {len(results)} artifacts verified in {args.dir}")
            sys.exit(0)
        else:
            print(f"\n[FAILURE] One or more artifacts failed verification.")
            sys.exit(1)

    elif args.file:
        success = verify_soul_artifact(args.file)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)
