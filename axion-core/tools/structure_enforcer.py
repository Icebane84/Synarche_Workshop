"""# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-EMPE-005`                                |
| **2. Official Name**   | `structure_enforcer.py`                        |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `GVRN` (Governance)                            |
| **6. Evolution**       | **Crystalline Coherence**                      |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **Guardian of Structure**                      |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `LINK: [UMB-STRUCT-001]`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |.
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

# --- CONFIGURATION (aligned with UMB-STRUCT-001) ---
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
DOMAINS = {
    "_governance",
    "nova-forge",
    "where-light-fades",
    "axion-core",
    "open-notebook",
    "playground",
    "_logs",
}
DEPRECATED_DOMAINS = {"nova_forge"}
NAME_KEBAB_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_SNAKE_PATTERN = re.compile(r"^[a-z0-9_]+$")

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("StructureEnforcer")


# Constants
RANK_CRYSTALLINE = 90
RANK_STABLE = 70
INITIAL_SCORE = 100.0


class StructureEnforcer:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.reports: dict[str, Any] = {
            "loose_files": [],
            "invalid_domains": [],
            "deprecated_domains": [],
            "naming_violations": [],
            "entropy_score": INITIAL_SCORE,
        }

    def _audit_root(self) -> None:
        """Audits root-level items (files and domains)."""
        allowed_files = {
            ".gitignore",
            "readme.md",
            "license",
            "package.json",
            "tsconfig.json",
        }
        root_items = list(self.root.iterdir())

        for item in root_items:
            if item.is_file():
                if item.name.lower() not in allowed_files:
                    self.reports["loose_files"].append(item.name)
            elif item.is_dir() and not item.name.startswith("."):
                self._validate_item(item)

    def _validate_item(self, item: Path) -> None:
        """Validates a single directory item."""
        name = item.name
        if name in DEPRECATED_DOMAINS:
            self.reports["deprecated_domains"].append(name)
        elif name not in DOMAINS:
            self.reports["invalid_domains"].append(name)

        if not NAME_KEBAB_PATTERN.match(name) and not name.startswith("_"):
            self.reports["naming_violations"].append(
                f"DIR: {name} (Expected kebab-case)"
            )

    def _audit_tools(self) -> None:
        """Audits tool naming in axion-core."""
        tool_dir = self.root / "axion-core" / "tools"
        if tool_dir.exists():
            for script in tool_dir.glob("*.py"):
                if not NAME_SNAKE_PATTERN.match(script.stem):
                    self.reports["naming_violations"].append(
                        f"TOOL: {script.name} (Expected snake_case)"
                    )

    def audit(self) -> None:
        logger.info(
            f"--- [EMPEROR AUDIT] Starting Workspace Scan: {self.root.name} ---"
        )
        self._audit_root()
        self._audit_tools()

        deductions = (
            len(self.reports["loose_files"]) * 5
            + len(self.reports["invalid_domains"]) * 10
            + len(self.reports["deprecated_domains"]) * 15
            + len(self.reports["naming_violations"]) * 2
        )
        self.reports["entropy_score"] = max(0.0, INITIAL_SCORE - deductions)

    def _print_reports(self) -> None:
        """Prints all violation segments."""
        segments = [
            ("loose_files", "[!] LOOSE FILES DETECTED", logger.warning),
            ("invalid_domains", "[!] NON-STANDARD DOMAINS", logger.warning),
            ("deprecated_domains", "[!] DEPRECATED DOMAINS FOUND", logger.error),
            ("naming_violations", "[!] NAMING CONVENTION VIOLATIONS", logger.warning),
        ]
        for key, title, log_func in segments:
            items = self.reports[key]
            if items:
                log_func(f"\n{title} ({len(items)}):")
                for item in items:
                    log_func(f"  - {item}")

    def report(self) -> None:
        logger.info("\n" + "=" * 40)
        logger.info("       WORKSPACE INTEGRITY REPORT       ")
        logger.info("=" * 40)

        score = self.reports["entropy_score"]
        status = (
            "CRYSTALLINE"
            if score > RANK_CRYSTALLINE
            else "STABLE" if score > RANK_STABLE else "DEGRADING"
        )
        logger.info(f"RANK: {status} | COHERENCE: {score:.1f}%")

        self._print_reports()

        if score == INITIAL_SCORE:
            logger.info(
                "\n[SUCCESS] Workspace is architecturally sound. The Emperor is pleased."
            )

        # Save to logs
        log_path = self.root / "_logs" / "structure_audit.json"
        try:
            log_path.parent.mkdir(exist_ok=True)
            with open(log_path, "w") as f:
                json.dump(self.reports, f, indent=2)
            logger.info(f"\nAudit saved to {log_path.relative_to(self.root)}")
        except Exception:
            logger.exception("Failed to save audit log")


if __name__ == "__main__":
    enforcer = StructureEnforcer(WORKSPACE_ROOT)
    enforcer.audit()
    enforcer.report()
