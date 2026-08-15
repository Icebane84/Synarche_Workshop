import yaml
import os

workspace_root = r"c:\Users\Chris\Synarche_Workspace"
registry_path = os.path.join(workspace_root, "_governance", "01_Registries", "GVRN.Master.Registry.yaml")

# Load registry
with open(registry_path, "r", encoding="utf-8") as f:
    registry = yaml.safe_load(f) or {}

# Add Keyring Spec
registry["SEC-KEY-001"] = {
    "artifact_id": "SEC-KEY-001",
    "domain": "Security / Access",
    "official_name": "UMB-SEC-KEYRING-001.md",
    "path": "_governance/10_Governance/UMB-SEC-KEYRING-001.md",
    "relations": "GOVERNED_BY: CORE-CODEX-001",
    "parsed_relations": [
        "GOVERNED_BY:CORE-CODEX-001"
    ],
    "status_(state)": "ACTIVE",
    "version": "v5.0 [OMEGA]"
}

# Save registry
with open(registry_path, "w", encoding="utf-8") as f:
    yaml.dump(registry, f, default_flow_style=False, sort_keys=True)

print("Keyring specification successfully registered in Master Registry!")
