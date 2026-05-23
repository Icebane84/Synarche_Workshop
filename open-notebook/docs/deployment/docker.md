---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `DOCKER` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# GVRN.NOTEBOOK.DEPLOY-001: Container Protocol

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `Docker, Deployment, Container` **Criticality: Technical**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                         | Description       |
| :---------------- | :---------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.NOTEBOOK.DEPLOY-001`    | The Sovereign ID. |
| **Official Name** | `docker.md`                   | The Filename.     |
| **Version**       | **v2.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `GVRN`                        | The Subject.      |
| **Status**        | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |

---

# Docker Deployment

For isolation and easy updates, Docker is the recommended way to run Open Notebook in a production-like environment or on a server.

## I. Architecture

The `docker-compose.full.yml` defines the full stack:

1.  **frontend**: The Streamlit UI.
2.  **api**: The FastAPI backend.
3.  **worker**: The Celery/RabbitMQ (or internal) task processor.
4.  **surrealdb**: The persistent database.

## II. Quick Start

1.  **Install Docker Desktop**.
2.  **Run Compose**:
    ```bash
    docker-compose -f docker-compose.full.yml up --build -d
    ```
3.  **Access**:
    - UI: `http://localhost:8501`
    - API Docs: `http://localhost:5055/docs`
    - Database Console: `http://localhost:8000`

## III. Volume Management

Data is persisted in Docker Volumes:

- `surreal_data`: Stores all vectors and relational data.
- `.env`: Passed through to containers for configuration.

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. ACTIONABLE PROMPT PACKET (APP)

> [!TIP]
> Use these commands to deploy.

1.  **Deploy Stack**
    - `CMD: DOCKER_UP`
    - _Function:_ Starts all containers in detached mode.

2.  **Tear Down**
    - `CMD: DOCKER_DOWN`
    - _Function:_ Stops and removes containers (data persisted).

**[ARTIFACT END]**
