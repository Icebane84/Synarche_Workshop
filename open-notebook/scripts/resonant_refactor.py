import csv
import os
import re
from pathlib import Path

# Paths
VAULT_ROOT = Path(
    r"c:\Users\Chris\Synarche_Workspace\where_light_fades\where_light_fades"
)
OUTPUT_DIR = Path(r"c:\Users\Chris\Synarche_Workspace\open-notebook\data")
OUTPUT_FILE = OUTPUT_DIR / "semantic_anchors.csv"

# Regex Patterns
FRONTMATTER_PATTERN = re.compile(r"^---(.*?)---", re.DOTALL | re.MULTILINE)
KV_PATTERN = re.compile(r"^(\w+):\s*(.*)$", re.MULTILINE)
RELATIONS_PATTERN = re.compile(r"relations:\s*(.*?)(?=\n\w+:|$)", re.DOTALL)
TAGS_PATTERN = re.compile(r"tags:\s*(.*?)(?=\n\w+:|$)", re.DOTALL)


def parse_frontmatter(content):
    match = FRONTMATTER_PATTERN.search(content)
    if not match:
        return {}

    yaml_text = match.group(1)
    metadata = {}

    # Simple KV extraction
    for kv_match in KV_PATTERN.finditer(yaml_text):
        key = kv_match.group(1).strip()
        value = kv_match.group(2).strip()
        metadata[key] = value

    tag_match = TAGS_PATTERN.search(yaml_text)
    if tag_match:
        tags = [
            t.strip("- ").strip() for t in tag_match.group(1).split("\n") if t.strip()
        ]
        metadata["tags"] = "; ".join(tags)

    rel_match = RELATIONS_PATTERN.search(yaml_text)
    if rel_match:
        rels = [
            r.strip("- ").strip() for r in rel_match.group(1).split("\n") if r.strip()
        ]
        metadata["relations"] = "; ".join(rels)

    return metadata


def extract_shard(content, filename_stem):
    # Remove frontmatter
    content = FRONTMATTER_PATTERN.sub("", content).strip()

    # Heuristics to find the REAL title and REAL content
    # Skip "Block A", "Identification Lock", "ARTIFACT START", "ARTIFACT END"
    # Skip tables

    lines = content.split("\n")
    name = filename_stem
    body_lines = []

    found_good_header = False

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        # Skip common boilerplate
        if any(
            x in clean
            for x in [
                "Identification Lock",
                "ARTIFACT START",
                "ARTIFACT END",
                "Block A",
                "Block B",
                "Block C",
                "Block D",
            ]
        ):
            continue
        if clean.startswith("|") or clean.startswith("---"):
            continue

        # First Level 1 or 2 header that isn't boilerplate is the name
        if (
            clean.startswith("# ") or clean.startswith("## ")
        ) and not found_good_header:
            name = clean.lstrip("# ").strip("*_")
            found_good_header = True
            continue

        # Collect narrative text
        if not clean.startswith("#") and len(clean) > 5:
            body_lines.append(clean)

    # Shard is the first few meaningful paragraphs
    shard = " ".join(body_lines[:5])
    return name, shard[:800]


def execute_refactor() -> None:

    if not OUTPUT_DIR.exists():
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    rows = []

    for folder in VAULT_ROOT.iterdir():
        if not folder.is_dir():
            continue

        match = re.match(r"^(\d+)\.\s*(.*)", folder.name)
        if not match:
            continue

        category_num = match.group(1)
        category_label = match.group(2)

        for md_file in folder.glob("**/*.md"):
            if "_nexus" in str(md_file) or ".obsidian" in str(md_file):
                continue

            try:
                content = md_file.read_text(encoding="utf-8")
                metadata = parse_frontmatter(content)
                name, shard = extract_shard(content, md_file.stem)

                rows.append(
                    {
                        "artifact_id": metadata.get("artifact_id", md_file.stem),
                        "category": f"{category_num}. {category_label}",
                        "name": name,
                        "status": metadata.get("status", "ACTIVE").strip("[]"),
                        "version": metadata.get("version", "v1.0"),
                        "semantic_anchors": metadata.get("relations", ""),
                        "tags": metadata.get("tags", ""),
                        "content_shard": shard,
                        "path": str(md_file.relative_to(VAULT_ROOT)),
                    }
                )
            except Exception as e:
                pass

    fieldnames = [
        "artifact_id",
        "category",
        "name",
        "status",
        "version",
        "semantic_anchors",
        "tags",
        "content_shard",
        "path",
    ]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    execute_refactor()
