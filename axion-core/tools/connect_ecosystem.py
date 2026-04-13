import os

# New rows for OSLM (Corrected to 4-column format matching OSLM v11.0)
# Structure: | Module ID | Title | Version | Status |
oslm_inserts = """| `AOP-RLM-001` | [Relational Linking Mandate](file:///c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library/2_Protocols/AOP-RLM-001_RelationalLinkingMandate_v5.1.md) | `v5.1` | `ACTIVE` |
| `UMB-CSP-001` | [Consolidated Synergy Protocol](file:///c:/Users/Chris/Synarche_Workspace/axion-core/docs/UMB-CSP-001.md) | `v10.0` | `ACTIVE` |
"""

# New rows for CSP (3-column Component Mapping)
csp_inserts = """| **UMB-TECH-001** (Agent Schema) | **UMB-CSE-001** (Coherent Synthesis Engine) | Agent Architecture |
| **OGLN.Governance** (Validation Protocol) | **UMB-SGM-001** (Standardized Governance Module) | Governance Validation |
| **AOP-CSM-001** (Complete Stack Mandate) | **UMB-SGM-001** (Standardized Governance Module) | Mandate Enforcement |
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
                    # Insert before not implemented for line-by-line easily without buffering,
                    # but we are inserting AFTER in this logic?
                    # Wait, if insert_before=True, we should have appended insert_content then line.
                    # Let's handle insert_after (default)
                    new_lines.append(insert_content)
                    inserted = True
                else:
                    new_lines.append(insert_content)
                    inserted = True

        # If we reached the end and marker wasn't found
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
csp_path = r"c:\Users\Chris\Synarche_Workspace\axion-core\docs\UMB-CSP-001.md"

# Markers
# OSLM: Insert after the last known entry in the main table
oslm_marker = "| `AOP-PHOENIX-001`"

# CSP: Insert into Component Mapping table
csp_marker = "| **AOP-PERPETUAL-COHERENCE-001**"

print("--- Updating OSLM ---")
# Check if already present
with open(oslm_path, "r", encoding="utf-8") as f:
    if "UMB-CSP-001" in f.read():
        print("UMB-CSP-001 already in OSLM")
    else:
        update_file(oslm_path, oslm_marker, oslm_inserts, insert_before=False)

print("\n--- Updating CSP ---")
with open(csp_path, "r", encoding="utf-8") as f:
    if "AOP-CSM-001" in f.read():
        print("AOP-CSM-001 already in CSP")
    else:
        update_file(csp_path, csp_marker, csp_inserts, insert_before=False)
