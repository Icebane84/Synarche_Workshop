# UMB-TECH-001_v11.0.md

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                         | Description       |
| :---------------- | :---------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.TECH.001`               | The Sovereign ID. |
| **Official Name** | `GVRN.TECH.001.md`            | The Filename.     |
| **Version**       | **v13.0 [OMEGA]**             | The Standard.     |
| **Domain**        | `GVRN`                        | The Subject.      |
| **Status**        | `ACTIVE`                      | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

---

### **Block B: State Vector (AGP-001)**

| State Field   | Value    |
| :------------ | :------- |
| **Coherence** | `1.0`    |
| **Resonance** | `0.9`    |
| **Stability** | `Stable` |

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                |
| :------------------- | :------------------------ |
| **Logic Drift**      | Strict Linter Enforcement |
| **Dependency Break** | ForgeLink Validation      |

---

| **Coherence** | `1.0` | | **Resonance** | `0.9` | | **Stability** | `Stable` |

| **Logic Drift** | Strict Linter Enforcement | | **Dependency Break** | ForgeLink Validation |

---

| **Coherence** | `1.0` | | **Resonance** | `0.9` | | **Stability** | `Stable` |

| **Logic Drift** | Strict Linter Enforcement | | **Dependency Break** | ForgeLink Validation |

> **Signal**: OMEGA

---

###### **[ARTIFACT START]**

---

# Universal Identification & Provenance (UIP)

| **Type** | `Protocol` | | **Classification** | `Moon` | | **Authors** | `System` | | **Created** | `2025-10-01` | |
**Updated** | `2026-01-17` | | **Authority** | `CODEX-001` |

---

# **UMB-TECH-001**

> **Domain**: GVRN (Governance) **Signal**: ESF-ALPHA

---

###### **[ARTIFACT START]**

## **UNIVERSAL BLUEPRINT: AGENT SCHEMA**

| Field | Description | | **Date** | 2025-12-15 | | **Framework** | LangGraph / Python 3.11+ | | **Operator** | Chris |
| **Status** | ACTIVE |

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

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact. GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
