package phoenix.finalize.graph_connectivity

import rego.v1

default allow := false

required_forward_type := "DERIVES_FROM"
required_reverse_type := "HAS_DERIVATION"

allow if {
	input.operation == "FINALIZE_PROPOSAL"
	valid_compiled_block
	has_forward_edge
	has_reverse_edge
}

deny contains "FINALIZE_PROPOSAL requires compiled_block.entry_id" if {
	not non_empty_string(input.compiled_block.entry_id)
}

deny contains "FINALIZE_PROPOSAL requires compiled_block.parent_hash" if {
	not non_empty_string(input.compiled_block.parent_hash)
}

deny contains "FINALIZE_PROPOSAL must create forward DERIVES_FROM edge" if {
	input.operation == "FINALIZE_PROPOSAL"
	not has_forward_edge
}

deny contains "FINALIZE_PROPOSAL must create reverse HAS_DERIVATION edge in the same transaction" if {
	input.operation == "FINALIZE_PROPOSAL"
	not has_reverse_edge
}

valid_compiled_block if {
	non_empty_string(input.compiled_block.entry_id)
	non_empty_string(input.compiled_block.parent_hash)
	is_array(input.compiled_block.edges)
}

has_forward_edge if {
	some edge in input.compiled_block.edges
	edge.from == input.compiled_block.entry_id
	edge.to == input.compiled_block.parent_hash
	edge.type == required_forward_type
}

has_reverse_edge if {
	some edge in input.compiled_block.edges
	edge.from == input.compiled_block.parent_hash
	edge.to == input.compiled_block.entry_id
	edge.type == required_reverse_type
}

non_empty_string(value) if {
	is_string(value)
	count(value) > 0
}
