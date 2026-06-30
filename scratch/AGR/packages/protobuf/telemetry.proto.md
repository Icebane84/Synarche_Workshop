syntax = "proto3";

package agr.telemetry;

message Metrics {

    double system_coherence_metric = 1;

    int64 logic_propagation_velocity_ms = 2;

    double adaptive_bias_coefficient = 3;
}