---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `SECURITY` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# GVRN.NOTEBOOK.DEPLOY-003: Security Protocol

> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `Security, Auth, Encryption` **Criticality: High**

---

###### **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.NOTEBOOK.DEPLOY-003` | The Sovereign ID. |
| **Official Name** | `security.md` | The Filename.     |
| **Version**       | **v2.0 [OMEGA]** | The Standard.     |
| **Domain**        | `GVRN` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |






---

# Security Configuration

Open Notebook is designed as a **Single-User, Local Application**. It does NOT include robust multi-user authentication by default.

## I. Default Security Model

- **Authentication**: None (Open Access on localhost).
- **Network**: Binds to `localhost` (127.0.0.1) by default, preventing external access.

## II. Protecting Your Instance

If you deploy this on a shared server or cloud instance:

### [2.1] Password Protection (Streamlit)

Streamlit has a built-in "Secrets" mode.

1.  Create `.streamlit/secrets.toml`.
2.  Add: `password = "YOUR_STRONG_PASSWORD"`.
3.  The UI will now prompt for a password before loading.

### [2.2] API Protection

The API is currently unsecured. **Do not expose port 5055 to the public internet** without a reverse proxy (Nginx/Traefik) handling Basic Auth or OAuth.

## III. API Key Safety

- API Keys (OpenAI, etc.) are stored in `.env`.
- **NEVER** commit your `.env` file to Git.
- The `.gitignore` file is pre-configured to exclude `.env`, but always double-check.

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. ACTIONABLE PROMPT PACKET (APP)

> [!TIP]
> Use these commands to harden the system.

1.  **Set UI Password**
    - `CMD: SET_UI_AUTH`
    - _Function:_ Configures Streamlit secrets.

2.  **Audit Secrets**
    - `CMD: SCAN_SECRETS`
    - _Function:_ Checks for leaked keys in git history.

**[ARTIFACT END]**


- [[reverse-proxy]]