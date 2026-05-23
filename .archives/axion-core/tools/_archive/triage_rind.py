import re
from pathlib import Path

WORKSPACE_ROOT = Path("c:/Users/Chris/Synarche_Workspace")
GOVERNANCE_DIR = WORKSPACE_ROOT / "_governance"
DIRECTORIES_TO_SCAN = ["1_Modules", "2_Protocols", "4_Blueprints"]

# Files explicitly queued in GVRN.Catalog.Master.md
QUEUED_LEGACY = [
    "AOP-AAR-001_TheAfter-ActionReviewProtocol_v11.0.md",
    "AOP-CORE-LOCK-001_AOP-CORE-LOCK-001_GenesisSeedLockProtocol_v10_v11.0.md",
    "UMB-ARCH-OATH-001_OathbringerSystemArchitecture_v11.0.md",
]


def scan_file(file_path):
    rel_path = file_path.relative_to(GOVERNANCE_DIR)
    filename = file_path.name

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for v13.0 or higher
    is_v13 = "v13.0" in content or "v13.1" in content

    # Check for new header format (Chronos Lock)
    # Looking for the 12/13-point table in Section I
    has_new_header = (
        "Artifact ID" in content
        and "Provenance" in content
        and "Celestial Class" in content
    )

    # Check naming convention
    # Legacy: ID-NAME_vVERSION.md
    # New: ID.Name.Type.md or GVRN-FMT-001...
    is_legacy_name = "_" in filename and "-v" not in filename and ".md" in filename
    if re.match(r"^[A-Z]+\.[A-Z][a-z]+\.[A-Z][a-z]+\.md$", filename):
        is_legacy_name = False
    if filename.startswith("GVRN-FMT") or filename.startswith("GVRN-CODEX"):
        is_legacy_name = False

    status = (
        "TRANSMUTED"
        if (not is_legacy_name and is_v13 and has_new_header)
        else "LEGACY_RIND"
    )

    # Refine status based on version
    version_match = re.search(r"v(\d+\.\d+)", content)
    version = version_match.group(1) if version_match else "unknown"

    return {
        "filename": filename,
        "path": str(rel_path),
        "status": status,
        "version": version,
        "has_header": has_new_header,
        "is_legacy_name": is_legacy_name,
    }


def main():
    results = []
    print("--- Starting TRIAGE_SCAN: Legacy_Rind ---")

    for subdir in DIRECTORIES_TO_SCAN:
        scan_path = GOVERNANCE_DIR / subdir
        if not scan_path.exists():
            continue

        for file in scan_path.glob("*.md"):
            res = scan_file(file)
            results.append(res)

    # Filter for Legacy Rind
    legacy_rind = [r for r in results if r["status"] == "LEGACY_RIND"]
    transmuted = [r for r in results if r["status"] == "TRANSMUTED"]

    print(f"\n{'-' * 40}")
    print("SCAN SUMMARY")
    print(f"{'-' * 40}")
    print(f"Total Artifacts Scanned: {len(results)}")
    print(f"Transmuted (v13.0+): {len(transmuted)}")
    print(f"Legacy Rind Found:    {len(legacy_rind)}")
    print(f"{'-' * 40}\n")

    print("DETAILED TRIAGE (Legacy_Rind scope):\n")
    print(f"{'Filename':<60} | {'Ver':<6} | {'Header':<6} | {'Queued'}")
    print(f"{'-' * 60}-|{'-' * 8}|{'-' * 8}|{'-' * 6}")

    for res in legacy_rind:
        is_queued = "YES" if res["filename"] in QUEUED_LEGACY else ""
        header_tick = "[x]" if res["has_header"] else "[ ]"
        print(
            f"{res['filename']:<60} | {res['version']:<6} | {header_tick:<6} | {is_queued}"
        )


if __name__ == "__main__":
    main()
