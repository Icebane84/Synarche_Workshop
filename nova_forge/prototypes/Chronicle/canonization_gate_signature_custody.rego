package phoenix.canonization.signature_custody

import rego.v1

default allow := false

allow if {
	input.operation == "CANONIZE"
	input.current_state == "IN_REVIEW"
	has_architect_signature
	has_sentinel_signature
	sentinel_key_authorized
}

deny contains "canonization requires current_state IN_REVIEW" if {
	input.operation == "CANONIZE"
	input.current_state != "IN_REVIEW"
}

deny contains "canonization requires ARCHITECT signature" if {
	input.operation == "CANONIZE"
	not has_architect_signature
}

deny contains "canonization requires SENTINEL service-account signature" if {
	input.operation == "CANONIZE"
	not has_sentinel_signature
}

deny contains "SENTINEL signing key must be active in AUTHORIZED_PUBLIC_KEYS" if {
	input.operation == "CANONIZE"
	has_sentinel_signature
	not sentinel_key_authorized
}

has_architect_signature if {
	some sig in input.signatures
	sig.role == "ARCHITECT"
	non_empty_string(sig.key_id)
	non_empty_string(sig.signature)
}

has_sentinel_signature if {
	some sig in input.signatures
	sig.role == "SENTINEL"
	sig.algorithm == "Ed25519"
	non_empty_string(sig.key_id)
	non_empty_string(sig.signature)
}

sentinel_key_authorized if {
	some sig in input.signatures
	sig.role == "SENTINEL"
	some key in input.authorized_public_keys
	key.key_id == sig.key_id
	key.role == "SENTINEL"
	key.algorithm == "Ed25519"
	key.status == "ACTIVE"
}

non_empty_string(value) if {
	is_string(value)
	count(value) > 0
}
