package phoenix.graph.anti_entropy_merge

import rego.v1

default allow := false

allow if {
	input.operation == "MERGE_GRAPH_STATE"
	input.merge_strategy == "CRDT"
	input.properties.commutative == true
	input.properties.associative == true
	input.properties.idempotent == true
	not uses_lww
}

deny contains "distributed graph merge must use CRDT strategy" if {
	input.operation == "MERGE_GRAPH_STATE"
	input.merge_strategy != "CRDT"
}

deny contains "merge function must be commutative" if {
	input.operation == "MERGE_GRAPH_STATE"
	input.properties.commutative != true
}

deny contains "merge function must be associative" if {
	input.operation == "MERGE_GRAPH_STATE"
	input.properties.associative != true
}

deny contains "merge function must be idempotent" if {
	input.operation == "MERGE_GRAPH_STATE"
	input.properties.idempotent != true
}

deny contains "timestamp or lexicographic last-writer-wins is not LAW-031 compliant" if {
	uses_lww
}

uses_lww if {
	input.merge_strategy == "LWW"
}

uses_lww if {
	input.conflict_resolution == "timestamp_then_lexicographic"
}
