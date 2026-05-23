import os
import sys

# Ensure the current directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from synarchy_bridge import SynarchyRegistry


def display_menu(menu_options):
    """Displays a menu of options and prompts the user to choose."""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

    print("\n--- Menu ---")
    for i, option in enumerate(menu_options):
        print(f"{i + 1}. {option}")
    choice = input("Enter your choice: ")
    return choice


def get_command_details(command):
    """Formats and displays the details of a command."""
    details = f"""
    Command Name: {command.get("name", "N/A")}
    Syntax: {command.get("syntax", "N/A")}
    Description: {command.get("description", "N/A")}
    Example Usage: {command.get("example_usage", "N/A")}
    """
    return details


def search_commands(search_term, registry):
    """Wraps the registry's search function."""
    return registry.search_commands(search_term)


def browse_recursively(node):
    """
    Recursively browses a node in the library.
    """
    # If list, it's a list of commands
    if isinstance(node, list):
        print("\n--- Commands ---")
        if not node:
            print("No commands in this category.")
        for command in node:
            print(get_command_details(command))
        input("\nPress Enter to return to the previous menu...")
        return

    # If dict, it's categories
    if isinstance(node, dict):
        while True:
            menu_options = list(node.keys()) + ["Return to Previous Menu"]
            choice_str = display_menu(menu_options)

            if choice_str.lower() == "return to previous menu":
                break

            try:
                choice_index = int(choice_str) - 1
                if choice_index < 0:
                    raise IndexError
                selected_key = menu_options[choice_index]
                if selected_key == "Return to Previous Menu":
                    break

                browse_recursively(node[selected_key])
            except (ValueError, IndexError):
                print("Invalid choice. Please try again.")
                continue


def navigate_library(registry):
    """Navigates the command library using a text-based menu."""
    library = registry.library
    while True:
        main_menu_options = list(library.keys()) + ["Search Command Library", "Exit"]
        choice = display_menu(main_menu_options)

        if choice.lower() == "exit":
            print("Exiting Synarchy Navigator.")
            break

        if choice.lower() == "search command library":
            search_term = input("Enter your search term: ")
            search_results = search_commands(search_term, registry)
            if search_results:
                print("--- Search Results ---")
                for command in search_results:
                    print(get_command_details(command))
            else:
                print("No commands found matching your search term.")
            input("\nPress Enter to continue...")
            continue

        try:
            category_index = int(choice) - 1
            if category_index < 0:
                raise IndexError
            selected_category = main_menu_options[category_index]
            if selected_category == "Search Command Library" or selected_category == "Exit":
                continue

            browse_recursively(library[selected_category])
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")


def main():
    print("Initializing Synarchy Command Navigator...")
    bridge = SynarchyRegistry()
    print("Registry Loaded.")
    navigate_library(bridge)


if __name__ == "__main__":
    main()
