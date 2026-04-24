import os
import re

def uncomment_logic(root_dir):
    # Regex to catch lines that were accidentally commented out
    # Matches lines starting with '# ' followed by common Python keywords or logic
    code_indicators = [
        r'^#\s*import\s+',
        r'^#\s*from\s+',
        r'^#\s*class\s+',
        r'^#\s*def\s+',
        r'^#\s*async\s+def\s+',
        r'^#\s*if\s+',
        r'^#\s*elif\s+',
        r'^#\s*else:',
        r'^#\s*try:',
        r'^#\s*except\s*',
        r'^#\s*finally:',
        r'^#\s*with\s+',
        r'^#\s*return\s+',
        r'^#\s*raise\s+',
        r'^#\s*@\w+',
        r'^#\s*\w+\s*=\s*',  # Assignments
        r'^#\s*logging\.',
        r'^#\s*logger\.',
        r'^#\s*\"\"\"',      # Triple quotes
        r'^#\s*\'\'\'',
    ]
    combined_regex = re.compile('|'.join(code_indicators))

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                changed = False
                new_lines = []
                
                for line in lines:
                    # Skip metadata block headers themselves if possible, but they are already commented usually
                    # Only uncomment if it matches a code indicator
                    if combined_regex.search(line):
                        # Remove the '# ' or '#' and any leading space after it once
                        uncommented = re.sub(r'^#\s*', '', line)
                        new_lines.append(uncommented)
                        changed = True
                    else:
                        new_lines.append(line)
                
                if changed:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Redeemed: {path}")

if __name__ == "__main__":
    uncomment_logic("c:/Users/Chris/Synarche_Workspace/axion-core/src")
