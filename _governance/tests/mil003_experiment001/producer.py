"""
artifact_anchor:
  id: GVRN.TEST.MIL003.EXP001.PRODUCER
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
import os
import sys
from pathlib import Path

# Add axion-core src to Python path
repo_root = Path(__file__).resolve().parents[3]
axion_core_src = repo_root / "axion-core" / "src"
if str(axion_core_src) not in sys.path:
    sys.path.insert(0, str(axion_core_src))

from engine.types import CognitiveEvent

def create_and_serialize_event() -> dict:
    # 1. Instantiate deterministic native CognitiveEvent
    raw_timestamp = datetime.datetime(2026, 8, 16, 13, 30, 0, 123456, tzinfo=datetime.timezone.utc)
    event = CognitiveEvent(
        event_id="e001-test-event-uuid4-fixture",
        event_type="COGNITIVE_EXPERIENCE",
        content="Synthesized cross-language semantic bridge verification payload.",
        source="Agent.TarotArtificer",
        timestamp=raw_timestamp,
        vector=[0.123456, -0.654321, 0.987654, 0.0, 0.42],
        importance=0.85,
        metadata={
            "session_id": "sess-omega-99",
            "priority_tier": 1,
            "nested": {"verified": True, "lossless": True}
        }
    )

    # 2. Map to EventContract v0.1 Wire Representation
    wire_contract = {
        "contract_version": "v0.1",
        "id": event.event_id,
        "source": event.source,
        "type": event.event_type,
        "payload": event.content,
        "timestamp": event.timestamp.isoformat(),
        "extension": {
            "kind": "cognitive",
            "data": {
                "vector": event.vector,
                "importance": event.importance,
                "metadata": event.metadata
            }
        }
    }

    # 3. Capture baseline producer ground truth for verification
    output_package = {
        "producer_ground_truth": {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            "content": event.content,
            "timestamp_iso": event.timestamp.isoformat(),
            "timestamp_epoch_ms": int(event.timestamp.timestamp() * 1000),
            "timestamp_microseconds": event.timestamp.microsecond,
            "vector": event.vector,
            "importance": event.importance,
            "metadata": event.metadata
        },
        "wire_payload": wire_contract
    }

    return output_package

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = create_and_serialize_event()
    out_path = Path(__file__).parent / "fixture.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"PRODUCER_SUCCESS: Fixture written to {out_path}")
