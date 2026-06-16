"""
artifact_anchor:
  id: CORE.SYNERGY.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-ECS-SYN-001`             | The Sovereign ID. |
| **Official Name**   | `synergy.py`                  | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-ECS`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Synergistic Resonance (Law 21)**
> Implemented from Blueprint `GVRN.REG.EcsSynergy.md`.
> Ethos: Coherence through Analysis.
"""

import logging
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

from .component import ComponentStore


@dataclass
class SynergyMetrics:
    """Mathematical representation of engine coherence and structural density.

    Attributes:
        node_density (float): Average number of components per active entity.
        coupling_resonance (float): Diversity of component types, normalized.
        orphanage_factor (float): Ratio of entities without active system targeting.
        coherence_index (float): The aggregate quality score of the ECS state.

    """

    node_density: float
    coupling_resonance: float
    orphanage_factor: float
    coherence_index: float


class SynergySystem:
    """Analyzes the ECS state to calculate the Graph Synergy Score (GSS).
    A core component of the Coherent Synthesis Engine (CSE) logic.

    The SynergySystem identifies 'Dissonance' (fragmented data) and
    calculates the 'Coherence Index' (CI) of the simulation.

    Public interface
    ----------------
    calculate_gss()
        Full ECS scan — returns SynergyMetrics directly.
    detect(nodes)
        Scheduler-facing adapter.  Accepts the CognitiveScheduler's
        ``graph.nodes`` dict (``Dict[int, CognitiveNode]``) and returns a
        ``List[Dict[str, Any]]`` of pattern-hit records suitable for
        appending to ``CognitiveState.pattern_hits``.
    """

    # Coherence index below this level emits a 'low_coherence' pattern hit.
    LOW_COHERENCE_THRESHOLD: float = 0.25
    # Orphanage factor above this level emits an 'high_orphanage' pattern hit.
    HIGH_ORPHANAGE_THRESHOLD: float = 0.50

    def __init__(self, component_store: ComponentStore) -> None:
        """Initializes the synergy system with a reference to the component store.

        Args:
            component_store (ComponentStore): The store to analyze.

        """
        self.store = component_store
        self.last_metrics: Optional[SynergyMetrics] = None
        self.logger = logging.getLogger("PhoenixLogger")

    def calculate_gss(self) -> SynergyMetrics:
        """Performs a full scan of the ComponentStore to compute structural synergy.
        Evaluates density, coupling, and aggregate coherence.

        Returns:
            SynergyMetrics: The calculated state metrics.

        """
        # 1. Track all entities that have at least one component
        entities_with_data: Set[uuid.UUID] = set()
        total_component_instances: int = 0

        for _comp_type, entity_map in self.store.stores.items():
            entities_with_data.update(entity_map.keys())
            total_component_instances += len(entity_map)

        num_entities = len(entities_with_data)

        # 2. Node Density (ND)
        # Average components per entity. Higher density = more complex entity logic.
        node_density = (
            (total_component_instances / num_entities) if num_entities > 0 else 0.0
        )

        # 3. Coupling Resonance (CR)
        # For now, we calculate this as the diversity of component types in use.
        num_types = len(self.store.stores)
        coupling_resonance = min(
            1.0, num_types / 10.0
        )  # Normalized to a base of 10 types

        # 4. Orphanage Factor (OF)
        # Placeholder: This will eventually track entities not targeted by any System in the DAG.
        orphanage_factor = 0.0

        # 5. Coherence Index (CI) - The master score (0.0 to 1.0)
        # We weight node complexity and type diversity.
        ci = (min(1.0, node_density / 5.0) * 0.5) + (coupling_resonance * 0.5)

        metrics = SynergyMetrics(
            node_density=node_density,
            coupling_resonance=coupling_resonance,
            orphanage_factor=orphanage_factor,
            coherence_index=ci,
        )

        self.last_metrics = metrics

        if ci < self.LOW_COHERENCE_THRESHOLD:
            self.logger.warning(
                f"LOW COHERENCE DETECTED: CI={ci:.4f}. Simulation may be fragmented."
            )

        return metrics

    def detect(self, nodes: Dict[int, Any]) -> List[Dict[str, Any]]:
        """Scheduler-facing adapter for the Π (pattern-mining) phase.

        Runs :meth:`calculate_gss` against the ECS component store, then
        translates the resulting :class:`SynergyMetrics` into the
        ``List[Dict]`` format expected by
        ``CognitiveState.pattern_hits``.

        The ``nodes`` argument mirrors the ``CognitiveGraph.nodes`` dict
        (``Dict[int, CognitiveNode]``) passed in by
        :class:`~engine.cognitive_scheduler.CognitiveScheduler._stage_pattern`.
        It is accepted for interface symmetry and future use (e.g. cross-
        referencing graph nodes against ECS entities) but is not consumed
        by the current implementation.

        Args:
            nodes: The scheduler's active ``CognitiveGraph.nodes`` dict.

        Returns:
            List of pattern-hit dicts.  Each dict contains at minimum a
            ``"trigger"`` key so the scheduler can log and react to it.
            Returns an empty list when no anomalies are detected.
        """
        metrics = self.calculate_gss()
        hits: List[Dict[str, Any]] = []

        if metrics.coherence_index < self.LOW_COHERENCE_THRESHOLD:
            hits.append(
                {
                    "trigger": "low_coherence",
                    "coherence_index": round(metrics.coherence_index, 4),
                    "node_density": round(metrics.node_density, 4),
                    "coupling_resonance": round(metrics.coupling_resonance, 4),
                }
            )
            self.logger.info(
                f"[Π] Synergy hit: low_coherence CI={metrics.coherence_index:.4f} "
                f"(threshold={self.LOW_COHERENCE_THRESHOLD})"
            )

        if metrics.orphanage_factor > self.HIGH_ORPHANAGE_THRESHOLD:
            hits.append(
                {
                    "trigger": "high_orphanage",
                    "orphanage_factor": round(metrics.orphanage_factor, 4),
                }
            )
            self.logger.info(
                f"[Π] Synergy hit: high_orphanage OF={metrics.orphanage_factor:.4f} "
                f"(threshold={self.HIGH_ORPHANAGE_THRESHOLD})"
            )

        return hits

    def __repr__(self) -> str:
        """Returns a string representation of the synergy system state."""
        ci_str = (
            f"{self.last_metrics.coherence_index:.4f}" if self.last_metrics else "N/A"
        )
        return f"<SynergySystem CI={ci_str}>"
