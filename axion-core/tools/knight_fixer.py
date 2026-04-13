"""
# TOOL-KNIG-002: The Transmutation Engine (Knight's Fixer)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-KNIG-002`                                          |
| **2. Official Name**   | `knight_fixer.py`                                        |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `EXEC`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Transmutation**                                        |
| **11. Catalyst**       | **Lint Fixing**                                          |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Knight of Swords persona uses this tool for fixes.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Active Execution (The Knight of Swords)
# Synergy Set: The Knight's Charge
# Primary Stat Buff: Speed (+10), Integrity (+15)
# Passive Ability: Transmutation (Bulk Remediation)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: TRANSMUTE` | Run Fixers (MD013, MD030, etc.) | Standardized Form |
| `⚡ EXECUTE: PURIFY` | Full Lint Cleanup | Zero Entropy |
"""

import argparse
import logging
import os
import re
import sys
import textwrap
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class KnightFixer:
    """The Knight of Swords: Master of Transmutation and Lint Remediation."""

    def __init__(self, line_length=120):
        self.line_length = line_length
        self.in_frontmatter = False
        self.in_code_block = False
        self.frontmatter_count = 0
        self.FRONTMATTER_LIMIT = 2

    def _should_skip_wrap(self, line: str) -> bool:
        """Determines if the line should be skipped for MD013 wrapping."""
        # Frontmatter Logic
        if self.in_frontmatter:
            if line.strip() == "---":
                self.frontmatter_count += 1
                if self.frontmatter_count == self.FRONTMATTER_LIMIT:
                    self.in_frontmatter = False
            return True

        if line.strip() == "---" and self.frontmatter_count == 0:
            self.in_frontmatter = True
            self.frontmatter_count = 1
            return True

        # Code Block Logic
        if line.strip().startswith("```"):
            self.in_code_block = not self.in_code_block
            return True

        if self.in_code_block:
            return True

        # Structural Logic: Tables and Headings usually shouldn't be wrapped by a simple logic
        return line.strip().startswith("|") or line.strip().startswith("#")

    def fix_md013(self, content: str) -> str:
        """Fixes MD013 (Line Length) violations."""
        lines = content.splitlines()
        new_lines = []
        self.in_frontmatter = False
        self.in_code_block = False
        self.frontmatter_count = 0

        for line in lines:
            if self._should_skip_wrap(line) or len(line.rstrip()) <= self.line_length:
                new_lines.append(line)
                continue

            # Handle Blockquotes
            stripped = line.strip()
            prefix = ""
            content_to_wrap = line.rstrip()

            if stripped.startswith("> "):
                prefix = "> "
                content_to_wrap = line.rstrip()[line.find("> ") + 2 :]
            elif stripped.startswith(">"):
                prefix = "> "
                content_to_wrap = line.rstrip()[line.find(">") + 1 :]

            wrapper = textwrap.TextWrapper(
                width=self.line_length,
                initial_indent=prefix,
                subsequent_indent=prefix,
                break_long_words=False,
                break_on_hyphens=False,
            )
            new_lines.extend(wrapper.wrap(content_to_wrap))

        return "\n".join(new_lines)

    def fix_md030(self, content: str) -> str:
        """Fixes MD030 (Spaces after list markers)."""
        # Ensure 1 space after - * + or numbered lists
        content = re.sub(r"^(\s*[-*+])\s+", r"\1 ", content, flags=re.MULTILINE)
        content = re.sub(r"^(\s*\d+\.)\s+", r"\1 ", content, flags=re.MULTILINE)
        return content

    def fix_md012(self, content: str) -> str:
        """Fixes MD012 (Multiple consecutive blank lines)."""
        return re.sub(r"\n\s*\n\s*\n", "\n\n", content)

    def fix_md007(self, content: str) -> str:
        """Heuristic fix for MD007 (Unordered list indentation)."""
        lines = content.splitlines()
        fixed_lines = []
        for line in lines:
            if re.match(r"^\s*[-*+]", line):
                ls = len(line) - len(line.lstrip())
                if ls > 0 and ls % 4 == 0:
                    line = " " * ((ls // 4) * 2) + line.lstrip()
                elif ls == 3:
                    line = "  " + line.lstrip()
            fixed_lines.append(line)
        return "\n".join(fixed_lines)

    def fix_md028(self, content: str) -> str:
        """Fixes MD028 (Blank line inside blockquote)."""
        lines = content.splitlines()
        new_lines = []
        for i, line in enumerate(lines):
            if 0 < i < len(lines) - 1:
                if line.strip() == "" and lines[i - 1].strip().startswith(">") and lines[i + 1].strip().startswith(">"):
                    new_lines.append(">")
                    continue
            new_lines.append(line)
        return "\n".join(new_lines)

    def process_file(self, filepath: str, dry_run: bool = False):
        """Applies all Knightly transmutations to a file."""
        try:
            with open(filepath, encoding="utf-8") as f:
                original = f.read()
        except Exception:
            logger.exception(f"[!] Read failed: {filepath}")
            return

        content = self.fix_md013(original)
        content = self.fix_md030(content)
        content = self.fix_md012(content)
        content = self.fix_md007(content)
        content = self.fix_md028(content)

        if content != original:
            if dry_run:
                logger.info(f"[DRY RUN] Would transmute: {filepath}")
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"[⚔️] Transmuted: {filepath}")
        else:
            logger.info(f"[✨] Refined: {filepath}")


def main() -> None:
    parser = argparse.ArgumentParser(description="The Knight's Fixer: Transmuting entropy to coherence.")
    parser.add_argument("targets", nargs="*", help="Optional target files or directories.")
    parser.add_argument("--length", type=int, default=120, help="Max line length (default: 120)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes.")
    args = parser.parse_args()

    fixer = KnightFixer(args.length)
    targets = args.targets or ["."]

    for target in targets:
        path = Path(target)
        if path.is_file() and path.suffix == ".md":
            fixer.process_file(str(path), args.dry_run)
        elif path.is_dir():
            for p in path.rglob("*.md"):
                fixer.process_file(str(p), args.dry_run)


if __name__ == "__main__":
    main()
