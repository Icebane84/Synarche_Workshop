syntax = "proto3";

package agr.policy;

import "identity.proto";
import "telemetry.proto";

message PolicyRequest {

    agr.identity.Identity identity = 1;

    agr.telemetry.Metrics metrics = 2;

    string ast_json = 3;
}

message PolicyDecision {

    bool allow = 1;

    bool quarantined = 2;

    repeated string violations = 3;
}

service PolicyAPI {

    rpc Evaluate(PolicyRequest)
        returns (PolicyDecision);

}