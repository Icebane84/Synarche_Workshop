import os

# New rows for OSLM
# Structure: | Module ID | Title | Version | Status |
inserts = """| `UMB-ARCH-CORE-001` | [Phoenix Core Architecture](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/ARCH/UMB-ARCH-CORE-001.md) | `v11.0.0` | `ACTIVE` |
| `AOP-AXIOM-WEAVE-001` | [The Axiom Weaving Protocol](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/AOP/AOP-AXIOM-WEAVE-001.md) | `v1.0` | `ACTIVE` |
| `CSL-LINK-001` | [Synergistic Links Expansion Log](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/CSL/CSL-LINK-001.md) | `v1.0` | `ACTIVE` |
| `AOP-AVATAR-001` | [Synarchy Avatar Protocol](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/GVRN/AOP-AVATAR-001.md) | `v1.1` | `ACTIVE` |
| `AOP-MAP-001` | [Disciplined Execution Playbook](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/GVRN/AOP-MAP-001.md) | `v2.0` | `ACTIVE` |
| `GUCA-MAP-001` | [Execute Musashi Audit](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/GVRN/GUCA-MAP-001.md) | `v2.0` | `ACTIVE` |
| `GUCA-DSA-001` | [Documentation Suite Architect Architecture](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/GVRN/GUCA-DSA-001.md) | `v11.1` | `ACTIVE` |
| `GVRN-SYNERGY-001` | [Agentic Workshop Synergy Matrix](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/GVRN/GVRN-SYNERGY-001.md) | `v11.1` | `ACTIVE` |
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
            # Check for marker (substring match)
            if marker in line and not inserted:
                if insert_before:
                    # Logic handled by appending AFTER logic here, simplied for this script context
                    # To insert BEFORE, we would need to splice.
                    # Simplest is to just insert into the table.
                    pass
                else:
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

# Marker: Insert after the UMB-CSP-001 entry we added last time
# If that doesn't exist, we fall back to a known entry.
marker = "| `UMB-CSP-001`"

print("--- Updating OSLM with Forge Artifacts ---")
if os.path.exists(oslm_path):
    with open(oslm_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "UMB-ARCH-CORE-001" in content:
            print("Artifacts already registered.")
        else:
            if "| `UMB-CSP-001`" in content:
                update_file(oslm_path, marker, inserts, insert_before=False)
            else:
                # Fallback to appending to the end of the table if CSP isn't found easily (should be there though)
                print("UMB-CSP-001 marker not found, trying different anchor.")
                update_file(oslm_path, "| `AOP-RLM-001`", inserts, insert_before=False)
else:
    print("OSLM Path invalid.")
