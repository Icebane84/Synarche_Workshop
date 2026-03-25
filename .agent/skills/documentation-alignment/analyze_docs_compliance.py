"""
## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.analyze.docs.compliance`                | The Sovereign ID. |
| **Official Name** | `analyze_docs_compliance.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |


---

## **Block B: State Vector (AGP-001)**

| State Field   | Value     |
| :------------ | :-------- |
| **Coherence** | `1.0`     |
| **Resonance** | `1.0`     |
| **Stability** | `Stable`  |


---

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                |
| :------------------- | :------------------------ |
| **Logic Drift**      | Strict Linter Enforcement |
| **Semantic Decay**   | Axiomatic Compass Audit   |


---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
| :---------------------- | :---------------- | :---------------------------------------------- |
| `CORE.Codex.Phoenix`    | `GOVERNS`         | Provides the supreme law and ethical framework. |


---
"""

import argparse
import os
import sys
from pathlib import Path
from governance_utils import ShadowLogger, is_v15_compliant


def analyze_docs(target_dir: str):
    """Deep audit for OMEGA v15.0 compliance."""
    shadow = ShadowLogger("Audit")
    root = Path(target_dir).resolve()
    print(f"\n>>> OMEGA v15.0 COMPLIANCE AUDIT: {root}\n")

    files = list(root.glob("**/*.md")) + list(root.glob("**/*.py"))
    total = 0
    compliant = 0

    print("-" * 80)
    print(f"  {'FILENAME':<50} | {'STATUS':<15}")
    print("-" * 80)

    for f in files:
        if ".git" in str(f) or "__pycache__" in str(f) or ".venv" in str(f):
            continue

        total += 1
        try:
            content = f.read_text(encoding="utf-8")
            if is_v15_compliant(content):
                compliant += 1
                print(f"  {f.name:<50} | [OK]")
            else:
                shadow.log_dissonance(str(f), "Missing Block A or UIP-V15 compliance")
                print(f"  {f.name:<50} | [FAIL]")
        except Exception as e:
            print(f"  {f.name:<50} | [ERROR: {e}]")

    rate = (compliant / total * 100) if total > 0 else 100.0
    summary = f"Scanned {total} files. {compliant} compliant ({rate:.1f}%)."
    print(f"\n>>> {summary}")
    shadow.finalize(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze Docs Compliance - OMEGA v15.0"
    )
    parser.add_argument("target", help="Directory to audit")
    args = parser.parse_args()
    analyze_docs(args.target)
