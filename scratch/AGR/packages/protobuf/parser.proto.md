syntax = "proto3";

package agr.parser;

message ParseRequest {

    string source = 1;

}

message AST {

    string json = 1;

}

service ParserAPI {

    rpc Parse(ParseRequest)
        returns (AST);

}