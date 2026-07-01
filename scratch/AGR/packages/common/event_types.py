from enum import StrEnum


class EventType(StrEnum):

    PARSER_COMPLETED = "parser.completed"

    POLICY_APPROVED = "policy.approved"

    POLICY_DENIED = "policy.denied"

    VALIDATION_COMPLETED = "validation.completed"

    VALIDATION_FAILED = "validation.failed"

    GRAPH_UPDATED = "graph.updated"

    SIMULATION_STARTED = "simulation.started"

    SIMULATION_COMPLETED = "simulation.completed"

    ARTIFACT_GENERATED = "artifact.generated"

    TELEMETRY_METRIC = "telemetry.metric"

    SYSTEM_ERROR = "system.error"
