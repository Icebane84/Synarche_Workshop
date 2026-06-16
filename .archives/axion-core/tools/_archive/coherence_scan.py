import json
import re
from pathlib import Path
from typing import Optional

# Configuration
PRS_PATH = r"c:\Users\Chris\Synarche_Workspace\axion-core\tools\PRS-001.json"
JSON_OUTPUT_PATH = r"c:\Users\Chris\Synarche_Workspace\playground\tarot-forge\src\engine\data\audit-report.json"
PROTOCOL_PREFIXES = ["UMB", "AOP", "GUCA", "CODEX", "CSL", "SELT", "MAP", "TOOL"]


def clean_val(val: Optional[str]) -> str:
    """Removes markdown markers and whitespace from a string."""
    if not val:
        return ""
    # Remove markdown markers (*, `) and whitespace
    return re.sub(r"[*`]", "", val).strip()


def is_protocol(id_str: Optional[str]) -> bool:
    """Checks if a given ID string belongs to a known protocol prefix."""
    if not id_str:
        return False
    return any(id_str.startswith(prefix) for prefix in PROTOCOL_PREFIXES)


def extract_kv_from_line(line: str) -> tuple[Optional[str], Optional[str]]:
    """Extracts a key-value pair from a markdown table line."""
    parts = [p.strip() for p in line.split("|")]
    # Expecting | Key | Value | -> parts length >= 3
    if len(parts) >= 3:
        k = clean_val(parts[1])
        v = clean_val(parts[2])
        if k.lower() not in ["field", "field name"] and k and v:
            return k.lower(), v
    return None, None


def extract_uip_map(content: str) -> dict[str, str]:
    """Parses markdown content to find and extract the UIP table as a dict."""
    data: dict[str, str] = {}
    lines = content.splitlines()
    potential_uip_table: list[str] = []
    in_table = False

    for line in lines:
        if "|" in line:
            potential_uip_table.append(line)
            in_table = True
        elif in_table:
            # Table ended, process it
            table_map: dict[str, str] = {}
            for tline in potential_uip_table:
                k, v = extract_kv_from_line(tline)
                if k and v:
                    table_map[k] = v

            # Check if this table is likely the UIP table (has ID or Version)
            if any("id" in k or "version" in k for k in table_map):
                data = table_map
                break

            potential_uip_table = []
            in_table = False

    return data


def get_id_from_uip(uip_map: dict[str, str]) -> Optional[str]:
    """Resolves the Artifact ID from the UIP map using multiple common keys."""
    # Priority keys for ID
    for k in uip_map:
        if "artifact id" in k or "module id" in k or "artifact_id" in k:
            return uip_map[k]
        if k == "id" or k.endswith(" id"):
            return uip_map[k]
    return None


def get_version_from_uip(uip_map: dict[str, str]) -> Optional[str]:
    """Resolves the Version from the UIP map."""
    for k, v in uip_map.items():
        if "version" in k:
            return v
    return None


def check_compliance(
    mod_id: str, expected_version: str, abs_path: Path, content: str
) -> Optional[dict[str, str]]:
    """Validates a file's UIP data against expected values.
    Returns a mismatch dict if validation fails, else None.
    """
    uip = extract_uip_map(content)
    actual_version = get_version_from_uip(uip)
    actual_id = get_id_from_uip(uip)

    if not actual_version:
        return {
            "id": mod_id,
            "file": abs_path.name,
            "type": "Version Missing",
            "expected": expected_version,
            "actual": "None",
        }

    v_exp = expected_version.split(" (")[0].lower()
    v_act = actual_version.split(" (")[0].lower()

    # Loose matching to allow for minor formatting differences
    if v_exp not in v_act and v_act not in v_exp:
        return {
            "id": mod_id,
            "file": abs_path.name,
            "type": "Version Drift",
            "expected": expected_version,
            "actual": actual_version,
        }

    if actual_id:
        # Check for ID mismatch
        if (
            actual_id.lower() != mod_id.lower()
            and mod_id.lower() not in actual_id.lower()
            and actual_id.lower() not in mod_id.lower()
        ):
            return {
                "id": mod_id,
                "file": abs_path.name,
                "type": "ID Mismatch",
                "expected": mod_id,
                "actual": actual_id,
            }

    return None


def analyze() -> None:
    """Executes the full architectural scan.
    Generates a textual report and a JSON data file for the Tarot Forge UI.
    """
    print(">>> INITIATING PROTOCOL COHERENCE SCAN v2.1")
    print("=" * 60)

    if not Path(PRS_PATH).exists():
        print(f"Error: PRS not found at {PRS_PATH}")
        return

    try:
        with open(PRS_PATH, "r", encoding="utf-8") as f:
            prs_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading PRS JSON: {e}")
        return

    mismatches: list[dict[str, str]] = []
    total_scanned = 0

    # Filter for protocols only to establish baseline first
    protocol_entries = [e for e in prs_data if is_protocol(e.get("Module ID", ""))]

    for entry in protocol_entries:
        mod_id = entry.get("Module ID")
        rel_path = entry.get("RelPath")
        expected_version = clean_val(entry.get("Version"))

        if not mod_id or not rel_path:
            continue

        abs_path = (Path(PRS_PATH).parent / rel_path).resolve()

        if not abs_path.exists() or abs_path.suffix != ".md":
            continue

        total_scanned += 1
        try:
            content = abs_path.read_text(encoding="utf-8", errors="ignore")
            mismatch = check_compliance(mod_id, expected_version, abs_path, content)
            if mismatch:
                mismatches.append(mismatch)

        except Exception as e:
            print(f"Error processing {abs_path.name}: {e}")

    # Calculate coherence BEFORE writing files
    coherence = (
        ((total_scanned - len(mismatches)) / total_scanned * 100)
        if total_scanned
        else 0.0
    )

    # 1. Write JSON Data for Tarot Forge
    scan_data = {
        "timestamp": "2026-01-25T18:59:00Z",  # In production this would be realtime
        "total_scanned": total_scanned,
        "dissonance_count": len(mismatches),
        "coherence_index": coherence,
        "mismatches": mismatches,
    }

    # Ensure directory exists
    Path(JSON_OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(scan_data, f, indent=4)

    # 2. Write Text Report for User/Console
    with open("scan_results.txt", "w", encoding="utf-8") as f:
        f.write("[!] PROTOCOL COHERENCE SUMMARY\n")
        f.write(f"Markdown Files Scanned:     {total_scanned}\n")
        f.write(f"Structural Dissonance:      {len(mismatches)}\n")
        f.write(f"System Coherence Index:     {coherence:.2f}%\n")
        f.write("-" * 60 + "\n")

        if mismatches:
            for m in mismatches[:15]:
                f.write(
                    f" - {m['id']} ({m['file']}): Found {m['actual']} [{m['type']}]\n"
                )

    print(f"Scan Complete. Coherence: {coherence:.2f}%")
    print(f"JSON Report written to: {JSON_OUTPUT_PATH}")


if __name__ == "__main__":
    analyze()
