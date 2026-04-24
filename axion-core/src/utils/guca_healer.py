import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# The GUCA-HEALER Unit
# Scans the workspace for Orphan Nodes missing the UIP / RNC v13.0 headers

WORKSPACE_ROOT = Path("C:/Users/Chris/Synarche_Workspace")
TARGET_DIRS = ["_governance", "axion-core"]

UIP_PATTERN = re.compile(r"# Universal Identification & Provenance \(UIP\)", re.IGNORECASE)
UIP_ALT_PATTERN = re.compile(r"UIP:", re.IGNORECASE)

def generate_uip_header(file_name):
    module_id = file_name.replace('.md', '').upper()
    return f"""---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `{module_id}` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

"""

def scan_for_orphans(heal=False):
    print("Initialize GUCA-HEALER: Commencing Orphan Node Scan...")
    orphan_nodes = []
    scanned_files = 0
    
    for target in TARGET_DIRS:
        target_path = WORKSPACE_ROOT / target
        if not target_path.exists():
            continue
            
        for root, dirs, files in os.walk(target_path):
            # Skip node_modules, python cache, vendor, and _archive
            if any(skip in root for skip in ["node_modules", "__pycache__", ".git", "vendor", "_archive", "docs\\agents", "docs\\commands", "docs\\specs"]):
                continue
                
            for file in files:
                if file.endswith(".md"):
                    scanned_files += 1
                    file_path = Path(root) / file
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read(2048) # Read just the head to look for UIP
                            
                            if not UIP_PATTERN.search(content) and not UIP_ALT_PATTERN.search(content):
                                orphan_nodes.append(file_path)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    print(f"\nScan Complete. Total MD files scanned: {scanned_files}")
    if orphan_nodes:
        print(f"Detected {len(orphan_nodes)} Orphan Nodes (Missing UIP):")
        for node in orphan_nodes:
            print(f" - {node.relative_to(WORKSPACE_ROOT)}")
            
            if heal:
                try:
                    with open(node, "r", encoding="utf-8") as f:
                        original_content = f.read()
                    
                    header = generate_uip_header(node.name)
                    with open(node, "w", encoding="utf-8") as f:
                        f.write(header + original_content)
                    print(f"   [HEALED] Applied canonical UIP to {node.name}")
                except Exception as e:
                    print(f"   [ERROR] Failed to heal {node.name}: {e}")
    else:
        print("System Coherence is at 100%. No Orphan Nodes detected.")

if __name__ == "__main__":
    heal_mode = "--heal" in sys.argv
    scan_for_orphans(heal=heal_mode)
