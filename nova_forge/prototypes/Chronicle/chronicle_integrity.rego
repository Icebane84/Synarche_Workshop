package phoenix.chronicle.integrity

import rego.v1

# CORE.CODEX.PhoenixSchema LAW-035: Immutable Chronicle
# Verification anchor: State(t) = S(0) + sum(Events)
#
# Expected input shape:
# {
#   "operation": "append_event" | "derive_state" | "delete_event" | "mutate_event",
#   "actor": {"id": "...", "role": "ARCHITECT" | "SENTINEL" | "..."},
#   "chronicle": {
#     "genesis_hash": "sha256...",
#     "latest_hash": "sha256...",
#     "events": [...]
#   },
#   "event": {
#     "id": "evt_...",
#     "artifact_id": "CORE.CODEX.PhoenixSchema",
#     "law_id": "LAW-035",
#     "type": "APPEND" | "DEPRECATE" | "CANONIZE" | "REVERT" | "REFINE",
#     "timestamp": "2026-06-25T00:00:00Z",
#     "prev_hash": "sha256...",
#     "content_hash": "sha256...",
#     "event_hash": "sha256...",
#     "payload": {...},
#     "signatures": [{"role": "ARCHITECT", "signature": "..."}]
#   }
# }

default allow := false

allowed_roles := {"ARCHITECT", "SENTINEL", "GOVERNANCE_AGENT"}

allowed_event_types := {
	"APPEND",
	"DEPRECATE",
	"CANONIZE",
	"REVERT",
	"REFINE",
	"TRANSCEND",
	"DISSONANCE",
}

destructive_operations := {"delete_event", "mutate_event", "truncate_chronicle", "rewrite_history"}

allow if {
	input.operation == "append_event"
	valid_actor
	valid_event
	append_only
	hash_chain_continues
	required_signature_present
}

allow if {
	input.operation == "derive_state"
	valid_actor
	chronicle_has_genesis
	chronicle_events_are_hash_chained
}

deny contains reason if {
	destructive_operations[input.operation]
	reason := sprintf("Immutable Chronicle rejects destructive operation: %v", [input.operation])
}

deny contains "actor role is not authorized for chronicle operations" if {
	not allowed_roles[input.actor.role]
}

deny contains "event id is required" if {
	not non_empty_string(input.event.id)
}

deny contains "artifact id is required" if {
	not non_empty_string(input.event.artifact_id)
}

deny contains "LAW-035 events must identify the Immutable Chronicle law" if {
	input.event.law_id != "LAW-035"
}

deny contains "event type is not recognized by the chronicle policy" if {
	not allowed_event_types[input.event.type]
}

deny contains "event timestamp is required" if {
	not non_empty_string(input.event.timestamp)
}

deny contains "event prev_hash must match the chronicle latest_hash" if {
	input.operation == "append_event"
	input.event.prev_hash != input.chronicle.latest_hash
}

deny contains "event_hash is required" if {
	not non_empty_string(input.event.event_hash)
}

deny contains "content_hash is required" if {
	not non_empty_string(input.event.content_hash)
}

deny contains "event_hash must not duplicate an existing chronicle event" if {
	some event in input.chronicle.events
	event.event_hash == input.event.event_hash
}

deny contains "chronicle genesis_hash is required" if {
	not chronicle_has_genesis
}

deny contains "chronicle event chain is broken" if {
	not chronicle_events_are_hash_chained
}

valid_actor if {
	allowed_roles[input.actor.role]
	non_empty_string(input.actor.id)
}

valid_event if {
	non_empty_string(input.event.id)
	non_empty_string(input.event.artifact_id)
	input.event.law_id == "LAW-035"
	allowed_event_types[input.event.type]
	non_empty_string(input.event.timestamp)
	non_empty_string(input.event.prev_hash)
	non_empty_string(input.event.content_hash)
	non_empty_string(input.event.event_hash)
}

append_only if {
	not destructive_operations[input.operation]
}

hash_chain_continues if {
	input.event.prev_hash == input.chronicle.latest_hash
}

required_signature_present if {
	some signature in input.event.signatures
	signature.role == input.actor.role
	non_empty_string(signature.signature)
}

chronicle_has_genesis if {
	non_empty_string(input.chronicle.genesis_hash)
}

chronicle_events_are_hash_chained if {
	count(input.chronicle.events) == 0
}

chronicle_events_are_hash_chained if {
	count(input.chronicle.events) > 0
	first := input.chronicle.events[0]
	first.prev_hash == input.chronicle.genesis_hash
	every i in numbers.range(1, count(input.chronicle.events) - 1) {
		input.chronicle.events[i].prev_hash == input.chronicle.events[i - 1].event_hash
	}
}

non_empty_string(value) if {
	is_string(value)
	count(value) > 0
}
