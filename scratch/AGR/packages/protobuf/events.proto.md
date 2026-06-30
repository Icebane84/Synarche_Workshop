syntax = "proto3";

package agr.events;

enum EventType {

    UNKNOWN = 0;

    PARSED = 1;

    POLICY_APPROVED = 2;

    POLICY_DENIED = 3;

    VALIDATED = 4;

    SIMULATION_STARTED = 5;

    SIMULATION_COMPLETED = 6;

    ARTIFACT_GENERATED = 7;

    ERROR = 8;

}

message Event {

    EventType type = 1;

    string payload = 2;

    int64 timestamp = 3;

}