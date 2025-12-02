import cmd
import os
import subprocess  # nosec

from synarchy_bridge import SynarchyRegistry

current_dir = os.path.dirname(os.path.abspath(__file__))


class SynarchyCLI(cmd.Cmd):
    intro = "Welcome to the Synarchy Command Library CLI. Type help or ? to list commands.\n"
    prompt = "(synarchy) "

    def __init__(self):
        super().__init__()
        self.registry = SynarchyRegistry(
            os.path.join(current_dir, "command_registry.json")
        )

    def do_list(self, _):
        """List all top-level categories in the registry."""
        categories = self.registry.get_all_categories()
        print("\nAvailable Categories:")
        for cat in categories:
            print(f" - {cat}")
        print()

    def do_search(self, arg):
        """Search for commands by keyword. Usage: search <keyword>"""
        if not arg:
            print("Usage: search <keyword>")
            return

        results = self.registry.search_commands(arg)
        print(f"\nFound {len(results)} matches for '{arg}':")
        for res in results:
            print(f" - {res['name']}")
        print()

    def do_get(self, arg):
        """Get details for a specific command. Usage: get <command_name>"""
        if not arg:
            print("Usage: get <command_name>")
            return

        cmd_spec = self.registry.get_command_spec(arg)
        if cmd_spec:
            print(f"\nName: {cmd_spec['name']}")
            print(f"Syntax: {cmd_spec['syntax']}")
            print(f"Description: {cmd_spec['description']}")
            if "example_usage" in cmd_spec:
                print(f"Example: {cmd_spec['example_usage']}")
        else:
            print(f"Command '{arg}' not found.")
        print()

    def do_clear(self, _):
        """Clear the console screen."""
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "cls"], check=False)  # nosec
        else:
            subprocess.run(["clear"], check=False)  # nosec

    def do_quit(self, _):
        """Exit the CLI."""
        print("Goodbye.")
        return True

    def do_exit(self, arg):
        """Exit the CLI."""
        return self.do_quit(arg)


if __name__ == "__main__":
    try:
        SynarchyCLI().cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye.")
