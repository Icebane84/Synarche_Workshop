---
command: "canonize"
description: Canonization workflow. Automate the transition of artifacts to CANONIZED state.
---

# /canonize - Immutable Artifact Sealing

$ARGUMENTS

---

## Purpose

This workflow automates the transition of artifacts to the `[CANONIZED]` state, ensuring total systemic alignment and cryptographic integrity under the OMEGA/v15.0 standard.

---

## Trigger Execution

Run the canonization ritual on a target artifact:

```bash
python axion-core/scripts/canonize_ritual.py --target "{{target}}"
```

---

## The Seven Gates Audit

The script executes the following validations:

1. **Block Map Scan**: Ensures Blocks A-G are structured.
2. **Registry Handshake**: Confirms entry in `GVRN.Master.Registry.yaml`.
3. **Linter Pass**: (Optional) Verifies standard markdown compliance.

---

## The Three Seals Ritual

1. **Seal of Status**: Block A status is set to `[CANONIZED]`.
2. **Seal of Synchronicity**: Registry entries are updated with atomic precision.
3. **Seal of the Anchor**: Block G Omni-Anchor is generated with a fresh timestamp and SHA256 fragment.

---

## Actionable Commands

| Command ID             | Action                          | Impact       |
| :--------------------- | :------------------------------ | :----------- |
| `⚡ EXECUTE: CANONIZE` | Initiate the automated ritual   | Zero Entropy |
| `CMD: AUDIT_REGISTRY`  | Verify registry synchronization | Coherence    |

---

## Usage

```
/canonize docs/PLAN-ecommerce-cart.md
/canonize _governance/10_Governance/GVRN.SCP.001.md
/canonize axion-core/agents/game-developer/agent.md
```

---

## After Canonization

Report to user:

```
[CANONIZED] Artifact sealed.
- Status: [CANONIZED]
- Registry: Updated
- Anchor: Block G generated
- Hash: AR-XXX-V15-YY
```
