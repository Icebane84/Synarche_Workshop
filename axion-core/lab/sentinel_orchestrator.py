"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-SENTINEL-ORCHESTRATOR-001`                | The Sovereign ID. |
| **Official Name** | `sentinel_orchestrator.py`                   | The Filename.     |
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
import asyncio
import json
import logging
import re
import sys
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("sentinel")

# --- ANSI COLORS ---
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

TOOLS_DIR = Path(__file__).parent.parent / "tools"


@dataclass
class SentinelReport:
    timestamp: str
    target: str
    coherence_score: float = 0.0
    tool_results: dict[str, Any] = field(default_factory=dict)
    dissonance_alerts: list[str] = field(default_factory=list)


class SentinelOrchestrator:
    def __init__(self, target: Path, quiet: bool = False) -> None:
        self.target = target
        self.quiet = quiet
        self.tools = [
            "compliance_audit.py",
            "ide_sentinel.py",
            "lint_artifact.py",
            "analyze_docs_compliance.py",
            "diagnose_paths.py",
            "verify_ast.py",
            "resonance_scanner.py",
            "sentinel_sword.py",
        ]

    def _build_command(self, tool_name: str, tool_path: Path) -> list[str]:
        if tool_name in ("lint_artifact.py", "verify_ast.py"):
            return [sys.executable, str(tool_path), "--target", str(self.target)]
        if tool_name in ("ide_sentinel.py", "sentinel_sword.py"):
            return [sys.executable, str(tool_path)]
        return [sys.executable, str(tool_path), str(self.target)]

    def _parse_tool_output(self, output: str, error: str, returncode: int) -> tuple[str, dict[str, Any]]:
        try:
            data = json.loads(output)
            internal_status = data.get("status")
            if internal_status in ("PASS", "COMPLETE", "V-SAFE", "OK"):
                return "COMPLETE", data
            if internal_status in ("FAIL", "ERROR", "CRITICAL_ERROR", "RISK_STATE"):
                return "FAILED", data
            status_flag = "COMPLETE" if returncode == 0 else "FAILED"
            return status_flag, data
        except json.JSONDecodeError:
            data = {"stdout_summary": output[-500:], "error": error}
            status_flag = "COMPLETE" if returncode == 0 else "FAILED"
            return status_flag, data

    async def run_tool(self, tool_name: str) -> dict[str, Any]:
        """Runs a single tool and returns its output parsing."""
        tool_path = TOOLS_DIR / tool_name
        if not tool_path.exists():
            return {"status": "MISSING"}

        try:
            cmd = self._build_command(tool_name, tool_path)
            proc = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout_lines: list[str] = []
            stderr_lines: list[str] = []

            async def stream_reader(stream: asyncio.StreamReader, prefix: str, dest_list: list[str], is_error: bool = False) -> None:
                async for line in stream:
                    text = line.decode(errors="replace").rstrip()
                    dest_list.append(text)
                    # Stream dynamically to the console as output arrives
                    if not self.quiet:
                        color = RED if is_error else CYAN
                        logger.info(f"{color}[{prefix}]{RESET} {text}")

            assert proc.stdout is not None
            assert proc.stderr is not None

            # Read stdout and stderr concurrently as they stream
            await asyncio.gather(
                stream_reader(proc.stdout, tool_name, stdout_lines),
                stream_reader(proc.stderr, tool_name, stderr_lines, is_error=True)
            )
            await proc.wait()

            output = "\n".join(stdout_lines).strip()
            error = "\n".join(stderr_lines).strip()

            status_flag, data = self._parse_tool_output(output, error, proc.returncode or 0)

            return {
                "status": status_flag,
                "data": data,
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    async def execute_vigil(self) -> SentinelReport:
        """Executes the full suite of Sentinel tools."""
        report = SentinelReport(
            timestamp=datetime.now().isoformat(), target=str(self.target)
        )

        tasks = [self.run_tool(t) for t in self.tools]
        results = await asyncio.gather(*tasks)

        for name, res in zip(self.tools, results, strict=False):
            report.tool_results[name] = res
            if res["status"] != "COMPLETE":

                # Extract detailed error messages from JSON if available
                data = res.get("data", {})
                error_msg = data.get("message") or data.get("error") or data.get("primary_violation") or "No specific message provided"
                report.dissonance_alerts.append(f"{RED}[{name}] {res['status']}: {error_msg}{RESET}")

        # Calculate Heuristic Coherence Score
        passed = sum(1 for r in results if r["status"] == "COMPLETE")
        report.coherence_score = (
            (passed / len(self.tools)) * 100.0 if self.tools else 0.0
        )

        return report


def export_to_markdown(report: SentinelReport, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_time = report.timestamp.replace(":", "-").split(".")[0]
    md_file = out_dir / f"Sentinel_Report_{safe_time}.md"

    # Regex to strip ANSI colors from alerts for the markdown file
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    md_content = [
        "# Sentinel Orchestrator — Vigil Report",
        f"> **Timestamp:** {report.timestamp} | **Target:** `{report.target}`",
        "",
        f"### **System Coherence Score:** {report.coherence_score:.2f}%",
        "",
        "## Tool Execution Summary",
        "| Tool | Status | Details |",
        "| :--- | :--- | :--- |"
    ]

    for name, res in report.tool_results.items():
        status = res['status']
        if status != "COMPLETE":
            data = res.get("data", {})
            error_msg = data.get("message") or data.get("error") or data.get("primary_violation") or ""
            clean_error = ansi_escape.sub('', str(error_msg)).replace('\n', '<br>')
            md_content.append(f"| `{name}` | **{status}** | {clean_error} |")
        else:
            md_content.append(f"| `{name}` | **{status}** | - |")

    md_content.extend(["", "## Dissonance Alerts", ""])


    if report.dissonance_alerts:
        for alert in report.dissonance_alerts:
            clean_alert = ansi_escape.sub('', alert)
            md_content.append(f"- {clean_alert}")
    else:
        md_content.append("*No dissonance alerts detected. Coherence is intact.*")

    md_file.write_text("\n".join(md_content), encoding="utf-8")
    logger.info(f"{CYAN}  Exported Markdown Report: {md_file}{RESET}")


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sentinel Orchestrator — Master Audit Engine"
    )
    parser.add_argument("target", help="Directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--quiet", action="store_true", help="Suppress dynamic stdout streaming")
    parser.add_argument("--outdir", default="logs", help="Directory to save the markdown report")
    parser.add_argument("--obsidian", default=os.getenv("OBSIDIAN_VAULT_PATH"), help="Obsidian vault path to push the report to")
    parser.add_argument("--min-coherence", type=float, default=0.0, help="Minimum coherence score percentage required to pass (0.0 to 100.0)")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    orchestrator = SentinelOrchestrator(target, quiet=args.quiet)
    report = await orchestrator.execute_vigil()

    if args.json:
        print(json.dumps(report.__dict__, indent=2))
    else:
        logger.info("=" * 80)
        logger.info("AXION SENTINEL ORCHESTRATOR — VIGIL REPORT".center(80))
        logger.info("=" * 80)
        logger.info(f"  Target:    {report.target}")
        logger.info(f"  Timestamp: {report.timestamp}")

        if report.coherence_score == 100:
            coh_color = GREEN
        elif report.coherence_score > 0:
            coh_color = YELLOW
        else:
            coh_color = RED
        logger.info(f"  Coherence: {coh_color}{report.coherence_score:.2f}%{RESET}")
        logger.info("-" * 80)
        logger.info(f"  Tools Executed: {len(report.tool_results)}")
        logger.info(f"  Alerts:         {len(report.dissonance_alerts)}")
        logger.info("-" * 80)
        for name, res in report.tool_results.items():
            status = res['status']
            status_color = GREEN if status == "COMPLETE" else RED
            logger.info(f"  [{status_color}{status:<8}{RESET}] {name}")
        logger.info("=" * 80)


        # Export the markdown report to the specified logs directory
        export_to_markdown(report, Path(args.outdir))

        # Automatically push to Obsidian vault if specified
        if args.obsidian:
            export_to_markdown(report, Path(args.obsidian))

    # Validate against minimum coherence threshold
    if report.coherence_score < args.min_coherence:
        logger.error(f"{RED}Error: Coherence score {report.coherence_score:.2f}% is below the minimum required {args.min_coherence:.2f}%{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

