"""# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-AES-001`                                 |
| **2. Official Name**   | `assess_elegance.py`                            |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `TECH` (Technical Standards)                    |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Operational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **Algorithmic Elegance**                       |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `JUDGES: SOURCE_CODE`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |.

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
| CORE-CODEX-001 | GOVERNS | This tool enforces the Algorithmic Elegance score. |
| METRIC-AES-001 | IMPLEMENTS | This tool calculates the AES-ALGO metric. |

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: ASSESS_AES` | Judge Algorithmic Elegance | Quality Gate |
"""

import argparse
import os


def assess_file(filepath: str) -> None:
    print(f"\n[AES] Assessing Elegance: {os.path.basename(filepath)}")

    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        return

    # 1. Metric: Conciseness (LOC check)
    # Filter empty lines and comments for "Code Density"
    code_lines = [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]
    total_loc = len(code_lines)

    if total_loc == 0:
        print("[AES] Empty file or only comments.")
        return

    # 2. Metric: Token Density (Average line length)
    total_chars = sum(len(line) for line in code_lines)
    avg_line_len = total_chars / total_loc

    # Heuristic Scoring (Subjective "Code Haiku" detection)
    # Ideal: Short functions, but descriptive lines.
    # Penalty for excessive verbosity (>100 chars avg) or excessive brevity (<10 chars avg)

    score = 5.0  # Baseline

    # Bonus for concise implementations (Small files often do one thing well)
    if total_loc < 50:
        score += 1.0
    elif total_loc > 300:
        score -= 1.0

    # Readability heuristic
    if 40 <= avg_line_len <= 80:
        score += 2.0  # Sweet spot
    elif avg_line_len > 120:
        score -= 1.0  # Too wide

    # Cap score
    score = min(10.0, max(1.0, score))

    print(f"  > Lines of Code: {total_loc}")
    print(f"  > Avg Line Len:  {avg_line_len:.1f}")
    print(f"  > Preliminary AES: {score:.1f}/10.0")

    if score >= 8.0:
        print("  💎 Status: DIAMOND (Elegant)")
    elif score >= 5.0:
        print("  🔹 Status: OBSIDIAN (Standard)")
    else:
        print("  🌑 Status: SLAG (Refine)")


def main():
    parser = argparse.ArgumentParser(
        description=">>> [SENT] Algorithmic Elegance Assessor v13.0 (The Judge)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example:\n  python assess_elegance.py axion-core/tools/reforge.py",
    )
    parser.add_argument("target", help="File to assess for algorithmic elegance")
    args = parser.parse_args()

    if os.path.isfile(args.target):
        assess_file(args.target)
    else:
        print("Target is not a file.")


if __name__ == "__main__":
    main()
