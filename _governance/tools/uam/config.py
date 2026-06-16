"""
artifact_anchor:
  id: GVRN.CONFIG.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: GVRN
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_GOVERNANCE_COMPONENT
  relations: []
"""

# Sovereign UAM Configuration Registry
# UIP-V15 Governance Contract Definitions

# UIP-V15 Canonical Schema for validation checks
UIP_V15_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "SovereignArtifactAnchor",
    "type": "object",
    "required": [
        "id",
        "version",
        "provenance",
        "domain",
        "celestial_class",
        "tier",
        "state",
        "ethos",
    ],
    "additionalProperties": False,
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[A-Z]{3,4}\\.[A-Z0-9._-]{3,30}\\.[0-9]{3}$",
        },
        "version": {
            "type": "string",
            "pattern": "^v[0-9]+\\.[0-9]+(?:\\.[0-9]+)?(?:\\s+\\[[A-Z]+\\])?$",
        },
        "provenance": {"type": "string", "format": "date"},
        "domain": {
            "type": "string",
            "enum": ["CORE", "FABRIC", "INFRA", "GVRN", "TEST", "LORE", "COMPUTE"],
        },
        "celestial_class": {"type": "string", "enum": ["STAR", "PLANET", "MOON"]},
        "tier": {
            "type": "string",
            "enum": ["PRESENTATION", "LOGIC", "DATA", "COMPUTE", "GOVERNANCE"],
        },
        "state": {
            "type": "string",
            "enum": ["PROPOSED", "DRAFT", "ACTIVE", "CANONIZED"],
        },
        "ethos": {"type": "string", "maxLength": 120},
        "relations": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "node"],
                "additionalProperties": False,
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": [
                            "GOVERNS",
                            "SYNERGIZES",
                            "DEPENDS_ON",
                            "CONTROLS",
                            "IMPLEMENTS",
                            "UPDATES",
                        ],
                    },
                    "node": {"type": "string"},
                },
            },
        },
    },
}

DOMAIN_PREFIXES = {
    "CORE": "CORE",
    "FABRIC": "FABR",
    "INFRA": "INFR",
    "GVRN": "GVRN",
    "TEST": "TEST",
    "LORE": "LORE",
    "COMPUTE": "COMP",
}

# Strict directional layered boundaries
FORBIDDEN_TIER_CROSSINGS = {
    "COMPUTE": ["PRESENTATION"],
    "DATA": ["PRESENTATION"],
    "GOVERNANCE": ["PRESENTATION", "DATA", "COMPUTE"],
}

# Configurable Artifact Provider Registry
# Maps imported python modules to their canonical standard Artifact IDs
ARTIFACT_REGISTRY = {
    "websockets": {"provider_id": "INFR.WEBSOCKETS_RUNTIME.001", "name": "websockets"},
    "watchdog": {"provider_id": "INFR.WATCHDOG_MONITOR.001", "name": "watchdog"},
    "supabase": {"provider_id": "INFR.SUPABASE_CONNECTOR.001", "name": "supabase"},
    "yaml": {"provider_id": "INFR.YAML_PARSER.001", "name": "yaml"},
    "jsonschema": {
        "provider_id": "INFR.JSON_SCHEMA_VALIDATOR.001",
        "name": "jsonschema",
    },
}
