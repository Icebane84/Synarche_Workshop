from typing import Any, List


class SELTLogger:
    """Immutable telemetry and Dissonance tracking logger."""

    def __init__(self):
        self.logs: List[dict] = []

    def log_event(self, frame: int, event_type: str, payload: Any) -> None:
        entry = {"frame": frame, "event_type": event_type, "payload": payload}
        self.logs.append(entry)

    def log_dissonance(self, frame: int, reason: str) -> None:
        self.log_event(frame, "DISSONANCE_DETECTED", {"reason": reason})

