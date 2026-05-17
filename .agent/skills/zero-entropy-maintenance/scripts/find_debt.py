import os
import re

def find_debt_files(directory):
    debt_files = []
    METADATA_PREFIXES = ("# |", "# ---", "# [", "# ##", "// |", "// ---", "// [", "// ##")
    
    for root, _, files in os.walk(directory):
        if any(x in root for x in ["node_modules", ".git", ".venv", "__pycache__", "out", "out_debug"]):
            continue
        for f in files:
            if f.endswith((".py", ".ts", ".tsx", ".js", ".md")):
                path = os.path.join(root, f)
                try:
                    with open(path, encoding="utf-8") as file:
                        content = file.read()
                        lines = content.splitlines()
                except:
                    continue
                
                file_todos = sum(1 for l in lines if "TODO" in l.upper())
                file_fixmes = sum(1 for l in lines if "FIXME" in l.upper())
                
                if f.endswith((".py", ".ts", ".tsx", ".js")):
                    content_no_strings = re.sub(r'"""[\s\S]*?"""', '', content)
                    content_no_strings = re.sub(r"'''[\s\S]*?'''", '', content_no_strings)
                    if f.endswith((".js", ".ts", ".tsx")):
                        content_no_strings = re.sub(r'`[\s\S]*?`', '', content_no_strings)
                    lines_to_check = content_no_strings.splitlines()
                else:
                    lines_to_check = lines

                file_shadow = 0
                consecutive = 0
                for line in lines_to_check:
                    stripped = line.strip()
                    is_comment = stripped.startswith("#") or stripped.startswith("//")
                    is_metadata = any(stripped.startswith(p) for p in METADATA_PREFIXES)
                    
                    if is_comment and not is_metadata:
                        consecutive += 1
                    else:
                        if consecutive >= 3:
                            file_shadow += consecutive
                        consecutive = 0
                if consecutive >= 3:
                    file_shadow += consecutive
                
                if file_todos > 0 or file_fixmes > 0 or file_shadow > 0:
                    debt_files.append((path, file_todos, file_fixmes, file_shadow))
    
    debt_files.sort(key=lambda x: (x[3]*2 + x[1]*5 + x[2]*15), reverse=True)
    
    print(f"{'File Path':<100} | TODO | FIXME | SHADOW | TDM")
    print("-" * 140)
    for path, todos, fixmes, shadow in debt_files[:30]:
        rel_path = os.path.relpath(path, directory)
        tdm = (todos * 5) + (fixmes * 15) + (shadow * 2)
        print(f"{rel_path:<100} | {todos:<4} | {fixmes:<5} | {shadow:<6} | {tdm}")

if __name__ == "__main__":
    find_debt_files(r"c:\Users\Chris\Synarche_Workspace\axion-core")
