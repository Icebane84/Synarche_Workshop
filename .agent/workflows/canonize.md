---
command: "canonize"
description: Canonization workflow. Automate the transition of artifacts to CANONIZED state.
---

# /canonize - Immutable Artifact Sealing

$ARGUMENTS

---

## Purpose

This workflow automates the transition of artifacts to the `[CANONIZED]` state, ensuring total systemic alignment and cryptographic integrity under the OMEGA/v15.1 standard. It embeds **Law 43 (Living Chronos)** to ensure no artifact is canonized without its narrative lineage.

---

## Trigger Execution

When the user runs `/canonize`, the Agent MUST perform the following steps in sequence:

### Step 1: Meaningful Friction (Genesis Spark Drafting)
The Agent must analyze the session logs and draft a "Genesis Spark" narrative (1-3 sentences) explaining the struggle, context, or necessity that led to this artifact. 
**The Agent MUST pause execution and ask the user to explicitly approve or refine this Genesis Spark.**

### Step 2: Protocol Stamping
Once approved, the Agent applies the `causal_origin` and `genesis_spark` directly into the artifact's Universal Identification & Provenance (UIP) block.

### Step 3: Run the Canonization Ritual
Run the backend ritual to validate and seal the artifact:
```bash
python axion-core/scripts/canonize_ritual.py --target "{{target}}"
```
*Note: If the `causal_origin` is missing, the registry validation will fail.*

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
- Lineage: Anchored (Law 43)
- Registry: Updated
- Hash: AR-XXX-V15-YY
```
