import os


def get_dir_size(path, ignore_patterns):
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_patterns]
        for f in files:
            fp = os.path.join(root, f)
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                    file_count += 1
                except OSError:
                    pass
    return total_size, file_count


ignore_list = [
    "node_modules",
    ".git",
    ".venv",
    "env",
    "venv",
    "__pycache__",
    ".gradle",
    "build",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".singularity_cache",
]

dev_dir = r"C:\Users\Chris\.dev"
print(f"Scanning {dev_dir}...")
if os.path.exists(dev_dir):
    for item in os.listdir(dev_dir):
        item_path = os.path.join(dev_dir, item)
        if os.path.isdir(item_path):
            has_git = os.path.exists(os.path.join(item_path, ".git"))
            size_clean, files_clean = get_dir_size(item_path, ignore_list)
            size_raw, files_raw = get_dir_size(item_path, [])

            size_clean_mb = size_clean / (1024 * 1024)
            size_raw_mb = size_raw / (1024 * 1024)

            print(f"Folder: {item}")
            print(f"  Git Repo: {has_git}")
            print(f"  Clean Size: {size_clean_mb:.2f} MB ({files_clean} files)")
            print(f"  Raw Size: {size_raw_mb:.2f} MB ({files_raw} files)")
            print("-" * 40)

workspace_dir = r"C:\Users\Chris\Synarche_Workspace"
print(f"\nScanning {workspace_dir}...")
if os.path.exists(workspace_dir):
    for item in os.listdir(workspace_dir):
        item_path = os.path.join(workspace_dir, item)
        if os.path.isdir(item_path):
            has_git = os.path.exists(os.path.join(item_path, ".git"))
            size_clean, files_clean = get_dir_size(item_path, ignore_list)
            size_raw, files_raw = get_dir_size(item_path, [])

            size_clean_mb = size_clean / (1024 * 1024)
            size_raw_mb = size_raw / (1024 * 1024)

            print(f"Folder: {item}")
            print(f"  Git Repo: {has_git}")
            print(f"  Clean Size: {size_clean_mb:.2f} MB ({files_clean} files)")
            print(f"  Raw Size: {size_raw_mb:.2f} MB ({files_raw} files)")
            print("-" * 40)
