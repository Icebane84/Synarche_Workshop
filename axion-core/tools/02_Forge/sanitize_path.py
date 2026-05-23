import os
import winreg


def get_registry_user_path():
    r"""Gets the raw User PATH string directly from HKCU\\Environment registry key."""
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ
        ) as key:
            value, _ = winreg.QueryValueEx(key, "Path")
            return value
    except FileNotFoundError:
        return ""


def set_registry_user_path(new_path):
    r"""Sets the User PATH string directly in HKCU\\Environment registry key."""
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)


def main():
    raw_path = get_registry_user_path()
    print("--- RAW USER PATH FROM REGISTRY ---")
    print(raw_path)

    seen = set()
    cleaned = []

    # Process paths
    for part in raw_path.split(";"):
        # Remove quotes and whitespace
        clean_part = part.replace('"', "").strip()
        if not clean_part:
            continue

        # If it accidentally points to an executable, clean to the parent directory
        if clean_part.lower().endswith(".exe"):
            clean_part = os.path.dirname(clean_part)

        if clean_part not in seen:
            seen.add(clean_part)
            cleaned.append(clean_part)

    sanitized_path = ";".join(cleaned)
    print("\n--- SANITIZED PATHS ---")
    for p in cleaned:
        print(f"  {p}")

    print("\n--- PROPOSED NEW USER PATH STRING ---")
    print(sanitized_path)

    # Let's save the sanitized path to registry
    set_registry_user_path(sanitized_path)
    print(
        "\nSuccessfully updated User PATH in registry! (No double quotes or file pointers)"
    )


if __name__ == "__main__":
    main()
