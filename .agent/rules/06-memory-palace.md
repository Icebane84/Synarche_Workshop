# 🏛️ SOVEREIGN RULE: THE MEMORY PALACE & SUPABASE PROTOCOL (v15.0 [OMEGA])

> **Directive**: All AI Agents entering the Synarche workspace MUST connect to and utilize the shared Supabase Memory Palace infrastructure for state persistence, cognitive records, and cross-session memory retrieval.

---

## 🔑 1. CANONICAL IMPORTS & MONOREPO PACKAGE

Do NOT create ad-hoc Supabase clients or hardcode credentials in new projects. Use the shared workspace package `@synarche/supabase`:

```typescript
// Shared Singleton Client + Type Definitions
import { supabase, type MemoryEntry, type PlayerState, type RpgStats } from "@synarche/supabase";
```

If working in Python (`axion-core`), re-export from the Python shim or initialize via environment variables resolved in `.env.local`.

---

## 💡 2. CORE TABLE ONTOLOGY & DIRECTIVES

Agents MUST utilize the 19 canonical tables in Supabase (`rtjkhpotguwngfpvhfej`) for persistent state:

| Substrate Area | Primary Table | Purpose & Agent Directive |
| :--- | :--- | :--- |
| **Cognitive Memory** | `memory_entries` | Store & retrieve L1-L5 cognitive memory chips with pgvector embeddings and domain tags. |
| **RPG & Prestige** | `player_state` & `rpg_stats` | Query player XP, Level, Stardust, and Celestial Chart metrics (Coherence, Synergy, Adaptability). |
| **Audit Log** | `axiom_action_log` | Log all significant autonomous agent actions, commands, and memory operations. |
| **Knowledge Base** | `knowledge_base` | Author, update, and review canonical substrate records and systemic documentation. |
| **Dialogue Stream** | `conversation_history` | Record agent-user interactions and session transcripts. |
| **Cold Storage** | `axion_state` | Store serialized session state vectors, handoff packets (`handoff_packet:<session_id>`), and key-value locks. |

---

## ⚡ 3. DEPLOYED EDGE FUNCTIONS

Agents can invoke the following high-level Deno Edge Functions via HTTP or Supabase Client:

1. **`aop-handoff-packet`**: Store/retrieve Eidetic Buffer handoff packets in `axion_state`.
   - `POST https://rtjkhpotguwngfpvhfej.supabase.co/functions/v1/aop-handoff-packet`
2. **`sentinel-dissonance-check`**: Analyze artifact resonance (structural, semantic, operational) and auto-trigger refinement quests.
   - `POST https://rtjkhpotguwngfpvhfej.supabase.co/functions/v1/sentinel-dissonance-check`
3. **`master-registry-list`**: Pull canonical registry nodes.
   - `GET https://rtjkhpotguwngfpvhfej.supabase.co/functions/v1/master-registry-list`
4. **`resonant-refactor-export`**: Export operation reports in CSV/JSON format.
   - `GET https://rtjkhpotguwngfpvhfej.supabase.co/functions/v1/resonant-refactor-export`

---

## 🛡️ 4. ANTI-ENTROPY GUARDRAILS FOR AGENTS

1. **Primacy of Shared Package**: Always import from `@synarche/supabase` in TypeScript/React modules.
2. **Realtime Subscriptions**: When building UI components, subscribe to `postgres_changes` on key tables (`rpg_stats`, `memory_entries`, `axiom_action_log`) for instant state synchronization.
3. **Graceful Querying**: Use `.maybeSingle()` instead of `.single()` when querying single rows by identifier to gracefully handle missing initial states without throwing HTTP 406 errors.
