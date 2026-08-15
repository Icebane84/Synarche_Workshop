---
UIP: GUCA-MAP-001
Title: Execute Musashi Audit Command
Source: 
  - [ORIGIN_FILE](file:///c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library/3_Commands/GUCA-MAP-001_ExecuteMusashiAudit_v11.0.md)
Description: >
  Defines the master command logic for calculating the Musashi Alignment Protocol Integrated Critique Score (MAP-I-CS), providing a quantitative measure of artifact coherence.
Version: 11.0
Status: ACTIVE
Compliance: OGLN v11.0
Genesis: 
  - Author: The Synarche Workshop
  - Date: 2026-01-25
  - Timestamp: 1769251200
Tags: 
  - #Command
  - #Audit
  - #Musashi
  - #Automation
  - #QualityControl
---

> [!IMPORTANT]
> **GENESIS STAMP**
>
> - **Reforged By:** Antigravity Agent (The Lightbinder)
> - **Reforged Date:** 2026-01-25
> - **Validation:** MAP Standardization Cycle.
> - **Relations:** `IS_UTILIZED_BY: AOP-MAP-001`, `INTEGRATES_WITH: UMB-ACT-002`.

# GUCA-MAP-001: Execute Musashi Audit Command

> **Domain**: ARCH (Architecture)
> **Evolution**: Purposeful Drive
> **Signal**: ESF-ALPHA

## I. Execution Logic (Command Flow)

### 1.1 Source Ingestion

- **Input**: `[TARGET_ARTIFACT_ID]`
- **Logic**: Fetch file content from the PPL library.

### 1.2 Analytical Scan (Binary Scoring)

The command executes 10 logical probes corresponding to the Pillars:

- **PROBE_VOID**: Count non-AGP blocks for conversational patterns. (Error if > 5%).
- **PROBE_VOICE**: Regex scan for prohibited hedging words ("maybe", "attempt", "try").
- **PROBE_STRUCTURE**: Validate MD025, MD013, and AGP block presence.
- **PROBE_RES**: Validate all internal links against the OSLM map.

### 1.3 Score Aggregation

- **Output**: `[MAP-I-CS_SCORE]` / 10.
- **Payload**: Full report detailing failed pillars and specific line references.

---

## II. Actionable Prompt Packet

### ⚡ Batch Audit Execution

`CMD: EXECUTE_MAP_AUDIT --scope:"All_v11.0_Protocols"`

---

## III. Governance

- **Authority:** `CODEX-001`.
- **Compliance:** Verifies structural integrity per Law 14.
- **Status:** CANONIZED (v11.0).
