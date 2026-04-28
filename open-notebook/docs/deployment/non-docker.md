---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `NON-DOCKER` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# GVRN.NOTEBOOK.DEPLOY-002: Bare Metal Protocol

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `Manual, Script, Local` **Criticality: Technical**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.NOTEBOOK.DEPLOY-002` | The Sovereign ID. |
| **Official Name** | `non-docker.md` | The Filename.     |
| **Version**       | **v2.0 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |






---

# Non-Docker Deployment

This method runs the services directly on your host OS. It is ideal for local development and debugging.

## I. Windows Setup (Automated)

We provide a PowerShell script that manages the entire lifecycle.

### [1.1] Controls

- **Start**: `.\dev_start.ps1`
- **Updates**: `git pull`, then run `dev_start.ps1` again (it auto-installs new deps).

## II. Linux/Mac Setup (Manual)

Since there is no automated script for Unix yet, follow the standard procedure:

1.  **Database**:
    ```bash
    surreal start --user root --pass root file://surreal.db
    ```
2.  **Backend Services**:

    ```bash
    # Terminal 1: API
    python open_notebook/run_api.py

    # Terminal 2: Worker
    python -m surreal_commands.cli.worker --import-modules commands
    ```

3.  **Frontend**:
    ```bash
    streamlit run open_notebook/app_home.py
    ```

## III. Service Dependencies

Ensure the following ports are free:

- `8000`: SurrealDB
- `5055`: API Server
- `8501`: Streamlit UI

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. ACTIONABLE PROMPT PACKET (APP)

> [!TIP]
> Use these commands to manage processes.

1.  **Check Process**
    - `CMD: CHECK_PID --service:[Service_Name]`
    - _Function:_ Verifies if the service is running.

**[ARTIFACT END]**
