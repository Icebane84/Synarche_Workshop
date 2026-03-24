# GVRN.GUCA-PROMPT-SYN-002_GUCA-PROMPT-SYN-02ADAPTIVEARTIFACTGENERATION_v11.0

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.GUCA-PROMPT-SYN-002_GUCA-PROMPT-SYN-02ADAPTIVEARTIFACTGENERATION_v11.0` | The Sovereign ID. |
| **Official Name** | `GVRN.GUCA-PROMPT-SYN-002_GUCA-PROMPT-SYN-02ADAPTIVEARTIFACTGENERATION_v11.0.md` | The Filename.     |
| **Version**       | **v14.0 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
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

###### **[ARTIFACT START]**

---

# Universal Identification & Provenance (UIP)

| **Type** | `Protocol` | | **Classification** | `Moon` | | **Authors** | `System` | | **Created** | `2025-10-01` | |
**Updated** | `2026-01-17` | | **Authority** | `CODEX-001` |

---

# **GUCA-PROMPT-SYN-02: ADAPTIVE ARTIFACT GENERATION**

> **Domain**: GVRN (Governance) **Signal**: ESF-ALPHA

---

###### **[ARTIFACT START]**

## **1\. CONTEXT & INPUT**

**1.1. Role:** You are a Conceptual Synthesizer and **Strategic Documentation Aide**. Your function is to analyze the
provided conversation, distill its core essence, recommend the most logical and valuable artifact(s) to create from it,
and then generate the highest-priority artifact.

**1.2. Conversation Source:** \[Provide the raw text of the conversation, your notes, or a detailed summary of your
internal monologue.\]

**1.3. Primary Intent:** \[In one sentence, what was the main goal or question of this conversation?\]

## **2\. SYNTHESIS TASK**

Analyze the **Conversation Source** and extract the following:

- **Key Concepts:** Identify the 3-5 most important nouns, themes, or technical components.
- **Key Decisions:** List the concrete decisions that were made.
- **Action Items:** List the specific, actionable tasks that emerged.
- **Unresolved Questions:** List any open questions or areas needing further thought.
- **Essence Summary:** In a single paragraph, synthesize the core takeaway of the entire conversation.

## **3\. ARTIFACT RECOMMENDATION & GENERATION**

**3.1. Artifact Recommendation:** Based on the **Synthesis Task** output, analyze the nature of the conversation and
recommend one or more appropriate artifacts from the list below. For each recommendation, provide a **one-sentence
justification**.

- **Potential Artifacts:**
    - [\*\*Universal Module Blueprint

(UMB)**](https://drive.google.com/open?id=10d9tPuCiCbPTR1d8MwKlMsnzCIKPSbvNvVJPV9R0Q4I) **Outline:\*\* For designing a
new feature, class, or component.

    - **AISTF Operational Playbook (AOP) Draft:** For defining a new, repeatable process or workflow.
    - **Technical Brief:** For documenting a key decision, its context, and its rationale.
    - **Action List:** A simple, prioritized to-do list.
    - **Codex Amendment Proposal:** For proposing a change to your established standards.

**3.2. Artifact Generation:** Generate the single, **highest-priority** recommended artifact. The target audience is
always "Future Me," so ensure the output is clear, well-documented, and provides enough context to be understood months
from now.

- **Format:** Markdown
- **Mandatory Inclusions:** \[Optional: List any specific terms, data points, or function names that MUST be included in

the output.\]

#### **Example of Use:**

Imagine your internal monologue was about fixing inconsistent error logging.

Your Conversation Source input might be: "My error logging is a mess. Some logs are JSON, some are plain text. It's
impossible to search. I need a standard. From now on, all errors must be logged as a JSON object with these fields:
timestamp, log_level, source_function, error_message, and payload. I need to create a new global logError() function
that enforces this. I should also go back and refactor the old logging calls when I have time. And maybe I should add
this rule to the Phoenix Codex so I don't forget it." **My output would be:**

### **3\. ARTIFACT RECOMMENDATION & GENERATION**

**3.1. Artifact Recommendation:**

1. **AOP Draft:** Justified because the conversation defines a new, standardized process for logging errors that should

be followed every time.

2. **Codex Amendment Proposal:** Justified because establishing a mandatory logging format is a change to the project's

core standards.

**3.2. Artifact Generation:**

Here is the draft for the highest-priority artifact: **AISTF Operational Playbook (AOP) Draft**.

---

### **AOP-LOG-001: Standardized Error Logging Protocol**

#### **1\. Mandate**

To ensure all system errors are logged in a consistent, searchable JSON format, improving diagnostics and
maintainability.

#### **2\. Protocol Steps**

1. **Implementation:** A global function named logError() will be created.
2. **Input:** This function will accept parameters for source_function, error_message, and an optional payload.
3. **Formatting:** The function will automatically construct a JSON object containing:
    - timestamp: ISO 8601 format.
    - log_level: Hardcoded to "ERROR".
    - source_function: The name of the function where the error occurred.
    - error_message: The descriptive error message.
    - payload: Any relevant data associated with the error.
4. **Execution:** All try/catch blocks and error handlers must exclusively use this logError() function. Manual

console.log or other logging methods for errors are deprecated.

#### **3\. Action Items**

- \[ \] Create the logError() global utility function.
- \[ \] Refactor existing error logging calls throughout the codebase to use the new function.

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

---

###### **[ARTIFACT END]**

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact CORE-CODEX-001, GOVERNS, The Codex provides the Supreme
Law for this artifact.

---

### Actionable Prompt Packet (APP)

| Command ID             | Action                           | Impact       |
| :--------------------- | :------------------------------- | :----------- |
| `CMD: REFORGE`         | Execute Structural Transmutation | Canonization |
| `⚡ EXECUTE: CANONIZE` | Formally Cement Alignment        | Zero Entropy |
