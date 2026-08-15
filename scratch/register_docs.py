import yaml
import os

workspace_root = r"c:\Users\Chris\Synarche_Workspace"
registry_path = os.path.join(workspace_root, "_governance", "01_Registries", "GVRN.Master.Registry.yaml")

# Load existing registry
with open(registry_path, "r", encoding="utf-8") as f:
    registry = yaml.safe_load(f) or {}

# Add PromptDSL
registry["GVRN.DOC.PROMPT_DSL_SPEC.004"] = {
    "artifact_id": "GVRN.DOC.PROMPT_DSL_SPEC.004",
    "domain": "GVRN",
    "official_name": "GVRN.Documentation.PromptDSL.md",
    "path": "_governance/08_Documentation/GVRN.Documentation.PromptDSL.md",
    "relations": "GOVERNED_BY: CORE-CODEX-001",
    "parsed_relations": [
        "GOVERNED_BY:CORE-CODEX-001"
    ],
    "status_(state)": "CANONIZED",
    "version": "v15.1 [OMEGA]"
}

# Add Verification Quad
registry["GVRN.SPEC.VERIFICATION_QUAD.001"] = {
    "artifact_id": "GVRN.SPEC.VERIFICATION_QUAD.001",
    "domain": "GVRN",
    "official_name": "GVRN.SPEC.VERIFICATION_QUAD.001.md",
    "path": "_governance/08_Documentation/GVRN.SPEC.VERIFICATION_QUAD.001.md",
    "relations": "GOVERNED_BY: CORE-CODEX-001",
    "parsed_relations": [
        "GOVERNED_BY:CORE-CODEX-001"
    ],
    "status_(state)": "CANONIZED",
    "version": "v15.0 [OMEGA]"
}

# Save back to registry
with open(registry_path, "w", encoding="utf-8") as f:
    yaml.dump(registry, f, default_flow_style=False, sort_keys=True)

print("PromptDSL and Verification Quad nodes successfully registered!")
