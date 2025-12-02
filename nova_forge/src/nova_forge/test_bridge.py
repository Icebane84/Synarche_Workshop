from synarchy_bridge import SynarchyRegistry


def run_verification():
    print("Initializing Synarchy Bridge...")
    registry = SynarchyRegistry()

    print(f"\n[1] Registry Loaded. Categories: {registry.get_all_categories()}")

    # Test SIVC (Simulate Inner Voice Check)
    print("\n[2] Testing Retrieval of 'SIVC' (Inner Voice)...")
    sivc = registry.get_command_spec("SIVC")
    if sivc:
        print(f"   SUCCESS: Found {sivc['name']}")
        print(f"   Syntax: {sivc['syntax']}")
    else:
        print("   FAILURE: Could not find SIVC")

    # Test Fuzzy Search
    print("\n[3] Testing Search for 'Prompt'...")
    results = registry.search_commands("Prompt")
    print(f"   Found {len(results)} commands related to 'Prompt'.")
    if len(results) > 0:
        print(f"   Example: {results[0]['name']}")

    print("\n[4] Verification Complete. Ready for Synarchy Workshop integration.")


if __name__ == "__main__":
    run_verification()
