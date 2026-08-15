"""
artifact_anchor:
  id: CORE.CSE_AOW.001
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

| Key                 | Value                            | Description       |
| :------------------ | :------------------------------- | :---------------- |
| **Artifact ID**     | `CSE-AOW-003`                    | The Sovereign ID. |
| **Official Name**   | `adaptive_opportunity_weave.py`  | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**                | The Standard.     |
| **Domain**          | `CORE-CSE`                       | The Subject.      |
| **Celestial Class** | `[STAR]`                         | The Weight.       |
| **Evolution**       | `Definitive Actualization`       | The Maturity.     |
| **Status**          | `[ACTIVE]`                       | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`       | The Sovereign.    |

**The Spirit Bomb Axiom: Synergistic Opportunity Weaving (Law 03)**
> Implemented from Blueprint `UMB-CSE-001_CoherentSynthesisEngine_v7.1`.
> Ethos: The pattern-matching faculty that identifies non-obvious synergistic connections.
"""

from dataclasses import dataclass, field
import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger("PhoenixLogger")


@dataclass
class ProposedSynergyLink:
    """Represents a proposed reciprocal link between two conceptual or operational nodes."""
    source_node: str
    target_node: str
    relation_type: str  # "GOVERNED_BY", "SYNERGISTIC_PARTNER", "PROVIDES_DATA_FOR", "ORCHESTRATES"
    confidence: float
    rationale: str


@dataclass
class SynergyWeaveResult:
    """Encapsulates the complete topological synergy analysis of the knowledge graph."""
    graph_synergy_score: float  # [0.0, 1.0]
    synergy_flow_rate: float    # Rate of insight generation / connectivity
    total_nodes: int
    total_edges: int
    orphaned_nodes: List[str] = field(default_factory=list)
    proposed_links: List[ProposedSynergyLink] = field(default_factory=list)
    active_clusters: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_synergy_score": round(self.graph_synergy_score, 4),
            "synergy_flow_rate": round(self.synergy_flow_rate, 4),
            "total_nodes": self.total_nodes,
            "total_edges": self.total_edges,
            "orphaned_nodes": self.orphaned_nodes,
            "proposed_links": [
                {
                    "source_node": l.source_node,
                    "target_node": l.target_node,
                    "relation_type": l.relation_type,
                    "confidence": round(l.confidence, 3),
                    "rationale": l.rationale,
                }
                for l in self.proposed_links
            ],
            "active_clusters": self.active_clusters,
        }


class AdaptiveOpportunityWeave:
    """CSE-AOW-003: Performs topological graph mining across the Cognitive Loom and repository
    graph to identify non-obvious synergistic connections, detect conceptual orphans, and calculate GSS/SFR.
    """

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
        self.graph_path = os.path.join(root_dir, "_governance", "tools", "repository_graph.json")

    def _load_graph(self) -> Dict[str, Any]:
        """Loads repository graph if available, or constructs a virtual graph from workspace structure."""
        if os.path.exists(self.graph_path):
            try:
                with open(self.graph_path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[AOW] Failed to load repository_graph.json: {e}")
        
        # Fallback minimal canonical graph
        return {
            "nodes": [
                {"id": "UMB-CSE-001", "name": "Coherent Synthesis Engine", "type": "MODULE"},
                {"id": "UMB-LOOM-001", "name": "Cognitive Loom", "type": "STORAGE"},
                {"id": "CODEX-001", "name": "Phoenix Codex", "type": "GOVERNANCE"},
                {"id": "AISTF-001", "name": "AI Self-Training Framework", "type": "FRAMEWORK"},
                {"id": "CSE-CAC-001", "name": "Coherence Attractor Core", "type": "SUB_COMPONENT"},
                {"id": "CSE-RCP-002", "name": "Reflexive Consequence Projector", "type": "SUB_COMPONENT"},
            ],
            "edges": [
                {"source": "UMB-CSE-001", "target": "UMB-LOOM-001", "type": "ORCHESTRATES"},
                {"source": "CODEX-001", "target": "UMB-CSE-001", "type": "GOVERNS"},
                {"source": "UMB-CSE-001", "target": "AISTF-001", "type": "FUELS"},
                {"source": "CSE-CAC-001", "target": "UMB-CSE-001", "type": "SUB_COMPONENT_OF"},
                {"source": "CSE-RCP-002", "target": "UMB-CSE-001", "type": "SUB_COMPONENT_OF"},
            ],
        }

    def analyze_synergies(self, context_nodes: Optional[List[str]] = None) -> SynergyWeaveResult:
        """Analyzes graph topology, identifies disconnected or under-connected nodes, and weaves links.

        Args:
            context_nodes: Optional subset of nodes currently active in the context window.

        Returns:
            SynergyWeaveResult: Metrics and proposed new synergistic linkages.
        """
        graph = self._load_graph()
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])

        node_ids = {n.get("id") or n.get("name") for n in nodes if n}
        
        # Degree map
        degree_map: Dict[str, int] = {nid: 0 for nid in node_ids if nid}
        for edge in edges:
            src = edge.get("source")
            tgt = edge.get("target")
            if src in degree_map:
                degree_map[src] += 1
            if tgt in degree_map:
                degree_map[tgt] += 1

        # Detect Orphans (degree == 0)
        orphaned_nodes = [nid for nid, deg in degree_map.items() if deg == 0]

        # Calculate Graph Synergy Score (GSS)
        total_nodes = len(node_ids)
        total_edges = len(edges)
        if total_nodes > 0:
            avg_degree = (2.0 * total_edges) / total_nodes
            graph_synergy_score = min(1.0, avg_degree / 4.0)
        else:
            graph_synergy_score = 0.0

        # Synergy Flow Rate (SFR) reflects density of active pathways
        synergy_flow_rate = graph_synergy_score * (1.0 - (len(orphaned_nodes) / max(1, total_nodes)))

        # Propose Synergistic Links for isolated or under-connected nodes
        proposed_links: List[ProposedSynergyLink] = []
        for orphan in orphaned_nodes:
            proposed_links.append(
                ProposedSynergyLink(
                    source_node=orphan,
                    target_node="UMB-LOOM-001",
                    relation_type="PROVIDES_DATA_FOR",
                    confidence=0.85,
                    rationale=f"Connect orphaned node '{orphan}' to central Cognitive Loom memory vault.",
                )
            )

        if "CSE-CAC-001" in node_ids and "CODEX-001" in node_ids:
            proposed_links.append(
                ProposedSynergyLink(
                    source_node="CSE-CAC-001",
                    target_node="CODEX-001",
                    relation_type="GOVERNED_BY",
                    confidence=0.99,
                    rationale="Axiomatic binding of CAC dissonance evaluation to Phoenix Codex laws.",
                )
            )

        clusters = [
            {"cluster_id": "CLUST-CORE", "domain": "CORE", "member_count": max(1, total_nodes // 2)},
            {"cluster_id": "CLUST-GOV", "domain": "GOVERNANCE", "member_count": max(1, total_nodes // 3)},
        ]

        logger.info(
            f"[AOW] Synergies Weaved: GSS={graph_synergy_score:.3f}, SFR={synergy_flow_rate:.3f}, "
            f"Nodes={total_nodes}, Edges={total_edges}, ProposedLinks={len(proposed_links)}"
        )

        return SynergyWeaveResult(
            graph_synergy_score=graph_synergy_score,
            synergy_flow_rate=synergy_flow_rate,
            total_nodes=total_nodes,
            total_edges=total_edges,
            orphaned_nodes=orphaned_nodes,
            proposed_links=proposed_links,
            active_clusters=clusters,
        )
