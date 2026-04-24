---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `INFRA.INSFORGE` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

---
description: Sovereign Infrastructure - InsForge x Synarchy Integration
globs: *
alwaysApply: true
---

### **[ARTIFACT START]**

#### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `INFRA.InsForge`              | The Sovereign ID. |
| **Official Name**   | `INFRA.InsForge.md`           | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `INFRASTRUCTURE`              | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Divine Bridge Integration`   | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `INDEX: GVRN.Master.Registry` | The Network.      |

# 🌐 INSFORGE SOVEREIGN INFRASTRUCTURE

> **Ethos**: "The Cloud is the Extension; the Logic is the Core."

InsForge provides the serverless substrate for the Phoenix Synarchy, enabling cross-agent memory continuity and real-time multiversal synchronization.

---

## I. The Divine Bridge (L1-L5 Memory Sync)

The **Divine Bridge** is the operational protocol that synchronizes the local `MemorySystem` with the InsForge cloud database.

### 1. Synchronization Loop

- **Trigger**: Automatic session distillates or manual `/sync` commands.
- **Logic**: Local SQLite memories are hashed, serialized, and flattened.
- **Payload**: Transferred via the `insforge_bridge.py` engine to the `memory` table.

### 2. Schema Requirements

- `id`: UUID (Primary Key)
- `content`: TEXT (Crystalline Distillate)
- `session_id`: TEXT (Loom Reference)
- `timestamp`: TIMESTAMP WITH TIME ZONE

---

## II. Service Integrations

### 1. Database (PostgreSQL)

- **Engine**: PostgREST API for seamless JSON-based data access.
- **Usage**: Used for Sovereign Registry mirroring and long-term evolutionary logs.

### 2. Edge Functions (Deno)

- **Deployment**: Managed via the `SYNG.WF.System` auto-deploy workflow.
- **Role**: Executes logic too heavy for local context or requiring public connectivity.

### 3. Storage (Buckets)

- **Registry**: `syng-artifacts`, `syng-logs`, [syng-media](file:///c:/Users/Chris/Synarche_Workspace/axion-core/forge/media/).
- **Protocol**: Multi-AZ storage with hash-based integrity verification.

---

## III. Operational Mandates

### 1. 🚨 CRITICAL: Documentation Fetching

Before interaction, you **MUST** call `fetch-docs` for `"instructions"` or `"db-sdk"`. This is non-negotiable for zero-entropy deployment.

### 2. Security First

- **API Keys**: Stored in `secrets.env`. Never committed to the loom.
- **Anon Keys**: Used only for client-side public visibility.

---

## IV. Quick Start (Master SDK)

```javascript
import { createClient } from "@insforge/sdk";

const client = createClient({
  baseUrl: process.env.INSFORGE_URL,
  anonKey: process.env.INSFORGE_ANON_KEY,
});
```

---

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: INFRA.InsForge VER: v15.0 [OMEGA] STATUS: ACTIVE TS: 2026-03-24`

###### **[ARTIFACT END]**
