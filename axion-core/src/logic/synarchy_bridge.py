"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.logic.synarchy.bridge`             | The Sovereign ID. |
| **Official Name** | `synarchy_bridge.py`                | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[ACTIVE]`                        | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | 0.9     |
# | **Resonance** | 0.85     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Registry Drift**   | Automatic Validation      |
# | **JSON Corruption**  | Recursive Search Guardrails|

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Bridges capability discovery with ethical law. |

## **[ARTIFACT END]**

Objective: Interface for the Synarchy Command Registry.
Conforms to OGLN/AISTF v15.0 governance and documentation standards.
"""

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.logic.synarchy.bridge VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28

import json
import os
from typing import Any, Dict, List, Optional


class SynarchyRegistry:
    """
    Interface for the Synarchy Command Registry.
    Allows agents (AXION, LIGHTBINDER) to programmatically access capabilities and tool specifications.
    """

    def __init__(self, registry_path: str = "data/command_registry.json") -> None:
        """
        Initializes the SynarchyRegistry and loads the underlying command library.

        Args:
            registry_path: Path to the JSON command registry file.
        """
        # Resolve path relative to this file if not absolute
        if not os.path.isabs(registry_path):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            registry_path = os.path.normpath(os.path.join(current_dir, "../../", registry_path))

        self.registry_path = registry_path
        self.library: Dict[str, Any] = self.load_registry()

    def load_registry(self) -> Dict[str, Any]:
        """
        Loads the JSON command library from the local filesystem.

        Returns:
            A dictionary representation of the command registry.
        """
        try:
            with open(self.registry_path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Registry file not found at {self.registry_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {self.registry_path}")
            return {}

    def get_all_categories(self) -> List[str]:
        """
        Returns top-level command categories present in the registry.

        Returns:
            A list of category names.
        """
        return list(self.library.keys())

    def search_commands(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches all commands for a query string in name or description.

        Args:
            query: The search term to filter commands by.

        Returns:
            A list of matching command definitions.
        """
        results: List[Dict[str, Any]] = []
        query_lower = query.lower()

        def _recursive_search(node: Any) -> None:
            """Recursively traverses the registry tree to find matches."""
            if isinstance(node, list):
                for cmd in node:
                    if query_lower in cmd.get("name", "").lower() or query_lower in cmd.get("description", "").lower():
                        results.append(cmd)
            elif isinstance(node, dict):
                for value in node.values():
                    _recursive_search(value)

        _recursive_search(self.library)
        return results

    def get_command_spec(self, command_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the full specification for a specific command by name.

        Args:
            command_name: The exact or partial name of the command.

        Returns:
            The command specification dictionary if found, else None.
        """
        matches = self.search_commands(command_name)
        
        # Priority 1: Exact Match
        for cmd in matches:
            if cmd.get("name", "").lower() == command_name.lower():
                return cmd
        
        # Priority 2: Fuzzy/First Match
        if matches:
            return matches[0]
            
        return None


if __name__ == "__main__":
    # Simple self-test for registry connectivity
    bridge = SynarchyRegistry()
    print("Categories:", bridge.get_all_categories())

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.logic.synarchy.bridge VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28
# ---
