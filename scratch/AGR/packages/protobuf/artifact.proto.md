syntax = "proto3";

package agr.artifact;

message ArtifactRequest {

    string specification = 1;

}

message ArtifactResponse {

    string project_path = 1;

}

service ArtifactAPI {

    rpc Generate(ArtifactRequest)

        returns (ArtifactResponse);

}