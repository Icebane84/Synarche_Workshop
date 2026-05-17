"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                                   | Description       |
| :------------------ | :-------------------------------------- | :---------------- |
| **Artifact ID**     | `CORE-BRIDGE-001`                       | The Sovereign ID. |
| **Official Name**   | `Synarche_bridge.py`                    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**                       | The Standard.     |
| **Domain**          | `CORE`                                  | The Subject.      |
| **Celestial Class** | `[STAR]`                                | The Weight.       |
| **Evolution**       | `Integration Layer`                     | The Maturity.     |
| **Status (State)**| `[CANONIZED]`                              | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess | The Sovereign.` | The Network.      |

## **[ARTIFACT END]**
"""

import json
import os
from typing import Any


class SynarcheRegistry:
    """
    Interface for the Synarche Command Registry.
    Allows agents (AXION, LIGHTBINDER) to programmatically access capabilities.
    """

    def __init__(self, registry_path: str = "command_registry.json") -> None:
        # Resolve path relative to this file if not absolute
        if not os.path.isabs(registry_path):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            registry_path = os.path.join(current_dir, registry_path)

        self.registry_path = registry_path
        self.library = self.load_registry()

    def load_registry(self) -> dict[str, Any]:
        """Loads the JSON command library."""
        try:
            with open(self.registry_path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # log or handle error appropriately instead of just printing in production
            return {}
        except json.JSONDecodeError:
            return {}

    def get_all_categories(self) -> list[str]:
        """Returns top-level categories (e.g., 'Prompt Engineering')."""
        return list(self.library.keys())

    def search_commands(self, query: str) -> list[dict[str, Any]]:
        """
        Searches all commands for a query string in name or description.
        Returns a list of matching command definitions.
        """
        results: list[dict[str, Any]] = []
        query = query.lower()

        # Helper to search recursively
        def _recursive_search(node: dict[str, Any] | list[Any]) -> None:
            """Recursively search for commands in the registry tree."""
            if isinstance(node, list):
                for cmd in node:
                    if (
                        query in cmd["name"].lower()
                        or query in cmd["description"].lower()
                    ):
                        results.append(cmd)
            elif isinstance(node, dict):
                for value in node.values():
                    _recursive_search(value)

        _recursive_search(self.library)
        return results

    def get_command_spec(self, command_name: str) -> dict[str, Any] | None:
        """
        Retrieves the full specification for a specific command by name (case-insensitive).
        """
        matches = self.search_commands(command_name)
        # return exact match if possible, else first match
        for cmd in matches:
            if cmd["name"].lower() == command_name.lower():
                return cmd
        if matches:
            return matches[0]
        return None


if __name__ == "__main__":
    # Simple self-test
    bridge = SynarcheRegistry()
    print("Categories:", bridge.get_all_categories())
    pass

# ---
# ---

# ---

### **Block G: The Omni-Anchor (System Snapshot)**

# [OMNI-ARTIFACT-ANCHOR] ID: CORE-BRIDGE-001 VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 57eb1326200f4015
