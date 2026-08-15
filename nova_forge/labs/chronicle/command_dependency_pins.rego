package phoenix.commands.dependency_pins

import rego.v1

default allow := false

required_commands := {
	"CMD.RequestClarification": "^1.0.0",
	"CMD.Deprecate": "^1.0.0",
	"CMD.Approve": "^1.0.0",
	"CMD.Refine": "^1.0.0",
	"CMD.EnactTranscendence": "^1.0.0",
}

allow if {
	every command, version in required_commands {
		input.command_registry[command].version_constraint == version
		input.command_registry[command].status == "ACTIVE"
	}
}

deny contains reason if {
	required_commands[command]
	not input.command_registry[command]
	reason := sprintf("missing command registry entry: %v", [command])
}

deny contains reason if {
	required_commands[command] == version
	input.command_registry[command].version_constraint != version
	reason := sprintf("command %v must be pinned to %v", [command, version])
}

deny contains reason if {
	required_commands[command]
	input.command_registry[command].status != "ACTIVE"
	reason := sprintf("command %v must be ACTIVE", [command])
}
