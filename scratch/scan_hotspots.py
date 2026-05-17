import os

workspace_root = r"C:\Users\Chris\Synarche_Workspace"

print("Scanning subdirectories up to 3 levels deep to find file count hotspots...")

hotspots = []

for root, dirs, files in os.walk(workspace_root):
    # Calculate depth relative to workspace root
    rel_path = os.path.relpath(root, workspace_root)
    if rel_path == ".":
        depth = 0
    else:
        depth = len(rel_path.split(os.sep))
    
    if depth > 3:
        # Don't recurse deeper in walk to keep it fast, but we want to count files
        continue
        
    file_count = len(files)
    if file_count > 100 or any(d in ['node_modules', '.venv', 'venv', '.git'] for d in dirs):
        hotspots.append((rel_path, file_count, len(dirs)))

# Let's also specifically check the size and file count of typical directories
target_dirs = [
    ".git",
    "open-notebook/.venv",
    "open-notebook/frontend/node_modules",
    "axion-core/.venv",
    "axion-core/.venv_prs",
    "axion-core/node_modules",
    "phoenix-rosetta-stone/node_modules",
    "nova_forge/playground/tarot-forge/node_modules",
    "_governance",
    "_governance/_archive",
    "_governance/60_Archives",
]

print("\n--- Specific Large Directories Scan ---")
for target in target_dirs:
    full_path = os.path.join(workspace_root, target.replace('/', os.sep))
    if os.path.exists(full_path):
        f_count = 0
        total_sz = 0
        for r, ds, fs in os.walk(full_path):
            f_count += len(fs)
        print(f"{target:<50} | {f_count:<10} files")
    else:
        print(f"{target:<50} | DOES NOT EXIST")
