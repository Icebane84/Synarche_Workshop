"""
Sub-command for checking environment integrity.
"""

import argparse
import hashlib
import sys
from pathlib import Path
from typing import NoReturn

# A known-good hash for the setup.py file.
# This value was generated from a trusted version of the file. It should be
# updated whenever setup.py is intentionally and safely modified.
KNOWN_SETUP_PY_HASH = "e7322c25eca3a48169fddf27412dcf3e97c4041987f2646db577fcdf3f82ab0c"


def register_command(subparsers: argparse._SubParsersAction):
    """Registers the 'check-integrity' command and its arguments."""
    parser = subparsers.add_parser(
        "check-integrity", help="Check the integrity of the environment."
    )
    parser.set_defaults(func=execute)


def generate_sha256_hash(filepath: str) -> str:
    """Generates the SHA-256 hash of a file.

    Args:
        filepath: The absolute path to the file.

    Returns:
        The hexadecimal SHA-256 hash string.
    """
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def execute(args: argparse.Namespace) -> NoReturn:
    """The handler function for the 'check-integrity' command."""
    try:
        if args.verbose:
            print("\n--- VERBOSE MODE ---")
            print("Verbose logging enabled by user.")

        print("\n--- INTEGRITY CHECK ---")

        # Find the project root directory relative to this file's location
        project_root = Path(__file__).parent.parent.parent.parent
        setup_py_path = project_root / "setup.py"

        if setup_py_path.exists():
            file_hash = generate_sha256_hash(str(setup_py_path))
            print(f"Verifying integrity of: {setup_py_path.name}")

            if file_hash == KNOWN_SETUP_PY_HASH:
                print("Status: [VERIFIED]")
                print(f"Hash: {file_hash}")
            else:
                raise ValueError(
                    f"Hash mismatch! File may be tampered with.\n  Expected: {KNOWN_SETUP_PY_HASH}\n  Got:      {file_hash}"
                )
        else:
            raise FileNotFoundError("setup.py not found at project root.")

        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Integrity check failed: {e}", file=sys.stderr)
        sys.exit(1)
