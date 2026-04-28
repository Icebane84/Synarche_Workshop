---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `INSTALLATION` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# GVRN.NOTEBOOK.INSTALL-001: Deployment Protocol

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `Installation, Manual, Config` **Criticality: Technical**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.NOTEBOOK.INSTALL-001` | The Sovereign ID. |
| **Official Name** | `installation.md` | The Filename.     |
| **Version**       | **v2.0 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |






---

# Installation Guide

This guide covers the complete installation process for Open Notebook.

## I. System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: Version 3.10 or higher (3.14 recommended)
- **Memory**: 8GB RAM minimum (16GB recommended for local LLMs)

## II. Installation Methods

### [2.1] Automated Windows Setup (Recommended)

If you are on Windows, use the `dev_start.ps1` script in the root directory. It handles virtual environment creation, dependency installation, and process management.

See the [Quick Start Guide](quick-start.md) for details.

### [2.2] Manual Setup (All Platforms)

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/open-notebook.git
    cd open-notebook
    ```

2.  **Create a Virtual Environment**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -e open_notebook
    ```

    _Note: You may need to install `surreal-commands` and `streamlit` explicitly if they are missing._

4.  **Start Services Manually**:
    You will need to run these in separate terminals:
    - **Database**: `surreal start --user root --pass root file://surreal.db`
    - **API**: `python open_notebook/run_api.py`
    - **Worker**: `python -m surreal_commands.cli.worker --import-modules commands`
    - **UI**: `streamlit run open_notebook/app_home.py`

### [2.3] Docker Setup

_Documentation coming soon in the Deployment section._

## III. Configuration

Open Notebook uses `.env` files for configuration.

- Copy `.env.example` to `.env`.
- Fill in your API keys (OpenAI, Anthropic, etc.) if planning to use cloud models.

## IV. Verification

To verify your installation is correct:

1.  Navigate to `http://localhost:8501`.
2.  Check the bottom right corner or logs for "Connected to Backend".
3.  Create a test notebook.

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## V. ACTIONABLE PROMPT PACKET (APP)

> [!TIP]
> Use these commands to verify readiness.

1.  **Verify Environment**
    - `CMD: VERIFY_INSTALL`
    - _Function:_ Checks python version and dependencies.

2.  **Start Services**
    - `CMD: LAUNCH_MANUAL`
    - _Function:_ Executes the manual startup sequence.

**[ARTIFACT END]**
