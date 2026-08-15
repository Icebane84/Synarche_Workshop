"""
artifact_anchor:
  id: CORE.ENGINE_V2.001
  version: v15.0 [OMEGA]
  provenance: '2026-08-13'
  domain: CORE-CSE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations:
    - GOVERNED_BY: CORE.Codex.Phoenix
    - EMBODIES: UMB-CSE-001
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CSE-ENG-V2-001`              | The Sovereign ID. |
| **Official Name**   | `engine_v2.py`                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-CSE`                    | The Subject.      |
| **Celestial Class** | `[STAR]`                      | The Weight.       |
| **Evolution**       | `Definitive Actualization`    | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Systemic Synthesis (Law 01)**
> Implemented from Blueprint `GVRN.REG.CseOrchestrator.md` & `UMB-CSE-001_CoherentSynthesisEngine_v7.1`.
> Ethos: The definitive Master Execution Kernel of the Phoenix Form AI.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from ...engine.ecs import ResonanceAuditor, ResonanceRegistry, World
from ...engine.ecs.compiler import ECSSystemCompiler
from ...engine.scheduling.layered_scheduler import LayeredScheduler
from ...phoenix.logging import EthicalLogger, ProcessStatus
from ...system.refactor.parallel_executor_v2 import DeterministicParallelExecutor
from ..guca_command import (
    AuditCoherenceCommand,
    ContextWeaveCommand,
    EnactTranscendenceCommand,
    EthicalEvaluationCommand,
    GUCAExecutor,
    OmniLogCommand,
)
from ..loggers.selt_logger import SeltLogger
from ..managers.guca_parser import GucaParser
from ..managers.mcp_injector import McpInjector
from ..parsers.loom_parser import LoomParser
from ..validators import GovernanceEngine, LawValidator
from .adaptive_opportunity_weave import AdaptiveOpportunityWeave
from .coherence_attractor_core import CoherenceAttractorCore
from .methodology_selector import MethodologySelectorLayer
from .reflexive_consequence_projector import ReflexiveConsequenceProjector
from .telemetry_engine import TelemetryEngine


class CoherentSynthesisEngine:
    """The master execution kernel for the Synarche OMEGA framework and Phoenix Form.
    Orchestrates the 4 core sub-components (CAC, RCP, AOW, MSL), evaluates governance laws,
    executes GUCA command pipelines, manages dynamic telemetry (V_State), and drives autonomous expansion.
    """

    def __init__(self, root_dir: Optional[str] = None) -> None:
        """Initializes the engine and all subordinate faculties with repository root context."""
        if root_dir:
            self.root_dir = root_dir
        else:
            self.root_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            )

        # 1. Base Ingestion & Management Sub-components
        self.loom_parser = LoomParser(self.root_dir)
        self.law_validator = LawValidator(self.root_dir)
        self.selt_logger = SeltLogger(self.root_dir)
        self.guca_parser = GucaParser(self.root_dir)
        self.mcp_injector = McpInjector(self.root_dir)
        self.governance_engine = GovernanceEngine()

        # 2. Phoenix 4 Core Sub-Components (UMB-CSE-001 v7.1)
        self.cac = CoherenceAttractorCore(self.root_dir, self.governance_engine)
        self.rcp = ReflexiveConsequenceProjector(self.root_dir)
        self.aow = AdaptiveOpportunityWeave(self.root_dir)
        self.msl = MethodologySelectorLayer()
        self.telemetry = TelemetryEngine()
        self.guca_executor = GUCAExecutor()

        # 3. Ethical Telemetry & ECS Scheduling Kernel
        self.ethos_logger = EthicalLogger("CoherentSynthesisEngine")
        self.world = World()
        self.registry = ResonanceRegistry()
        self.auditor = ResonanceAuditor(self.registry)
        self.executor = DeterministicParallelExecutor(max_workers=2)

        systems = self.registry.get_systems()
        compiler = ECSSystemCompiler(systems)
        self.graph = compiler.compile()
        self.graph.build()
        self.scheduler = LayeredScheduler(self.graph, self.executor)

    async def execute_audit_cycle(self) -> Dict[str, Any]:
        """Executes the Zero Entropy state validation using the Coherence Attractor Core (CAC)."""
        try:
            await self.ethos_logger.log_event("Initiating Zero Entropy Audit Cycle...", ProcessStatus.INFO)

            loom_state = self.loom_parser.extract_state()
            cac_result = self.cac.evaluate_coherence(loom_state)

            # ECS Layered execution for runtime determinism
            context = {"world": self.world}
            self.scheduler.execute(context)

            status = "STABLE" if cac_result.is_coherent else "DEGRADED"

            await self.ethos_logger.log_event(
                f"Audit Complete. Status: {status} | CI: {cac_result.coherence_index:.3f} | Entropy: {cac_result.entropy:.2f}",
                ProcessStatus.INFO,
            )

            self.selt_logger.record_synthesis(
                f"AUDIT_{status}",
                cac_result.entropy,
                [d.description for d in cac_result.dissonances],
            )

            return {
                "status": status,
                "coherence_index": cac_result.coherence_index,
                "contextual_integrity_score": cac_result.contextual_integrity_score,
                "entropy": cac_result.entropy,
                "dissonances": [d.dissonance_id for d in cac_result.dissonances],
                "dissonance_quests": cac_result.dissonance_quests,
            }
        except Exception as e:
            error_msg = f"AUDIT_HALTED: {e!s}"
            await self.ethos_logger.log_event(error_msg, ProcessStatus.ERROR)
            self.selt_logger.record_synthesis("HALTED", 1.0, [error_msg])
            return {"status": "HALTED", "error": error_msg}

    async def execute_expansion_cycle(self) -> Dict[str, Any]:
        """Executes autonomous tool registration from the Forge (.agent/skills/)."""
        skills_dir = os.path.join(self.root_dir, ".agent", "skills")
        findings = []
        registered_count = 0

        try:
            await self.ethos_logger.log_event("Initiating Autonomous Expansion Cycle...", ProcessStatus.INFO)

            if not os.path.exists(skills_dir):
                return {"status": "STATIC", "registered": 0, "findings": ["Skills directory not present."]}

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
            await self.ethos_logger.log_event(
                f"Expansion Cycle {status}. Registered {registered_count} tools.",
                ProcessStatus.INFO,
            )

            self.selt_logger.record_synthesis(f"EXPANSION_{status}", 0.0, findings)
            return {"status": status, "registered": registered_count, "findings": findings}
        except Exception as e:
            error_msg = f"EXPANSION_HALTED: {e!s}"
            await self.ethos_logger.log_event(error_msg, ProcessStatus.ERROR)
            self.selt_logger.record_synthesis("HALTED", 1.0, [error_msg])
            return {"status": "HALTED", "error": error_msg}

    async def synthesize_task(self, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Holistic synthesis loop: MSL selects methodology -> RCP simulates -> Pipeline executes -> CAC verifies."""
        await self.ethos_logger.log_event(f"Synthesizing Task: {task_spec.get('name', 'ANONYMOUS_TASK')}", ProcessStatus.INFO)

        # 1. Evaluate current state & select methodology (Athena's Gambit)
        loom_state = self.loom_parser.extract_state()
        state_snapshot = self.get_telemetry_snapshot()
        methodology = self.msl.select_methodology(task_spec, state_snapshot)

        # 2. Consequence simulation (RCP)
        sim_result = self.rcp.simulate_action(
            {"name": task_spec.get("name", "TASK"), "target_nodes": task_spec.get("targets", [])},
            state_snapshot,
        )

        if not sim_result.is_safe:
            await self.ethos_logger.log_event("Action halted due to high consequence risk score.", ProcessStatus.WARNING)
            return {
                "status": "BLOCKED_BY_RCP",
                "methodology": methodology.to_dict(),
                "simulation": sim_result.to_dict(),
                "telemetry": state_snapshot,
            }

        # 3. Execute GUCA Pipeline
        context = {
            "task_spec": task_spec,
            "loom_state": loom_state,
            "cac_engine": self.cac,
            "rcp_engine": self.rcp,
            "aow_engine": self.aow,
            "telemetry_engine": self.telemetry,
            "selt_logger": self.selt_logger,
            "cognitive_load": 35.0,
        }

        pipeline = [
            AuditCoherenceCommand(),
            ContextWeaveCommand(),
            EthicalEvaluationCommand(),
            OmniLogCommand(),
            EnactTranscendenceCommand(),
        ]
        pipeline_result = self.guca_executor.execute_commands(pipeline, context)

        # 4. Final Telemetry Vector
        final_telemetry = self.get_telemetry_snapshot()

        return {
            "status": "SYNTHESIZED",
            "methodology": methodology.to_dict(),
            "simulation": sim_result.to_dict(),
            "pipeline_summary": {
                "coherence_index": pipeline_result.get("coherence_index"),
                "graph_synergy_score": pipeline_result.get("graph_synergy_score"),
                "audit_status": pipeline_result.get("audit_status"),
                "transcendence_status": pipeline_result.get("transcendence_status"),
            },
            "telemetry": final_telemetry,
        }

    def get_telemetry_snapshot(self) -> Dict[str, Any]:
        """Calculates and returns the latest State Vector (V_State)."""
        loom_state = self.loom_parser.extract_state()
        cac_res = self.cac.evaluate_coherence(loom_state)
        aow_res = self.aow.analyze_synergies()
        msl_res = self.msl.select_methodology({"domain": "GENERAL", "complexity": 0.5})

        state_vector = self.telemetry.compute_state_vector(
            cac_result=cac_res.to_dict(),
            aow_result=aow_res.to_dict(),
            msl_result=msl_res.to_dict(),
            cognitive_load=28.5,
        )
        return state_vector.to_dict()

    async def run_full_synthesis(self) -> Dict[str, Any]:
        """The Master OMEGA Loop: Audits the system and expands if stable."""
        await self.ethos_logger.log_event("Starting Full System Synthesis...", ProcessStatus.INFO)

        audit_result = await self.execute_audit_cycle()

        if audit_result["status"] == "STABLE":
            expansion_result = await self.execute_expansion_cycle()
            result = {"audit": audit_result, "expansion": expansion_result}
        else:
            await self.ethos_logger.log_event("Expansion SKIPPED due to systemic entropy.", ProcessStatus.WARNING)
            result = {"audit": audit_result, "expansion": "SKIPPED_DUE_TO_ENTROPY"}

        result["telemetry"] = self.get_telemetry_snapshot()
        await self.ethos_logger.log_event("Full Synthesis Cycle Complete.", ProcessStatus.INFO)
        return result


async def main():
    engine = CoherentSynthesisEngine()
    final_state = await engine.run_full_synthesis()
    print(f"\n[*] SYNTHESIS COMPLETE:\n{json.dumps(final_state, indent=4)}")


if __name__ == "__main__":
    asyncio.run(main())
