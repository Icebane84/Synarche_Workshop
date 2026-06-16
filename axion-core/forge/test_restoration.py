import os

from rnc_engine import RNCEngine


def test_engine():
    print("--- [RNC ENGINE VERIFICATION] ---")

    # 1. Test Validation
    test_id = "GVRN.AVATAR.Core-Alpha"
    is_valid = RNCEngine.validate_id(test_id)
    print(f"[ID VALIDATION] {test_id}: {'PASS' if is_valid else 'FAIL'}")

    invalid_id = "BAD_ID"
    is_valid_bad = RNCEngine.validate_id(invalid_id)
    print(f"[ID VALIDATION] {invalid_id}: {'PASS' if not is_valid_bad else 'FAIL'}")

    # 2. Test Path Suggestion
    try:
        path = RNCEngine.suggest_path(test_id)
        print(f"[PATH SUGGESTION] {test_id} -> {path}: PASS")
    except Exception as e:
        print(f"[PATH SUGGESTION] {test_id}: FAIL ({e})")

    # 3. Test Safe Transform (Dry Run)
    temp_file = "test_transform.txt"
    with open(temp_file, "w") as f:
        f.write("Original Content")

    def mock_transformer(content):
        return content.replace("Original", "Transformed")

    try:
        RNCEngine.safe_transform(temp_file, mock_transformer)
        with open(temp_file, "r") as f:
            new_content = f.read()
        print(
            f"[SAFE TRANSFORM] Result: {new_content}: {'PASS' if new_content == 'Transformed Content' else 'FAIL'}"
        )
    except Exception as e:
        print(f"[SAFE TRANSFORM]: FAIL ({e})")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    test_engine()
