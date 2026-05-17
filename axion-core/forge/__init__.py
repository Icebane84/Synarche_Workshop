# axion-core/forge module initialization

import os
import sys
from pathlib import Path

# Add forge to Python path for imports
forge_path = Path(__file__).parent.resolve()
sys.path.insert(0, str(forge_path))

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Import submodules
from . import builder, enums, graph, manager, parser, registry, runner, standards, tools

__all__ = [
    "builder",
    "enums",
    "graph",
    "manager",
    "parser",
    "registry",
    "runner",
    "standards",
    "tools",
]

__version__ = "1.0.0"


def version() -> str:
    """Get the Forge version number"""
    return __version__


print(f"Axion Forge v{__version__} loaded successfully")
