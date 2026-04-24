import os

from ..loggers import SeltLogger
from ..parsers import LoomParser
from ..validators import LawValidator


class CoherentSynthesisEngine:
    """
    WHAT: The primary execution orchestrator for repository-wide synthesis.
    HOW: Calls discrete sub-components (Parsers, Validators, Loggers) in sequence.
    WHY: To achieve a Zero Entropy state without violating Single Responsibility limits.
    """

    def __init__(self) -> None:
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.parser = LoomParser(self.root_dir)
        self.validator = LawValidator(self.root_dir)
        self.logger = SeltLogger(self.root_dir)

    def execute_cycle(self) -> dict:
        try:
            # Step 1: Ingest
            loom_state = self.parser.extract_state()

            # Step 2: Validate
            drift_findings = self.validator.audit_drift(loom_state)

            # Step 3: Calculate Entropy
            entropy_level = len(drift_findings) * 0.5
            status = "STABLE" if entropy_level == 0.0 else "DEGRADED"

            # Step 4: Log
            self.logger.record_synthesis(status, entropy_level, drift_findings)

            return {"status": status, "entropy": entropy_level, "findings": drift_findings}

        except Exception as e:
            error_msg = f"HALTED: {e!s}"
            self.logger.record_synthesis("HALTED", 1.0, [error_msg])
            return {"status": "HALTED", "error": error_msg}


if __name__ == "__main__":
    cse = CoherentSynthesisEngine()
    result = cse.execute_cycle()
    print(f"[*] CSE Cycle Complete. Status: {result['status']}")
