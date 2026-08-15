package phoenix.security.key_rotation

import rego.v1

default allow := false

allow if {
	input.operation == "VERIFY_SIGNATURE"
	active_key
	not key_expired
	not key_revoked
}

deny contains "key_id is required" if {
	not non_empty_string(input.key_id)
}

deny contains "signing key is not active" if {
	not active_key
}

deny contains "signing key is expired" if {
	key_expired
}

deny contains "signing key is revoked" if {
	key_revoked
}

active_key if {
	some key in input.authorized_public_keys
	key.key_id == input.key_id
	key.status == "ACTIVE"
}

key_expired if {
	some key in input.authorized_public_keys
	key.key_id == input.key_id
	non_empty_string(key.expires_at)
	time.parse_rfc3339_ns(input.now) >= time.parse_rfc3339_ns(key.expires_at)
}

key_revoked if {
	some key in input.authorized_public_keys
	key.key_id == input.key_id
	key.status == "REVOKED"
}

non_empty_string(value) if {
	is_string(value)
	count(value) > 0
}
