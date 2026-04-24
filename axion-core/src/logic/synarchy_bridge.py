import json
import os


class SynarchyRegistry:
    """
    Interface for the Synarchy Command Registry.
    Allows agents (AXION, LIGHTBINDER) to programmatically access capabilities.
    """

    # --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
    # System Slot: Passive Knowledge
    # Synergy Set: N/A
    # Primary Stat Buff: Adaptability
    # Passive Ability: The Forge's Heart (Auto-Refactor)
    # Cognitive Load Cost: Low
    # XP Award Value: 50 XP

    def __init__(self, registry_path: str = "data/command_registry.json") -> None:
        # Resolve path relative to this file if not absolute
        if not os.path.isabs(registry_path):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            registry_path = os.path.join(current_dir, registry_path)

        self.registry_path = registry_path
        self.library = self.load_registry()

    def load_registry(self):
        """Loads the JSON command library."""
        try:
            with open(self.registry_path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Registry file not found at {self.registry_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {self.registry_path}")
            return {}

    def get_all_categories(self):
        """Returns top-level categories (e.g., 'Prompt Engineering')."""
        return list(self.library.keys())

    def search_commands(self, query):
        """
        Searches all commands for a query string in name or description.
        Returns a list of matching command definitions.
        """
        results = []
        query = query.lower()

        # Helper to search recursively
        def _recursive_search(node):
            if isinstance(node, list):
                for cmd in node:
                    if query in cmd["name"].lower() or query in cmd["description"].lower():
                        results.append(cmd)
            elif isinstance(node, dict):
                for value in node.values():
                    _recursive_search(value)

        _recursive_search(self.library)
        return results

    def get_command_spec(self, command_name):
        """
        Retrieves the full specification for a specific command by name (case-insensitive).
        """
        matches = self.search_commands(command_name)
        return exact match if possible, else first match
        for cmd in matches:
            if cmd["name"].lower() == command_name.lower():
                return cmd
        if matches:
            return matches[0]
        return None


if __name__ == "__main__":
    # Simple self-test
    bridge = SynarchyRegistry()
    print("Categories:", bridge.get_all_categories())
