"""
artifact_anchor:
  id: GVRN.TEST.MIL003.EXP003.PRODUCER
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

from logic.memory.memory_system import MemoryEntry, MemoryProtocols

def create_and_serialize_memory() -> dict:
    created_dt = datetime.datetime(2026, 7, 16, 12, 0, 0, tzinfo=datetime.timezone.utc)
    last_retrieved_dt = datetime.datetime(2026, 8, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

    # 1. Instantiate native MemoryEntry (Layer 2 Kinetic memory with 15 days elapsed since retrieval)
    entry = MemoryEntry(
        id=1042,
        content="Autonomous cognitive loop execution and boundary verification protocols.",
        domain="CognitiveArchitecture",
        relevance=0.85,
        confidence=0.98,
        tags=["harmonization", "runtime", "e003"],
        state="Active",
        source="Agent.MasterArtificer",
        usage_count=12,
        layer=2,
        vector=[0.11, 0.22, -0.33, 0.44, 0.55],
        created_at=created_dt,
        last_retrieved=last_retrieved_dt
    )

    # 2. Execute authoritative decay & PAD-SIP activation calculation
    entry.decay()
    computed_activation = entry.activation_score

    # 3. Serialize to MemoryNodeContract v0.1 Wire Representation
    wire_contract = {
        "contract_version": "v0.1",
        "id": entry.id,
        "content": entry.content,
        "domain": entry.domain,
        "tags": entry.tags,
        "layer": entry.layer,
        "state": entry.state,
        "usage_count": entry.usage_count,
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "last_access": entry.last_retrieved.isoformat() if entry.last_retrieved else None,
        "relevance": entry.relevance,
        "confidence": entry.confidence,
        "vector": entry.vector,
        "derived_activation": round(computed_activation, 6)
    }

    output_pkg = {
        "producer_ground_truth": {
            "id": entry.id,
            "content": entry.content,
            "domain": entry.domain,
            "tags": entry.tags,
            "layer": entry.layer,
            "state": entry.state,
            "usage_count": entry.usage_count,
            "created_at_iso": entry.created_at.isoformat(),
            "last_access_iso": entry.last_retrieved.isoformat(),
            "relevance": entry.relevance,
            "confidence": entry.confidence,
            "vector": entry.vector,
            "activation_score": computed_activation,
            "recency_halflife_days": MemoryProtocols.RECENCY_HALFLIFE
        },
        "wire_payload": wire_contract
    }

    return output_pkg

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = create_and_serialize_memory()
    out_path = Path(__file__).parent / "fixture.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"PRODUCER_SUCCESS: Memory fixture written to {out_path}")
