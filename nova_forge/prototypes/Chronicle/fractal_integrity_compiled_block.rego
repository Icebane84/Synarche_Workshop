package phoenix.fractal.compiled_block

import rego.v1

default allow := false

required_policy_refs := {"LAW-004", "LAW-035", "LAW-042"}

allow if {
	input.operation in {"REGISTER_FORK", "FINALIZE_PROPOSAL"}
	valid_fractal_metadata
	required_policy_refs_present
}

deny contains "compiled_block.artifact_id is required" if {
	not non_empty_string(input.compiled_block.artifact_id)
}

deny contains "compiled_block.schema_version is required" if {
	not non_empty_string(input.compiled_block.schema_version)
}

deny contains "compiled_block.policy_refs is required" if {
	not is_array(input.compiled_block.policy_refs)
}

deny contains reason if {
	required_policy_refs[policy_ref]
	not policy_ref in input.compiled_block.policy_refs
	reason := sprintf("compiled_block.policy_refs must include %v", [policy_ref])
}

valid_fractal_metadata if {
	non_empty_string(input.compiled_block.artifact_id)
	non_empty_string(input.compiled_block.schema_version)
	is_array(input.compiled_block.policy_refs)
}

required_policy_refs_present if {
	every policy_ref in required_policy_refs {
		policy_ref in input.compiled_block.policy_refs
	}
}

non_empty_string(value) if {
	is_string(value)
	count(value) > 0
}
