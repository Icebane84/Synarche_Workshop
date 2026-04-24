import hashlib
import os
import re

FORGE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(FORGE_DIR, "registry.yaml")


def get_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def extract_metadata(content, filename):
    # Try block A extraction
    art_search = re.search(r"Artifact ID(?:\*\*|:*)\s*`?([A-Za-z0-9_-]+)", content)
    status_search = re.search(r"Status(?:\s*\(State\))?(?:\*\*|:*)\s*`?(\[[A-Z]+\])", content)
    ver_search = re.search(r"Version(?:\*\*|:*)\s*`?(v[0-9.]+(?:\s*\[OMEGA\])?)", content)

    art_id = art_search.group(1) if art_search else None
    if not art_id:
        # try older generic extraction "CORE-HEPH-SOUL-001"
        m = re.search(r"^\"\"\"([A-Za-z0-9_-]+)\s*\(", content, re.MULTILINE)
        if m:
            art_id = m.group(1)

    if not art_id:
        art_id = f"TOOL-{filename.upper().replace('.PY', '')}"

    status = status_search.group(1) if status_search else "[ACTIVE]"
    status = status.replace("`", "")
    version = ver_search.group(1) if ver_search else "v15.0 [OMEGA]"
    version = version.replace("**", "").replace("`", "")

    return art_id, status, version


def main():
    registry_str = "################################################\n"
    registry_str += "# AXION-CORE FORGE REGISTRY\n"
    registry_str += "# AUTO-GENERATED FOR OMEGA V15.0 CONTINUITY\n"
    registry_str += "################################################\n\n"

    files = [f for f in os.listdir(FORGE_DIR) if f.endswith(".py") and f != "generate_forge_registry.py"]
    for f in sorted(files):
        filepath = os.path.join(FORGE_DIR, f)
        with open(filepath, encoding="utf-8") as fh:
            content = fh.read()

        art_id, status, version = extract_metadata(content, f)
        chash = get_hash(filepath)

        # Write yaml block
        registry_str += f"{art_id}:\n"
        registry_str += f"  artifact_id: {art_id}\n"
        registry_str += f"  content_hash: {chash}\n"
        registry_str += "  domain: FORGE\n"
        registry_str += f"  official_name: {f}\n"
        registry_str += f"  path: axion-core/forge/{f}\n"
        registry_str += f"  status: '{status}'\n"
        registry_str += f"  version: {version}\n"

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        out.write(registry_str)

    print(f"Generated {OUT_FILE} with {len(files)} tool entries.")


if __name__ == "__main__":
    main()
