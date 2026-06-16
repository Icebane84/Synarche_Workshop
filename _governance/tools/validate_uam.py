#!/usr/bin/env python
# Sovereign UAM Static Validator Wrapper
# UIP-V15 Protocol Engine

import os
import sys
from uam.cli import execute_pipeline

if __name__ == "__main__":
    target_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    strict_mode = False

    args = sys.argv[1:]
    if "--strict" in args:
        strict_mode = True
        args.remove("--strict")

    if args:
        target_dir = args[0]

    # validate_uam always runs in non-destructive 'lint' mode
    # If strict_mode is requested, we can handle it or pass it.
    is_valid = execute_pipeline(target_dir, mode="lint")
    sys.exit(0 if is_valid else 1)
