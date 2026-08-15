package phoenix.chronicle.integrity

import rego.v1

base_input := {
	"operation": "append_event",
	"actor": {"id": "user_architect", "role": "ARCHITECT"},
	"chronicle": {
		"genesis_hash": "sha256:genesis",
		"latest_hash": "sha256:event-001",
		"events": [
			{
				"id": "evt_001",
				"prev_hash": "sha256:genesis",
				"event_hash": "sha256:event-001",
			},
		],
	},
	"event": {
		"id": "evt_002",
		"artifact_id": "CORE.CODEX.PhoenixSchema",
		"law_id": "LAW-035",
		"type": "APPEND",
		"timestamp": "2026-06-25T00:00:00Z",
		"prev_hash": "sha256:event-001",
		"content_hash": "sha256:content-002",
		"event_hash": "sha256:event-002",
		"payload": {"state_delta": {"status": "CANONIZED"}},
		"signatures": [{"role": "ARCHITECT", "signature": "sig_architect"}],
	},
}

test_allow_valid_append if {
	allow with input as base_input
}

test_reject_delete_event if {
	denied := deny with input as object.union(base_input, {"operation": "delete_event"})
	"Immutable Chronicle rejects destructive operation: delete_event" in denied
}

test_reject_broken_append_hash if {
	bad_event := object.union(base_input.event, {"prev_hash": "sha256:wrong"})
	bad_input := object.union(base_input, {"event": bad_event})
	denied := deny with input as bad_input
	"event prev_hash must match the chronicle latest_hash" in denied
}

test_reject_duplicate_event_hash if {
	duplicate_event := object.union(base_input.event, {"event_hash": "sha256:event-001"})
	duplicate_input := object.union(base_input, {"event": duplicate_event})
	denied := deny with input as duplicate_input
	"event_hash must not duplicate an existing chronicle event" in denied
}

test_allow_state_derivation_on_valid_chain if {
	derive_input := object.union(base_input, {"operation": "derive_state"})
	allow with input as derive_input
}
