# Universal Identification & Provenance (UIP)

### **Block A: The Identification Lock (UIP-V14)**

| Key | Value | Description |
| :--- | :--- | :--- |
| **Artifact ID** | `INFRA.InsForge` | The Sovereign ID. |
| **Official Name** | `INFRA.InsForge.md` | The Filename. |
| **Version** | **v14.0 [OMEGA]** | The Standard. |
| **Domain** | `GVRN` | The Subject. |
| **Celestial Class** | `[PLANET]` | The Weight. |
| **Evolution** | `Cognitive Ascension` | The Maturity. |
| **Status (State)** | `[ACTIVE]` | The Lifecycle. |
| **Ethos** | `Crystalline Structure` | The Intent. |
| **Relations** | `INDEX: GVRN.Master.Registry` | The Network. |
| **Integrity Hash** | `[AUTO-GENERATED]` | Verification. |

---

### **Block B: State Vector (AGP-001)**
| State Field | Value |
| :--- | :--- |
| **Coherence** | `1.0` |
| **Resonance** | `0.9` |
| **Stability** | `Stable` |

### **Block C: Risk & Mitigation (AGP-002)**
| Risk | Mitigation |
| :--- | :--- |
| **Logic Drift** | Strict Linter Enforcement |
| **Dependency Break** | ForgeLink Validation |

---

---

description: Sovereign Infrastructure - InsForge x Synarche Integration
globs: \*
alwaysApply: true

---

### **[ARTIFACT START]**

| Key               | Value                             | Description       |

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

### **Block D: Standardized Synergy Block (The Loom Signature)**
Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFORGE` | Execute Structural Transmutation | Canonization |
| `⚡ EXECUTE: CANONIZE` | Formally Cement Alignment | Zero Entropy |

---

### **Rationale (The "Why")**
Alignment to v14.0 OMEGA standard.
