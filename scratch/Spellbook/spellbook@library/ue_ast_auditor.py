#!/usr/bin/env python3
"""
ue_ast_auditor.py — Gate 1 of the MECS pipeline.
Line-aware structural auditor for Unreal C++ headers (GC hazards, missing
GENERATED_BODY, missing/misplaced .generated.h include, naming conventions).
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

UOBJECT_PREFIXES = ("A", "U", "I")
STRUCT_PREFIX = "F"

CLASS_DECL_RE = re.compile(r'^\s*class\s+[A-Z_][A-Z0-9_]*_API\s+([AUF][A-Za-z0-9_]*)\s*:\s*public\s+')
GENERIC_CLASS_DECL_RE = re.compile(r'^\s*class\s+([AUF][A-Za-z0-9_]*)\s*(:|{)')
POINTER_DECL_RE = re.compile(
    r'^\s*(?:const\s+)?([AUI][A-Z][A-Za-z0-9_]*)\s*\*\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:=\s*nullptr)?\s*;'
)
UPROPERTY_RE = re.compile(r'UPROPERTY\s*\(')
GENERATED_BODY_RE = re.compile(r'GENERATED_BODY\s*\(\s*\)')
GENERATED_INCLUDE_RE = re.compile(r'#include\s+"([^"]+)\.generated\.h"')


@dataclass
class Violation:
    severity: str
    rule: str
    line: int
    message: str


def audit_header(path: Path) -> list[Violation]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    violations: list[Violation] = []

    gen_match = GENERATED_INCLUDE_RE.search(text)
    if not gen_match:
        violations.append(Violation("CRITICAL", "MISSING_GENERATED_INCLUDE", 0,
            f"No #include \"{path.stem}.generated.h\" found."))
    else:
        include_lines = [i for i, l in enumerate(lines, 1) if l.strip().startswith("#include")]
        last_include_line = max(include_lines) if include_lines else -1
        gen_line = text[:gen_match.start()].count("\n") + 1
        if gen_line != last_include_line:
            violations.append(Violation("ERROR", "GENERATED_INCLUDE_NOT_LAST", gen_line,
                f"{path.stem}.generated.h include exists but is not the final #include."))

    prev_nonblank = ""
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        m = POINTER_DECL_RE.match(line)
        if m:
            ptr_class, ptr_name = m.group(1), m.group(2)
            if not UPROPERTY_RE.search(prev_nonblank):
                violations.append(Violation("CRITICAL", "GC_HAZARD", i,
                    f"Raw pointer '{ptr_class}* {ptr_name}' has no preceding UPROPERTY()."))
        prev_nonblank = stripped

    class_starts = []
    for i, line in enumerate(lines, 1):
        m = CLASS_DECL_RE.match(line) or GENERIC_CLASS_DECL_RE.match(line)
        if m:
            class_starts.append((i, m.group(1)))

    for start_line, class_name in class_starts:
        depth = 0
        started = False
        body_lines = []
        for i in range(start_line - 1, len(lines)):
            l = lines[i]
            depth += l.count("{") - l.count("}")
            if "{" in l:
                started = True
            if started:
                body_lines.append(l)
            if started and depth <= 0:
                break
        body_text = "\n".join(body_lines)
        if class_name[0] in UOBJECT_PREFIXES and not GENERATED_BODY_RE.search(body_text):
            violations.append(Violation("ERROR", "MISSING_GENERATED_BODY", start_line,
                f"Class '{class_name}' derives from a reflected UE type but has no GENERATED_BODY()."))

    for start_line, class_name in class_starts:
        prefix = class_name[0]
        if prefix not in (*UOBJECT_PREFIXES, STRUCT_PREFIX):
            violations.append(Violation("WARNING", "NAMING_CONVENTION", start_line,
                f"Class '{class_name}' does not use a standard UE prefix (A/U/I/F)."))

    return violations


def main():
    parser = argparse.ArgumentParser(description="Gate 1: UE header structural auditor")
    parser.add_argument("header_path", type=Path)
    parser.add_argument("source_path", type=Path, nargs="?", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.header_path.exists():
        print(f"ERROR: header not found: {args.header_path}", file=sys.stderr)
        sys.exit(2)

    violations = audit_header(args.header_path)

    if args.json:
        print(json.dumps({
            "file": str(args.header_path),
            "violation_count": len(violations),
            "violations": [asdict(v) for v in violations],
        }, indent=2))
    else:
        if not violations:
            print("AST_VALIDATION_PASSED: Structural integrity verified.")
        else:
            for v in violations:
                print(f"[{v.severity}] {v.rule} (line {v.line}): {v.message}")

    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
