import os


def scan_dir(path, max_depth=3, depth=1):
    if depth > max_depth:
        return
    try:
        items = os.listdir(path)
    except OSError:
        return

    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            # Calculate size
            total_size = 0
            file_count = 0
            for root, _dirs, files in os.walk(item_path):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        total_size += os.path.getsize(fp)
                        file_count += 1
                    except OSError:
                        pass
            size_mb = total_size / (1024 * 1024)
            print(
                "  " * (depth - 1)
                + f"[DIR] {item}: {size_mb:.2f} MB ({file_count} files)"
            )
            # Recurse
            scan_dir(item_path, max_depth, depth + 1)
        else:
            try:
                size_kb = os.path.getsize(item_path) / 1024
                print("  " * (depth - 1) + f"[FILE] {item}: {size_kb:.2f} KB")
            except OSError:
                pass


print("Scanning C:\\Users\\Chris\\Synarche_Workspace\\_governance:")
scan_dir(r"C:\Users\Chris\Synarche_Workspace\_governance", max_depth=2)

print("\nScanning C:\\Users\\Chris\\Synarche_Workspace\\.archives:")
scan_dir(r"C:\Users\Chris\Synarche_Workspace\.archives", max_depth=2)
