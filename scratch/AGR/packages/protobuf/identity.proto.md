syntax = "proto3";

package agr.identity;

message Identity {

  string spiffe_id = 1;

  string workload = 2;

  string namespace = 3;

  string service_account = 4;

  repeated string roles = 5;
}