import subprocess
import sys

def find_large_objects():
    # Step 1: Get all objects and their sizes
    try:
        # We use rev-list to get all object SHAs, then pipe to cat-file for sizes
        rev_list = subprocess.Popen(["git", "rev-list", "--objects", "--all"], stdout=subprocess.PIPE)
        cat_file = subprocess.check_output(["git", "cat-file", "--batch-check=%(objectname) %(objectsize) %(rest)"], stdin=rev_list.stdout).decode('utf-8', errors='ignore')
        rev_list.stdout.close()
    except Exception as e:
        print(f"Error running git: {e}")
        return

    objects = []
    for line in cat_file.strip().split('\n'):
        parts = line.split(' ')
        if len(parts) >= 2:
            sha = parts[0]
            try:
                size = int(parts[1])
            except ValueError:
                continue
            name = " ".join(parts[2:]) if len(parts) > 2 else "[No Path]"
            objects.append({'sha': sha, 'size': size, 'name': name})

    # Sort by size
    objects.sort(key=lambda x: x['size'], reverse=True)

    print(f"{'SHA':<10} {'Size (MB)':<10} {'Path'}")
    print("-" * 60)
    for obj in objects[:20]:
        size_mb = obj['size'] / (1024 * 1024)
        if size_mb > 1: # Only show objects > 1MB
            print(f"{obj['sha'][:8]:<10} {size_mb:<10.2f} {obj['name']}")

if __name__ == "__main__":
    find_large_objects()
