import re
from pathlib import Path

# Configuration
OSLM_FILENAME = "UMB-OSLM-001_PPLGraphOutline_v11.0.md"
SEARCH_DIRS = [
    "c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library/1_Modules",
    "c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation",
    "Documentation",
    "docs",
]

ARTIFACT_ID_REGEX = (
    r"(?:UMB|AOP|GUCA|CSL|UEB|UIB|UWB|CMD|ENTITY|SELT|MAP|TOOL)-[A-Z]+-\d+"
)


def find_oslm_file():
    for d in SEARCH_DIRS:
        path = Path(d)
        if not path.is_absolute():
            path = Path.cwd() / d

        if path.exists():
            found = list(path.rglob(OSLM_FILENAME))
            if found:
                return found[0]
            # Fallback
            found = list(path.rglob("UMB-OSLM-001*.md"))
            if found:
                return found[0]
    return None


# Enhanced parsing logic with Name->ID mapping
def parse_registry_for_map(content):
    name_to_id = {}
    lines = content.splitlines()
    ARBITRARY_ID_REGEX = r"[A-Z]{3,}-[A-Z0-9]+-\d+"  # Loosened regex

    for line in lines:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        # Heuristic: Find a row with Name and ID
        # Many formats in the messy file.
        # Line 623: | Name | ID | Type | ...

        for p in parts:
            if not p:
                continue
            # If p looks like an ID
            if re.match(ARBITRARY_ID_REGEX, p):
                match_id = p
                # Check neighbors for Name
                idx = parts.index(p)
                if idx > 0 and parts[idx - 1]:
                    name_candidate = parts[idx - 1]
                    if (
                        len(name_candidate) > 5 and "-" not in name_candidate[:4]
                    ):  # Basic heuristic
                        name_to_id[name_candidate] = match_id

    # Manual overwrites for known stubborn keys if regex misses
    name_to_id["The Phoenix Codex"] = "CODEX-001"
    name_to_id["The AI Codex"] = "CPD-001"
    name_to_id["The Phoenix Genesis Pipeline"] = "UWB-PGP-001"

    return name_to_id


def _resolve_source_id(raw_name: str, id_map: dict) -> str:
    src_id = id_map.get(raw_name)
    if not src_id:
        src_match = re.search(ARTIFACT_ID_REGEX, raw_name)
        if src_match:
            src_id = src_match.group(0)
        else:
            src_id = raw_name
    return src_id


def _parse_link_items(raw_links: str, src_id: str) -> list[dict]:
    edges = []
    link_items = raw_links.split("- ")
    for item in link_items:
        item = item.strip()
        if not item:
            continue

        target_match = re.search(ARTIFACT_ID_REGEX, item)
        if target_match:
            target_id = target_match.group(0)
            desc = item.replace(target_id, "").strip(": .").strip()
            if src_id and target_id:
                edges.append(
                    {
                        "source": src_id,
                        "relation": "Synergistic Link",
                        "target": target_id,
                        "desc": desc,
                    }
                )
    return edges


def parse_synergistic_links(content, id_map):
    edges = []
    lines = content.splitlines()
    in_table = False
    current_source = None

    for line in lines:
        stripped = line.strip()
        if "Synergistic Links" in stripped and "|" in stripped:
            in_table = True
            continue
        if "---" in stripped and "|" in stripped:
            continue

        if in_table:
            if stripped.startswith("#"):
                in_table = False
                continue

            if stripped.startswith("|"):
                parts = stripped.split("|")
                if len(parts) >= 3:
                    raw_name = parts[1].strip()
                    raw_links = parts[2].strip()

                    if raw_name:
                        current_source = raw_name

                    if not current_source:
                        continue

                    src_id = _resolve_source_id(current_source, id_map)
                    edges.extend(_parse_link_items(raw_links, src_id))

    return edges


def main():
    f = find_oslm_file()
    # Check for backup first (source of truth for old data)
    source_file = f
    if f:
        backup = f.with_suffix(".bak.md")
        if backup.exists():
            print(f"📂 Found backup file {backup}, using it as source.")
            source_file = backup

    if not source_file or not source_file.exists():
        print("❌ OSLM file/backup not found.".")
        return

    print(f"📖 Parsing {source_file}...")
    try:
        content = source_file.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    print("🔍 Building ID Map...")
    id_map = parse_registry_for_map(content)
    print(f"   Mapped {len(id_map)} artifact names to IDs.")

    edges = parse_synergistic_links(content, id_map)
    print(f"✅ Found {len(edges)} raw edges.")

    if not edges:
        print("⚠️ No edges found. Aborting.")
        return

    # Target is ALWAYS the .md file, even if we read from backup
    target_f = f if f else source_file

    # Backup again if we read from main file?
    if target_f == source_file:
        backup = target_f.with_suffix(".bak.md")
        target_f.rename(backup)
        print(f"💾 Backed up to {backup}")
        # Now target_f is missing, we open it for writing regular
        target_f = f

    # Generate New Content
    new_content = """---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `UMB-OSLM-001` |
| **Version** | `v11.1` |
| **Status** | `ACTIVE` |
| **Type** | `Master Matrix` |
---

# UMB-OSLM-001: Omni-Log Synergistic Links Matrix (Reforged)

> **Purpose**: The definitive machine-readable registry of all synergistic connections within the Phoenix Protocol Library.

## V. Master Synergistic Links Matrix

| Source Artifact | Relationship | Target Artifact | Description |
| :--- | :--- | :--- | :--- |
"""

    unique_rows = set()
    rows_str = []
    count = 0

    for e in edges:
        key = (e["source"], e["target"])
        if key in unique_rows:
            continue
        unique_rows.add(key)

        desc = e["desc"].replace("|", "-")
        # Ensure IDs are wrapped in code ticks?
        # If Source is a Name (fallback), maybe don't wrap?
        src_display = f"`{e['source']}`" if "-" in e["source"] else e["source"]
        tgt_display = f"`{e['target']}`"

        row = f"| {src_display} | {e['relation']} | {tgt_display} | {desc} |"
        rows_str.append(row)
        count += 1

    new_content += "\n".join(rows_str)

    try:
        target_f.write_text(new_content, encoding="utf-8")
        print(f"✨ Successfully reforged {target_f} with {count} unique rows.")
    except Exception as e:
        print(f"❌ Failed to write new file: {e}")
        # Restore backup?
        print("⚠️ Original file is at .bak.md")


if __name__ == "__main__":
    main()
