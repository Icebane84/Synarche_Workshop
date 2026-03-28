"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.cli`                | The Sovereign ID. |
| **Official Name** | `cli.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

---

## **Block B: State Vector (AGP-001)**

| State Field   | Value     |
| :------------ | :-------- |
| **Coherence** | `{resonance}`     |
| **Resonance** | `{resonance}`     |
| **Stability** | `Stable`  |

---

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                |
| :------------------- | :------------------------ |
| **Logic Drift**      | Strict Linter Enforcement |
| **Semantic Decay**   | Axiomatic Compass Audit   |

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
| :---------------------- | :---------------- | :---------------------------------------------- |
| `CORE.Codex.Phoenix`    | `GOVERNS`         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**
"""

import cmd
import os
import subprocess  # nosec
import sys
from typing import Any, List, Optional, dict

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

# ---
# 
# ---

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: CORE.cli VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 6363a973ac38796c`
