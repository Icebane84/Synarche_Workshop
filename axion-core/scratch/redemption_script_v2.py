import os
import re


def uncomment_logic(root_dir):
    code_indicators = [
        r"^#\s*import\s+",
        r"^#\s*from\s+",
        r"^#\s*class\s+",
        r"^#\s*def\s+",
        r"^#\s*async\s+def\s+",
        r"^#\s*if\s+",
        r"^#\s*elif\s+",
        r"^#\s*else:",
        r"^#\s*try:",
        r"^#\s*except\s*",
        r"^#\s*finally:",
        r"^#\s*with\s+",
        r"^#\s*return\s+",
        r"^#\s*raise\s+",
        r"^#\s*@\w+",
        r"^#\s*\w+\s*=\s*",
        r"^#\s*logging\.",
        r"^#\s*logger\.",
        r"^#\s*\"\"\"",
        r"^#\s*\'\'\'",
    ]
    combined_regex = re.compile("|".join(code_indicators))

    for root, _dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                changed = False
                new_lines = []

                for line in lines:
                    # Look for lines that start with some whitespace, then a #, then optional space, then code
                    # Match: ^(\s*)#\s?(.*code_regex.*)
                    match = re.match(r"^(\s*)#\s?(.*)", line)
                    if match:
                        indent = match.group(1)
                        content = match.group(2)

                        # Check if the content (ignoring its own leading space) looks like code
                        if combined_regex.search(f"# {content}"):
                            new_lines.append(f"{indent}{content}\n")
                            changed = True
                            continue

                    new_lines.append(line)

                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"Redeemed with Indent: {path}")


if __name__ == "__main__":
    uncomment_logic("c:/Users/Chris/Synarche_Workspace/axion-core/src")
