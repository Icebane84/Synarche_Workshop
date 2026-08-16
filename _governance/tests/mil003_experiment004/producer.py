"""
artifact_anchor:
  id: GVRN.TEST.MIL003.EXP004.PRODUCER
  version: v15.0 [OMEGA]
  provenance: '2026-08-16'
  domain: GVRN-TEST
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_TEST_COMPONENT
  relations:
    - GOVERNED_BY: CORE.Codex.Phoenix
    - EMBODIES: GVRN.HARMONIZATION.Milestone002.Contracts
"""

import datetime
import json
import sys
from pathlib import Path

# Add axion-core src to Python path
repo_root = Path(__file__).resolve().parents[3]
axion_core_src = repo_root / "axion-core" / "src"
if str(axion_core_src) not in sys.path:
    sys.path.insert(0, str(axion_core_src))

from engine.types import CognitiveEdge

def create_and_serialize_edges() -> dict:
    created_dt = datetime.datetime(2026, 8, 16, 12, 0, 0, tzinfo=datetime.timezone.utc)

    # 1. Edge 1: SIMILAR_TO (Symmetric Semantic Relationship)
    edge_similar = CognitiveEdge(
        edge_id="edge-e004-similar-001",
        source_id=1042,
        target_id=1088,
        rel_type="SIMILAR_TO",
        strength=0.88,
        created_at=created_dt,
        metadata={"similarity_metric": "cosine", "threshold": 0.85}
    )

    # 2. Edge 2: CAUSED_BY (Asymmetric Causal Relationship)
    edge_caused = CognitiveEdge(
        edge_id="edge-e004-caused-002",
        source_id=1042,
        target_id=1001,
        rel_type="CAUSED_BY",
        strength=0.95,
        created_at=created_dt,
        metadata={"causal_confidence": 0.95, "mechanism": "temporal_precedence"}
    )

    # 3. Edge 3: GOVERNED_BY (Asymmetric Governance Relationship)
    edge_governed = CognitiveEdge(
        edge_id="edge-e004-governed-003",
        source_id=1042,
        target_id=2001,
        rel_type="GOVERNED_BY",
        strength=1.0,
        created_at=created_dt,
        metadata={"law_anchor": "CORE.Codex.Phoenix", "enforceable": True}
    )

    def serialize_edge(edge: CognitiveEdge) -> dict:
        return {
            "contract_version": "v0.1",
            "id": edge.edge_id,
            "source": {
                "domain": "RUNTIME_INSTANCE",
                "token_type": "INTEGER_PK",
                "value": edge.source_id
            },
            "target": {
                "domain": "RUNTIME_INSTANCE",
                "token_type": "INTEGER_PK",
                "value": edge.target_id
            },
            "type": edge.rel_type,
            "extensions": {
                "runtime": {
                    "strength": edge.strength,
                    "created_at": edge.created_at.isoformat(),
                    "metadata": edge.metadata
                }
            }
        }

    output_pkg = {
        "producer_ground_truth": {
            "edges": [
                {
                    "edge_id": edge_similar.edge_id,
                    "source_id": edge_similar.source_id,
                    "target_id": edge_similar.target_id,
                    "rel_type": edge_similar.rel_type,
                    "strength": edge_similar.strength,
                    "created_at_iso": edge_similar.created_at.isoformat(),
                    "metadata": edge_similar.metadata,
                    "expected_semantics": "SYMMETRIC"
                },
                {
                    "edge_id": edge_caused.edge_id,
                    "source_id": edge_caused.source_id,
                    "target_id": edge_caused.target_id,
                    "rel_type": edge_caused.rel_type,
                    "strength": edge_caused.strength,
                    "created_at_iso": edge_caused.created_at.isoformat(),
                    "metadata": edge_caused.metadata,
                    "expected_semantics": "ASYMMETRIC_CAUSAL"
                },
                {
                    "edge_id": edge_governed.edge_id,
                    "source_id": edge_governed.source_id,
                    "target_id": edge_governed.target_id,
                    "rel_type": edge_governed.rel_type,
                    "strength": edge_governed.strength,
                    "created_at_iso": edge_governed.created_at.isoformat(),
                    "metadata": edge_governed.metadata,
                    "expected_semantics": "ASYMMETRIC_GOVERNANCE"
                }
            ]
        },
        "wire_payload": {
            "edge_similar": serialize_edge(edge_similar),
            "edge_caused": serialize_edge(edge_caused),
            "edge_governed": serialize_edge(edge_governed)
        }
    }

    return output_pkg

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = create_and_serialize_edges()
    out_path = Path(__file__).parent / "fixture.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"PRODUCER_SUCCESS: Edge fixture written to {out_path}")
