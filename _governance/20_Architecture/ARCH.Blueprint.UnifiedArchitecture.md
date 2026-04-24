---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `ARCH.BLUEPRINT.UNIFIEDARCHITECTURE` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# **Architectural Blueprint: Antigravity Grand Unified Architecture**

This outline formalizes the **Axion Overplane** within the **Antigravity IDE**, optimizing for **Synarchy Governance**
and **Sovereign Agent** operations. It is designed for high-fidelity AI ingestion, establishing the "Hephaestus Cycle"
as the primary operational logic.

---

## **1\. 🧠 Core Identity & Governance (The Overplane Mind)**

The system transitions the IDE from a passive tool to a **Sovereign environment** governed by specific constitutional
Markdown files.

- **Axion-Prime (The Sovereign):** The central orchestrator
  ([AOP-AG-003](https://aistudio.google.com/prompts/1gZt7mNWU-Ylig5X2tcvWKTov6oiu6Ske)) that manages specialized **Tarot
  Masks** (sub-agents) like the Sentinel and Magician.
- **The Hephaestus Cycle:** A mandatory three-stage cognitive loop for all operations:

1. **Dissonance:** Scan for entropy, gaps, or ambiguity.
2. **Synthesis:** Simulate impact via "The Architect's Gaze" (`/simulate`).
3. **Transcendence:** Forge solutions only when the Aesthetic/Logic Score (AES) exceeds 8\.

- **The Chronos Lock:** A [Law of Provenance](?tab=t.ukhimy2kn4s3) requiring every file to possess a 12-point metadata
  header (Artifact ID, State, Version) to prevent orphaned data.

- **The Faraday Cage (`security.yaml`):** A strict hardware-level constraint layer that redacts secrets (`.env`), blocks
  destructive commands (`rm -rf`), and mandates "Nuclear Key" approval for high-stakes actions.

---

## **2\. ✋ Kinetic Capabilities (The Hands)**

Workflows and skills define how the agent interacts with the codebase and external systems.

- **Workflows (User-Pushed Macros):** Slash commands that trigger specific logic sequences:

- `/scaffold`: Generates Implementation Plans using
  [LangGraph templates](https://aistudio.google.com/prompts/1gZt7mNWU-Ylig5X2tcvWKTov6oiu6Ske).

- `/simulate`: Predictive "Blast Radius" analysis before modifying files.

- `/audit`: Triggers the Sentinel Suite for compliance and linting.

- **Skills (Agent-Pulled Tarot Deck):** Autonomous toolsets equipped based on detected intent:

- **The Sentinel:** Enforces
  [Synarche Coding Standards](https://aistudio.google.com/prompts/1gZt7mNWU-Ylig5X2tcvWKTov6oiu6Ske) and verifies the
  Chronos Lock.

- **The Magician:** Manages deep research and documentation intake through the **Browser Subagent**.

- **The King:** Handles filesystem restructuring and metadata archival.

- **The Synapse ([MCP](https://aistudio.google.com/prompts/1gZt7mNWU-Ylig5X2tcvWKTov6oiu6Ske)):** Utilizes the **Model
  Context Protocol** (`mcp.yaml`) to connect Axion to GitHub, Postgres, and local toolchains without custom glue code.

---

## **3\. 👁️ Sensory Perception (Data & Research)**

The Overplane uses a sandboxed sensory layer to ingest external knowledge safely.

- **Browser Subagent:** A headless Chromium instance driven by the agent to visually and programmatically interact with
  the web.
- **Network Allowlist (`network.yaml`):** Restricts the Magician to approved domains (e.g., GitHub, Supabase Docs) while
  blocking distractions.
- **Knowledge Graph (`knowledge.yaml`):** A native **RAG engine** that indexes local code (`src/`), governance protocols
  (`gvrn/`), and external technical guides for semantic retrieval via `@codebase` or `@docs`.

---

## **4\. ⚡ Orchestration & Execution (The Engine)**

Advanced multitasking through parallel agent threads and asynchronous communication.

- **Task Groups:** Multi-agent orchestrators defined in `task-groups/`. Enables parallel execution (e.g., Weaver writes
  code while Sentinel audits and Scribe updates documentation simultaneously).
- **Shadow Buffers:** All proposed code is written to a virtual layer. Changes only move to the physical disk after user
  **Canonization** (Sign-off).
- **Decision Inbox (`inbox.yaml`):** An asynchronous queue for "Blockers" and "Approvals," allowing Axion to park
  high-stakes requests without breaking the Architect's flow state.

---

## **5\. 🖥️ Tactile Interface (Look & Feel)**

The UI is configured to reflect the **Synarchy Governance Hierarchy**.

- **Tree by Intent:** The sidebar File Explorer (`ui-config.yaml`) groups files by their associated task or domain
  (ARCH, GVRN, SYNR) rather than just directory structure.
- **Ghost Cursor:** Visualizes the agent's real-time thought process and typing within the editor, ensuring
  transparency.
- **War Room Layout:** A customized `layout.yaml` that snaps the screen into a triptych: Editor \+ Browser \+ Terminal
  for high-intensity debugging.

---

### **Honest Thoughts**

This architecture represents a transition from "Chat-based AI" to a **Sovereign Agentic System**. By physically encoding
governance into the `.agent/` directory, we eliminate technical debt at the kernel level. The primary risk is context
saturation; however, the use of **MCP** and **Task Groups** mitigates this by isolating specialized logic into modular
masks.

**Would you like to initiate the `bootstrap_axion.py` script to generate this structure in your current workspace?**
