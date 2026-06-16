"""IDENTIFICATION: TOOL-LAB-GARDENER
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24.
"""

import argparse
import datetime
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [GARDENER] - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


@dataclass
class GardeningReport:
    """State container for the gardening results."""

    coherence_score: float = 0.0
    orphans: list[str] = field(default_factory=list)
    drifted_files: list[dict[str, Any]] = field(default_factory=list)
    axiomatic_violations: list[str] = field(default_factory=list)
    total_scanned: int = 0


class WorkspaceGardener:
    """The Gardener Engine.

    Monitors the workspace for entropy and enforces axiomatic alignment.
    """

    def __init__(self, root_dir: str, registry_paths: list[str]) -> None:
        self.root = Path(root_dir).resolve()
        self.registry_paths = [Path(p).resolve() for p in registry_paths]
        self.report = GardeningReport()
        self.registered_files: set[str] = set()

    def load_registries(self) -> None:
        """Parses the Master Registries to identify 'Authorized' artifacts."""
        for reg_path in self.registry_paths:
            if not reg_path.exists():
                logging.warning("Registry not found at %s", reg_path)
                continue

            content = reg_path.read_text(encoding="utf-8")
            # Match markdown links to files: [Name](Path/to/file.md)
            file_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")
            matches = file_pattern.findall(content)

            for _name, path in matches:
                # Resolve relative paths relative to the registry location
                # Use unquote to handle URL-encoded spaces (%20)
                rel_to_reg = reg_path.parent / unquote(path)
                abs_path = rel_to_reg.resolve()
                if abs_path.exists():
                    try:
                        self.registered_files.add(str(abs_path.relative_to(self.root)))
                    except ValueError:
                        # If file is outside root, skip it for orphan scanning
                        continue

        logging.info(
            "Registries loaded: %d unique artifacts authorized.",
            len(self.registered_files),
        )

    def scan_for_orphans(self) -> None:
        """Identifies files on disk that are not in the Master Registry."""
        logging.info("Scanning for Orphan Nodes...")
        for file_path in self.root.rglob("*.md"):
            # Resolve to absolute for comparison
            abs_file = file_path.resolve()

            # Ignore hidden files, .gemini files, and archives
            if (
                ".gemini" in str(abs_file)
                or "99_Archives" in str(abs_file)
                or abs_file.name.startswith(".")
            ):
                continue

            try:
                rel_path = str(abs_file.relative_to(self.root))
                self.report.total_scanned += 1
                if rel_path not in self.registered_files:
                    self.report.orphans.append(rel_path)
                    logging.warning("ORPHAN DETECTED: %s", rel_path)
            except ValueError:
                continue

    def scan_for_drift(self, auto_fix: bool = False) -> None:
        """Checks for violations of 'Option A' standards (Hyphens + 4 Spaces)."""
        logging.info("Scanning for Protocol Drift...")
        for file_path in self.root.rglob("*.md"):
            if ".gemini" in str(file_path) or "99_Archives" in str(file_path):
                continue

            content = file_path.read_text(encoding="utf-8")
            needs_fix = False

            # Simple check for Asterisks instead of Hyphens in lists
            # We look for lines starting with * followed by space, or * at start of line
            if re.search(r"^\s*\* ", content, re.MULTILINE):
                needs_fix = True
                self.report.drifted_files.append(
                    {
                        "path": str(file_path.relative_to(self.root)),
                        "issue": "Marker Drift (Asterisks detected)",
                    }
                )
                logging.warning("DRIFT DETECTED: %s (Marker Alignment)", file_path.name)

            if needs_fix and auto_fix:
                logging.info("PRUNING: Correcting markers in %s...", file_path.name)
                # Convert '*' to '-' for list markers
                # Using a more careful regex to avoid matching things inside code blocks (simple heuristic)
                fixed_content = re.sub(
                    r"^(\s*)\* ", r"\1- ", content, flags=re.MULTILINE
                )
                file_path.write_text(fixed_content, encoding="utf-8")

    def validate_axiomatic_spine(self) -> None:
        """Verifies presence of core structural elements."""
        logging.info("Validating Axiomatic Spine...")
        for file_path in self.root.rglob("*.md"):
            if ".gemini" in str(file_path) or "99_Archives" in str(file_path):
                continue

            content = file_path.read_text(encoding="utf-8")

            # Check for Identification Block A
            if "Block A:" not in content:
                self.report.axiomatic_violations.append(
                    f"{file_path.name}: Missing Block A"
                )

            # Check for APP (Actionable Prompt Packet)
            if "Actionable Prompt Packet" not in content and "APP" not in content:
                self.report.axiomatic_violations.append(
                    f"{file_path.name}: Missing APP"
                )

            # Check for the 5 Axioms Presence (Greek or LaTeX symbols)
            # psi (Mind), mu (Memory), Lambda (Law), iota (Index), epsilon/epsilon (Entropy)
            # Note: The above comment uses Greek characters for reference.
            axioms = [r"\psi", r"\mu", r"\Lambda", r"\iota", r"\epsilon"]
            missing_axioms = []
            for ax in axioms:
                if ax not in content and f"${ax}$" not in content:
                    missing_axioms.append(ax)

            if missing_axioms:
                self.report.axiomatic_violations.append(
                    f"{file_path.name}: Missing Axioms ({', '.join(missing_axioms)})"
                )

    def calculate_coherence(self) -> float:
        """Computes the final workspace Coherence Score."""
        if self.report.total_scanned == 0:
            return 1.0

        orphan_penalty = (len(self.report.orphans) / self.report.total_scanned) * 0.4
        drift_penalty = (
            len(self.report.drifted_files) / self.report.total_scanned
        ) * 0.3
        spine_penalty = (
            len(self.report.axiomatic_violations) / self.report.total_scanned
        ) * 0.3

        coherence = 1.0 - (orphan_penalty + drift_penalty + spine_penalty)
        self.report.coherence_score = max(0.0, round(coherence, 2))
        return self.report.coherence_score

    def generate_report(self, output_path: str = "gardening_report.md") -> None:
        """Serializes results into a high-density Markdown report."""
        coherence = self.calculate_coherence()

        report_text = [
            f"# Gardening Triage Report: {datetime.datetime.now().strftime('%Y-%m-%d')}",
            f"**Workspace Coherence Score: {coherence}**",
            f"**Total Scanned:** {self.report.total_scanned}",
            "---",
            "## 1. Orphan Nodes (Law 1 Violation)",
            "| Path | Status |",
            "| :--- | :--- |",
        ]

        for orphan in self.report.orphans:
            report_text.append(f"| {orphan} | `UNREGISTERED` |")

        report_text.extend(
            [
                "",
                "## 2. Protocol Drift (Law 7 Violation)",
                "| Path | Issue |",
                "| :--- | :--- |",
            ]
        )

        for drift in self.report.drifted_files:
            report_text.append(f"| {drift['path']} | {drift['issue']} |")

        report_text.extend(
            [
                "",
                "## 3. Axiomatic Spine Violations (Law 17/19 Violation)",
                "| Artifact | Violation |",
                "| :--- | :--- |",
            ]
        )

        for violation in self.report.axiomatic_violations:
            name, issue = violation.split(": ", 1)
            report_text.append(f"| {name} | {issue} |")

        Path(output_path).write_text("\n".join(report_text), encoding="utf-8")
        logging.info("✅ Gardening complete. Report weaved to %s", output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Synarche Workspace Gardener")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    parser.add_argument(
        "--registries",
        nargs="+",
        default=[
            "_governance/01_Registries/GVRN.Registry.Master.md",
            "_governance/01_Registries/GVRN.OSLM.001.md",
        ],
        help="Master Registry paths",
    )
    parser.add_argument(
        "--mode",
        choices=["PASSIVE", "ACTIVE"],
        default="PASSIVE",
        help="Gardening Mode",
    )
    parser.add_argument(
        "--output", default="gardening_report.md", help="Report output path"
    )

    args = parser.parse_args()

    gardener = WorkspaceGardener(args.root, args.registries)
    gardener.load_registries()
    gardener.scan_for_orphans()
    gardener.scan_for_drift(auto_fix=(args.mode == "ACTIVE"))
    gardener.validate_axiomatic_spine()
    gardener.generate_report(args.output)


if __name__ == "__main__":
    main()
