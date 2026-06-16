import os
import shutil
import sys
import time
import zipfile

# Configure stdout encoding safely for Windows console environments
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

_builtin_print = print


def safe_print(*args, **kwargs):
    """Safely print Unicode text on standard consoles without crashes."""
    sep = kwargs.get("sep", " ")
    text = sep.join(str(arg) for arg in args)

    try:
        _builtin_print(text, **{k: v for k, v in kwargs.items() if k != "sep"})
    except UnicodeEncodeError:
        try:
            enc = sys.stdout.encoding or "cp1252"
            safe_text = text.encode(enc, errors="replace").decode(enc)
            _builtin_print(safe_text, **{k: v for k, v in kwargs.items() if k != "sep"})
        except Exception:
            ascii_text = "".join(c if ord(c) < 128 else "?" for c in text)
            _builtin_print(
                ascii_text, **{k: v for k, v in kwargs.items() if k != "sep"}
            )


# Overwrite default print function globally in this module
print = safe_print


# Define absolute paths for all sources
SOURCES = {
    "Synarche_Workspace": r"C:\Users\Chris\Synarche_Workspace",
    "dot_dev": r"C:\Users\Chris\.dev",
    "Ashen_Oath_RPG": r"C:\Users\Chris\Ashen Oath-3rd Person RPG",
    "Disengage_Entropy": r"C:\Users\Chris\Disengage Entropy",
    "Desktop_Vault_dev": r"C:\Users\Chris\_Desktop_Vault\dev",
}

# Freeplane backup zip directly copied
FREEPLANE_BACKUP = r"C:\Users\Chris\Freeplane_Consolidated_Backup.zip"

# Consolidation destination folder
DESTINATION_ROOT = r"C:\Users\Chris\Sovereign_Consolidated_Backup"
ZIP_DESTINATION = r"C:\Users\Chris\Sovereign_Consolidated_Backup.zip"

# Global Exclusions - directories to skip completely (checked by exact directory name)
BANNED_DIR_NAMES = {
    "node_modules",
    ".git",
    ".venv",
    ".godot",
    ".gradle",
    "build",
    "__pycache__",
    ".mypy_cache",
    ".idea",
    ".gemini",
    "obj",
    "bin",
    ".trunk",
}

# Custom exclusions mapping source keys to sub-paths to skip (relative to the source folder)
# All paths here are normalized to lower-case with forward slashes for cross-platform safety
CUSTOM_EXCLUSIONS = {
    "Synarche_Workspace": {
        ".archives/governance_legacy_archive.zip",
        "_governance/cdl/collaborative synthesis log archive.zip",
        "_governance/cdl/csl_archive_extracted",
    },
    "Desktop_Vault_dev": {"synarche_workspace"},  # 31 GB duplicate copy
    "dot_dev": {
        "old projects",  # 2.1 GB archived copy
        "new folder",  # 183 MB redundant files
    },
}


def get_dir_size(path):
    """Calculate total size of directory, ignoring errors."""
    total_size = 0
    try:
        for dirpath, _dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
    except Exception:
        pass
    return total_size


def format_size(size_bytes):
    """Convert bytes into human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def is_excluded(src_key, relative_path, is_dir=True):
    """Determine if a given relative path within a source should be excluded."""
    norm_rel = relative_path.replace("\\", "/").lower().strip("/")

    # Check custom exclusions
    if src_key in CUSTOM_EXCLUSIONS:
        for custom_ex in CUSTOM_EXCLUSIONS[src_key]:
            if norm_rel == custom_ex or norm_rel.startswith(custom_ex + "/"):
                return True

    # Check banned base directory names
    parts = norm_rel.split("/")
    for part in parts:
        if part in BANNED_DIR_NAMES:
            return True

    return False


def copy_clean_tree(src_key, src_dir, dest_dir):
    """Safely and recursively copy files, applying strict exclusion criteria."""
    copied_files = 0
    copied_bytes = 0
    skipped_files = 0
    skipped_dirs = 0

    if not os.path.exists(src_dir):
        print(f"⚠️ Source directory does not exist: {src_dir}")
        return 0, 0, 0, 0

    print(f"\n🚀 Scanning & Copying: {src_key} ({src_dir})")

    for dirpath, dirnames, filenames in os.walk(src_dir):
        # Calculate relative path from root
        rel_path = os.path.relpath(dirpath, src_dir)
        if rel_path == ".":
            rel_path = ""

        # Filter directories in-place to prevent os.walk from entering them
        i = len(dirnames) - 1
        while i >= 0:
            d_name = dirnames[i]
            d_rel = os.path.join(rel_path, d_name)
            if is_excluded(src_key, d_rel, is_dir=True):
                print(f"   🚫 Skipping directory: {d_rel}")
                skipped_dirs += 1
                dirnames.pop(i)
            i -= 1

        # Create target directory
        target_dir = os.path.join(dest_dir, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        # Copy files
        for filename in filenames:
            f_rel = os.path.join(rel_path, filename)
            if is_excluded(src_key, f_rel, is_dir=False):
                skipped_files += 1
                continue

            src_file = os.path.join(dirpath, filename)
            dest_file = os.path.join(target_dir, filename)

            try:
                # Copy file and metadata (permissions)
                shutil.copy2(src_file, dest_file)
                f_size = os.path.getsize(src_file)
                copied_bytes += f_size
                copied_files += 1

                # Visual micro-feedback for large files or periodically
                if copied_files % 1000 == 0:
                    print(
                        f"   ✔️ Copied {copied_files} files... ({format_size(copied_bytes)})"
                    )
            except Exception as e:
                print(f"   ❌ Error copying {src_file} -> {dest_file}: {e}")

    print(
        f"   ✅ Finished {src_key}: Copied {copied_files} files ({format_size(copied_bytes)}), Skipped {skipped_dirs} dirs, {skipped_files} files."
    )
    return copied_files, copied_bytes, skipped_dirs, skipped_files


def main():
    start_time = time.time()

    print("=" * 60)
    print("⚜️  SOVEREIGN SYSTEM CONSOLIDATION AND BACKUP ENGINE  ⚜️")
    print("=" * 60)

    # 1. Clean previous destination runs if any
    if os.path.exists(DESTINATION_ROOT):
        print(f"🧹 Cleaning previous backup folder: {DESTINATION_ROOT}")
        shutil.rmtree(DESTINATION_ROOT)

    os.makedirs(DESTINATION_ROOT, exist_ok=True)

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("  SOVEREIGN SYSTEM CONSOLIDATION BACKUP REPORT")
    report_lines.append(f"  Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 60 + "\n")

    total_files = 0
    total_bytes = 0
    total_skipped_dirs = 0
    total_skipped_files = 0

    # 2. Process all mapped sources
    for src_key, src_path in SOURCES.items():
        dest_path = os.path.join(DESTINATION_ROOT, src_key)

        raw_size = get_dir_size(src_path)
        print(f"\n📁 Audit: {src_key} Raw Size: {format_size(raw_size)}")

        copied_files, copied_bytes, skipped_dirs, skipped_files = copy_clean_tree(
            src_key, src_path, dest_path
        )

        total_files += copied_files
        total_bytes += copied_bytes
        total_skipped_dirs += skipped_dirs
        total_skipped_files += skipped_files

        report_lines.append(f"Source: {src_key}")
        report_lines.append(f"  Raw Footprint: {format_size(raw_size)}")
        report_lines.append(f"  Clean Copy Size: {format_size(copied_bytes)}")
        report_lines.append(f"  Files Copied: {copied_files}")
        report_lines.append(f"  Directories Skipped: {skipped_dirs}")
        report_lines.append(f"  Files Skipped: {skipped_files}")
        report_lines.append("-" * 40)

    # 3. Direct Copy of Freeplane Zip Archive
    if os.path.exists(FREEPLANE_BACKUP):
        print(f"\n📦 Copying Freeplane Archive: {FREEPLANE_BACKUP}")
        fp_dest = os.path.join(DESTINATION_ROOT, os.path.basename(FREEPLANE_BACKUP))
        shutil.copy2(FREEPLANE_BACKUP, fp_dest)
        fp_size = os.path.getsize(FREEPLANE_BACKUP)
        total_bytes += fp_size
        total_files += 1
        print(
            f"   ✅ Done: Copied {os.path.basename(FREEPLANE_BACKUP)} ({format_size(fp_size)})"
        )
        report_lines.append(f"Source: {os.path.basename(FREEPLANE_BACKUP)}")
        report_lines.append(f"  Direct Copy: {format_size(fp_size)}")
        report_lines.append("-" * 40)
    else:
        print(f"\n⚠️ Freeplane backup zip not found at: {FREEPLANE_BACKUP}")

    # 4. Generate report file in the consolidated root directory
    report_lines.append("\n" + "=" * 60)
    report_lines.append("  CONSOLIDATION SUMMARY METRICS")
    report_lines.append("=" * 60)
    report_lines.append(f"Total Unique Files Copied: {total_files}")
    report_lines.append(f"Total Clean Backup Size: {format_size(total_bytes)}")
    report_lines.append(
        f"Total Caches/Redundancies Skipped (Directories): {total_skipped_dirs}"
    )
    report_lines.append(
        f"Total Caches/Redundancies Skipped (Files): {total_skipped_files}"
    )

    # Write report file locally
    report_text = "\n".join(report_lines)
    report_path = os.path.join(DESTINATION_ROOT, "consolidation_report.txt")
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(report_text)

    print(f"\n📊 Summary report written to: {report_path}")

    # 5. Compress to final sovereign zip archive
    print(f"\n🤐 Creating compressed zip archive: {ZIP_DESTINATION}")

    # Remove old zip if exists
    if os.path.exists(ZIP_DESTINATION):
        os.remove(ZIP_DESTINATION)

    zip_start_time = time.time()

    with zipfile.ZipFile(ZIP_DESTINATION, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Walk consolidated folder and add to zip
        for root, _dirs, files in os.walk(DESTINATION_ROOT):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Skip symlinks if they are broken/unreadable
                    if os.path.islink(file_path):
                        continue
                    # Store with relative path inside the zip file
                    arcname = os.path.relpath(
                        file_path, os.path.dirname(DESTINATION_ROOT)
                    )
                    zipf.write(file_path, arcname)
                except (OSError, Exception) as e:
                    print(
                        f"   ⚠️ Skipping unreadable/locked file: {file_path} due to error: {e}"
                    )

    zip_end_time = time.time()
    zip_size = os.path.getsize(ZIP_DESTINATION)

    print(
        f"✅ Zip compilation finished in {zip_end_time - zip_start_time:.2f} seconds."
    )
    print(f"🎁 Consolidated Zip Size: {format_size(zip_size)}")
    print(f"🗜️  Compression ratio achieved: {total_bytes / zip_size:.2f}x compression!")

    # Update report with zip metrics
    with open(report_path, "a", encoding="utf-8") as rf:
        rf.write(f"\n🎁 Compressed Zip Path: {ZIP_DESTINATION}\n")
        rf.write(f"🎁 Compressed Zip Size: {format_size(zip_size)}\n")
        rf.write(f"⏱️ Total Execution Time: {time.time() - start_time:.2f} seconds\n")
        rf.write("=" * 60 + "\n")

    print("\n" + "=" * 60)
    print("✨ CONSOLIDATION SYSTEM COMPLETE! ZERO ENTROPY ACHIEVED. ✨")
    print("=" * 60)


if __name__ == "__main__":
    main()
