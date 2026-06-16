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
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("sentinel")

TOOLS_DIR = Path(__file__).parent


@dataclass
class SentinelReport:
    timestamp: str
    target: str
    coherence_score: float = 0.0
    tool_results: dict[str, Any] = field(default_factory=dict)
    dissonance_alerts: list[str] = field(default_factory=list)


class SentinelOrchestrator:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.tools = [
            "compliance_audit.py",
            "ide_sentinel.py",
            "lint_artifact.py",
            "analyze_docs_compliance.py",
            "diagnose_paths.py",
            "verify_ast.py",
            "aes_calculator.py",
            "synergy_calculator.py",
            "sot_scanner.py",
            "resonance_scanner.py",
            "entropy_auditor.py",
        ]

    async def run_tool(self, tool_name: str) -> dict[str, Any]:
        """Runs a single tool and returns its output parsing."""
        tool_path = TOOLS_DIR / tool_name
        if not tool_path.exists():
            return {"status": "MISSING"}

        try:
            cmd = [sys.executable, str(tool_path), str(self.target)]
            proc = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            output = stdout.decode(errors="replace").strip()
            error = stderr.decode(errors="replace").strip()

            # Heuristic: If it looks like JSON, parse it.
            try:
                data = json.loads(output)
            except json.JSONDecodeError:
                data = {"stdout_summary": output[-500:], "error": error}

            return {
                "status": "COMPLETE" if proc.returncode == 0 else "FAILED",
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
                report.dissonance_alerts.append(f"Tool {name} status: {res['status']}")

        # Calculate Heuristic Coherence Score
        passed = sum(1 for r in results if r["status"] == "COMPLETE")
        report.coherence_score = (
            (passed / len(self.tools)) * 100.0 if self.tools else 0.0
        )

        return report


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sentinel Orchestrator — Master Audit Engine"
    )
    parser.add_argument("target", help="Directory or file to audit")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    orchestrator = SentinelOrchestrator(target)
    report = await orchestrator.execute_vigil()

    if args.json:
        print(json.dumps(report.__dict__, indent=2))
    else:
        logger.info("=" * 80)
        logger.info("AXION SENTINEL ORCHESTRATOR — VIGIL REPORT".center(80))
        logger.info("=" * 80)
        logger.info(f"  Target:    {report.target}")
        logger.info(f"  Timestamp: {report.timestamp}")
        logger.info(f"  Coherence: {report.coherence_score:.2f}%")
        logger.info("-" * 80)
        logger.info(f"  Tools Executed: {len(report.tool_results)}")
        logger.info(f"  Alerts:         {len(report.dissonance_alerts)}")
        logger.info("-" * 80)
        for name, res in report.tool_results.items():
            logger.info(f"  [{res['status']:<8}] {name}")
        logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
