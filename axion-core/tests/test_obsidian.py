import importlib.util
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

print(f"Python sys.path: {sys.path}")


def import_path(path: Path):
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        return module
    return None


try:
    # Fallback resolution: Try systems/ first, then tools/03_Systems/
    bridge_path = PROJECT_ROOT / "systems" / "obsidian_bridge.py"
    if not bridge_path.exists():
        bridge_path = PROJECT_ROOT / "tools" / "03_Systems" / "obsidian_bridge.py"
        
    obsidian_module = import_path(bridge_path)
    if obsidian_module:
        ObsidianBridge = obsidian_module.ObsidianBridge
        print("Success: Successfully imported ObsidianBridge using importlib.")
    else:
        print("Error: Failed to load ObsidianBridge module.")
        sys.exit(1)
except Exception as e:
    print(f"Error: Import error: {e}")
    sys.exit(1)

API_KEY = "75d743e71b4e0ec1b4e04aeabea1a2695b5cff03a899020de6519248e3c26db2"
CERT = "c:/Users/Chris/Synarche_Workspace/obsidian-local-rest-api.crt"

print(f"Testing Obsidian Bridge with API_KEY: {API_KEY[:5]}...")
if not os.path.exists(CERT):
    print(f"Warning: Certificate not found at {CERT}. Proceeding with verify=False.")

bridge = ObsidianBridge(api_key=API_KEY, cert_path=CERT)

try:
    if bridge.check_connection():
        print("Success: Connection Successful!")
        # notes = bridge.list_notes() # This might fail if the API structure is different
        # print(f"Found {len(notes)} notes.")
    else:
        print(
            "Error: Connection Failed. Is Obsidian running and the Local REST API plugin enabled?"
        )
except Exception as e:
    print(f"Error: An error occurred during connection: {e}")
