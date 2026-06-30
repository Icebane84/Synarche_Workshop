syntax = "proto3";

package agr.common;

message Empty {}

message Status {
  bool success = 1;
  string message = 2;
}

message Timestamp {
  int64 unix_seconds = 1;
}