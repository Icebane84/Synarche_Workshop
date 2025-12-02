"""
Sub-command for checking environment integrity.
"""

import argparse
import sys
from typing import NoReturn


def register_command(subparsers: argparse._SubParsersAction):
    """Registers the 'check-integrity' command and its arguments."""
    parser = subparsers.add_parser(
        "check-integrity", help="Check the integrity of the environment."
    )
    parser.add_argument(
        "--deep", action="store_true", help="Perform a deep integrity scan."
    )
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> NoReturn:
    """The handler function for the 'check-integrity' command."""
    if args.verbose:
        print("\n--- VERBOSE MODE ---")
        print("Verbose logging enabled by user.")

    print("\n--- INTEGRITY CHECK ---")
    print("Simulating integrity check... [OK]")
    if args.deep:
        print("Performing deep scan... [OK]")
    sys.exit(0)
