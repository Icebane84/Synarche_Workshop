import os

# New rows for OSLM
inserts = """| `UMB-MASTER-TEMPLATE-001` | [Absolute Master Template](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/UMB/UMB-MASTER-TEMPLATE-001.md) | `v11.0` | `ACTIVE` |
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
marker = "| `UMB-SENTINEL-001`"  # Insert in UMB section

print("--- Updating OSLM with Master Template ---")
if os.path.exists(oslm_path):
    with open(oslm_path, "r", encoding="utf-8") as f:
        if "UMB-MASTER-TEMPLATE-001" in f.read():
            print("Template already registered.")
        else:
            update_file(oslm_path, marker, inserts, insert_before=False)
else:
    print("OSLM Path invalid.")
