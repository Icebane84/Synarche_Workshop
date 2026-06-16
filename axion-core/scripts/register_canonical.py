import os
import hashlib
import re


def compute_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def extract_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Matches """<whitespace>artifact_anchor: ... """
    match = re.search(r'"""\s*artifact_anchor:(.*?)\s*"""', content, re.DOTALL)
    if not match:
        return None

    lines = match.group(1).split("\n")
    data = {}
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            val = parts[1].strip().strip("'\"")
            if val.startswith("[") and val.endswith("]"):
                # Simple list parsing
                inner = val[1:-1].strip()
                val = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
            data[key] = val
    return data


def generate_entry_block(file_path, workspace_root):
    if not os.path.exists(file_path):
        print(f"Warning: file not found at {file_path}")
        return None, None

    sha = compute_sha256(file_path)
    fm = extract_frontmatter(file_path)
    if not fm:
        print(f"Error: Could not extract frontmatter from {file_path}")
        return None, None

    status_raw = fm.get('state', 'CANONIZED')
    causal_origin = fm.get('causal_origin')
    
    # Law 43 Enforcement: Living Chronos
    if status_raw == 'CANONIZED' and not causal_origin:
        print(f"Error: Law 43 Violation. 'causal_origin' is required for CANONIZED state in {file_path}")
        return None, None

    artifact_id = fm.get("id")
    if not artifact_id:
        print(f"Error: 'id' not found in frontmatter of {file_path}")
        return None, None

    rel_path = file_path.replace(workspace_root, "").replace("\\", "/").lstrip("/")
    name = os.path.basename(file_path)

    domain = fm.get("domain", "GVRN")
    version = fm.get("version", "v15.0 [OMEGA]")
    status = f"[{fm.get('state', 'CANONIZED')}]"

    relations_list = fm.get("relations", [])
    if not relations_list:
        relations_str = '""'
        parsed_relations = []
    else:
        relations_str = ", ".join(relations_list)
        parsed_relations = relations_list

    yaml_block = f"""{artifact_id}:
  artifact_id: {artifact_id}
  content_hash: {sha}
  domain: {domain}
  official_name: {name}
  parsed_relations:"""
    if not parsed_relations:
        yaml_block += " []\n"
    else:
        yaml_block += "\n"
        for rel in parsed_relations:
            yaml_block += f"    - {rel}\n"

    yaml_block += f"""  path: {rel_path}
  relations: {relations_str}
  status: "{status}"
  version: {version}"""
    
    if causal_origin:
        yaml_block += f"\n  causal_origin: \"{causal_origin}\""
        
    yaml_block += "\n"
    return artifact_id, yaml_block


def parse_existing_registry(registry_content):
    entries = {}
    if not registry_content:
        return entries

    current_key = None
    current_block = []

    lines = registry_content.splitlines()
    for line in lines:
        if not line.strip():
            continue
        if not line.startswith(" ") and ":" in line:
            if current_key:
                entries[current_key] = "\n".join(current_block) + "\n"
            current_key = line.split(":", 1)[0].strip()
            current_block = [line]
        else:
            if current_key:
                current_block.append(line)
    if current_key:
        entries[current_key] = "\n".join(current_block) + "\n"

    return entries


def register_files():
    workspace_root = r"c:\Users\Chris\Synarche_Workspace"
    registry_path = os.path.join(
        workspace_root, "_governance", "01_Registries", "GVRN.Master.Registry.yaml"
    )

    files_to_register = [
        os.path.join(
            workspace_root, "_governance", "10_Governance", "GVRN.Registry.Origins.md"
        ),
        os.path.join(workspace_root, "_governance", "09_Link", "SYNG.Link.Forge.md"),
        os.path.join(
            workspace_root,
            "_governance",
            "10_Governance",
            "GVRN.ID.SynthesisInsights.md",
        ),
        os.path.join(
            workspace_root,
            "_governance",
            "10_Governance",
            "GVRN.Framework.Synthesis.001.md",
        ),
    ]

    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            registry_content = f.read()
    else:
        registry_content = ""

    updated_entries = {}
    for file_path in files_to_register:
        artifact_id, yaml_block = generate_entry_block(file_path, workspace_root)
        if artifact_id and yaml_block:
            updated_entries[artifact_id] = yaml_block
            print(f"Generated registry entry for {artifact_id}")

    entries = parse_existing_registry(registry_content)

    for key, block in updated_entries.items():
        entries[key] = block

    sorted_keys = sorted(entries.keys())
    with open(registry_path, "w", encoding="utf-8") as f:
        for key in sorted_keys:
            f.write(entries[key])

    print("Master Registry updated successfully!")


if __name__ == "__main__":
    register_files()
