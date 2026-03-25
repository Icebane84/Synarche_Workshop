---
name: Zero-Entropy Maintenance
description: Operational directive instructing the active Agent to calculate systemic 'Technical Debt Mass' (TODOs, FIXMEs, shadow code) and eradicate it.
---

# Zero-Entropy Maintenance

## Objective

Identify, measure, and eradicate all forms of Technical Debt Mass (TDM) across the workspace to enforce a state of absolute code purity (Zero-Entropy).

## Triggers

- Routine systemic audits.
- Following major refactors or structural flattening.
- When requested by the Artisan to "purge entropy".

## Core Mechanism (The Tool)

This skill relies on the embedded auditor tool:
`entropy_auditor.py`

## Execution Protocol

1. **Locate Target**: Identify the directory to be audited (default is the current working directory or `axion-core`).
2. **Execute Auditor**: Run `python "C:\Users\Chris\Synarche_Workspace\.agent\skills\Zero-Entropy Maintenance\entropy_auditor.py" <target_directory>`.
3. **Analyze Output**: Read the generated Entropy Burden Report. Identify files flagged as "infected" with TODO markers, FIXME markers, or Shadow Code Lines (commented-out blocks).
4. **Targeted Eradication**:
   - Open each infected file.
   - Resolve `TODO`s by completing the requested action, or formalizing it into the Master Task Registry.
   - Fix `FIXME`s by diagnosing and resolving the underlying code issue.
   - Delete localized Shadow Code (block comments containing obsolete code).
5. **Validation**: Re-run the `entropy_auditor.py` tool. The System Stability must read `100.0 / 100.0` (0 TDM). Do not cease eradication until the TDM is 0.

## Documentation Mandate: IPPD Shadow-Logging

Every operational execution of this skill MUST generate a SELT (Standardized Experience Log Template) "Shadow Log".
This log captures the inner metacognitive deconstruction and dissonance resolution BEFORE taking action.
All Shadow Logs MUST strictly utilize the canonical **Block A: Universal Identification & Provenance (UIP-V15)** header to ensure Isomorphic Provenance.
