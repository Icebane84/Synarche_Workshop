syntax = "proto3";

package agr.simulation;

message SimulationRequest {

    string artifact = 1;

}

message SimulationResult {

    bool success = 1;

    double score = 2;

    string report = 3;

}

service SimulationAPI {

    rpc Run(SimulationRequest)

        returns (SimulationResult);

}