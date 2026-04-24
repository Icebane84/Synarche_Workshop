"""
IDENTIFICATION: SYNG.ENGINE.CSE.ORCHESTRATOR
VERSION: v15.0 [OMEGA]
STATUS: KINETIC
TIMESTAMP: 2026-04-22
"""

import os

from ..loggers.selt_logger import SeltLogger
from ..managers.guca_parser import GucaParser
from ..managers.mcp_injector import McpInjector
from ..parsers.loom_parser import LoomParser
from ..validators import LawValidator


class CoherentSynthesisEngine:
    """
    WHAT: The master execution kernel for the Synarche OMEGA framework.
    HOW: Coordinates the Audit Cycle (Zero Entropy validation) and the Expansion Cycle (MCP Tool Registration).
    WHY: To facilitate continuous, autonomous 'Conceptual Engineering' without human bottlenecking.
    """

    def __init__(self) -> None:
        # Anchor to the repository root relative to axion-core/src/cse/
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        # Initialize Sub-Components
        self.loom_parser = LoomParser(self.root_dir)
        self.law_validator = LawValidator(self.root_dir)
        self.selt_logger = SeltLogger(self.root_dir)
        self.guca_parser = GucaParser(self.root_dir)
        self.mcp_injector = McpInjector(self.root_dir)

    def execute_audit_cycle(self) -> dict:
        """Executes the Zero Entropy state validation."""
        try:
            loom_state = self.loom_parser.extract_state()
            findings = self.law_validator.audit_drift(loom_state)

            entropy = len(findings) * 0.5
            status = "STABLE" if entropy == 0.0 else "DEGRADED"

            self.selt_logger.record_synthesis(f"AUDIT_{status}", entropy, findings)
            return {"status": status, "entropy": entropy, "findings": findings}
        except Exception as e:
            error_msg = f"AUDIT_HALTED: {e!s}"
            self.selt_logger.record_synthesis("HALTED", 1.0, [error_msg])
            return {"status": "HALTED", "error": error_msg}

    def execute_expansion_cycle(self) -> dict:
        """Executes autonomous tool registration from the Forge (.agent/skills/)."""
        skills_dir = os.path.join(self.root_dir, ".agent", "skills")
        findings = []
        registered_count = 0

        try:
            if not os.path.exists(skills_dir):
                raise FileNotFoundError(f"Missing Forge Substrate: {skills_dir}")

            for filename in os.listdir(skills_dir):
                if filename.startswith("kcap_") and filename.endswith(".py"):
                    schema = self.guca_parser.extract_capability(filename)
                    if schema:
                        success = self.mcp_injector.register_tool(schema)
                        if success:
                            registered_count += 1
                            findings.append(f"KCAP_REGISTERED: {schema['name']}")
                    else:
                        findings.append(f"KCAP_REJECTED: {filename} (Phoenix Compliance Failure)")

            status = "EXPANDED" if registered_count > 0 else "STATIC"
            self.selt_logger.record_synthesis(f"EXPANSION_{status}", 0.0, findings)
            return {"status": status, "registered": registered_count, "findings": findings}

        except Exception as e:
            error_msg = f"EXPANSION_HALTED: {e!s}"
            self.selt_logger.record_synthesis("HALTED", 1.0, [error_msg])
            return {"status": "HALTED", "error": error_msg}

    def run_full_synthesis(self):
        """The Master OMEGA Loop."""
        audit_result = self.execute_audit_cycle()

        # Only expand if the base system is stable (Zero Entropy)
        if audit_result["status"] == "STABLE":
            expansion_result = self.execute_expansion_cycle()
            return {"audit": audit_result, "expansion": expansion_result}
        else:
            return {"audit": audit_result, "expansion": "SKIPPED_DUE_TO_ENTROPY"}


if __name__ == "__main__":
    engine = CoherentSynthesisEngine()
    final_state = engine.run_full_synthesis()
    import json

    print(f"[*] SYNTHESIS COMPLETE:\n{json.dumps(final_state, indent=4)}")
