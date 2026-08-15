---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `CONTEXT-MANAGEMENT` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# GVRN.NOTEBOOK.FEATURE-005: Context Protocol

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `Memory, Privacy, Data` **Criticality: High**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                         | Description       |
| :---------------- | :---------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.NOTEBOOK.FEATURE-005`   | The Sovereign ID. |
| **Official Name** | `context-management.md`       | The Filename.     |
| **Version**       | **v2.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                        | The Subject.      |
| **Status**        | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

---

# Context Management

Understanding how Open Notebook handles memory and context is key to getting the best results.

## I. Context Levels

### [1.1] Document Context

This is the text extracted from your files.

- **Chunking**: Large files are split into smaller "chunks" (usually 1000 tokens) to fit into the AI's memory.
- **Limit**: Depending on the model, you can fit between 8k to 128k tokens (roughly 15 to 300 pages) in a single prompt.

### [1.2] Chat History Context

The AI remembers previous turns in the conversation.

- **Sliding Window**: If the conversation gets too long, the oldest messages are dropped to make room for new ones.

## II. Privacy Architecture

- **Local Vectors**: Your document embeddings (the mathematical representation of text) are stored locally in SurrealDB.
- **Zero-Training**: Even if you use Cloud models (like OpenAI), your data is sent via API with a "Zero-Retention" policy (according to their Enterprise terms). Your data is NOT used to train their models.
- **Offline Mode**: If you use Ollama, **zero** data leaves your device.

## III. Data Retention

- **Delete Notebook**: Deletes all associated vectors and chat history.
- **Clear Chat**: Resets the conversation context but keeps the notebook data.

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. ACTIONABLE PROMPT PACKET (APP)

> [!TIP]
> Use these commands to manage memory.

1.  **Flush Memory**
    - `CMD: CLEAR_CONTEXT`
    - _Function:_ Resets the active chat window.

2.  **Purge Data**
    - `CMD: PURGE_DATA --target:[NotebookID]`
    - _Function:_ Irreversibly wipes vectors and metadata.

**[ARTIFACT END]**
