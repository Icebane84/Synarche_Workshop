
# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

import os
import sys

# Add src to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from synarchy_bridge import SynarchyRegistry


def test_bridge():
    print("Testing SynarchyRegistry...")
    bridge = SynarchyRegistry("data/command_registry.json")

    categories = bridge.get_all_categories()
    print(f"Categories found: {len(categories)}")

    total_commands = 0
    valid_commands = 0

    print("\nValidating all commands in registry...")

    # Helper to traverse and validate
    def validate_node(node, path="root"):
        nonlocal total_commands, valid_commands
        if isinstance(node, dict):
            for key, value in node.items():
                validate_node(value, path + f" -> {key}")
        elif isinstance(node, list):
            for cmd in node:
                total_commands += 1
                issues = []
                if "name" not in cmd:
                    issues.append("Missing 'name'")
                if "syntax" not in cmd:
                    issues.append("Missing 'syntax'")
                if "description" not in cmd:
                    issues.append("Missing 'description'")

                if not issues:
                    valid_commands += 1
                    # print(f"  OK: {cmd.get('name', 'UNKNOWN')}")
                else:
                    print(f"  FAIL: {path} -> {cmd.get('name', 'UNKNOWN')} Issues: {', '.join(issues)}")

    validate_node(bridge.library)

    print("\nVerification Complete.")
    print(f"Total Commands: {total_commands}")
    print(f"Valid Commands: {valid_commands}")

    if total_commands == valid_commands and total_commands > 0:
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")


if __name__ == "__main__":
    test_bridge()
