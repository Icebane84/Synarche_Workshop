"""
## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.standardize.docs`                | The Sovereign ID. |
| **Official Name** | `standardize_docs.py`                   | The Filename.     |
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
from pathlib import Path
from governance_utils import ShadowLogger, is_v15_compliant


def standardize_docs(directory: str):
    """Scan directory and report compliance with OMEGA v15.0."""
    shadow = ShadowLogger("Standardize")
    root = Path(directory).resolve()
    print(f"\n>>> STANDARDIZE DOCS (v15.0): {root}\n")

    total = 0
    compliant = 0
    violations = []

    files = list(root.rglob("*.md")) + list(root.rglob("*.py"))

    for f in files:
        if any(
            skip in str(f)
            for skip in [".git", "node_modules", ".venv", "__pycache__", ".v13bak"]
        ):
            continue

        total += 1
        content = f.read_text(encoding="utf-8")
        if is_v15_compliant(content):
            compliant += 1
        else:
            violations.append(f.name)
            shadow.log_dissonance(str(f), "Non-compliant with OMEGA v15.0 structure")

    print("=" * 70)
    print("  OMEGA v15.0 COMPLIANCE REPORT".center(70))
    print("=" * 70)
    print(f"  Files Scanned:   {total}")
    print(f"  Fully Resonant:  {compliant}")
    print(f"  Dissonant:       {len(violations)}")
    rate = (compliant / total * 100) if total > 0 else 100.0
    print(f"  Resonance Rate:  {rate:.1f}%")
    print("-" * 70)

    for v in violations[:20]:
        print(f"  [!] DISSONANCE DETECTED: {v}")

    if len(violations) > 20:
        print(f"  ... and {len(violations) - 20} more.")

    summary = f"Audit complete. Resonance: {rate:.1f}%"
    shadow.finalize(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Standardize Docs - OMEGA v15.0 Checker"
    )
    parser.add_argument("target", help="Directory to scan")
    args = parser.parse_args()
    standardize_docs(args.target)
