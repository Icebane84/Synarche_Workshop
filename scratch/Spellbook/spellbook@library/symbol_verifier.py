#!/usr/bin/env python3
"""
symbol_verifier.py — API surface gate.

This exists because Gates 1 and 2 (structural/macro audit) are blind to a
whole class of real bug: a method call that is syntactically perfect, uses
correctly-typed pointers, and compiles as valid C++ grammar, but calls a
method that doesn't exist on the target class. That's exactly what happened
with `UFieldSystemComponent::ApplyStrainField(...)` in the Ashen Oath boss
orchestrator draft — real class, plausible name, not a real member function.

This script cross-references `Object->Method(` call sites in a .cpp against
a manifest of confirmed-real / confirmed-hallucinated symbols per class. It
tracks which manifest class each variable belongs to by reading declarations
from the paired .h file, so `FieldSystemComponent->Foo()` resolves to
`UFieldSystemComponent`'s manifest entry via the member declaration
`TObjectPtr<UFieldSystemComponent> FieldSystemComponent;`.

Three outcomes per call site:
  PASS      - method is in known_methods
  CRITICAL  - method is in known_hallucinated (previously confirmed fake)
  UNVERIFIED - method is in neither list; not failed, but not passed either

Exit codes: 0 = no CRITICAL findings, 1 = at least one CRITICAL finding.
UNVERIFIED findings alone do not fail the gate but are always reported —
this gate refuses to silently upgrade "unknown" to "pass".
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

MEMBER_DECL_RE = re.compile(
    r'(?:TObjectPtr<\s*([A-Za-z0-9_]+)\s*>|([A-Za-z0-9_]+)\s*\*)\s*([A-Za-z_][A-Za-z0-9_]*)\s*;'
)
LOCAL_DECL_RE = re.compile(
    r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\*\s*([A-Za-z_][A-Za-z0-9_]*)\s*='
)
CALL_RE = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*->\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(')


@dataclass
class Finding:
    status: str  # PASS | CRITICAL | UNVERIFIED
    line: int
    variable: str
    class_name: str
    method: str
    message: str


def build_variable_class_map(header_text: str, source_text: str) -> dict[str, str]:
    var_class: dict[str, str] = {}
    for text in (header_text, source_text):
        for m in MEMBER_DECL_RE.finditer(text):
            cls = m.group(1) or m.group(2)
            var = m.group(3)
            var_class[var] = cls
        for m in LOCAL_DECL_RE.finditer(text):
            var_class[m.group(2)] = m.group(1)
    return var_class


def verify(header_path: Path, source_path: Path, manifest: dict) -> list[Finding]:
    header_text = header_path.read_text(encoding="utf-8", errors="replace") if header_path else ""
    source_text = source_path.read_text(encoding="utf-8", errors="replace") if source_path else ""
    var_class = build_variable_class_map(header_text, source_text)

    findings: list[Finding] = []
    lines = source_text.splitlines()
    for i, line in enumerate(lines, 1):
        for m in CALL_RE.finditer(line):
            var, method = m.group(1), m.group(2)
            cls = var_class.get(var)
            if not cls or cls not in manifest:
                continue  # not a class we have a manifest entry for; skip silently
            entry = manifest[cls]
            if method in entry.get("known_hallucinated", []):
                findings.append(Finding("CRITICAL", i, var, cls, method,
                    f"{cls}::{method} is a CONFIRMED non-existent method (previously fabricated). "
                    f"This will fail to compile."))
            elif method in entry.get("known_methods", []):
                note = entry.get("note")
                if note:
                    findings.append(Finding("UNVERIFIED", i, var, cls, method,
                        f"{cls}::{method} is real but flagged: {note}"))
                else:
                    findings.append(Finding("PASS", i, var, cls, method,
                        f"{cls}::{method} confirmed against manifest."))
            else:
                findings.append(Finding("UNVERIFIED", i, var, cls, method,
                    f"{cls}::{method} is not in the manifest as either real or fake. "
                    f"Verify against engine headers before trusting this call site."))
    return findings


def main():
    parser = argparse.ArgumentParser(description="API surface gate: catch hallucinated engine calls")
    parser.add_argument("--header", type=Path, default=None)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).parent / "known_api_symbols.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.source.exists():
        print(f"ERROR: source not found: {args.source}", file=sys.stderr)
        sys.exit(2)
    if not args.manifest.exists():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(2)

    manifest = json.loads(args.manifest.read_text())
    findings = verify(args.header, args.source, manifest)
    critical = [f for f in findings if f.status == "CRITICAL"]

    if args.json:
        print(json.dumps({
            "source": str(args.source),
            "critical_count": len(critical),
            "unverified_count": len([f for f in findings if f.status == "UNVERIFIED"]),
            "pass_count": len([f for f in findings if f.status == "PASS"]),
            "findings": [asdict(f) for f in findings],
        }, indent=2))
    else:
        if not findings:
            print("SYMBOL_VERIFIER: no manifest-tracked class calls found.")
        for f in findings:
            print(f"[{f.status}] line {f.line}: {f.class_name}::{f.method} ({f.variable}) — {f.message}")

    sys.exit(1 if critical else 0)


if __name__ == "__main__":
    main()
