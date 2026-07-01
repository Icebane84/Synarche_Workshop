from dataclasses import dataclass, field
from datetime import datetime, UTC
import uuid


@dataclass(slots=True)
class EventEnvelope:
    """
    Canonical event envelope used throughout AGR.
    """

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    source: str = ""

    event_type: str = ""

    schema_version: str = "1.0.0"

    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    payload: dict = field(default_factory=dict)
