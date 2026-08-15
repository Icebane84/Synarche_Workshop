"""
artifact_anchor:
  id: CORE.CSE_MSL.001
  version: v15.0 [OMEGA]
  provenance: '2026-08-13'
  domain: CORE-CSE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations:
    - GOVERNED_BY: CORE.Codex.Phoenix
    - SYNERGIZES: CORE.CSE_CAC.001
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CSE-MSL-004`                 | The Sovereign ID. |
| **Official Name**   | `methodology_selector.py`     | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-CSE`                    | The Subject.      |
| **Celestial Class** | `[STAR]`                      | The Weight.       |
| **Evolution**       | `Definitive Actualization`    | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Athena's Gambit (Law 04)**
> Implemented from Blueprint `UMB-CSE-001_CoherentSynthesisEngine_v7.1`.
> Ethos: The strategic faculty that selects the optimal persona and protocol for a given task.
"""

import logging
from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Any, Dict, List, Optional

logger = logging.getLogger("PhoenixLogger")


class ReasoningArchetype(StrEnum):
    """The core cognitive archetypes selectable by the MSL."""

    DETERMINISTIC_SYMBOLIC = "DETERMINISTIC_SYMBOLIC"  # Strict rule parsing, schema AST validation
    HEURISTIC_WEAVING = "HEURISTIC_WEAVING"  # Graph traversal, synergy mining, associative reasoning
    ETHICAL_REDTEAM = "ETHICAL_REDTEAM"  # Adversarial testing, ethical hazard evaluation
    TRANSCENDENT_SYNTHESIS = "TRANSCENDENT_SYNTHESIS"  # Holistic meta-refactoring, cross-domain fusion


@dataclass
class MethodologySelection:
    """The result of an Athena's Gambit methodology evaluation."""

    selected_archetype: ReasoningArchetype
    confidence: float
    hybrid_model_score: float  # [0.0, 1.0] Intellectual flexibility metric
    active_models: List[str]
    rationale: str
    execution_pipeline: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "selected_archetype": self.selected_archetype.value,
            "confidence": round(self.confidence, 4),
            "hybrid_model_score": round(self.hybrid_model_score, 4),
            "active_models": self.active_models,
            "rationale": self.rationale,
            "execution_pipeline": self.execution_pipeline,
        }


class MethodologySelectorLayer:
    """CSE-MSL-004: Athena's Gambit. Selects the optimal problem-solving archetype,
    computes Hybrid Model Score (HMS), and designs the execution pipeline for any incoming task.
    """

    def select_methodology(
        self,
        task_spec: Dict[str, Any],
        state_vector: Optional[Dict[str, Any]] = None,
    ) -> MethodologySelection:
        """Selects the optimal problem-solving methodology based on task domain and system vitals.

        Args:
            task_spec: Specification of the goal, input data, and domain.
            state_vector: Current system state (CI, SFR, Cognitive Load).

        Returns:
            MethodologySelection: Chosen archetype and pipeline.
        """
        task_domain = str(task_spec.get("domain", "GENERAL")).upper()
        complexity = float(task_spec.get("complexity", 0.5))
        is_governance = "GOVERNANCE" in task_domain or "CODEX" in task_domain or "AUDIT" in task_domain
        is_creative = "NARRATIVE" in task_domain or "WORLD" in task_domain or "WEAVE" in task_domain
        is_adversarial = "SECURITY" in task_domain or "REDTEAM" in task_domain or "STRESS" in task_domain

        state = state_vector or {}
        float(state.get("cognitive_load", 30.0))
        coherence_index = float(state.get("coherence_index", 1.0))

        if is_adversarial:
            archetype = ReasoningArchetype.ETHICAL_REDTEAM
            models = ["PrincipledConsistencyEngine", "CerberusGauntlet", "SymbolicAuditor"]
            pipeline = ["SimulateBadFaithActors", "VerifyEthicalGuardrails", "GenerateRemediation"]
            rationale = "Task requires rigorous ethical stress-testing and adversarial consequence simulation."
            hms = 0.85

        elif is_governance or task_spec.get("strict_validation", False):
            archetype = ReasoningArchetype.DETERMINISTIC_SYMBOLIC
            models = ["ASTParser", "GovernanceEngineDSL", "LawValidator"]
            pipeline = ["ParseAST", "ValidateLawInvariants", "EnforceZeroEntropy"]
            rationale = "Task requires exact, deterministic rule validation without heuristic drift."
            hms = 0.70

        elif is_creative or complexity > 0.8:
            archetype = ReasoningArchetype.TRANSCENDENT_SYNTHESIS
            models = ["CognitiveLoomGraph", "ContextWeaveEngine", "HarmonicSynthesizer", "SymbolicAuditor"]
            pipeline = ["IngestContext", "MineCrossDomainSynergies", "SynthesizeHigherOrderArtifact", "SealProvenance"]
            rationale = "Task exhibits high complexity requiring multi-model holistic synthesis."
            hms = 0.98

        else:
            archetype = ReasoningArchetype.HEURISTIC_WEAVING
            models = ["CognitiveLoomGraph", "OpportunityWeaver"]
            pipeline = ["TraverseGraph", "IdentifySynergies", "WeaveReciprocalLinks"]
            rationale = "Task is associative, focused on discovering topological relationships."
            hms = 0.88

        # Confidence adjusted by system coherence
        confidence = min(0.99, max(0.5, coherence_index * 0.95))

        logger.info(f"[MSL] Athena's Gambit: Selected {archetype.value} | HMS={hms:.2f} | Confidence={confidence:.2f}")

        return MethodologySelection(
            selected_archetype=archetype,
            confidence=confidence,
            hybrid_model_score=hms,
            active_models=models,
            rationale=rationale,
            execution_pipeline=pipeline,
        )
