import os
import re

def uncomment_logic(root_dir):
    # Expanded list of code indicators
    code_indicators = [
        r'^#\s*import\s+',
        r'^#\s*from\s+',
        r'^#\s*class\s+',
        r'^#\s*def\s+',
        r'^#\s*async\s+',
        r'^#\s*if\s+',
        r'^#\s*elif\s+',
        r'^#\s*else\b',
        r'^#\s*try\b',
        r'^#\s*except\b',
        r'^#\s*finally\b',
        r'^#\s*with\s+',
        r'^#\s*return\b',
        r'^#\s*raise\b',
        r'^#\s*for\s+',
        r'^#\s*while\s+',
        r'^#\s*pass\b',
        r'^#\s*break\b',
        r'^#\s*continue\b',
        r'^#\s*yield\b',
        r'^#\s*global\b',
        r'^#\s*nonlocal\b',
        r'^#\s*@\w+',
        r'^#\s*self\.',
        r'^#\s*log\.',
        r'^#\s*logger\.',
        r'^#\s*logging\.',
        r'^#\s*\"\"\"',
        r'^#\s*\'\'\'',
        r'^#\s*#', # Double hash comments that might be code
        r'^#\s*\[', # List/Index
        r'^#\s*\{', # Dict/Set
        r'^#\s*\w+\s*\(', # Function calls
        r'^#\s*\w+\s*=\s*', # Assignments
        r'^#\s*[\w\.]+\s*[=+\-*/%]=', # AugAssignments
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
                    # Match: ^(\s*)#\s?(.*)
                    match = re.match(r'^(\s*)#\s?(.*)', line)
                    if match:
                        indent = match.group(1)
                        content = match.group(2)
                        
                        # Special check: Don't uncomment metadata blocks
                        if any(marker in line for marker in ["|", "[ARTIFACT", "Block ", "Official Name", "Version", "Artifact ID"]):
                            new_lines.append(line)
                            continue

                        # Check if the line looks like it WAS code
                        # We use f"# {content}" to test against the indicators which expect a leading #
                        if combined_regex.search(f"# {content}"):
                            new_lines.append(f"{indent}{content}\n")
                            changed = True
                            continue
                    
                    new_lines.append(line)
                
                if changed:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Redeemed v3: {path}")

if __name__ == "__main__":
    uncomment_logic("c:/Users/Chris/Synarche_Workspace/axion-core/src")
