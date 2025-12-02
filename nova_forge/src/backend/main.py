"""
Artifact ID: CODE-REF-004
Module: Backend Entry Point
Context: Nova Forge > Backend
Description: Main entry point for the backend application.
"""

import sys
from pathlib import Path

# Add the src directory to the python path so we can import modules
sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("Nova Forge Backend Initialized.")


if __name__ == "__main__":
    main()
