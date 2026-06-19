#!/usr/bin/env python3
"""
Phoenix Vault: a simple tool for tracking shared claims/decisions over time
and whether each party still endorses them.

Two separate record types, intentionally kept apart:

  CLAIM       - a factual statement or decision, with history (append-only,
                each edit creates a new version linked to the previous one).
                No psychological language belongs here - just "what was said
                and why."

  ENDORSEMENT - a first-person-only record of whether a specific person
                still agrees with a specific claim version. Nobody can write
                an endorsement on behalf of someone else. This is how
                "do we still agree with this" gets tracked, without one
                party ever declaring what the other "really" thinks.

Storage: a single JSON file (vault.json) for simplicity. Swap for sqlite
later if the vault gets big.
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional

VAULT_PATH = os.environ.get("VAULT_PATH", "vault.json")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return uuid.uuid4().hex[:12]


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ClaimVersion:
    claim_id: str          # stable id across versions of the "same" claim
    version_id: str        # unique id for this specific version
    text: str               # the factual statement / decision itself
    rationale: str          # why it was decided / believed at the time
    prev_version_id: Optional[str]   # lineage pointer, or None if first version
    created_at: str
    created_by: str         # who proposed this version ("user" / "axion" / name)


@dataclass
class Endorsement:
    endorsement_id: str
    claim_version_id: str   # which specific version this applies to
    party: str               # who is speaking - first person only
    still_agree: bool
    note: str
    created_at: str


@dataclass
class Vault:
    claims: list = field(default_factory=list)        # list of ClaimVersion dicts
    endorsements: list = field(default_factory=list)  # list of Endorsement dicts

    def load(self, path=VAULT_PATH):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.claims = data.get("claims", [])
                self.endorsements = data.get("endorsements", [])

    def save(self, path=VAULT_PATH):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"claims": self.claims, "endorsements": self.endorsements}, f, indent=2)

    # -- claims --------------------------------------------------------

    def add_claim(self, text, rationale, created_by, claim_id=None, prev_version_id=None):
        """Add a new claim, or a new version of an existing claim_id."""
        cid = claim_id or new_id()
        version = ClaimVersion(
            claim_id=cid,
            version_id=new_id(),
            text=text,
            rationale=rationale,
            prev_version_id=prev_version_id,
            created_at=now_iso(),
            created_by=created_by,
        )
        self.claims.append(asdict(version))
        return version

    def latest_version(self, claim_id):
        versions = [c for c in self.claims if c["claim_id"] == claim_id]
        if not versions:
            return None
        return max(versions, key=lambda c: c["created_at"])

    def history(self, claim_id):
        versions = [c for c in self.claims if c["claim_id"] == claim_id]
        return sorted(versions, key=lambda c: c["created_at"])

    # -- endorsements ----------------------------------------------------

    def endorse(self, claim_version_id, party, still_agree, note=""):
        """Record (or update) a party's own stance on a specific claim version.
        Only the speaker can set their own endorsement - this function takes
        `party` as an explicit argument because nothing in this tool infers
        or guesses what someone else believes."""
        e = Endorsement(
            endorsement_id=new_id(),
            claim_version_id=claim_version_id,
            party=party,
            still_agree=still_agree,
            note=note,
            created_at=now_iso(),
        )
        self.endorsements.append(asdict(e))
        return e

    def endorsements_for(self, claim_version_id):
        return [e for e in self.endorsements if e["claim_version_id"] == claim_version_id]

    def current_stance(self, claim_version_id, party):
        """Most recent endorsement by a given party for a given version, if any."""
        relevant = [e for e in self.endorsements_for(claim_version_id) if e["party"] == party]
        if not relevant:
            return None
        return max(relevant, key=lambda e: e["created_at"])

    # -- review helpers ----------------------------------------------------

    def stale_claims(self, parties):
        """Return latest-version claims where any listed party has never
        endorsed, or has previously marked still_agree=False."""
        flagged = []
        for claim_id in {c["claim_id"] for c in self.claims}:
            latest = self.latest_version(claim_id)
            missing_or_disagreed = []
            for party in parties:
                stance = self.current_stance(latest["version_id"], party)
                if stance is None or stance["still_agree"] is False:
                    missing_or_disagreed.append(party)
            if missing_or_disagreed:
                flagged.append((latest, missing_or_disagreed))
        return flagged


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_add(args, vault):
    text = input("Claim text: ").strip()
    rationale = input("Rationale: ").strip()
    by = args.by or input("Created by (name): ").strip()
    v = vault.add_claim(text, rationale, by)
    vault.save()
    print(f"\nAdded claim_id={v.claim_id} version_id={v.version_id}")


def cmd_revise(args, vault):
    latest = vault.latest_version(args.claim_id)
    if not latest:
        print("No such claim_id.")
        return
    print(f"Current text: {latest['text']}")
    text = input("New text: ").strip()
    rationale = input("Rationale for the change: ").strip()
    by = args.by or input("Revised by (name): ").strip()
    v = vault.add_claim(text, rationale, by, claim_id=args.claim_id, prev_version_id=latest["version_id"])
    vault.save()
    print(f"\nNew version_id={v.version_id} (supersedes {latest['version_id']})")


def cmd_endorse(args, vault):
    version_id = args.version_id
    party = args.party or input("Your name: ").strip()
    answer = input("Do you still agree with this? (y/n): ").strip().lower()
    still_agree = answer.startswith("y")
    note = input("Note (optional): ").strip()
    vault.endorse(version_id, party, still_agree, note)
    vault.save()
    print("Recorded.")


def cmd_history(args, vault):
    for v in vault.history(args.claim_id):
        print(f"\n[{v['created_at']}] version={v['version_id']} by={v['created_by']}")
        print(f"  text: {v['text']}")
        print(f"  rationale: {v['rationale']}")
        for e in vault.endorsements_for(v["version_id"]):
            mark = "agrees" if e["still_agree"] else "DISAGREES"
            print(f"    - {e['party']} {mark} ({e['created_at']}){': ' + e['note'] if e['note'] else ''}")


def cmd_review(args, vault):
    parties = args.parties.split(",")
    flagged = vault.stale_claims(parties)
    if not flagged:
        print("Nothing flagged - all claims endorsed by all listed parties.")
        return
    for latest, missing in flagged:
        print(f"\nclaim_id={latest['claim_id']} version={latest['version_id']}")
        print(f"  text: {latest['text']}")
        print(f"  needs review from: {', '.join(missing)}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Phoenix Vault CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a brand new claim")
    p_add.add_argument("--by", help="Name of person/agent adding the claim")
    p_add.set_defaults(func=cmd_add)

    p_rev = sub.add_parser("revise", help="Add a new version of an existing claim")
    p_rev.add_argument("claim_id")
    p_rev.add_argument("--by")
    p_rev.set_defaults(func=cmd_revise)

    p_end = sub.add_parser("endorse", help="Record your own stance on a claim version")
    p_end.add_argument("version_id")
    p_end.add_argument("--party")
    p_end.set_defaults(func=cmd_endorse)

    p_hist = sub.add_parser("history", help="Show full version + endorsement history for a claim")
    p_hist.add_argument("claim_id")
    p_hist.set_defaults(func=cmd_history)

    p_rev2 = sub.add_parser("review", help="List claims missing endorsement from given parties")
    p_rev2.add_argument("parties", help="comma-separated names, e.g. user,axion")
    p_rev2.set_defaults(func=cmd_review)

    args = parser.parse_args()
    vault = Vault()
    vault.load()
    args.func(args, vault)


if __name__ == "__main__":
    main()
