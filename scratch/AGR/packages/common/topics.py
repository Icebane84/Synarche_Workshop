from enum import StrEnum


class Topic(StrEnum):

    PARSER = "agr.parser"

    POLICY = "agr.policy"

    VALIDATION = "agr.validation"

    GRAPH = "agr.graph"

    SIMULATION = "agr.simulation"

    ARTIFACT = "agr.artifact"

    TELEMETRY = "agr.telemetry"

    SYSTEM = "agr.system"
