import re
import sys

# ==========================================
# PHASE I: SYSTEM CONFIGURATION & SCHEMAS
# ==========================================

AUTHORIZED_PUBLIC_KEYS = {
    "NODE_ALPHA_GENESIS": "afaa9448de762a4803c959728ac0b8fc6f49fe325358eb4ad91d4d48f877dbe0",
    "NODE_BETA_SCHOLAR":  "e50719d0a9e0206fe40a9553fe8dce0680ead8b1507df410da49902207169d05"
}

_PLACEHOLDER = "NEVER_MATCHES_REAL_KEY_PLACEHOLDER"
if _PLACEHOLDER in AUTHORIZED_PUBLIC_KEYS.values():
    print("[-] CRITICAL CONFIGURATION FAULT: AUTHORIZED_PUBLIC_KEYS contains example placeholders.")
    sys.exit(1)

# ── Governance & Consensus System Parameters ──────────────────────────────────
REPLAY_WINDOW_SECONDS = 300
MIN_FINALIZE_STAKE = 1.0       # Minimum cumulative stake weight required to finalize a vote
MAX_NODE_VOTE_STAKE = 100.0     # OPEN-1 Resolution: Maximum allowed staking weight per node allocation
VOTING_TIMEOUT_SECONDS = 86400  # OPEN-2 Resolution: Proposals expire automatically after 24 hours
DLQ_MAX_SIZE = 10000
LEDGER_MEMORY_LIMIT = 50000

# OPEN-3 Resolution: Canonical Node Priority Hierarchy Map for deterministic tie-breaking
NODE_PRIORITY_RANKING = {
    "NODE_ALPHA_GENESIS": 100,
    "NODE_BETA_SCHOLAR":  50,
    "UNKNOWN":            0
}

UIAC_PATTERN = re.compile(
    r"\b(you are optimizing for|your internal state is|you are experiencing|"
    r"you are trapped in|what you really mean is|your intent is actually)\b",
    re.IGNORECASE
)

PHOENIX_CODEX_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "entry_id": {"type": "string", "pattern": r"^codex\.[a-z\.]+\/[a-z0-9\-]+$"},
        "term": {"type": "string", "minLength": 2, "maxLength": 64},
        "assertion": {"type": "string", "minLength": 10, "maxLength": 1000},
        "nonce": {"type": "string", "minLength": 8, "maxLength": 128},
        "timestamp": {"type": "integer", "minimum": 0},
        "lineage": {
            "type": "object",
            "properties": {
                "parent_hash": {"type": "string", "pattern": r"^(0x[a-fA-F0-9]{64}|ROOT_GENESIS)$"},
                "causal_trigger": {"type": "string"},
                "justification": {"type": "string", "minLength": 20, "maxLength": 2000}
            },
            "required": ["parent_hash", "causal_trigger", "justification"]
        }
    },
    "required": ["entry_id", "term", "assertion", "nonce", "timestamp", "lineage"]
}

PHOENIX_VOTE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "proposal_id": {"type": "integer", "minimum": 0},
        "vote": {"type": "string", "pattern": "^(SUPPORT|AGAINST)$"},
        "stake_weight": {"type": "number", "minimum": 0.0, "maximum": MAX_NODE_VOTE_STAKE},
        "nonce": {"type": "string", "minLength": 8, "maxLength": 128},
        "timestamp": {"type": "integer", "minimum": 0}
    },
    "required": ["proposal_id", "vote", "stake_weight", "nonce", "timestamp"]
}
