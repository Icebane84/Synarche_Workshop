import os

gov_dir = r"C:\Users\Chris\Synarche_Workspace\_governance"

print("Scanning _governance subdirectories to find file hotspots...")

results = []
for root, _dirs, files in os.walk(gov_dir):
    file_count = len(files)
    if file_count > 0:
        rel_path = os.path.relpath(root, gov_dir)
        results.append((rel_path, file_count))

results.sort(key=lambda x: x[1], reverse=True)

print("\nHotspots in _governance:")
for rel_path, count in results[:20]:
    print(f"{rel_path:<60} | {count:<10} files")
