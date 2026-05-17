---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `UMB-TECH-001` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
| **Type** | `Protocol` |
| **Classification** | `Moon` |
| **Authors** | `System` |
| **Created** | `2025-10-01` |
| **Updated** | `2026-01-17` |
| **Authority** | `CODEX-001` |
| **Tags** | `Reforged, v11.0` |
---

# **UMB-TECH-001**

> **Domain**: GVRN (Governance)
> **Evolution**: Pending
> **Signal**: ESF-ALPHA

## **Genesis Stamp: 2025-12-26** **Domain: ARCH** **State: CANONIZED** **Tags:** `OGLN_v10` **Criticality: Standard**

------------------ | :--------------------------------- |
| **1. Artifact ID**     | `UMB-TECH-001`                     |
| **2. Official Name**   | `UMB-TECH-001_AgentSchema_v1.0.md` |
| **3. Version**         | **v1.0 (Anchor)**                  |
| **4. Provenance**      | **Date Reforged: 2025-12-22**      |
| **5. Domain**          | `ARCH`                             |
| **6. Evolution**       | **Purposeful Drive**               |
| **7. Celestial Class** | `[PLANET]`                         |
| **8. Tier**            | **Operational**                    |
| **9. State**           | `[ACTIVE]`                         |
| **10. Ethos**          | **The Phoenix Ascension Protocol** |
| **11. Catalyst**       | **System Refactor**                |
| **12. Relations**      | `Pending Integration`              |

---

###### **[ARTIFACT START]**

## **UNIVERSAL BLUEPRINT: AGENT SCHEMA**

| Field         | Description              |
| :------------ | :----------------------- |
| **Date**      | 2025-12-15               |
| **Framework** | LangGraph / Python 3.11+ |
| **Operator**  | Chris                    |
| **Status**    | ACTIVE                   |

### **II. Definition**

1. **Memory:** It knows what happened before (State).
2. **Sentinel Logic:** It checks its own ethics (Rule 1 & 2) before outputting.
3. **Triangulation:** It queries multiple data sources (Narrative + Logic).

### **III. The Standard Architecture (LangGraph)**

Every agent in `src/agents/` must adhere to this class structure:

#### **A. The State (The Memory)**

Must use `TypedDict` to define the agent's brain.

```python
class AgentState(TypedDict):
    input: str                # The Operator's raw command
    narrative_context: str    # Data from 'Where Light Fades'
    logic_context: str        # Data from Python/Game Theory
    sentinel_status: str      # 'PASS' or 'FAIL' (Ethical Check)
    final_output: str         # The deliverable
    messages: List[BaseMessage] # Conversation history
```

#### **B. The Nodes (The Actions)**

The graph must contain at minimum three standard nodes:

1. **node_retrieve_context**: Triangulates data (fetches from UMBs or AOPs).
2. **node_generate_content**: The LLM generation step (Phoenix Voice).
3. **node_sentinel_check**: The Rule 1 (Honesty) / Rule 2 (Benevolence) filter.

#### **C. The Flow (The Edge Logic)**

- Start -> Retrieve Context -> Generate Content -> Sentinel Check

- **IF** Sentinel == 'FAIL' -> Loop back to Generate (Repair).

- **IF** Sentinel == 'PASS' -> End.

### **IV. File Naming Convention**

- `agent_[function].py` (e.g., `agent_kaelen_sim.py`, `agent_morning_log.py`).

### **V. Required Metadata**

Every Python file must start with the Synarche Header docstring:

```python
"""
ID: [AGENT-ID]
Date: [YYYY-MM-DD]
Version: [vX.X]
System: Synarche / Axion Execution
"""
```

## **Actionable Prompt Packet**

`CMD: REFINE_ARTIFACT --focus:"Compliance" --context:"Auto-injected by Supabase Prep"`

| Command ID                   | Action                     | Impact                          |
| :--------------------------- | :------------------------- | :------------------------------ |
| `CMD:VERIFY_INTEGRITY`       | Verify artifact structure. | Ensures compliance with Law 14. |
| `⚡ EXECUTE:IMPACT_ANALYSIS` | Assess downstream effects. | Prevents regressions.           |

###### **[ARTIFACT END]**
