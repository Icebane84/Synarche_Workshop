from synarchy_bridge import SynarchyRegistry


def demo():
    # Initialize (Activate) the Registry
    print("Initializing Synarchy Bridge...")
    bridge = SynarchyRegistry()

    # Verify it's working
    print("\n[1] Loaded Categories:")
    print(bridge.get_all_categories())

    # Example: Retrieving a Command
    command_name = "Bridge-Execute"
    print(f"\n[2] Searching for command: '{command_name}'...")

    cmd_spec = bridge.get_command_spec(command_name)

    if cmd_spec:
        print(f"   SUCCESS: Command Found: {cmd_spec['name']}")
        print(f"   Syntax: {cmd_spec['syntax']}")
        print(f"   Description: {cmd_spec['description']}")
    else:
        print("   Command not found.")


if __name__ == "__main__":
    demo()
