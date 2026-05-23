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

paths = {
    "Ashen Oath RPG": r"C:\Users\Chris\Ashen Oath-3rd Person RPG",
    "Disengage Entropy": r"C:\Users\Chris\Disengage Entropy",
    "Desktop Vault Dev": r"C:\Users\Chris\_Desktop_Vault\dev",
}

for name, path in paths.items():
    if os.path.exists(path):
        size_clean, files_clean = get_dir_size(path, ignore_list)
        size_raw, files_raw = get_dir_size(path, [])
        print(f"Project: {name}")
        print(
            f"  Clean Size: {size_clean / (1024 * 1024):.2f} MB ({files_clean} files)"
        )
        print(f"  Raw Size: {size_raw / (1024 * 1024):.2f} MB ({files_raw} files)")
        print("-" * 40)
    else:
        print(f"Project: {name} [NOT FOUND at {path}]")
