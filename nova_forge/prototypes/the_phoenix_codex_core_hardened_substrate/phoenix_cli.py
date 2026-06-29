#!/usr/bin/env python3
"""
Phoenix CLI: the only thing that should ever construct and sign a request to
the Phoenix Codex server. Generates node identities, builds correctly-shaped
payloads (nonce + timestamp included automatically), signs the EXACT bytes
that get transmitted, and posts them.

This matters because of a subtlety in the v3.1 design: the server verifies
the Ed25519 signature against the literal raw request body bytes it receives.
If you build a dict, re-serialize it differently than how you signed it (key
order, whitespace), the signature breaks. This client guarantees you always
sign and send the same bytes by constructing the body once and reusing it.

Usage:
    python3 phoenix_cli.py keygen
    python3 phoenix_cli.py propose --entry-id codex.economics/property \\
        --term "Property Ownership" \\
        --assertion "..." --parent-hash 0x... --trigger "..." --justification "..." \\
        --node-id NODE_ALPHA_GENESIS --key-file alpha.key
    python3 phoenix_cli.py vote --proposal-id 0 --vote SUPPORT --stake 1.0 \\
        --node-id NODE_ALPHA_GENESIS --key-file alpha.key
"""

import argparse
import json
import os
import sys
import time
import uuid

try:
    import requests
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("[-] Missing dependencies. Run: pip install requests cryptography")
    sys.exit(1)

DEFAULT_SERVER = os.environ.get("PHOENIX_SERVER_URL", "http://127.0.0.1:8000")


def cmd_keygen(args):
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_hex = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()

    public_hex = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()

    key_file = args.key_file or "phoenix_node.key"
    if os.path.exists(key_file) and not args.force:
        print(f"[-] {key_file} already exists. Use --force to overwrite.")
        sys.exit(1)

    # Private key file only - 0600 permissions, never printed in full to stdout.
    with open(key_file, "w", encoding="utf-8") as f:
        f.write(private_hex)
    os.chmod(key_file, 0o600)

    print("========================================")
    print("[+] PHOENIX NODE IDENTITY GENERATED")
    print("========================================")
    print(f"PRIVATE KEY -> written to {key_file} (chmod 600, do not share or commit)")
    print(f"PUBLIC KEY (add to server's AUTHORIZED_PUBLIC_KEYS) : {public_hex}")
    print("========================================")


def _load_private_key(key_file: str) -> ed25519.Ed25519PrivateKey:
    if not os.path.exists(key_file):
        print(f"[-] Key file not found: {key_file}. Run 'keygen' first.")
        sys.exit(1)
    with open(key_file, "r", encoding="utf-8") as f:
        private_hex = f.read().strip()
    return ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_hex))


def _sign_and_post(server: str, route: str, body_dict: dict, node_id: str, key_file: str):
    """The one place a request body gets serialized. Signs those exact bytes,
    then sends those exact bytes - never a re-encoded copy."""
    private_key = _load_private_key(key_file)
    raw_body = json.dumps(body_dict).encode("utf-8")
    signature_hex = private_key.sign(raw_body).hex()

    headers = {
        "Content-Type": "application/json",
        "x-phoenix-node-id": node_id,
        "x-phoenix-signature": signature_hex,
    }

    resp = requests.post(f"{server}{route}", data=raw_body, headers=headers, timeout=10)
    print(f"[{resp.status_code}] {resp.text}")
    return resp


def cmd_propose(args):
    body = {
        "entry_id": args.entry_id,
        "term": args.term,
        "assertion": args.assertion,
        "nonce": uuid.uuid4().hex,
        "timestamp": int(time.time()),
        "lineage": {
            "parent_hash": args.parent_hash,
            "causal_trigger": args.trigger,
            "justification": args.justification,
        },
    }
    _sign_and_post(args.server, "/api/v1/governance/propose", body, args.node_id, args.key_file)


def cmd_vote(args):
    body = {
        "proposal_id": args.proposal_id,
        "vote": args.vote,
        "stake_weight": args.stake,
        "nonce": uuid.uuid4().hex,
        "timestamp": int(time.time()),
    }
    _sign_and_post(args.server, "/api/v1/governance/vote", body, args.node_id, args.key_file)


def cmd_history(args):
    resp = requests.get(f"{args.server}/api/v1/codex/entry/{args.entry_id}", timeout=10)
    print(f"[{resp.status_code}]")
    if resp.ok:
        print(json.dumps(resp.json(), indent=2))
    else:
        print(resp.text)


def cmd_status(args):
    resp = requests.get(f"{args.server}/api/v1/node/sync-state", timeout=10)
    print(f"[{resp.status_code}]")
    print(json.dumps(resp.json(), indent=2) if resp.ok else resp.text)


def main():
    parser = argparse.ArgumentParser(description="Phoenix Codex node client")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="Server base URL")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_keygen = sub.add_parser("keygen", help="Generate a new Ed25519 node identity")
    p_keygen.add_argument("--key-file", default="phoenix_node.key")
    p_keygen.add_argument("--force", action="store_true")
    p_keygen.set_defaults(func=cmd_keygen)

    p_propose = sub.add_parser("propose", help="Submit a new codex entry or revision")
    p_propose.add_argument("--entry-id", required=True)
    p_propose.add_argument("--term", required=True)
    p_propose.add_argument("--assertion", required=True)
    p_propose.add_argument("--parent-hash", required=True, help="ROOT_GENESIS or 0x<64 hex>")
    p_propose.add_argument("--trigger", required=True, dest="trigger")
    p_propose.add_argument("--justification", required=True)
    p_propose.add_argument("--node-id", required=True)
    p_propose.add_argument("--key-file", required=True)
    p_propose.set_defaults(func=cmd_propose)

    p_vote = sub.add_parser("vote", help="Cast a stake-weighted vote on a proposal")
    p_vote.add_argument("--proposal-id", type=int, required=True)
    p_vote.add_argument("--vote", choices=["SUPPORT", "AGAINST"], required=True)
    p_vote.add_argument("--stake", type=float, required=True)
    p_vote.add_argument("--node-id", required=True)
    p_vote.add_argument("--key-file", required=True)
    p_vote.set_defaults(func=cmd_vote)

    p_history = sub.add_parser("history", help="Fetch full revision history for an entry")
    p_history.add_argument("--entry-id", required=True)
    p_history.set_defaults(func=cmd_history)

    p_status = sub.add_parser("status", help="Fetch substrate sync-state telemetry")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
