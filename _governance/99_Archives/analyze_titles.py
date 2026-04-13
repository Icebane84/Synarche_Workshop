import os
import re

LIBRARY_ROOT = r"c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library"
SUBDIRS = ["1_Modules", "2_Protocols", "3_Commands", "4_Blueprints", "5_Metrics", "6_Specifications"]

def get_title_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Strategy 1: Look for "Official Name" or "Title" in a table (Loose match)
        for line in lines:
            if "|" in line and ("Official Name" in line or "Title" in line):
                parts = line.split("|")
                # Usually Key | Value or | Key | Value |
                if len(parts) >= 3:
                     # Check if this row is actually the one we want
                    key_cell = parts[1].strip().replace("*", "")
                    if "Official Name" in key_cell or "Title" in key_cell:
                        val = parts[2].strip().strip("`").strip()
                        if val: return val
            
        # Strategy 2: Look for the first meaningful Header
        for line in lines:
            if line.startswith("#"):
                clean = line.lstrip("#").strip()
                # meaningful = not UIP header, not "Tab X", not "Unknown", not "Genesis Stamp"
                if "Universal Identification" in clean: continue
                if "Genesis Stamp" in clean: continue
                if re.match(r"\**Tab \d+\**", clean, re.IGNORECASE): continue
                if clean.lower() == "unknown": continue
                
                return clean.replace("*", "")

    except Exception as e:
        return f"Error: {e}"
        
    # Strategy 3: filename fallback
    fname = os.path.basename(filepath)
    fname = fname.replace("_v11.0.md", "").replace(".md", "")
    return fname

def scan_library():
    results = []
    
    for subdir in SUBDIRS:
        dir_path = os.path.join(LIBRARY_ROOT, subdir)
        if not os.path.exists(dir_path):
            continue
            
        for filename in os.listdir(dir_path):
            if filename.endswith(".md"):
                # Filter: only interested in Tab or Unknown files
                if "tab" not in filename.lower() and "unknown" not in filename.lower():
                    continue
                    
                filepath = os.path.join(dir_path, filename)
                title = get_title_from_file(filepath)
                
                results.append({
                    "subdir": subdir,
                    "filename": filename,
                    "title": title
                })

    # Output as a markdown table for easy reading by the LLM
    print(f"| Subdirectory | Filename | Actual Title |")
    print(f"| :--- | :--- | :--- |")
    for r in results:
        print(f"| {r['subdir']} | {r['filename']} | {r['title']} |")

if __name__ == "__main__":
    scan_library()
