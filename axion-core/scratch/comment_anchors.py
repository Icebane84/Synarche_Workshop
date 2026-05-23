import os


def recommend_anchors(root_dir):
    for root, _dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8") as f:
                    lines = f.readlines()

                changed = False
                new_lines = []
                inside_triple_quotes = False

                for line in lines:
                    stripped = line.strip()

                    # Track triple quotes to avoid commenting things inside them
                    if '"""' in line:
                        # Count number of triple quotes to handle single-line triple quotes
                        count = line.count('"""')
                        if count % 2 != 0:
                            inside_triple_quotes = not inside_triple_quotes

                    if not inside_triple_quotes:
                        # If the line starts with [ or ## and isn't already commented
                        if (
                            stripped.startswith("[") or stripped.startswith("##")
                        ) and not stripped.startswith("#"):
                            new_lines.append(f"# {line}")
                            changed = True
                            continue

                    new_lines.append(line)

                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"Commented Anchors: {path}")


if __name__ == "__main__":
    recommend_anchors("c:/Users/Chris/Synarche_Workspace/axion-core/src")
