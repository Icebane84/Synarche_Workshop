"""### **Block A: The Identification Lock (UIP-V15)**
ID: AGENT-OUROBOROS-SCAN-001
Official Name: ouroboros_scan.py
Version: v1.0 [OMEGA]
Domain: ENGINE
Status: [ACTIVE]
Ethos: "Zero Duplication through Systemic Introspection.".
"""

import argparse
import ast
from pathlib import Path
from typing import Dict, Set


class OuroborosScanner:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.function_registry: Dict[str, Set[str]] = {}

    def scan(self):
        print(f"--- 🌀 OUROBOROS SCAN: {self.root_dir} ---")
        for py_file in self.root_dir.rglob("*.py"):
            if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            self._analyze_file(py_file)

        self._report_redundancy()

    def _analyze_file(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name not in self.function_registry:
                        self.function_registry[node.name] = set()
                    self.function_registry[node.name].add(
                        str(file_path.relative_to(self.root_dir))
                    )
        except Exception as e:
            print(f"⚠️ Error analyzing {file_path}: {e}")

    def _report_redundancy(self):
        duplicates = {k: v for k, v in self.function_registry.items() if len(v) > 1}

        if not duplicates:
            print("✅ No redundant function names detected. Ouroboros is satisfied.")
            return

        print(f"🚨 Redundancy Detected ({len(duplicates)} names):")
        for name, paths in duplicates.items():
            print(f"  - [{name}]: found in {', '.join(paths)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ouroboros Redundancy Scan")
    parser.add_argument("--dir", default=".", help="Directory to scan")
    args = parser.parse_args()

    scanner = OuroborosScanner(args.dir)
    scanner.scan()
