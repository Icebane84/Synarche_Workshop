import os
import sys
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

BACKUP_ROOT = r"C:\Users\Chris\Sovereign_Consolidated_Backup"
ZIP_PATH = r"C:\Users\Chris\Sovereign_Consolidated_Backup.zip"

EXPECTED_SUBFOLDERS = [
    "Synarche_Workspace",
    "dot_dev",
    "Ashen_Oath_RPG",
    "Disengage_Entropy",
    "Desktop_Vault_dev",
]

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
}


def format_size(size_bytes):
    """Convert bytes into human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def run_verification():
    print("=" * 60)
    print("🔬 SOVEREIGN BACKUP VERIFICATION & AUDIT SYSTEM 🔬")
    print("=" * 60)

    errors = []
    warnings = []

    # 1. Check backup root folder existence
    if not os.path.exists(BACKUP_ROOT):
        errors.append(
            f"CRITICAL: Consolidated backup root folder does not exist: {BACKUP_ROOT}"
        )
        print("[FAIL] Backup root directory not found.")
        return False
    else:
        print(f"[PASS] Consolidated backup root directory exists: {BACKUP_ROOT}")

    # 2. Check each expected source folder
    for folder in EXPECTED_SUBFOLDERS:
        f_path = os.path.join(BACKUP_ROOT, folder)
        if not os.path.exists(f_path):
            errors.append(f"CRITICAL: Missing consolidated subfolder: {folder}")
            print(f"[FAIL] Subfolder missing: {folder}")
        else:
            # Count files and get size
            f_count = 0
            f_size = 0
            for r, d, files in os.walk(f_path):
                f_count += len(files)
                for f in files:
                    try:
                        f_size += os.path.getsize(os.path.join(r, f))
                    except Exception:
                        pass
            print(
                f"[PASS] Subfolder verified: {folder:<20} | Files: {f_count:<6} | Size: {format_size(f_size)}"
            )

    # 3. Check Freeplane Archive
    fp_path = os.path.join(BACKUP_ROOT, "Freeplane_Consolidated_Backup.zip")
    if os.path.exists(fp_path):
        fp_size = os.path.getsize(fp_path)
        print(
            f"[PASS] Freeplane Archive present: {os.path.basename(fp_path)} | Size: {format_size(fp_size)}"
        )
    else:
        warnings.append(
            "WARNING: Freeplane backup zip not found (expected if user skipped it)."
        )
        print("[WARN] Freeplane backup zip not found.")

    # 4. Strict Redundancy Check (Search for banned folders)
    print(
        "\nChecking for zero-redundancy compliance (scanning for banned caches/history)..."
    )
    banned_found = []
    for r, d, files in os.walk(BACKUP_ROOT):
        # Normalize folder check
        for dir_name in d:
            if dir_name.lower() in BANNED_DIR_NAMES:
                full_banned_path = os.path.join(r, dir_name)
                banned_found.append(full_banned_path)

    if banned_found:
        errors.append(
            f"CRITICAL: Found banned directories in consolidated backup: {banned_found[:5]}..."
        )
        print(
            f"[FAIL] Redundancy check failed. Found {len(banned_found)} banned items in backup!"
        )
        for item in banned_found[:10]:
            print(f"  -> Banned: {item}")
    else:
        print(
            "[PASS] Zero-redundancy compliance verified! 0% banned folders (.git, node_modules, etc.) present."
        )

    # 5. Config Preservation Check (Confirm existence of .env, code-workspace files, etc.)
    print("\nVerifying presence of critical configuration files...")
    configs_checked = [
        ("Synarche_Workspace/.code-workspace", True),
        ("Synarche_Workspace/package.json", False),
        ("Ashen_Oath_RPG/project.godot", False),
        ("Disengage_Entropy/package.json", False),
    ]
    for rel_conf_path, is_critical in configs_checked:
        c_path = os.path.join(BACKUP_ROOT, rel_conf_path)
        if os.path.exists(c_path):
            print(f"[PASS] Configuration file preserved: {rel_conf_path}")
        else:
            msg = f"Missing configuration file: {rel_conf_path}"
            if is_critical:
                errors.append(f"CRITICAL: {msg}")
                print(f"[FAIL] Critical configuration missing: {rel_conf_path}")
            else:
                warnings.append(f"WARNING: {msg}")
                print(f"[WARN] Optional configuration missing: {rel_conf_path}")

    # 6. Check consolidated report file
    rep_path = os.path.join(BACKUP_ROOT, "consolidation_report.txt")
    if os.path.exists(rep_path):
        print(f"[PASS] Consolidation report is present: {rep_path}")
    else:
        errors.append("CRITICAL: Consolidation summary report missing.")
        print("[FAIL] Consolidation report missing.")

    # 7. Check final compressed Zip file existence and integrity
    print("\nVerifying final consolidated ZIP archive...")
    if not os.path.exists(ZIP_PATH):
        errors.append(f"CRITICAL: Compressed ZIP file not found at: {ZIP_PATH}")
        print("[FAIL] Compressed ZIP file not found.")
    else:
        zip_size = os.path.getsize(ZIP_PATH)
        if zip_size == 0:
            errors.append(f"CRITICAL: Compressed ZIP file is empty: {ZIP_PATH}")
            print("[FAIL] Compressed ZIP file is empty.")
        else:
            print(
                f"[PASS] Compressed ZIP file exists: {ZIP_PATH} | Size: {format_size(zip_size)}"
            )
            # Try loading zip metadata to verify it isn't corrupted
            try:
                with zipfile.ZipFile(ZIP_PATH, "r") as zf:
                    bad_file = zf.testzip()
                    if bad_file:
                        errors.append(
                            f"CRITICAL: Corrupted file inside ZIP archive: {bad_file}"
                        )
                        print(
                            f"[FAIL] ZIP verification failed. Bad file detected: {bad_file}"
                        )
                    else:
                        print("[PASS] ZIP structural integrity verified (no errors).")
            except Exception as e:
                errors.append(f"CRITICAL: Failed to read ZIP file: {e}")
                print(f"[FAIL] ZIP structure is invalid/corrupt: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total Errors Found: {len(errors)}")
    print(f"Total Warnings Found: {len(warnings)}")

    if errors:
        print("\n❌ VERIFICATION FAILED! Critical discrepancies were found:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(
            "\n✨ VERIFICATION SUCCESSFUL! THE BACKUP IS STABLE AND PERFECTLY CONSOLIDATED! ✨"
        )
        if warnings:
            print("Non-critical warnings to keep in mind:")
            for warn in warnings:
                print(f"  - {warn}")
        return True


if __name__ == "__main__":
    run_verification()
