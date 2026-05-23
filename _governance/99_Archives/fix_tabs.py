
import os
import re

target_dir = r'c:\Users\Chris\_Desktop_Vault\Phoenix\Documentation\Library\2_Protocols'
registry_file = r'c:\Users\Chris\_Desktop_Vault\Phoenix\Documentation\Library\0_Registries\UMB-OSLM-001_MasterArtifactRegistry_v11.0.md'

renamed_files = {}

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    name = name.replace(' ', '')
    return name

def fix_file(filename):
    filepath = os.path.join(target_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find the ID and Title
    # Looking for 'Forged Artifact: ID: Title' or similar
    # In the viewed file: "### **Forged Artifact: AOP-VIS-ICOM-001: The Gravitational Lensing Protocol**"
    
    title_match = re.search(r'Forged Artifact: (.*?): (.*?)(\*\*|\n)', content)
    real_title = None
    module_id = None

    if title_match:
        module_id = title_match.group(1).strip()
        real_title = title_match.group(2).strip()
    else:
        # Try looking for "Official Name" in the table
        # | **2. Official Name** | `AOP-VIS-ICOM-001.md` | -> not helpful for title
        # Try finding the H1 replacement from the text?
        # Maybe search for "Title: " lines?
        pass

    if not real_title and 'Tab' in filename:
        # Fallback: extraction from filename AOP-XXX-XXX_Tab...
        parts = filename.split('_')
        if len(parts) > 0:
            module_id = parts[0]
            # Verify if there's a title in the content near "Forged Artifact"
            # Some might match: "- **Title:** The Unseen Gravity" (Line 49)
            sub_title_match = re.search(r'\- \*\*Title:\*\* (.*)', content)
            if sub_title_match:
                real_title = sub_title_match.group(1).strip()

    if real_title and module_id:
        # Construct new filename
        # Format: ID_TitleCamelCase_v11.0.md
        safe_title = sanitize_filename(real_title)
        new_filename = f"{module_id}_{safe_title}_v11.0.md"
        
        # Rename file
        new_filepath = os.path.join(target_dir, new_filename)
        
        # Update H1 in content
        # Check for "# **Tab X**"
        new_content = re.sub(r'# \*\*Tab \d+\*\*', f'# {module_id}: {real_title}', content)
        new_content = re.sub(r'# Tab \d+', f'# {module_id}: {real_title}', new_content)

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        # Rename
        if filename != new_filename:
            try:
                os.rename(filepath, new_filepath)
                renamed_files[filename] = new_filename
                print(f"Renamed: {filename} -> {new_filename}")
            except OSError as e:
                print(f"Error renaming {filename}: {e}")
        else:
             print(f"File {filename} content updated but name is same (unexpected).")
    else:
        print(f"Could not determine title for {filename}")

files = os.listdir(target_dir)
for f in files:
    if '_Tab' in f and f.endswith('.md'):
        fix_file(f)
