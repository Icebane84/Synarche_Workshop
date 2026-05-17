---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `AOP-SUPABASE-001_INTEGRATIONPROTOCOL` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# **AOP-SUPABASE-001: Deployment Protocol**

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
| **1. Artifact ID** | `AOP-SUPABASE-001_IntegrationProtocol` |
| **2. Official Name** | `AOP-SUPABASE-001_IntegrationProtocol.md` |
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

### **Phase 1: Foundation (Database)**

1. **Execute SQL:** Run the schema definitions from `SPEC-SUPABASE-001` in the Supabase SQL Editor.
2. **Verify Tables:** Confirm existence of `conversation_history`, `axion_state`, `discovered_insights`,
`notifications`.
3. **Enable Realtime:** Go to **Database -> Replication** and enable replication for `conversation_history` and
`notifications`.

### **Phase 2: Logic (Edge Functions)**

1. **Initialize:** `supabase functions new on-new-message`.
2. **Deploy:** `supabase functions deploy on-new-message`.
3. **Secrets:** Set `OPENAI_API_KEY` (or equivalent) in Supabase via `supabase secrets set`.

### **Phase 3: Wiring (Webhooks & Cron)**

1. **Webhook:** Create a Database Webhook in the Dashboard:
    - Name: `axion-chat-trigger`
    - Table: `conversation_history`
    - Event: `INSERT`
    - HTTP Request: `POST` to the `on-new-message` function URL.
2. **Cron:** Enable `pg_cron`.
    - Run: `select cron.schedule('axion-discovery', '0 3 * * *', $$ select net.http_post(...) $$);`

### **Phase 4: Client Connection**

1. **Install SDK:** `npm install @supabase/supabase-js`.
2. **Subscribe:**

    ```javascript
    supabase
      .channel("chat")
      .on(
        "postgres_changes",
        { event: "INSERT", table: "conversation_history" },
        (payload) => {
          console.log("New Message:", payload.new);
        }
      )
      .subscribe();
    ```

---

## **II. Troubleshooting & Maintenance**

- **Logs:** Check Edge Function logs for execution errors.
- **Security:** Ensure **RLS (Row Level Security)** is enabled on all tables to prevent public access. create policies
allowing access only to authenticated users (The Architect).

---

*Forged by the Scribe.*

## **Actionable Prompt Packet**

`CMD: REFINE_ARTIFACT --focus:"Compliance" --context:"Auto-injected by Supabase Prep"`

| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD:VERIFY_INTEGRITY` | Verify artifact structure. | Ensures compliance with Law 14. |
| `⚡ EXECUTE:IMPACT_ANALYSIS` | Assess downstream effects. | Prevents regressions. |

###### **[ARTIFACT END]**
