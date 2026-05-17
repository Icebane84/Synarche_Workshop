---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `UMB-FLICSS-HEART-001_CONTEXTURGENCYORCHESTRATOR_V1.0` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

---
# UMB-FLICSS-HEART-001_ContextUrgencyOrchestrator_v1.0
# [STAR] (The Central Gravity)

| :------------------ | :--------------------------------------------- |
| **1. Artifact ID** | `UMB-FLICSS-HEART-001` |
| **2. Official Name** | `UMB-FLICSS-HEART-001_ContextUrgencyOrchestrator_v1.0.md` |
| **3. Version** | **v1.0** |
| **4. Provenance** | **Genesis Stamp: 2025-11-23** |
| **5. Domain** | `FLICSS` (Synthesis System) |
| **6. Evolution** | **Contextual Awakening** |
| **7. Celestial Class** | `[STAR]` (The Central Gravity) |
| **8. Tier** | **Core Module** |
| **9. State** | `[ACTIVE]` |
| **10. Ethos** | **Empathic Filter** |
| **11. Catalyst** | **FLICSS Strategy Phase 5.1** |
| **12. Relations** | `DEPENDS_ON: FLICSS-STOMACH; FEEDS: FLICSS-BRAIN, FLICSS-HANDS` |
---

> [!IMPORTANT]
> **The Heart:** Context & Urgency Orchestrator.
> While "The Stomach" handles raw data digestion, "The Heart" assigns **meaning**, **emotional tone**, and **urgency** to that data. It functions as the system's emotional intelligence and strategic compass.

## **1. Module Identity & Purpose**

### **What: The Cognitive Core**
**"The Heart"** is the primary "Cognitive Organ" responsible for **central processing and contextual routing**.

### **How: The "Pulse" Mechanism**
It operates via a continuous feedback loop known as the **"Pulse Protocol."** This mechanism evaluates incoming synthesized data against the user's current psychological state and strategic goals, assigning a **Context Vector** before routing the data to **"The Brain"** (Storage) or **"The Hands"** (Action).

### **Why: Synergistic Alignment**
Raw data without context is noise. "The Heart" ensures that the FLICSS ecosystem remains **empathic and user-centric**, preventing information overload by filtering content based on *relevance* rather than just *volume*.

---

## **2. Technical Architecture & Data Flow**

### **2.1. Inputs (Afferent Streams)**
*   **Source:** **The Stomach** (via **The Spine**)
*   **Data Type:** `Synthesized_Packet_JSON`
*   **Payload:** Raw summaries, Deconstruction Layer tags, initial RSM Score.

*   **Source:** **The Spine** (Telemetry)
*   **Data Type:** `System_Pulse_Signal`
*   **Payload:** Current system load, user interaction frequency, active "Focus Mode" status.

### **2.2. Internal Processing (The Ventricles)**
"The Heart" processes data through two distinct chambers:

1.  **The Left Ventricle (Logic/Urgency):**
    *   Re-evaluates the `RSM_Score` based on *immediate* user needs.
    *   Modifies the **Priority Flag**.
    *   *Logic:* `IF (Topic == "Current_Project") THEN (Priority = "Critical")`

2.  **The Right Ventricle (Emotion/Tone):**
    *   Analyzes the sentiment of the synthesis.
    *   Tags the data with an **Emotional Resonance Score (ERS)**.
    *   *Logic:* Determines if the content is "Inspiring," "Warning," or "Neutral Fact."

### **2.3. Outputs (Efferent Streams)**

*   **Destination:** **The Brain**
    *   **Action:** Archival of high-context memories.
    *   **Payload:** `Enriched_Packet` (Includes Context Vector + ERS).

*   **Destination:** **The Hands**
    *   **Action:** Immediate user notification or report generation.
    *   **Payload:** `Actionable_Insight` (Only Tier 1 items with high Urgency).

---

## **3. Configuration & Optimization**

### **3.1. Component Fingerprint**
As defined in the **FLICSS Strategy (Phase 5.1)**, "The Heart" operates under the **Empathy and Context** optimization profile.

*   **Latency Tolerance:** Moderate (Prioritizes accuracy of context over raw speed).
*   **Filter Bias:** High Recall (Prefers to flag potentially relevant emotional context rather than discarding it).

### **3.2. Adaptive Learning Targets**
"The Heart" is subject to **Dynamic Re-weighting** via `CMD:LEARN:REWEIGHT`.

*   **Success Metric:** User Engagement Rate with "Heart-flagged" notifications.
*   **Failure Metric:** User dismissal of "High Urgency" alerts (Indicates a calibration error in the Left Ventricle).

---

## **4. Dependencies & Interfaces**

| Dependency | Type | Relationship |
| :--- | :--- | :--- |
| **The Spine** | Infrastructure | **Critical.** The Heart cannot receive input or transmit output without the Spine's message bus. |
| **The Stomach** | Upstream Organ | **Provider.** The Heart relies on the Stomach for pre-digested, coherent summaries. |
| **UMB-MAP** | Standard | **Governing.** The Heart must preserve all UMB-MAP tags while adding its own Context Vectors. |

---

## **Actionable Prompt Packet**
*   `CMD: CHECK_PULSE --target:system`
*   `CMD: REWEIGHT_VENTRICLES --logic:0.8 --emotion:0.2`
