import os

workspace_root = r"C:\Users\Chris\Synarche_Workspace"

print(f"Scanning subdirectories under {workspace_root}...")

results = []
for entry in os.scandir(workspace_root):
    if entry.is_dir():
        file_count = 0
        total_size = 0
        try:
            for root, _dirs, files in os.walk(entry.path):
                file_count += len(files)
                for f in files:
                    try:
                        total_size += os.path.getsize(os.path.join(root, f))
                    except OSError:
                        pass
        except Exception as e:
            print(f"Error scanning {entry.name}: {e}")
        results.append((entry.name, file_count, total_size))

results.sort(key=lambda x: x[1], reverse=True)

print("\nSubdirectory File Counts and Sizes:")
print(f"{'Directory':<30} | {'File Count':<12} | {'Size (MB)':<12}")
print("-" * 60)
for name, count, size in results:
    size_mb = size / (1024 * 1024)
    print(f"{name:<30} | {count:<12} | {size_mb:<12.2f}")
