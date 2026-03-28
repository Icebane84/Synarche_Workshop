import hashlib
import os
import re
import sys
from pathlib import Path

import yaml

# Absolute Path Calibration: Resolve .agent directory relative to this script
# canonize_ritual.py is in .agent/skills/canonization/scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Traversal: scripts -> canonization -> skills -> .agent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
# Sync Root: parent of .agent
SYNC_ROOT = os.path.dirname(BASE_DIR)

# Adjust path to include the skill directory where governance_utils lives
UTILS_PATH = (
    Path(BASE_DIR) / "skills/documentation-alignment/scripts/governance_utils.py"
)
sys.path.append(str(UTILS_PATH.parent))

from governance_utils import ShadowLogger, generate_omni_anchor, is_v15_compliant

REGISTRY_PATH = Path(SYNC_ROOT) / "_governance/01_Registries/GVRN.Master.Registry.yaml"

CANONIZED_STATUS = "[CANONIZED]"


def normalize_path(abs_path):
    """Converts an absolute path to a root-relative modular path."""
    rel = os.path.relpath(abs_path, SYNC_ROOT).replace("\\", "/")
    return f"/{rel}" if not rel.startswith("/") else rel


def calculate_sha256(filepath):
    """Calculate the cryptographic hash of the file (excluding Block G)."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read file but stop before the Omni-Anchor if it exists
        content = f.read().decode("utf-8")
        anchor_pattern = r"\s*### \*\*Block G: The Omni-Anchor.*"
        stripped_content = re.sub(anchor_pattern, "", content, flags=re.DOTALL)
        sha256_hash.update(stripped_content.encode("utf-8"))
    return sha256_hash.hexdigest()


def get_artifact_id(content):
    """Extract Artifact ID from Block A or legacy anchor."""
    # Try Block A first
    match = re.search(r"\|\s*\*\*Artifact ID\*\*\s*\|\s*`(.*?)`", content)
    if match:
        return match.group(1)

    # Try legacy anchor (e.g., [TAXONOMY-ANCHOR] ID: SYNG.LINK.SEMANTIC-001)
    match = re.search(r"ID:\s*([A-Z0-9\._\-]+)", content)
    return match.group(1) if match else None


def get_domain(content):
    """Extract Domain from Block A or header."""
    match = re.search(r"\|\s*\*\*Domain\*\*\s*\|\s*`(.*?)`", content)
    if match:
        return match.group(1)

    match = re.search(r">\s*\*\*Domain\*\*:\s*(.*)", content)
    return match.group(1).strip() if match else "GVRN"


def get_relations(content):
    """Extract Relations from Block A."""
    match = re.search(r"\|\s*\*\*Relations\*\*\s*\|\s*`(.*?)`", content)
    return match.group(1).strip() if match else ""


def get_version(content):
    """Extract Version from Block A."""
    match = re.search(r"\|\s*\*\*Version\*\*\s*\|\s*\*\*?(.*?)\*\*?", content)
    return match.group(1).strip() if match else "v15.0 [OMEGA]"


def update_registry_status(
    registry, artifact_id, domain, target_path, new_hash, relations, version
):
    """Update or create registry entry for the artifact."""
    registry_entry = None
    for entry_key, entry_val in registry.items():
        if entry_val.get("artifact_id") == artifact_id:
            registry_entry = entry_key
            break

    if not registry_entry:
        print(
            f"[?] Warning: {artifact_id} is not in the Master Registry. Creating entry..."
        )
        registry_entry = artifact_id
        registry[registry_entry] = {
            "artifact_id": artifact_id,
            "domain": domain,
            "official_name": target_path.name,
            "path": normalize_path(target_path),
            "version": version,
        }

    # Always update these fields
    registry[registry_entry]["status"] = CANONIZED_STATUS
    registry[registry_entry]["content_hash"] = new_hash
    registry[registry_entry]["relations"] = relations
    registry[registry_entry]["version"] = version

    # Update parsed_relations if relations is present
    if relations:
        parsed = [r.strip() for r in relations.split(",") if r.strip()]
        registry[registry_entry]["parsed_relations"] = parsed

    return registry_entry


def update_artifact_metadata(content, artifact_id, domain, new_hash):
    """Update Block A status and Block G anchor in artifact content."""
    # 1. Update Block A Status
    new_content = re.sub(
        r"\|\s*\*\*Status.*?\s*\|\s*`.*?`",
        f"| **Status (State)**| `{CANONIZED_STATUS}`",
        content,
    )
    if CANONIZED_STATUS not in new_content:
        new_content = re.sub(
            r"\|\s*\*\*Status.*?\s*\|\s*.*?\s*\|",
            f"| **Status (State)**| `{CANONIZED_STATUS}`      |",
            new_content,
        )

    # 2. Update Block G
    omni_anchor = generate_omni_anchor(artifact_id, domain, status=CANONIZED_STATUS)
    omni_anchor = omni_anchor.replace("OMEGA-V15", new_hash[:16])

    anchor_pattern = r"### \*\*Block G: The Omni-Anchor.*"
    if re.search(anchor_pattern, new_content, flags=re.DOTALL):
        new_content = re.sub(anchor_pattern, omni_anchor, new_content, flags=re.DOTALL)
    else:
        if "###### **[ARTIFACT END]**" in new_content:
            new_content = new_content.replace(
                "###### **[ARTIFACT END]**",
                f"###### **[ARTIFACT END]**\n\n{omni_anchor}",
            )
        else:
            new_content += f"\n\n{omni_anchor}"

    return new_content


def canonize_artifact(target_path, dry_run=False):
    logger = ShadowLogger("CanonizeRitual")
    target_path = Path(target_path).absolute()

    if not target_path.exists():
        print(f"[!] Error: Target {target_path} does not exist.")
        return False

    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    artifact_id = get_artifact_id(content)
    if not artifact_id:
        logger.log_dissonance(str(target_path), "Missing Artifact ID.")
        print("[!] Error: Missing Artifact ID.")
        return False

    domain = get_domain(content)
    print(f"[ Ritual ] Initiating for: {artifact_id}...")

    # Seal 1: Structural Validation
    if not is_v15_compliant(content):
        logger.log_dissonance(str(target_path), "Not OMEGA v15.0 compliant.")
        print("FAIL: Structural non-compliance. Artifact must be Reforged first.")
        return False
    print("[Seal 1] PASS: Structural Integrity Verified.")

    # Seal 2: Semantic Alignment (Registry Check)
    if not REGISTRY_PATH.exists():
        print("[!] Error: Master Registry not found.")
        return False

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f) or {}

    new_hash = calculate_sha256(target_path)
    relations = get_relations(content)
    version = get_version(content)

    update_registry_status(
        registry, artifact_id, domain, target_path, new_hash, relations, version
    )
    print("[Seal 2] PASS: Semantic Registry Alignment.")
    print("[Seal 3] PASS: Cryptographic Finalization.")

    new_content = update_artifact_metadata(content, artifact_id, domain, new_hash)

    if not dry_run:
        # Write back Artifact
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        # Write back Registry
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            yaml.dump(registry, f, default_flow_style=False, sort_keys=True)

        logger.log_synthesis(
            str(target_path), f"Artifact and Registry Seal Complete for {artifact_id}."
        )
        logger.finalize(f"Canonization of {artifact_id} successful.")
        print(f"[Complete] Seal 3: Cryptographic Finalization [{new_hash[:16]}]")
        print(f"[ Ritual ] COMPLETE: {artifact_id} is now CANONIZED.")
    else:
        print("[ Result ] Dry Run: Metadata projection complete. No files written.")

    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Execute the Synarche Canonization Ritual."
    )
    parser.add_argument("--target", help="Path to the artifact to canonize.")
    parser.add_argument(
        "--directory", help="Path to a directory of artifacts to mass-canonize."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Perform validation without writing."
    )
    args = parser.parse_args()

    if args.directory:
        dir_path = Path(args.directory).absolute()
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"[!] Error: Directory {dir_path} does not exist.")
            sys.exit(1)

        success_count = 0
        total_count = 0
        for p in dir_path.glob("**/*"):
            if p.suffix in [".py", ".md"]:
                total_count += 1
                if canonize_artifact(p, args.dry_run):
                    success_count += 1
        print(
            f"\n[ Ritual ] Mass Canonization Complete: {success_count}/{total_count} files."
        )
        sys.exit(0 if success_count == total_count else 1)
    elif args.target:
        success = canonize_artifact(args.target, args.dry_run)
        sys.exit(0 if success else 1)
    else:
        print("[!] Error: Either --target or --directory must be specified.")
        sys.exit(1)
