import os

# New rows for OSLM
inserts = """| `METRIC-AES-001` | [Algorithmic Elegance Score](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/GVRN/METRIC-AES-001.md) | `v1.0` | `ACTIVE` |
"""


def update_file(path, marker, insert_content, insert_before=False):
    try:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return False

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        inserted = False
        for line in lines:
            new_lines.append(line)
            if marker in line and not inserted:
                new_lines.append(insert_content)
                inserted = True

        if not inserted:
            print(f"Marker '{marker}' not found in {os.path.basename(path)}")
            return False

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(f"Successfully updated {os.path.basename(path)}")
        return True
    except Exception as e:
        print(f"Error updating {path}: {e}")
        return False


# Paths
oslm_path = r"c:\Users\Chris\_Desktop_Vault\Phoenix\Documentation\Library\0_Registries\UMB-OSLM-001_MasterArtifactRegistry_v11.0.md"
marker = (
    "| `UMB-OSLM-001`"  # Insert near OSLM itself or in Metrics section if possible.
)
# Better yet, let's look for a Metrics section or insert near other metrics.
# OSLM usually has a section. Let's try to find METRIC-AES-001 check first.

print("--- Updating OSLM with AES ---")
if os.path.exists(oslm_path):
    with open(oslm_path, "r", encoding="utf-8") as f:
        if "METRIC-AES-001" in f.read():
            print("AES already registered.")
        else:
            # Try to find a metric anchor
            update_file(oslm_path, "| `AOP-MAP-001`", inserts, insert_before=False)
            # Appending near MAP-001 (Execution Playbook) is safe contextually if Metrics section is elusive.
else:
    print("OSLM Path invalid.")
