"""
Block A: The Identification Lock (UIP-V15)

| Key                 | Value                                   | Description       |
| :------------------ | :-------------------------------------- | :---------------- |
| **Artifact ID**     | `CORE-CLI-001`                          | The Sovereign ID. |
| **Official Name**   | `cli.py`                                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**                       | The Standard.     |
| **Domain**          | `CORE`                                  | The Subject.      |
| **Celestial Class** | `[STAR]`                                | The Weight.       |
| **Evolution**       | `Operational Interface`                 | The Maturity.     |
| **Status**          | `[ACTIVE]`                              | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess | The Sovereign.` | The Network.      |
"""

import cmd
import os
import subprocess  # nosec
import sys
from typing import Any, dict, List, Optional

# Ensure we can import from the same directory safely
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from synarchy_bridge import SynarchyRegistry
except ImportError:
    # Fallback for when running from a different context
    sys.path.append(os.path.join(current_dir, "..", "src"))
    from synarchy_bridge import SynarchyRegistry


class SynarchyCLI(cmd.Cmd):
    """
    Command Line Interface for the Synarchy Command Library.
    Attributes:
        intro (str): Welcome message displayed on startup.
        prompt (str): The CLI prompt string.
        registry (SynarchyRegistry): The registry manager instance.
    """

    intro: str = (
        "Welcome to the Synarchy Command Library CLI. Type help or ? to list commands.\n"
    )
    prompt: str = "(synarchy) "

    def __init__(self) -> None:
        """Initialize the CLI and load the command registry."""
        super().__init__()
        # Point to data/command_registry.json
        registry_path = os.path.join(current_dir, "data", "command_registry.json")
        self.registry = SynarchyRegistry(registry_path)

    def do_list(self, _: str) -> None:
        """
        List all top-level categories in the registry.
        Args:
            _: Unused argument (required by cmd.Cmd signature).
        """
        categories: List[str] = self.registry.get_all_categories()
        print("\nAvailable Categories:")
        for cat in categories:
            print(f" - {cat}")
        print()

    def do_search(self, arg: str) -> None:
        """
        Search for commands by keyword.

        Args:
            arg (str): The keyword to search for.

        Usage:
            search <keyword>
        """
        if not arg:
            print("Usage: search <keyword>")
            return

        results: List[Dict[str, Any]] = self.registry.search_commands(arg)
        print(f"\nFound {len(results)} matches for '{arg}':")
        for res in results:
            print(f" - {res['name']}")
        print()

    def do_get(self, arg: str) -> None:
        """
        Get details for a specific command.

        Args:
            arg (str): The name of the command to retrieve.

        Usage:
            get <command_name>
        """
        if not arg:
            print("Usage: get <command_name>")
            return

        cmd_spec: Optional[Dict[str, Any]] = self.registry.get_command_spec(arg)
        if cmd_spec:
            print(f"\nName: {cmd_spec['name']}")
            print(f"Syntax: {cmd_spec['syntax']}")
            print(f"Description: {cmd_spec['description']}")
            if "example_usage" in cmd_spec:
                print(f"Example: {cmd_spec['example_usage']}")
        else:
            print(f"Command '{arg}' not found.")
        print()

    def do_clear(self, _: str) -> None:
        """
        Clear the console screen.
        Args:
            _: Unused argument.
        """
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "cls"], check=False)  # nosec
        else:
            subprocess.run(["clear"], check=False)  # nosec

    def do_quit(self, _: str) -> bool:
        """
        Exit the CLI.
        Returns:
            bool: True to signal the command loop to stop.
        """
        print("Goodbye.")
        return True

    def do_exit(self, _: str) -> bool:
        """Alias for quit."""
        return self.do_quit(_)


if __name__ == "__main__":
    try:
        SynarchyCLI().cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye.")
