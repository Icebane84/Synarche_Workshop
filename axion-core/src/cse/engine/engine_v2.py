"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CSE-ENG-V2-001`              | The Sovereign ID. |
| **Official Name**   | `engine_v2.py`                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CSE-ENG`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Systemic Synthesis (Law 01)**
> Implemented from Blueprint `GVRN.REG.CseOrchestrator.md`.
> Ethos: Clarity through initialization.
"""

import asyncio
import json
import os
from typing import Any, Dict

from ...engine.ecs import ResonanceAuditor, ResonanceRegistry, World
from ...engine.ecs.compiler import ECSSystemCompiler
from ...engine.scheduling.layered_scheduler import LayeredScheduler
from ...phoenix.logging import EthicalLogger, ProcessStatus
from ...system.refactor.parallel_executor_v2 import DeterministicParallelExecutor
from ..loggers.selt_logger import SeltLogger
from ..managers.guca_parser import GucaParser
from ..managers.mcp_injector import McpInjector
from ..parsers.loom_parser import LoomParser
from ..validators import LawValidator


class CoherentSynthesisEngine:
    """The master execution kernel for the Synarche OMEGA framework.
    Coordinates the Audit Cycle (Zero Entropy validation) and the Expansion Cycle (MCP Tool Registration).
    Facilitates continuous, autonomous 'Conceptual Engineering' without human bottlenecking.
    """

    def __init__(self) -> None:
        """Initializes the engine and its sub-components with the repository root context."""
        # Anchor to the repository root relative to axion-core/src/cse/
        self.root_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )

        # Initialize Sub-Components
        self.loom_parser = LoomParser(self.root_dir)
        self.law_validator = LawValidator(self.root_dir)
        self.selt_logger = SeltLogger(self.root_dir)
        self.guca_parser = GucaParser(self.root_dir)
        self.mcp_injector = McpInjector(self.root_dir)

        # OMEGA v15.1 - Ethical Telemetry
        self.ethos_logger = EthicalLogger("CoherentSynthesisEngine")

        # OMEGA v15.1 - ECS & Governance
        self.world = World()
        self.registry = ResonanceRegistry()
        self.auditor = ResonanceAuditor(self.registry)
        self.executor = DeterministicParallelExecutor(max_workers=2)

        # OMEGA v15.1 - Scheduling Core Integration
        # Note: Systems would typically be pulled from the registry/auditor
        systems = []
        compiler = ECSSystemCompiler(systems)
        self.graph = compiler.compile()
        self.graph.build()

        # Bind graph to the LayeredScheduler with parallel executor
        self.scheduler = LayeredScheduler(self.graph, self.executor)

    async def execute_audit_cycle(self) -> Dict[str, Any]:
        """Executes the Zero Entropy state validation by auditing structural drift.
        Integrates the ECS Scheduler for deterministic governance checks.

        Returns:
            Dict[str, Any]: Results including status, entropy score, and specific findings.

        """
        try:
            await self.ethos_logger.log_event(
                "Initiating Zero Entropy Audit Cycle...", ProcessStatus.INFO
            )

            # 1. Structural Audit (Loom/Law)
            loom_state = self.loom_parser.extract_state()
            findings = self.law_validator.audit_drift(loom_state)

            # Run a frame of the scheduler to verify runtime integrity
            await self.ethos_logger.log_event(
                "Executing ECS Deterministic Logic Audit...", ProcessStatus.INFO
            )

            # Layered execution with world context
            context = {"world": self.world}
            self.scheduler.execute(context)

            entropy = len(findings) * 0.5
            status = "STABLE" if entropy == 0.0 else "DEGRADED"

            await self.ethos_logger.log_event(
                f"Audit Complete. Status: {status} | Entropy: {entropy}",
                ProcessStatus.INFO,
            )

            self.selt_logger.record_synthesis(f"AUDIT_{status}", entropy, findings)
            return {"status": status, "entropy": entropy, "findings": findings}
        except Exception as e:
            error_msg = f"AUDIT_HALTED: {e!s}"
            await self.ethos_logger.log_event(error_msg, ProcessStatus.ERROR)
            self.selt_logger.record_synthesis("HALTED", 1.0, [error_msg])
            return {"status": "HALTED", "error": error_msg}

    async def execute_expansion_cycle(self) -> Dict[str, Any]:
        """Executes autonomous tool registration from the Forge (.agent/skills/).
        Identifies and registers kcap_*.py capabilities as MCP tools.

        Returns:
            Dict[str, Any]: Results including status, count of registered tools, and findings.

        """
        skills_dir = os.path.join(self.root_dir, ".agent", "skills")
        findings = []
        registered_count = 0

        try:
            await self.ethos_logger.log_event(
                "Initiating Autonomous Expansion Cycle...", ProcessStatus.INFO
            )

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
                        findings.append(
                            f"KCAP_REJECTED: {filename} (Phoenix Compliance Failure)"
                        )

            status = "EXPANDED" if registered_count > 0 else "STATIC"
            await self.ethos_logger.log_event(
                f"Expansion Cycle {status}. Registered {registered_count} tools.",
                ProcessStatus.INFO,
            )

            self.selt_logger.record_synthesis(f"EXPANSION_{status}", 0.0, findings)
            return {
                "status": status,
                "registered": registered_count,
                "findings": findings,
            }

        except Exception as e:
            error_msg = f"EXPANSION_HALTED: {e!s}"
            await self.ethos_logger.log_event(error_msg, ProcessStatus.ERROR)
            self.selt_logger.record_synthesis("HALTED", 1.0, [error_msg])
            return {"status": "HALTED", "error": error_msg}

    async def run_full_synthesis(self) -> Dict[str, Any]:
        """The Master OMEGA Loop: Audits the system and expands if stable.

        Returns:
            Dict[str, Any]: The aggregate result of the audit and expansion cycles.

        """
        await self.ethos_logger.log_event(
            "Starting Full System Synthesis...", ProcessStatus.INFO
        )

        audit_result = await self.execute_audit_cycle()

        # Only expand if the base system is stable (Zero Entropy)
        if audit_result["status"] == "STABLE":
            expansion_result = await self.execute_expansion_cycle()
            result = {"audit": audit_result, "expansion": expansion_result}
        else:
            await self.ethos_logger.log_event(
                "Expansion SKIPPED due to systemic entropy.", ProcessStatus.WARNING
            )
            result = {"audit": audit_result, "expansion": "SKIPPED_DUE_TO_ENTROPY"}

        await self.ethos_logger.log_event(
            "Full Synthesis Cycle Complete.", ProcessStatus.INFO
        )
        return result


async def main():
    engine = CoherentSynthesisEngine()
    final_state = await engine.run_full_synthesis()
    print(f"\n[*] SYNTHESIS COMPLETE:\n{json.dumps(final_state, indent=4)}")


if __name__ == "__main__":
    asyncio.run(main())
