import sys
import os
import json
import re
import hashlib
from datetime import datetime, timezone

# Rule IV: Standardize console encoding for Windows stability
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load symbol whitelists dynamically from manifest files (Compiler's Oath)
def load_symbol_manifests(manifest_dir=None):
    if manifest_dir is None:
        manifest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "known_api_symbols")
    symbols = set()
    if os.path.exists(manifest_dir):
        for file in os.listdir(manifest_dir):
            if file.endswith(".json"):
                with open(os.path.join(manifest_dir, file), "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        symbols.update(data.get("allowed_symbols", []))
                    except Exception as e:
                        print(f"Warning: Failed to load manifest {file}: {e}", file=sys.stderr)
    return symbols

ALLOWED_UE_SYMBOLS = load_symbol_manifests()

def analyze_cpp_file(file_path):
    violations = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    
    # 1. Balanced Brackets Check
    braces_stack = []
    parens_stack = []
    for char_idx, char in enumerate(content):
        # Tracking lines for index
        if char == "{":
            braces_stack.append(char_idx)
        elif char == "}":
            if not braces_stack:
                violations.append({
                    "line": content[:char_idx].count("\n") + 1,
                    "rule": "SYNTAX_UNBALANCED_BRACES",
                    "message": "Unbalanced closing brace '}' found without opening brace."
                })
            else:
                braces_stack.pop()
        elif char == "(":
            parens_stack.append(char_idx)
        elif char == ")":
            if not parens_stack:
                violations.append({
                    "line": content[:char_idx].count("\n") + 1,
                    "rule": "SYNTAX_UNBALANCED_PARENS",
                    "message": "Unbalanced closing parenthesis ')' found without opening parenthesis."
                })
            else:
                parens_stack.pop()

    if braces_stack:
        violations.append({
            "line": content[:braces_stack[0]].count("\n") + 1,
            "rule": "SYNTAX_UNBALANCED_BRACES",
            "message": f"Unbalanced opening braces: {len(braces_stack)} braces remain unclosed."
        })
    if parens_stack:
        violations.append({
            "line": content[:parens_stack[0]].count("\n") + 1,
            "rule": "SYNTAX_UNBALANCED_PARENS",
            "message": f"Unbalanced opening parentheses: {len(parens_stack)} parentheses remain unclosed."
        })

    # Find the class name if declared (handle optional API macro)
    class_decl_match = re.search(r"\bclass\s+(?:[A-Za-z0-9_]+_API\s+)?([A-Za-z0-9_]+)\s*:\s*public\s+([A-Za-z0-9_]+)", content)
    class_name = class_decl_match.group(1) if class_decl_match else None
    
    # Dynamically whitelist the class name and its variant without prefix
    file_allowed_symbols = ALLOWED_UE_SYMBOLS.copy()
    if class_name:
        file_allowed_symbols.add(class_name)
        if class_name.startswith(("U", "A", "F", "T")):
            file_allowed_symbols.add(class_name[1:])
    
    # 2. Line-by-Line Checks
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("//") or stripped.startswith("/*"):
            continue

        # Pointer Safety: Raw delete prevention
        if re.search(r"\bdelete\s+[a-zA-Z_]", stripped):
            violations.append({
                "line": idx,
                "rule": "SAFETY_RAW_DELETE",
                "message": "Raw 'delete' operator is forbidden. Use TSharedPtr / TUniquePtr or engine garbage collection."
            })
        if re.search(r"\bnew\s+[A-Za-z0-9_]", stripped):
            violations.append({
                "line": idx,
                "rule": "SAFETY_RAW_NEW",
                "message": "Raw 'new' allocation is forbidden. Use CreateDefaultSubobject or MakeShared."
            })

        # Class Reflection Checks
        if stripped.startswith("class ") and ":" in stripped:
            # Check matching generated include on lines preceding or following
            filename_basename = os.path.basename(file_path).replace(".cpp", "").replace(".h", "")
            expected_gen_include = f'#include "{filename_basename}.generated.h"'
            
            class_basename = class_name
            if class_name and class_name.startswith(("U", "A", "F", "T")):
                class_basename = class_name[1:]
            expected_class_include = f'#include "{class_basename}.generated.h"' if class_basename else None
            
            has_correct_include = (expected_gen_include in content) or (expected_class_include and expected_class_include in content)
            if not has_correct_include:
                expected_desc = f"{expected_gen_include}"
                if expected_class_include:
                    expected_desc += f" or {expected_class_include}"
                violations.append({
                    "line": idx,
                    "rule": "REFLECTION_MISSING_GENERATED_INCLUDE",
                    "message": f"Missing generated include directive: expected {expected_desc}"
                })
            
            # Check GENERATED_BODY() exists in class declaration
            class_end_block = content[content.find(stripped):]
            if "GENERATED_BODY()" not in class_end_block.split("};")[0]:
                violations.append({
                    "line": idx,
                    "rule": "REFLECTION_MISSING_BODY_MACRO",
                    "message": "Class declaration is missing the GENERATED_BODY() macro."
                })

        # Pointer Safety: Raw pointer member tracking
        # Matches class members like 'UActorComponent* MyComp;' or 'AActor* Target;'
        pointer_decl_match = re.match(r"^([A-Za-z0-9_]+)\*\s+([A-Za-z0-9_]+)\s*;", stripped)
        if pointer_decl_match:
            ptr_type = pointer_decl_match.group(1)
            # Exclude standard types or if it is inside function (we only check class fields/members)
            # Typically class members are preceded by UPROPERTY() in the preceding lines
            # Let's check if the previous non-empty line has UPROPERTY
            prev_line_idx = idx - 2
            has_uproperty = False
            while prev_line_idx >= 0:
                prev_stripped = lines[prev_line_idx].strip()
                if prev_stripped.startswith("UPROPERTY"):
                    has_uproperty = True
                    break
                if prev_stripped and not prev_stripped.startswith("//"):
                    break
                prev_line_idx -= 1
            
            if not has_uproperty and (ptr_type.startswith("U") or ptr_type.startswith("A")):
                violations.append({
                    "line": idx,
                    "rule": "SAFETY_UNTRACKED_POINTER",
                    "message": f"Raw member pointer '{stripped}' of type '{ptr_type}' must be tracked by a UPROPERTY() macro to prevent garbage collection."
                })

        # Symbol Verification
        # Find all capitalized C++ symbols (e.g., words starting with U, A, F, T or macro names)
        potential_symbols = re.findall(r"\b([UATF][A-Z][a-zA-Z0-9_]+|[A-Z_]{4,})\b", stripped)
        for symbol in potential_symbols:
            if symbol == class_name:
                continue
            if symbol.endswith("_API"):
                continue
            # If symbol is not allowed
            if symbol not in file_allowed_symbols:
                # Basic wildcard check for custom class generated names
                if symbol.startswith("FID_") or symbol.endswith("_generated_h"):
                    continue
                violations.append({
                    "line": idx,
                    "rule": "SYMBOL_UNRECOGNIZED",
                    "message": f"Unrecognized engine or system symbol referenced: '{symbol}'"
                })

    return violations

def run_verifier(targets):
    all_violations = {}
    verified_files = []

    for target in targets:
        if os.path.isdir(target):
            # Recursively find .cpp and .h files
            for root, _, files in os.walk(target):
                for file in files:
                    if file.endswith((".cpp", ".h")):
                        file_path = os.path.join(root, file)
                        verified_files.append(os.path.abspath(file_path))
                        v = analyze_cpp_file(file_path)
                        if v:
                            all_violations[file_path] = v
        elif os.path.isfile(target):
            verified_files.append(os.path.abspath(target))
            v = analyze_cpp_file(target)
            if v:
                all_violations[target] = v

    exit_code = 1 if all_violations else 0

    # Calculate count of violations
    violation_count = sum(len(v) for v in all_violations.values())

    # Serialization of Earned Telemetry to Logs
    telemetry_data = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "verified_files": verified_files,
        "violations": all_violations,
        "exit_code": exit_code,
        "telemetry_metrics": {
            "files_scanned": {
                "value": len(verified_files),
                "provenance": "MEASURED"
            },
            "violation_count": {
                "value": violation_count,
                "provenance": "MEASURED"
            },
            "exit_code": {
                "value": exit_code,
                "provenance": "MEASURED"
            }
        }
    }

    log_dir = "c:\\Users\\Chris\\Synarche_Workspace\\_governance\\50_Logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "LOG.MECS.TELEMETRY_CPP.json")
    with open(log_path, "w", encoding="utf-8") as lf:
        json.dump(telemetry_data, lf, indent=2)

    # Waning Seal Ledger Update (Only for files with no violations)
    if exit_code == 0:
        ledger_path = os.path.join(log_dir, "LOG.MECS.LEDGER.json")
        ledger_data = {"records": []}
        if os.path.exists(ledger_path):
            try:
                with open(ledger_path, "r", encoding="utf-8") as lf:
                    ledger_data = json.load(lf)
            except Exception:
                ledger_data = {"records": []}
        if not isinstance(ledger_data, dict) or "records" not in ledger_data:
            ledger_data = {"records": []}
        ledger = ledger_data["records"]
            
        workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        for fpath in verified_files:
            if fpath in all_violations and all_violations[fpath]:
                continue
            
            rel_path = os.path.relpath(fpath, workspace_root).replace("\\", "/")
            
            h = hashlib.sha256()
            try:
                with open(fpath, "rb") as f:
                    while True:
                        chunk = f.read(65536)
                        if not chunk:
                            break
                        h.update(chunk)
                file_hash = h.hexdigest()
            except Exception:
                continue
                
            entry_found = False
            for entry in ledger:
                if entry.get("artifact_path") == rel_path:
                    entry["content_sha256"] = file_hash
                    entry["verified_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                    entry_found = True
                    break
            if not entry_found:
                ledger.append({
                    "artifact_path": rel_path,
                    "content_sha256": file_hash,
                    "verified_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                })
        try:
            with open(ledger_path, "w", encoding="utf-8") as lf:
                json.dump({"records": ledger}, lf, indent=2)
        except Exception as e:
            print(f"Warning: Failed to update ledger: {e}", file=sys.stderr)

    # Console Output
    print(f"\n--- [C++ OOB VERIFIER] EXECUTION COMPLETE ---")
    print(f"Verified files: {len(verified_files)}")
    if all_violations:
        print(f"STATUS: FAILED (Exit Code: {exit_code})", file=sys.stderr)
        for file, violations in all_violations.items():
            print(f"\nFile: {file}", file=sys.stderr)
            for v in violations:
                print(f"  Line {v['line']}: [{v['rule']}] {v['message']}", file=sys.stderr)
    else:
        print(f"STATUS: SUCCESS (Exit Code: {exit_code})")
        print("No structural or safety violations detected.")
    
    return exit_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cpp_verifier.py <file_or_directory_paths...>")
        sys.exit(2)
    sys.exit(run_verifier(sys.argv[1:]))
