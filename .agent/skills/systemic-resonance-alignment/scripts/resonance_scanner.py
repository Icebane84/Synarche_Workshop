"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-RESONANCE-SCANNER-001`                | The Sovereign ID. |
| **Official Name** | `resonance_scanner.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
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
import re
import sys
from pathlib import Path


def extract_terms_from_text(text: str) -> list[str]:
    """Extracts alphanumeric words > 3 chars, lowercased."""
    text = re.sub(r"[^A-Za-z0-9_]", " ", text)
    words = text.split()
    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "your",
        "have",
        "more",
        "will",
        "the",
        "and",
        "for",
        "are",
        "not",
    }
    return [w.lower() for w in words if len(w) > 3 and w.lower() not in stop_words]


def parse_python_semantics(filepath: Path) -> list[str]:
    """Analyzes Python AST to pull meaningful tokens (names, docs, comments)."""
    try:
        with open(filepath, encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception:
        return []

    terms = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            terms.extend(extract_terms_from_text(node.name))
            if ast.get_docstring(node):
                terms.extend(extract_terms_from_text(ast.get_docstring(node) or ""))
        elif isinstance(node, ast.Name):
            if len(node.id) > 4:
                terms.extend(extract_terms_from_text(node.id))

    comments = re.findall(r"#.*", source)
    for c in comments:
        terms.extend(extract_terms_from_text(c))
    return terms


def parse_markdown_semantics(filepath: Path) -> list[str]:
    """Extracts raw terms from a markdown file."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    content = re.sub(r"\| Key\s*\| Value.*?(?=---)", "", content, flags=re.DOTALL)
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    return extract_terms_from_text(content)


def calculate_cosine_similarity(vec1: dict[str, int], vec2: dict[str, int]) -> float:
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x] ** 2 for x in vec1])
    sum2 = sum([vec2[x] ** 2 for x in vec2])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return float(numerator) / denominator if denominator else 0.0


def get_term_frequencies(terms: list[str]) -> dict[str, int]:
    freq = {}
    for term in terms:
        freq[term] = freq.get(term, 0) + 1
    return freq


def scan_pair(py_path: Path, md_path: Path) -> float:
    print(f"  >>> RESONANCE: {py_path.name} <==> {md_path.name}")

    py_terms = parse_python_semantics(py_path)
    md_terms = parse_markdown_semantics(md_path)

    if not py_terms or not md_terms:
        print("      [SKIP] Missing tokens in one or both files.")
        return 0.0

    py_freq = get_term_frequencies(py_terms)
    md_freq = get_term_frequencies(md_terms)
    similarity = calculate_cosine_similarity(py_freq, md_freq)

    rpg_score = min(100.0, similarity * 300.0)
    print(f"      [SCORE] {rpg_score:.1f}/100.0")
    return rpg_score


def main() -> None:
    parser = argparse.ArgumentParser(description="Semantic Resonance Calculator")
    parser.add_argument("target", help="File or directory to scan.")
    parser.add_argument(
        "--doc",
        help="Specific markdown file to compare against (if target is a single file).",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    print(f"\n>>> SEMANTIC RESONANCE: {target}\n")

    scores = []

    if target.is_file():
        if target.suffix == ".py" and args.doc:
            scores.append(scan_pair(target, Path(args.doc).resolve()))
        else:
            print("Error: For single file scan, must provide --doc path.")
            sys.exit(1)
    elif target.is_dir():
        # Match all .py files to likely .md counterparts
        for py_file in target.rglob("*.py"):
            if any(p in py_file.parts for p in [".git", "node_modules", "__pycache__"]):
                continue

            # Simple heuristic matching
            md_name = py_file.stem + ".md"
            md_path = py_file.with_name(md_name)

            if not md_path.exists():
                # Search project for similar named md
                for candidate in target.rglob(md_name):
                    md_path = candidate
                    break

            if md_path.exists():
                scores.append(scan_pair(py_file, md_path))

    avg_score = sum(scores) / len(scores) if scores else 0.0
    print(f"\n>>> AGGREGATE RESONANCE: {avg_score:.2f}% (Across {len(scores)} pairs)")

    if avg_score < 40.0 and scores:
        sys.exit(1)


if __name__ == "__main__":
    main()
