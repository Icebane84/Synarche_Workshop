import sys
sys.stdout.reconfigure(encoding="utf-8")

"""
Synarche Knowledge Base Builder
================================
Collects canonical governance documents and consolidates them into
chunked knowledge files ready for upload to OpenWebUI's Knowledge system.

Output: _governance/knowledge_export/ (one .md file per knowledge domain)
"""

import os
import re
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path("C:/Users/Chris/Synarche_Workspace")
OUTPUT_DIR = WORKSPACE_ROOT / "_governance" / "knowledge_export"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Canonical documents to include — ordered by importance
KNOWLEDGE_MANIFEST = {
    "01_SynarcheCore": [
        "_governance/00_Codex/CORE.Codex.Phoenix.md",
        "_governance/10_Governance/GVRN.HUD.Map.md",
        "_governance/10_Governance/GVRN.ID.Standard.md",
        ".agent/substrate/OGLN_Directory_Standard.md",
    ],
    "02_Architecture": [
        "_governance/20_Architecture/GVRN.STRUCT.001.md",
        "_governance/20_Architecture/ARCH.ARCH.GrandUnifiedArchitecture.md",
        "_governance/01_Registries/PRS-001_PathMapping.md",
        "tsconfig.json",
    ],
    "03_Registries": [
        "_governance/01_Registries/GVRN.Registry.Master.md",
        "_governance/01_Registries/GVRN.Registry.PhoenixRosettaStone.md",
    ],
    "04_CodingStandards": [
        "_governance/GVRN.Guide.Coding.md",
        "_governance/08_Documentation/GVRN.Documentation.Architecture.md",
    ],
}

MAX_CHUNK_BYTES = 300_000  # OpenWebUI handles up to ~300KB well per document

def clean_content(text: str, source_path: str) -> str:
    """Strip noise, preserve semantic content."""
    # Remove TRANSCLUDE directives (unresolved)
    text = re.sub(r"\{\{.*?\}\}", "", text)
    return text.strip()

def build_knowledge_file(domain_name: str, source_paths: list[str]) -> tuple[str, int]:
    """Merge sources into a single annotated knowledge document."""
    sections = []
    total_bytes = 0

    header = f"""# Synarche Knowledge Base: {domain_name}
> Generated: {datetime.now().isoformat()}
> Source: Synarche_Workspace Governance Registry
> Standard: OMEGA v15.0 [CANONIZED]

---
"""
    sections.append(header)

    for rel_path in source_paths:
        abs_path = WORKSPACE_ROOT / rel_path
        if not abs_path.exists():
            sections.append(f"\n> [MISSING]: `{rel_path}` - skipped\n")
            print(f"  [SKIP] Not found: {rel_path}")
            continue

        raw = abs_path.read_text(encoding="utf-8", errors="replace")
        content = clean_content(raw, rel_path)
        size = len(content.encode("utf-8"))
        total_bytes += size

        section = f"""
---
## SOURCE: `{rel_path}`
> Size: {size:,} bytes

{content}
"""
        sections.append(section)
        print(f"  [OK] {rel_path} ({size:,} bytes)")

    return "\n".join(sections), total_bytes

print("=" * 60)
print("SYNARCHE KNOWLEDGE BASE BUILDER")
print("=" * 60)

manifest_lines = []
for domain_name, sources in KNOWLEDGE_MANIFEST.items():
    print(f"\n[{domain_name}]")
    content, total = build_knowledge_file(domain_name, sources)

    output_file = OUTPUT_DIR / f"SYKB_{domain_name}.md"
    output_file.write_text(content, encoding="utf-8")

    size_kb = total / 1024
    status = "[OK]" if total < MAX_CHUNK_BYTES else "[LARGE]"
    print(f"  >> Written: {output_file.name} ({size_kb:.1f} KB) {status}")
    manifest_lines.append(f"| `SYKB_{domain_name}.md` | {size_kb:.1f} KB | {status} |")

# Write manifest index
manifest = f"""# Synarche Knowledge Export Manifest
Generated: {datetime.now().isoformat()}

## Upload Order (OpenWebUI → Workspace → Knowledge → New Collection)

| File | Size | Status |
|------|------|--------|
""" + "\n".join(manifest_lines) + """

## How to Use in OpenWebUI
1. Go to **Workspace → Knowledge → + New Collection**
2. Name it: `Synarche-Core`
3. Upload all `SYKB_*.md` files
4. In any chat, type `#Synarche-Core` to ground the model in these docs

## How to Use in Continue
The `@codebase` context provider in your config.json already indexes your
source files. For governance context, use `@docs` and reference the
Phoenix Codex or PRS-001 PathMapping.
"""

(OUTPUT_DIR / "MANIFEST.md").write_text(manifest, encoding="utf-8")

print("\n" + "=" * 60)
print(f"[DONE] Export complete: {OUTPUT_DIR}")
print(f"   Upload these files to OpenWebUI: Workspace → Knowledge")
print("=" * 60)
