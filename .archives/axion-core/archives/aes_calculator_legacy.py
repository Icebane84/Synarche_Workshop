"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-AES-CALCULATOR-001`                | The Sovereign ID. |
| **Official Name** | `aes_calculator.py`                   | The Filename.     |
| **Version**       | **v14.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import argparse
import ast
import math
import os
import sys
from typing import Any

# Ensure src in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    AxionCognition = None


class MetricsVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.complexity = 0
        self.functions = 0
        self.typed_args = 0
        self.total_args = 0
        self.typed_returns = 0
        self.total_returns = 0
        self.has_jsdoc = 0
        self.total_documented = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.functions += 1
        self.complexity += 1

        self.total_returns += 1
        if node.returns is not None:
            self.typed_returns += 1

        for arg in node.args.args:
            if arg.arg in ("self", "cls"):
                continue
            self.total_args += 1
            if arg.annotation is not None:
                self.typed_args += 1

        # Compliance Check: Documentation (JSDoc-style or Docstrings)
        docstring = ast.get_docstring(node)
        if docstring:
            self.has_jsdoc += 1
        self.total_documented += 1

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)  # type: ignore

    def _inc_complexity(self, node: ast.AST) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self._inc_complexity(node)

    def visit_For(self, node: ast.For) -> None:
        self._inc_complexity(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._inc_complexity(node)

    def visit_While(self, node: ast.While) -> None:
        self._inc_complexity(node)

    def visit_Try(self, node: ast.Try) -> None:
        self.complexity += len(node.handlers)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += len(node.values) - 1
        self.generic_visit(node)


def calculate_halstead_volume(content: str) -> float:
    words = content.split()
    n_words = len(words)
    if n_words == 0:
        return 0.0
    n_unique = len(set(words))
    if n_unique == 0:
        return 0.0
    return n_words * math.log2(n_unique)


def calculate_maintainability_index(volume: float, cc: int, loc: int) -> float:
    if volume <= 0:
        return 100.0
    mi = 171 - 5.2 * math.log(volume) - 0.23 * cc - 16.2 * math.log(max(1, loc))
    mi_percentage = max(0.0, (mi * 100) / 171.0)
    return min(100.0, mi_percentage)


def analyze_file(filepath: str, cognition: AxionCognition = None) -> dict[str, Any]:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    lines = [
        line
        for line in content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    loc = len(lines)

    visitor = MetricsVisitor()
    try:
        tree = ast.parse(content)
        visitor.visit(tree)
    except Exception:
        return {"error": "SyntaxError", "score": 0.0}

    # Standard AES Metrics
    total_types_needed = visitor.total_args + visitor.total_returns
    total_types_found = visitor.typed_args + visitor.typed_returns
    type_coverage = (
        total_types_found / total_types_needed if total_types_needed > 0 else 1.0
    )

    avg_complexity = visitor.complexity / max(1, visitor.functions)
    loc / max(1, visitor.functions)
    volume = calculate_halstead_volume(content)
    mi = calculate_maintainability_index(volume, visitor.complexity, loc)

    # Synarche Compliance Score (v14.0 Expansion)
    header_check = 20.0 if "Artifact ID" in content and "Version" in content else 0.0
    doc_coverage = (visitor.has_jsdoc / max(1, visitor.total_documented)) * 30.0
    compliance_score = header_check + doc_coverage + (type_coverage * 50.0)

    # Resonance Scoring (Cognitive Integration)
    resonance = 1.0
    if cognition:
        analysis = cognition.process(content[:2000])
        resonance = analysis.get("magician_efficiency", 1.0)

    base = 100.0
    complexity_drag = max(0.0, (avg_complexity - 2.0) * 5.0)
    type_drag = (1.0 - type_coverage) * 30.0

    aes_raw = (base - complexity_drag - type_drag) * (compliance_score / 100.0)
    aes = max(0.0, min(100.0, aes_raw * (mi / 100.0) * resonance))

    return {
        "file": filepath,
        "loc": loc,
        "avg_complexity": round(avg_complexity, 2),
        "type_coverage": round(type_coverage * 100, 2),
        "compliance": round(compliance_score, 2),
        "resonance": round(resonance, 2),
        "aes": round(aes, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Algorithmic Elegance Score (AES) — v14.0 [OMEGA]"
    )
    parser.add_argument("target", help="File or directory to scan.")
    args = parser.parse_args()

    cognition = AxionCognition() if AxionCognition else None
    target = os.path.abspath(args.target)
    results = []

    if os.path.isfile(target):
        targets = [target]
    else:
        targets = []
        for root, _dirs, files in os.walk(target):
            for f in files:
                if f.endswith(".py"):
                    targets.append(os.path.join(root, f))

    for t in targets:
        res = analyze_file(t, cognition)
        if "error" not in res:
            results.append(res)

    results.sort(key=lambda x: x["aes"], reverse=True)

    print("\n" + "=" * 100)
    print("  AES OMEGA REPORT (v14.0)".center(100))
    print("=" * 100)
    print(
        f"{'FILE':<40} | {'AES':<6} | {'COMPLIANCE':<10} | {'RESONANCE':<9} | {'COMPLEX':<7} | {'TYPE %':<6}"
    )
    print("-" * 100)
    for r in results:
        fname = os.path.basename(r["file"])
        print(
            f"{fname:<40} | {r['aes']:<6.2f} | {r['compliance']:<10.1f} | {r['resonance']:<9.2f} | {r['avg_complexity']:<7.1f} | {r['type_coverage']:<6.1f}"
        )
    print("=" * 100)


if __name__ == "__main__":
    main()
