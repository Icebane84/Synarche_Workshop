---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `AI-MODELS` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# GVRN.NOTEBOOK.FEATURE-001: Model Configuration Protocol

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `AI, LLM, Providers` **Criticality: Core**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                         | Description       |
| :---------------- | :---------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.NOTEBOOK.FEATURE-001`   | The Sovereign ID. |
| **Official Name** | `ai-models.md`                | The Filename.     |
| **Version**       | **v2.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                        | The Subject.      |
| **Status**        | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

---

# AI Models & Providers

Open Notebook is "Model Agnostic." You are not locked into a single AI provider. You can mix and match models for different tasks (e.g., use a cheap model for summarization and a smart one for complex reasoning).

## I. Supported Providers

| Provider          | Type  | Best For                             | Setup Difficulty     |
| :---------------- | :---- | :----------------------------------- | :------------------- |
| **OpenAI**        | Cloud | General Reasoning (GPT-4o)           | Easy (API Key)       |
| **Anthropic**     | Cloud | Long Context / Coding (Claude 3.5)   | Easy (API Key)       |
| **Ollama**        | Local | Privacy / Offline (Llama 3, Mistral) | Medium (Install App) |
| **Google Gemini** | Cloud | Large Context Windows                | Easy (API Key)       |
| **Groq**          | Cloud | Extreme Speed                        | Easy (API Key)       |

## II. Configuration

### [2.1] API Keys

1.  Navigate to **Settings** -> **LLM Configuration**.
2.  Enter your API keys for the providers you wish to use.
3.  Keys are stored locally in your `.env` file (or secure storage).

### [2.2] Selecting Models

You can assign different models to different "System Slots":

- **Chat Model**: The main brain you talk to. (Rec: GPT-4o / Claude 3.5 Sonnet)
- **Fast Model**: Used for quick summaries and extraction. (Rec: GPT-4o-mini / Llama 3 8b)
- **Embedding Model**: Used for vector search. (Rec: OpenAI text-3-large / Nomic Embed)

## III. Local LLMs (Ollama)

To run fully offline:

1.  Install [Ollama](https://ollama.com).
2.  Pull a model: `ollama pull llama3`.
3.  In Open Notebook, select **Ollama** as the provider and type `llama3` as the model name.

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. ACTIONABLE PROMPT PACKET (APP)

> [!TIP]
> Use these commands to configure intelligence.

1.  **Set Provider**
    - `CMD: CONFIGURE_PROVIDER --name:[OpenAI|Ollama]`
    - _Function:_ Opens the configuration panel.

2.  **Test Connection**
    - `CMD: TEST_LLM_CONNECTION`
    - _Function:_ Verifies API keys and model availability.

**[ARTIFACT END]**
