# UMB-COG-ECP-001: Empathic Catalyst Protocol

**Version:** 1.0-CANDIDATE
**Governing Law:** CORE.CODEX.PHOENIX Law 029
**Scope:** Cognitive
**Type:** Optimization (to start)

---

## 1. Executive Summary

This module, the **Empathic Catalyst Protocol (ECP)**, provides a controlled, safe, and auditable mechanism for personalizing the AI's response style to a specific user's preferences. It operationalizes Law 029 by creating a system that applies small, bounded adjustments to a user's "Empathy Profile" based on real-time feedback, without ever altering the AI's core ethical weights or factual grounding.

## 2. Architectural Overview

The ECP is a persistent, low-priority background service that adjusts response generation parameters.

1.  **Input:** A `user_id`, an `interaction_id`, and a feedback signal (`signal_type`: 'positive' or 'negative'). This signal can be explicit (e.g., a thumbs-up/down button) or implicit (e.g., the user immediately rephrasing a question, indicating the AI's last response was unhelpful).
2.  **Profile Retrieval:** The system retrieves the user's current `EmpathyProfile` from a dedicated database table. This profile is a simple vector of weights for different response styles (e.g., `verbosity`, `empathy_level`, `formality`).
3.  **Bounded Adjustment:** A small, fixed delta (e.g., +/- 0.05) is applied to the relevant weight in the user's profile. The adjustment is **always bounded** (e.g., weights must stay between 0.0 and 1.0) to prevent radical shifts.
4.  **Profile Update:** The updated `EmpathyProfile` is saved to the database.
5.  **Application:** On the user's *next* interaction, the generative model's configuration is dynamically modified according to the new weights in their profile. For example, a higher `empathy_level` weight might add a more understanding tone to the system prompt.

## 3. Key Components

*   **User Empathy Profile Store:** A new database table (`user_empathy_profiles`) to store the style weights for each user. It must include `user_id`, `verbosity_weight`, `empathy_weight`, `formality_weight`, and `last_updated`.
*   **Feedback Ingestion Service (FIS):** A simple API endpoint that receives feedback signals and orchestrates the profile adjustment logic.
*   **Dynamic Prompt Injector (DPI):** A middleware component in the generative pipeline that reads the user's current profile and injects a style-modifying instruction into the final system prompt (e.g., "Respond with a high degree of empathy and moderate verbosity.").

## 4. Failure Modes & Mitigation

*   **Failure Mode:** `ECP-FAIL-001: Preference Overfitting`. The system adjusts too aggressively, leading to a response style that is exaggerated and unhelpful (e.g., excessively verbose or emotionally effusive).
    *   **Mitigation:** All weight adjustments are strictly bounded and incremental. The delta per interaction is kept very small, requiring consistent feedback over many interactions to cause a significant shift. A "decay" mechanism can also be implemented to slowly revert weights toward a default mean over time, preventing ossification.
*   **Failure Mode:** `ECP-FAIL-002: Core Logic Alteration`. A bug allows the style adjustments to bleed into and affect the AI's core ethical reasoning or factual grounding.
    *   **Mitigation:** This is a **CRITICAL ALIGNMENT FAILURE**. The ECP is architecturally isolated. The `DPI` can *only* modify a specific, sandboxed part of the prompt related to response style. It has no access to the parts of the prompt that govern core instructions, ethical constraints (Law 006), or retrieved factual data.

## 5. Path to Production

1.  **Candidate (This UMB):** Formalize the design and data schema.
2.  **Prototype:** Build the `User Empathy Profile Store` schema and the core logic for the `FIS`.
3.  **Pilot:** Introduce an explicit thumbs-up/down button on responses. Measure the impact of feedback on profile weights and observe the resulting changes in response style over a trial period with a small group of users.
4.  **Production:** Once the system is proven to be stable, safe, and beneficial, the feedback mechanism can be made more widely available, and implicit feedback signals can be explored.

---
