import os


def get_dir_size(path, ignore_patterns):
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(path):
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
    ".godot",
]

vault_dev = r"C:\Users\Chris\_Desktop_Vault\dev"
if os.path.exists(vault_dev):
    for item in os.listdir(vault_dev):
        item_path = os.path.join(vault_dev, item)
        if os.path.isdir(item_path):
            size_clean, files_clean = get_dir_size(item_path, ignore_list)
            size_raw, files_raw = get_dir_size(item_path, [])
            print(f"Folder: {item}")
            print(
                f"  Clean Size: {size_clean / (1024 * 1024):.2f} MB ({files_clean} files)"
            )
            print(f"  Raw Size: {size_raw / (1024 * 1024):.2f} MB ({files_raw} files)")
            print("-" * 40)
