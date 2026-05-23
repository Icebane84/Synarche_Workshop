import os


def sanitize_stubs(root_dir):
    for root, _dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8") as f:
                    content = f.read()

                # Remove the garbage markers
                new_content = content.replace('""" (Fixing unterminated string)', "")
                # Also ensure the metadata block is closed correctly if I broke it

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Sanitized: {path}")


if __name__ == "__main__":
    sanitize_stubs("c:/Users/Chris/Synarche_Workspace/axion-core/src")
