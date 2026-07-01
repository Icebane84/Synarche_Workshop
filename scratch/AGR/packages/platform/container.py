from dataclasses import dataclass

from packages.common.event_bus import EventBus


@dataclass(slots=True)
class PlatformContainer:

    event_bus: EventBus

    logger: object | None = None

    telemetry: object | None = None

    graph: object | None = None

    policy: object | None = None
