"""
phoenix_framework/commands/executor.py

Command Executor — the runtime enforcement point.

This is where the full Doc 4 stack comes together:

    ARCHITECTURAL PRINCIPLES
            ↓
        UMB (ADR)           ← adr_refs on every command
            ↓
   GOVERNANCE ENGINE        ← GovernanceEngine.evaluate()
            ↓
      GUCA (API)            ← CommandRegistry.get()
            ↓
    EXECUTION LAYER         ← CommandExecutor.execute()
            ↓
      SELT (TELEMETRY)      ← SELTPipeline.emit_many()
            ↓
   OMNI-LOG (ANALYSIS)      ← OmniLog.record()
            ↓
AISTF (CONTINUOUS IMPROV.)  ← AISTFCycle.run_cycle()
            ↓
   UPDATED GOVERNANCE        ← human reviews + accepts/rejects recs

Every execute() call:
  1. Resolves the command from the registry
  2. Runs governance evaluation (policy-as-code)
  3. Produces a Decision via the DOL
  4. Emits SELT events
  5. Writes to OMNI-LOG
  6. Returns Decision + OMNI-LOG entry for human inspection
"""

from __future__ import annotations
from typing import Any, Callable, Optional
import uuid

from phoenix_framework.core.types import SELTEvent, RiskLevel
from phoenix_framework.core.principles import assert_principle, PrincipleViolationError
from phoenix_framework.commands.registry import CommandRegistry, CommandNotFoundError
from phoenix_framework.governance.engine import GovernanceEngine
from phoenix_framework.orchestration.dol import DecisionOrchestrationLayer, DOLInput
from phoenix_framework.telemetry.pipeline import SELTPipeline, OmniLog
from phoenix_framework.aistf.cycle import AISTFCycle


class HumanApprovalRequired(Exception):
    """
    Raised when a command requires human approval before execution can proceed.
    The caller must collect human authorization and re-submit.
    """
    def __init__(self, decision, message: str):
        self.decision = decision
        super().__init__(message)


class PolicyBlockedError(Exception):
    """Raised when governance policies block a command from executing."""
    def __init__(self, decision, violations):
        self.decision = decision
        self.violations = violations
        super().__init__(
            f"Command blocked by {len(violations)} policy violation(s). "
            "See decision.policy_results for details."
        )


class CommandExecutor:
    """
    The unified runtime executor.

    All Phoenix 'CMD:' invocations go through this class.
    No command may run without passing governance evaluation first.

    Usage:
        result = executor.execute(
            command_id="CMD-QCL-001",
            parameters={"query": "What is the current architecture?"},
            context={"read_only": True, "session_id": "abc123"},
            handler=my_rag_query_fn,
        )
    """

    def __init__(
        self,
        registry: CommandRegistry,
        governance: GovernanceEngine,
        dol: DecisionOrchestrationLayer,
        selt: SELTPipeline,
        omni_log: OmniLog,
        aistf: AISTFCycle,
    ):
        self._registry = registry
        self._gov = governance
        self._dol = dol
        self._selt = selt
        self._omni_log = omni_log
        self._aistf = aistf

    def execute(
        self,
        command_id: str,
        parameters: dict[str, Any],
        context: dict[str, Any],
        handler: Optional[Callable[..., Any]] = None,
        trace_id: Optional[str] = None,
        authorization_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Execute a command through the full governance stack.

        Args:
            command_id:        GUCA command ID (e.g. "CMD-QCL-001")
            parameters:        Command input parameters
            context:           Execution context (session_id, read_only, handles_user_data, etc.)
            handler:           Optional callable that implements the command's actual logic.
                               Receives (parameters, context) → returns dict.
                               If None, the framework validates + returns the Decision only.
            trace_id:          Optional — generated if not provided (P1 compliance)
            authorization_key: Required for R4/R5 commands

        Returns:
            {
                "trace_id": str,
                "decision": Decision,
                "omni_log_entry": OmniLogEntry,
                "result": dict | None,   # handler output if provided
                "kpis": dict,
            }

        Raises:
            CommandNotFoundError:    command_id not in registry
            PolicyBlockedError:      governance policies blocked execution
            HumanApprovalRequired:   R4/R5 command needs human gate
            PrincipleViolationError: architectural principle violated
        """
        trace_id = trace_id or str(uuid.uuid4())

        # --- P1: trace_id must be present before anything else runs ---
        assert_principle("P1", bool(trace_id), "trace_id is empty at executor entry")

        # --- Resolve command ---
        command = self._registry.get(command_id)

        # --- Build DOL input ---
        dol_input = DOLInput(
            command_id=command_id,
            parameters=parameters,
            context=context,
            trace_id=trace_id,
            adr_refs=command.adr_refs,
        )

        # --- Decision Orchestration Layer ---
        decision, selt_events = self._dol.decide(dol_input, command)

        # --- Emit all SELT events (P3) ---
        self._selt.emit_many(selt_events)

        # --- Handle human approval gate ---
        if decision.requires_human_review:
            if authorization_key is None:
                entry = self._omni_log.record(decision, command, execution_result=None)
                raise HumanApprovalRequired(
                    decision,
                    f"Command '{command_id}' (risk={command.risk_level.value}) "
                    f"requires human approval. Re-submit with authorization_key. "
                    f"Trace: {trace_id}"
                )

        # --- Handle policy blocks ---
        if not decision.approved and not decision.requires_human_review:
            violations = [
                pid for pid, passed in decision.policy_results.items() if not passed
            ]
            self._selt.emit(SELTEvent(
                trace_id=trace_id,
                command_id=command_id,
                event_type="EXECUTION_BLOCKED",
                payload={"violated_policies": violations},
                outcome="blocked",
                risk_level=command.risk_level,
            ))
            entry = self._omni_log.record(decision, command, execution_result=None)
            raise PolicyBlockedError(decision, violations)

        # --- Execute handler (if provided) ---
        execution_result: Optional[dict] = None
        if handler:
            self._selt.emit(SELTEvent(
                trace_id=trace_id,
                command_id=command_id,
                event_type="COMMAND_START",
                payload={"parameters": parameters},
                outcome="pending",
                risk_level=command.risk_level,
            ))
            try:
                execution_result = handler(parameters, context)
                self._selt.emit(SELTEvent(
                    trace_id=trace_id,
                    command_id=command_id,
                    event_type="COMMAND_SUCCESS",
                    payload={"result_keys": list(execution_result.keys()) if execution_result else []},
                    outcome="success",
                    risk_level=command.risk_level,
                ))
            except Exception as exc:
                self._selt.emit(SELTEvent(
                    trace_id=trace_id,
                    command_id=command_id,
                    event_type="COMMAND_FAIL",
                    payload={"error": str(exc)},
                    outcome="failure",
                    risk_level=command.risk_level,
                ))
                raise

        # --- OMNI-LOG record (P4) ---
        omni_entry = self._omni_log.record(decision, command, execution_result)

        # --- AISTF cycle pass ---
        self._aistf.run_cycle()

        return {
            "trace_id": trace_id,
            "decision": decision,
            "omni_log_entry": omni_entry,
            "result": execution_result,
            "kpis": self._dol.compute_kpis(),
        }
