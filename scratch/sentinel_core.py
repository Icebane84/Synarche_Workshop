# c:\Users\Chris\Synarche_Workspace\axion-core\src\sentinel\sentinel_core.py
"""
This module contains the core implementation of The Sentinel, the meta-cognitive
oversight and governance enforcement engine for the Phoenix Protocol.

Governed by: UMB-SENTINEL-001, OGLN.Architecture.LayerProtocol
"""

import time
from enum import Enum, auto
from typing import Any, Dict, List, NamedTuple


class Verdict(Enum):
	"""
	The binary judgment returned by The Sentinel after an Axiomatic Resonance Check.
	"""
	AFFIRM = auto()    # The action is coherent and may proceed.
	ADMONISH = auto()  # The action is dissonant, must be halted, and requires review.


class DissonanceReport(NamedTuple):
	"""
	A structured report generated when an ADMONISH verdict is issued.
	"""
	timestamp: float
	action_id: str
	checked_action: Dict[str, Any]
	violated_axioms: List[str]
	reasoning: str


class Sentinel:
	"""
	Acts as the system's "internal conscience" and "Guardian of Coherence."

	It maintains integrity through The Vigil, a continuous three-phase cycle:
	1. The Watchful Eye (Observation): Intercepts a proposed action.
	2. The Axiomatic CORE (Analysis): Validates the action against core principles.
	3. The Resonant Voice (Judgment): Issues a verdict.
	"""

	def __init__(self, codex_axioms: Dict[str, callable]):
		"""
		Initializes The Sentinel with a read-only cache of the Phoenix Codex axioms.

		Args:
			codex_axioms: A dictionary where keys are axiom IDs (e.g., "CODEX-001.LAW.1")
						  and values are validation functions that return True if the
						  axiom is upheld, False otherwise.
		"""
		if not codex_axioms:
			raise ValueError("Sentinel requires a non-empty set of codex_axioms for governance.")
		self._codex_axioms = codex_axioms
		print("Sentinel Core Initialized. The Vigil has begun.")

	def perform_vigil(self, action_id: str, proposed_action: Dict[str, Any]) -> Verdict:
		"""
		Executes the full three-phase Vigil cycle on a proposed action.

		This is the primary public method of The Sentinel.

		Args:
			action_id: A unique identifier for the action being checked.
			proposed_action: The action payload to be validated.

		Returns:
			A Verdict enum (AFFIRM or ADMONISH).
		"""
		print(f"[Sentinel/WatchfulEye]: Intercepted action '{action_id}'. Commencing analysis.")

		# Phase 2: The Axiomatic CORE
		violated_axioms = self._run_axiomatic_core_check(proposed_action)

		# Phase 3: The Resonant Voice
		if violated_axioms:
			verdict = Verdict.ADMONISH
			report = self._generate_dissonance_report(action_id, proposed_action, violated_axioms)
			print(f"[Sentinel/ResonantVoice]: Verdict: {verdict.name}. Dissonance detected.")
			# In a real system, this report would be dispatched to a Dissonance Engine.
			# For now, we'll just print the reasoning.
			print(f"  > Reasoning: {report.reasoning}")
		else:
			verdict = Verdict.AFFIRM
			print(f"[Sentinel/ResonantVoice]: Verdict: {verdict.name}. Action is coherent.")

		return verdict

	def _run_axiomatic_core_check(self, proposed_action: Dict[str, Any]) -> List[str]:
		"""
		Performs the Axiomatic Resonance Check, validating the action against all axioms.

		Args:
			proposed_action: The action payload.

		Returns:
			A list of axiom IDs that were violated. An empty list means no violations.
		"""
		violations = []
		for axiom_id, validation_func in self._codex_axioms.items():
			try:
				if not validation_func(proposed_action):
					violations.append(axiom_id)
			except Exception as e:
				# If a validation function itself fails, it's a critical error.
				print(f"[Sentinel/ERROR]: Axiom check for '{axiom_id}' failed with exception: {e}")
				violations.append(f"{axiom_id} (RUNTIME_ERROR)")
		return violations

	def _generate_dissonance_report(
		self,
		action_id: str,
		action: Dict[str, Any],
		violations: List[str]
	) -> DissonanceReport:
		"""
		Constructs a formal DissonanceReport when a violation is detected.
		"""
		reason = (
			f"Action violates {len(violations)} core axiom(s): "
			f"{', '.join(violations)}. Execution halted pending review."
		)
		return DissonanceReport(
			timestamp=time.time(),
			action_id=action_id,
			checked_action=action,
			violated_axioms=violations,
			reasoning=reason
		)

# Example Usage (Conceptual)
if __name__ == '__main__':
	# Define some simple validation functions representing Codex Axioms
	def check_law_003(action: Dict) -> bool:
		# Sentinel's Oath: Must be traceable
		return 'trace_id' in action.get('metadata', {})

	def check_law_010(action: Dict) -> bool:
		# Preservation Mandate: No destructive deletes
		return action.get('operation') != 'DELETE_HARD'

	AXIOM_REGISTRY = {
		"CODEX-001.LAW.003": check_law_003,
		"CODEX-001.LAW.010": check_law_010,
	}

	# Initialize the Sentinel
	sentinel = Sentinel(codex_axioms=AXIOM_REGISTRY)

	print("\n--- [Simulation 1: Coherent Action] ---")
	coherent_action = {
		"operation": "CREATE_ARTIFACT",
		"payload": {"id": "UMB-TEST-001", "content": "..."},
		"metadata": {"trace_id": "trace-123"}
	}
	sentinel.perform_vigil("action-001", coherent_action)

	print("\n--- [Simulation 2: Dissonant Action (No Trace)] ---")
	dissonant_action_1 = {
		"operation": "UPDATE_ARTIFACT",
		"payload": {"id": "UMB-TEST-001", "content": "new content"},
		"metadata": {}  # Missing trace_id
	}
	sentinel.perform_vigil("action-002", dissonant_action_1)

	print("\n--- [Simulation 3: Dissonant Action (Destructive)] ---")
	dissonant_action_2 = {
		"operation": "DELETE_HARD", # Violates Law 010
		"payload": {"id": "UMB-TEST-001"},
		"metadata": {"trace_id": "trace-456"}
	}
	sentinel.perform_vigil("action-003", dissonant_action_2)
