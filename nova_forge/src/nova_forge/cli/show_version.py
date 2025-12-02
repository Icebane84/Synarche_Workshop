"""
Sub-command for showing version information.
"""

import argparse
import sys
from typing import NoReturn


def register_command(subparsers: argparse._SubParsersAction):
    """Registers the 'show-version' command and its arguments."""
    parser = subparsers.add_parser("show-version", help="Show version information.")
    parser.set_defaults(func=execute)


def execute(args: argparse.Namespace) -> NoReturn:
    """The handler function for the 'show-version' command."""
    if args.verbose:
        print("\n--- VERBOSE MODE ---")
        print(f"Verbose logging enabled by user.")

    print("\n--- VERSION INFO ---")
    print("Protocol Version: 2.0.0-Genesis")
    print(f"Package Path: {__file__.split('cli')[0]}")
    sys.exit(0)
