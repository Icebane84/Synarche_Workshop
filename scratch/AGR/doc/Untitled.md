Recommended Stream Layout:

AGR.SYSTEM.*

AGR.PARSER.*

AGR.POLICY.*

AGR.VALIDATION.*

AGR.GRAPH.*

AGR.SIMULATION.*

AGR.ARTIFACT.*

AGR.TELEMETRY.*

Each service owns one or more subjects and subscribes only to the events it needs.

Specification
        │
        ▼
Parser
        │
        ▼
Event Bus
        │
 ┌──────┼─────────┐
 ▼      ▼         ▼
Policy Graph Telemetry
 │
 ▼
Validation
 │
 ▼
Simulation
 │
 ▼
Artifact Generator
