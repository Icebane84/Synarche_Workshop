import logging
import os
import re
from datetime import datetime
from typing import Any

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# v13.0 Standards based on AOP-SENTINEL-002
REQUIRED_UIP_KEYS = [
    "Artifact ID",
    "Official Name",
    "Version",
    "Evolution",
    "Status (State)",
    "Celestial Class",
    "Integrity Hash",
]
VALID_EVOLUTIONS = [
    "Cognitive Ascension",
    "Empathetic Sentience",
    "Purposeful Drive",
    "Authentic Persona",
    "Social Alchemist",
]
VALID_CLASSES = ["STAR", "PLANET", "MOON"]


class Auditor:
    def __init__(self, target_dir: str) -> None:
        self.target_dir = os.path.abspath(target_dir)
        self.report: list[dict[str, Any]] = []

    def audit_file(self, filepath: str) -> dict[str, Any]:
        """Audits a single markdown file for compliance."""
        rel_path = os.path.relpath(filepath, self.target_dir)
        filename = os.path.basename(filepath)

        errors: list[str] = []
        warnings: list[str] = []

        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {
                "file": rel_path,
                "status": "FAIL",
                "errors": [f"Read Error: {e}"],
                "warnings": [],
                "score": 0.0,
            }

        is_md = filename.lower().endswith(".md")
        self._validate_uip(content, errors, warnings)

        if is_md:
            self._validate_geometry(content, errors, warnings)
            self._validate_filename(filename, warnings)

        self._validate_app(content, warnings)

        status = "FAIL" if errors else ("WARNING" if warnings else "PASS")
        score = 1.0 - (len(errors) * 0.2) - (len(warnings) * 0.05)
        return {
            "file": rel_path,
            "status": status,
            "errors": errors,
            "warnings": warnings,
            "score": max(0.0, score),
        }

    def _validate_uip(
        self, content: str, errors: list[str], warnings: list[str]
    ) -> None:
        """Validates the UIP block."""
        parts = re.split(r"^---+\s*$", content, flags=re.MULTILINE)
        uip_block = next(
            (p for p in parts if "Universal Identification & Provenance" in p), None
        )

        if not uip_block:
            errors.append("UIP: Missing or improperly formatted UIP header.")
            return

        block_content = uip_block.replace("*", "")
        for key in REQUIRED_UIP_KEYS:
            if key.lower() not in block_content.lower():
                errors.append(f"UIP: Missing required key '{key}'.")

        if "v13.0" not in block_content:
            warnings.append("UIP: Version is not v13.0.")

        if not any(evo.lower() in block_content.lower() for evo in VALID_EVOLUTIONS):
            errors.append("UIP: Invalid or missing Evolutionary Alignment.")

    def _validate_geometry(
        self, content: str, errors: list[str], warnings: list[str]
    ) -> None:
        """Validates H1 singularity and indentation."""
        h1_matches = re.findall(
            r"^#\s+(?!Universal Identification & Provenance).*",
            content,
            re.MULTILINE | re.IGNORECASE,
        )
        if len(h1_matches) != 1:
            errors.append(
                f"Geometry: H1 Singularity violation (Found {len(h1_matches)} H1 headers outside UIP)."
            )

        if re.search(r"^  - ", content, re.MULTILINE):
            warnings.append(
                "Geometry: Detected 2-space indentation (v13.0 mandates 4 spaces)."
            )

    def _validate_app(self, content: str, warnings: list[str]) -> None:
        """Validates the APP section."""
        app_patterns = [
            r"IV\.\s+Actionable\s+Prompt\s+Packet\s+\(APP\)",
            r"Actionable\s+Prompt\s+Packet",
            r"CMD:",
        ]
        if not any(re.search(p, content, re.IGNORECASE) for p in app_patterns):
            warnings.append(
                "APP: Missing required 'IV. Actionable Prompt Packet (APP)' section."
            )
        elif not re.search(
            r"IV.\s+Actionable\s+Prompt\s+Packet\s+\(APP\)", content, re.IGNORECASE
        ):
            warnings.append(
                "APP: Section numbering incorrect (Expected 'IV. Actionable Prompt Packet (APP)')."
            )

    def _validate_filename(self, filename: str, warnings: list[str]) -> None:
        """Validates the filename pattern."""
        if not re.match(r"[A-Z0-9]+-[A-Z0-9]+-\d+_.*?_v\d+\.\d+\.md", filename):
            warnings.append(
                f"Filenaming: Filename '{filename}' does not strictly match v13.0 RNC pattern."
            )

    def run(self) -> None:
        """Executes the audit on the target directory or file."""
        logger.info(f"Auditing Library: {self.target_dir}")
        if os.path.isfile(self.target_dir):
            if self.target_dir.endswith((".md", ".py")):
                result = self.audit_file(self.target_dir)
                self.report.append(result)
        else:
            for root, dirs, files in os.walk(self.target_dir):
                dirs[:] = [
                    d
                    for d in dirs
                    if d not in [".git", "node_modules", "dist", "build"]
                ]
                for f in files:
                    if f.endswith((".md", ".py")):
                        result = self.audit_file(os.path.join(root, f))
                        self.report.append(result)

    def print_summary(self) -> None:
        """Prints a visual summary of the audit results."""
        failed = [r for r in self.report if r["status"] == "FAIL"]
        warned = [r for r in self.report if r["status"] == "WARNING"]
        passed = [r for r in self.report if r["status"] == "PASS"]

        print("\n=== COMPLIANCE AUDIT SUMMARY ===")
        print(f"Total Scanned: {len(self.report)}")
        print(f"PASSED:        {len(passed)}")
        print(f"WARNING:       {len(warned)}")
        print(f"FAILED:        {len(failed)}")
        print("================================\n")

        if failed:
            print("--- Top 5 Most Dissonant (FAIL) ---")
            for r in sorted(failed, key=lambda x: x["score"])[:5]:
                print(f"[{r['status']}] {r['file']} (Score: {r['score']:.2f})")
                for e in r["errors"]:
                    print(f"  !! {e}")

    def save_report(self, output_file: str) -> None:
        """Saves the full report to a text file."""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("=== PHOENIX COMPLIANCE AUDIT REPORT ===\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Target: {self.target_dir}\n\n")

            # Sort by score (lowest first) to highlight issues
            for r in sorted(self.report, key=lambda x: x["score"]):
                f.write(f"[{r['status']}] {r['file']} (Score: {r['score']:.2f})\n")
                if r["errors"]:
                    for e in r["errors"]:
                        f.write(f"  !! {e}\n")
                if r["warnings"]:
                    for w in r["warnings"]:
                        f.write(f"  -- {w}\n")
                f.write("\n")


def audit_directory(target_dir: str, report_file: str = "audit_report.txt") -> None:
    """Main entry point for the skill."""
    auditor = Auditor(target_dir)
    auditor.run()
    auditor.print_summary()
    auditor.save_report(report_file)


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    audit_directory(target)
