# UMB-PHX-LOG-001: The Complete Phoenix Logging Protocol (V1.2)

- **System ID:** UMB-PHX-LOG-001
- **Official Name:** The Phoenix Logging Protocol (V1.2)
- **Module:** LOG-M (Logging & Monitoring)
- **Domain:** GVRN (Governance) / ETH-A (Ethical Architecture)
- **Objective:** To establish the architectural standard for transitioning from transient system feedback (e.g., `print()`) to a persistent, high-fidelity audit trail. This protocol codifies the Law of Separation of Concerns (SoC) as foundational, ensuring system observation remains decoupled from core operational logic, and embeds ethical values directly into telemetry.

---

### **I. The Philosophical Framework (Ethos) - Shared Governance**

This protocol is built upon three core pillars of conceptual engineering that define why this standard is mandatory for the Synarche, moving from "how it works" to "why it matters" and fostering Shared Governance:

| Pillar | Ethical Value | Technical Translation |
| :--- | :--- | :--- |
| **Accountability** | The "Black Box" Protocol | Every action must leave a trace for future audit via **persistent error_audit.log** (Persistent Error Logs). |
| **Transparency** | Real-time Clarity | The system must communicate its state honestly to the operator via **console output** (StreamHandler). |
| **Integrity** | Non-Invasive Observation | Logs must observe without altering system behavior through **asynchronous handling** (e.g., `asyncio`). |

---

### **II. Operational Playbook (AOP) - The Dual-Stream Workflow**

Every software module must initialize a standard logging architecture that satisfies the Dual-Stream Requirement, ensuring real-time operational feedback while maintaining a high-fidelity audit trail.

*   **StreamHandler (The Pulse):**
    *   **Target:** `stdout` (Console)
    *   **Level:** `INFO` and above
    *   **Purpose:** Real-time status updates and immediate human-AI awareness for the operator.
*   **FileHandler (The Memory):**
    *   **Target:** `error_audit.log`
    *   **Level:** `ERROR` and `CRITICAL`
    *   **Purpose:** Post-mortem debugging, root-cause analysis, and persistent audit trails for the OGLN and PRS-001 metrics.

---

### **III. Command Architecture (GUCA) - Core Implementation Standard**

The Phoenix Logging Protocol is enforced through specific commands and automated architectural wrappers.

1.  **Standard Initialization (`setup_synarche_logging`):**
    *   Initializes the `PhoenixLogger` at the system entry point (`@system/logging`) to ensure all sub-components are captured.
    *   Mandates `ISO-8601` timestamps for temporal precision (Phoenix V-Control).

2.  **The `synarche_audit` Decorator (`@nexus/decorators`):**
    *   An architectural wrapper that automates the logging ethos by capturing function entry, exit, and critical failures with full stack traces.
    *   **Phases:** `DEBUG` (Start - Args/Kwargs), `INFO` (Success - Duration), `ERROR` (Failure - Exception/StackTrace).
    *   **Benefits:** Efficiency (minimizes duplication), Integrity (guarantees `T201` compliance), Traceability (automates stack trace persistence).

3.  **Mandatory Rule T201 (print found):**
    *   **Law/Rule Reference:** `Ruff Rule T201`
    *   **Requirement:** Use of `print()` (Python) or `console.log()` (JavaScript) is strictly prohibited in final code artifacts.
    *   **Ethos:** "Amateurism is a silent failure; Professionalism is documented."

---

### **IV. Experience Log (SELT) - Navigational Routing & Metrics**

Compliance is measured by the "Zero-Transient Policy." A codebase is compliant only when a linting pass (e.g., via Ruff) returns zero instances of transient output calls, ensuring the PRS-001 knowledge network remains high-fidelity.

*   **PRS-001 Integration:** The Phoenix Rosetta Stone (PRS-001) acts as the master navigational hub and query router for knowledge.
    *   `@system/logging`: Houses the core logger initialization logic.
    *   `@nexus/decorators`: Houses the `synarche_audit` execution wrapper.
    *   `PRS-001`: Indexes these performance logs to calculate the system's Coherence Index (CI) and feed into the OGLN's Cognitive Loom.