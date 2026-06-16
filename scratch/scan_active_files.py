import os

workspace_root = r"C:\Users\Chris\Synarche_Workspace"

print(
    "Scanning for active JS/TS/PY files (excluding node_modules, .venv, _governance)..."
)

extensions = [".ts", ".tsx", ".js", ".jsx", ".py"]
ignored_dirs = [
    "node_modules",
    ".venv",
    "venv",
    ".git",
    "_governance",
    ".archives",
    ".mypy_cache",
    ".ruff_cache",
    ".trunk",
    "scratch",
]

counts = {}
for root, dirs, files in os.walk(workspace_root):
    # Modify dirs in-place to skip scanning ignored directories
    dirs[:] = [d for d in dirs if d not in ignored_dirs]

    rel_path = os.path.relpath(root, workspace_root)
    for f in files:
        _, ext = os.path.splitext(f)
        if ext in extensions:
            path_key = rel_path if rel_path != "." else "root"
            counts[path_key] = counts.get(path_key, 0) + 1

print("\nActive JS/TS/PY file counts by directory (excluding ignored):")
print(f"{'Directory':<40} | {'File Count':<10}")
print("-" * 55)
for path, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{path:<40} | {count:<10}")
