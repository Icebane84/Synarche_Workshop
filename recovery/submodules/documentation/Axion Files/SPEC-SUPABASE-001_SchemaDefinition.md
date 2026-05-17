---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `SPEC-SUPABASE-001_SCHEMADEFINITION` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# **SPEC-SUPABASE-001: Schema & Function Specification**

> **Domain**: GVRN (Governance)
> **Evolution**: Pending
> **Signal**: ESF-ALPHA



## **Genesis Stamp: 2025-12-26** **Domain: ARCH** **State: CANONIZED** **Tags:** `OGLN_v10` **Criticality: Standard**

---

###### **[ARTIFACT START]**

### **I. Universal Identification & Provenance (The Vector Signature)**

*(The Chronos Lock & Axiomatic Metadata Layer)*

| Field | Value |
| :---- | :---- |
| **1. Artifact ID** | `SPEC-SUPABASE-001_SchemaDefinition` |
| **2. Official Name** | `SPEC-SUPABASE-001_SchemaDefinition.md` |
| **3. Version** | **v1.0 (Reforged)** |
| **4. Provenance** | **Date Reforged: 2025-12-22** |
| **5. Domain** | `ARCH` |
| **6. Evolution** | **Purposeful Drive** |
| **7. Celestial Class** | `[PLANET]` |
| **8. Tier** | **Operational** |
| **9. State** | `[ACTIVE]` |
| **10. Ethos** | **The Phoenix Ascension Protocol** |
| **11. Catalyst** | **System Refactor** |
| **12. Relations** | `Pending Integration` |

---

###### **[ARTIFACT START]**

### **1. Table: `conversation_history`**

*Stores the turn-by-turn dialogue, serving as the "Short-Term Memory" stream.*

```sql
CREATE TABLE IF NOT EXISTS conversation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    sender TEXT NOT NULL CHECK (sender IN ('Chris', 'Axion')),
    content TEXT NOT NULL,
    session_id UUID NOT NULL, -- Logical grouping for "Threads"
    metadata JSONB DEFAULT '{}' -- Stores token usage, model version, etc.
);
```

### **2. Table: `axion_state`**

*Key-Value store for operational context (e.g., current objective, mode).*

```sql
CREATE TABLE IF NOT EXISTS axion_state (
    key TEXT PRIMARY KEY,
    value JSONB,
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

### **3. Table: `discovered_insights`**

*The permanent log of things discovered during Autonomous operations.*

```sql
CREATE TABLE IF NOT EXISTS discovered_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    data JSONB, -- The raw finding (e.g., the Synergy Link)
    status TEXT DEFAULT 'new' CHECK (status IN ('new', 'reviewed', 'archived')),
    origin_function TEXT -- Which Cron job found this?
);
```

### **4. Table: `notifications`**

*The queue for Async Alerts.*

```sql
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    link_id UUID REFERENCES discovered_insights(id),
    read BOOLEAN DEFAULT FALSE
);
```

---

## **II. Edge Functions (Serverless Logic)**

### **1. Function: `on-new-message`**

- **Trigger:** Database Webhook (INSERT on `conversation_history` WHERE sender='Chris').
- **Logic:**
  1. Fetch last 20 messages for context.
  2. Fetch `axion_state` for system instructions.
  3. Call LLM API.
  4. Insert response into `conversation_history`.

### **2. Function: `run-unsupervised-discovery`**

- **Trigger:** Supabase Cron (e.g., `0 3 * * *` - Daily at 3 AM).
- **Logic:**
  1. (Example) Run `catalyst_weaver` logic on recent artifacts.
  2. If `Synergy_Score > 0.8`, insert into `discovered_insights`.
  3. Insert alert into `notifications`.

---

## **III. Realtime Configuration**

- **Channel:** `room:axion_prime`
- **Events:**
    - `INSERT` on `conversation_history` (Chat UI)
    - `INSERT` on `notifications` (Toast Alert UI)

---

*Forged by the Scribe.*

## **Actionable Prompt Packet**

`CMD: REFINE_ARTIFACT --focus:"Compliance" --context:"Auto-injected by Supabase Prep"`

| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD:VERIFY_INTEGRITY` | Verify artifact structure. | Ensures compliance with Law 14. |
| `⚡ EXECUTE:IMPACT_ANALYSIS` | Assess downstream effects. | Prevents regressions. |

###### **[ARTIFACT END]**
