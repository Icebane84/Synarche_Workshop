syntax = "proto3";

package agr.validation;

message ValidationRequest {

    string ast_json = 1;

}

message ValidationResult {

    bool passed = 1;

    repeated string findings = 2;

}

service ValidationAPI {

    rpc Validate(ValidationRequest)

        returns (ValidationResult);

}