"""
SentinelPrime: The Epistemic Verification Engine (Modularized)

This file serves as the main entry point and orchestrator for the Sentinel Prime system.
It integrates the following modular components:

  - claim_ingestor.py: Extracts declared state from artifact headers.
  - measurement_core.py: Executes verifiers to observe artifact state.
  - delta_engine.py: Compares declared and observed states to find deltas.
  - models.py: Defines the core data structures (DeclaredState, etc.).
  - verifiers.py: Contains standalone verification functions.
  - kpi_tracker.py: Manages Key Performance Indicators for Sentinel operations.
  - verdict_publisher.py: Issues a final, structured Epistemic Verdict.

This modular architecture enhances maintainability, testability, and clarity
by adhering to the Single Responsibility Principle.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import functools
import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, cast

from .claim_ingestor import ClaimIngestor
from .delta_engine import DeltaEngine
from .kpi_tracker import KPITracker
from .measurement_core import MeasurementCore
from .models import EpistemicVerdict
from .quarantine_protocol import QuarantineProtocol
from .verdict_publisher import VerdictPublisher

logger = logging.getLogger("sentinel_prime")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

# --- Main SentinelPrime Class ---


class SentinelPrime:
    """
    UMB-SENTINEL-PRIME-001: The Epistemic Verification Engine.
    """

    def __init__(self, on_quarantine: Optional[Callable[[str, EpistemicVerdict], None]] = None) -> None:
        self.claim_ingestor = ClaimIngestor()
        self.measurement_core = MeasurementCore()
        self.delta_engine = DeltaEngine()
        self.verdict_publisher = VerdictPublisher()
        self.quarantine_protocol = QuarantineProtocol(on_quarantine=on_quarantine)
        self.kpi_tracker = KPITracker()
        self.registered_verifiers = list(self.measurement_core.verifiers.keys())

    def sentinel_audit(self, artifact_path: str, verifiers: Optional[List[str]] = None) -> EpistemicVerdict:
        """
        Runs the full Sentinel verification lifecycle on a target.
        """
        logger.info("--- Sentinel Audit: %s ---", artifact_path)

        declared_state = self.claim_ingestor.ingest_metadata(artifact_path)
        if not declared_state:
            logger.warning("No declared state found for %s. Cannot proceed with audit.", artifact_path)
            return EpistemicVerdict(
                claim="N/A",
                observed="N/A",
                evidence=[],
                delta="CLAIM_NOT_TESTABLE",
                verdict="CLAIM_NOT_TESTABLE",
                reason="No metadata found or parsed.",
                confidence=0.0,
            )

        observed_state = self.measurement_core.measure_artifact(artifact_path, declared_state, verifiers)
        delta_details = self.delta_engine.calculate_delta(declared_state, observed_state)
        verdict = self.verdict_publisher.publish_verdict(declared_state, delta_details)
        self.quarantine_protocol.enforce_quarantine(declared_state.artifact_id, verdict)
        self.kpi_tracker.update_kpis(verdict)

        logger.info("Audit complete for %s. Verdict: %s", artifact_path, verdict.verdict)
        return verdict

    def sentinel_probe(self, claim_type: str, search_root: str = ".", parallel_audits: int = 4) -> List[Dict[str, Any]]:
        """
        Walks the filesystem looking for artifacts matching a claim.
        Runs audits in parallel for better performance.
        """
        logger.info("--- Sentinel Probe: searching for claims of '%s' under %s ---", claim_type, search_root)
        results = []

        # Collect all potential artifact paths first
        potential_artifacts = []
        for path in Path(search_root).rglob("*.py"):
            declared = self.claim_ingestor.ingest_metadata(str(path))
            if declared and declared.status == claim_type:
                potential_artifacts.append((str(path), declared.artifact_id, declared.status))

        # Use a ThreadPoolExecutor to run audits in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_audits) as executor:
            # functools.partial is used to pass additional arguments to sentinel_audit
            # beyond the artifact_path, which is mapped by the executor.
            audit_func = functools.partial(self.sentinel_audit)

            # Map the audit function to each artifact path
            for artifact_path, artifact_id, declared_status in potential_artifacts:
                verdict = executor.submit(audit_func, artifact_path).result()
                results.append(
                    {
                        "artifact_id": artifact_id,
                        "path": artifact_path,
                        "declared_status": declared_status,
                        "current_verdict": verdict.verdict,
                        "delta": verdict.delta,
                        "confidence": verdict.confidence,
                        "reason": verdict.reason,
                    }
                )

        if not results:
            logger.info("No artifacts found with claim '%s'.", claim_type)
        return results

    def sentinel_define_verifier(
        self, name: str, script: Callable[[str, Optional[DeclaredState]], Dict[str, Any]]
    ) -> None:
        """Registers a new verifier script."""
        if name in self.measurement_core.verifiers:
            logger.warning("Verifier '%s' already exists. Overwriting.", name)
        self.measurement_core.verifiers[name] = script
        self.registered_verifiers = list(self.measurement_core.verifiers.keys())
        logger.info("Verifier '%s' registered.", name)

    def get_kpis(self) -> Dict[str, Any]:
        """Returns the current Key Performance Indicators."""
        return self.kpi_tracker.get_kpis()


# --- Example Usage ---
def main() -> None:
    """Main entry point for the SentinelPrime CLI."""

    parser = argparse.ArgumentParser(description="Sentinel Prime: The Epistemic Verification Engine.")
    parser.add_argument(
        "target",
        nargs="*",
        help="One or more file or directory paths to audit.",
    )
    parser.add_argument(
        "--probe",
        type=str,
        metavar="CLAIM",
        help="Probe for all artifacts making a specific claim (e.g., '[CANONIZED]').",
    )
    parser.add_argument(
        "--probe-root",
        type=str,
        default=".",
        help="Root directory to search when using --probe (default: current directory).",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers for the probe (default: 4).",
    )
    args = parser.parse_args()

    if not args.probe and not args.target:
        parser.error("Provide at least one target path, or use --probe.")

    sentinel = SentinelPrime()

    if args.probe:
        results = sentinel.sentinel_probe(args.probe, search_root=args.probe_root, parallel_audits=args.workers)
        print(json.dumps(results, indent=2))  # Pretty-print the JSON output
    else:
        for target_path in args.target:
            verdict = sentinel.sentinel_audit(target_path)
            print(f"\n--- Verdict for {target_path} ---\n{verdict}")


if __name__ == "__main__":
    main()
