"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-HEPH-TRANSMUTE-001`     | The Sovereign ID. |
| **Official Name**   | `transmute_context.py`        | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-HEPH`                   | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Context Token Optimizer`     | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Artisan`           | The Sovereign.    |

**The Spirit Bomb Axiom: Contextual Compression (Law 30)**
> Implemented to optimize LLM Token Constraints by distilling structural 
> Markdown into dense JSON metadata mapping.
"""

import sys
import re
import json
from pathlib import Path

def compress_metadata(content: str) -> str:
    """
    Finds the UIP-V15 Block A metadata table in a markdown file and 
    compresses it into a dense JSON payload to save LLM context tokens.
    """
    
    # Regex to match the Block A metadata section
    # Matches the header, the table, and stops at the next major section or end of table
    block_pattern = re.compile(
        r'(###? \*\*Block A:.*?UIP-V15.*?\*\*\n+)(?:> .*?\n+)*(\|.*\|.*\|.*\|\n)(?:\|[- :\.]+\|\n)?((?:\|.*\|.*\|.*\|\n)+)', 
        re.MULTILINE | re.IGNORECASE | re.DOTALL
    )

    match = block_pattern.search(content)
    if not match:
        return content  # No compressible metadata block found

    header_block = match.group(0)
    data_rows = match.group(3).strip().split('\n')
    
    metadata = {}
    for row in data_rows:
        cols = [c.strip() for c in row.split('|')[1:-1]]
        if len(cols) >= 2:
            # Strip exact markdown formatting like **, backticks, etc.
            key = re.sub(r'[*`]', '', cols[0]).strip()
            value = re.sub(r'[*`]', '', cols[1]).strip()
            metadata[key] = value

    json_payload = json.dumps({"UIP-V15": metadata}, separators=(',', ':'))
    
    # Replace the entire bulky markdown block with the compressed JSON
    compact_content = content.replace(header_block, f"```json\n{json_payload}\n```\n")
    return compact_content


def transmute_file(filepath: Path) -> None:
    """Read a file, transmute its context, and print to stdout."""
    if not filepath.exists():
        print(f"Error: File '{filepath}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    try:
        raw_text = filepath.read_text(encoding="utf-8")
        optimized_text = compress_metadata(raw_text)
        print(optimized_text)
    except Exception as e:
        print(f"Failed to transmute file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transmute_context.py <path_to_markdown_file>")
        sys.exit(1)
        
    target_path = Path(sys.argv[1]).resolve()
    transmute_file(target_path)
