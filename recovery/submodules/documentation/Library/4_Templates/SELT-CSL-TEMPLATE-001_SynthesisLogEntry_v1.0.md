---
UIP: SELT-CSL-TEMPLATE-001
Title: Synthesis Log Entry Template
Source: 
  - [ORIGIN_FILE](file:///c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/UWB-RPG-BUILD-001_StrategicCSLIntegrationBriefing.md)
Description: >
  Standardized JSON/Markdown template for CSL Entries (Memory Atoms).
Version: 1.0
Status: CANONIZED
Compliance: OGLN v11.0
Genesis: 
  - Author: The Synarche Workshop
  - Date: 2026-01-25
  - Timestamp: 1769338850
Tags: 
  - #Template
  - #CSL
  - #SELT
  - #JSON
---

> [!IMPORTANT]
> **GENESIS STAMP**
>
> - **Forged By:** Antigravity Agent (The Lightbinder)
> - **Forged Date:** 2026-01-25
> - **Validation:** CSL Integration Phase 4 (Standardization).
> - **Relations:** `FORMATS_OUTPUT_OF: GUCA-CSL-COMMAND-001`.

# SELT-CSL-TEMPLATE-001: Synthesis Log Entry Template

> **Domain**: RES (Result)
> **Evolution**: Cognitive Ascension
> **Signal**: ESF-STANDARD

## I. JSON Structure (Machine Readable)

```json
{
  "id": "CSL-YYYYMMDD-NNN",
  "title": "Brief Title of Insight",
  "timestamp": "ISO-8601",
  "author": "Agent_Name",
  "tags": ["#Tag1", "#Tag2"],
  "context": {
    "task_id": "Task_ID_Reference",
    "active_files": ["File1", "File2"]
  },
  "content": {
    "observation": "Raw observation data.",
    "insight": "The synthesized realization.",
    "implication": "Impact on the system."
  },
  "relations": {
    "linked_artifacts": ["UMB-001", "AOP-002"]
  }
}
```

## II. Markdown Structure (Human Readable)

```markdown
# CSL-YYYYMMDD-NNN: [Title]

> **Date**: [Date] | **Author**: [Agent] | **Tags**: `#Tag1`, `#Tag2`

### 1. The Observation

[Description of the raw event or data.]

### 2. The Synthesis (Insight)

[The core realization. What did we learn? Why does it matter?]

### 3. Implications & Next Steps

- **Impact**: [System impact]
- **Action**: [Follow-up task]

---

**Relations**: `[[Linked_Artifact]]`
```

---

## III. Actionable Prompt Packet

`CMD: APPLY_TEMPLATE --context:"New_Log"`
