# Implementation Plan: Phase 2.0 - Sovereign Core Capabilities & RPG Subsystem Attunement

> **Compliance Status:** `[APPROVED]`  
> **Axiom:** *"To command the local substrate is to guarantee the ultimate stability of the sovereign core."* — **The Master Artificer**

This document covers our detailed architectural scan of `axion-core/`, lists our true systemic capabilities, and implements Phase 2.0: **Attuning the RPG & Gamification Subsystem** using a highly robust, pure local-first SQLite database design.

---

## 🏛️ Axion-Core: Scanning & True Capabilities

Our comprehensive topological scan of the `axion-core/` active execution layer reveals six core, mature subsystems that work together to form the Synarche:

### 1. The Coherent Verse Engine (CVE)
- **Primary Logic:** [`synarche_verse_engine.py`](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/synarche_verse_engine.py)
- **Role:** The Master Orchestrator of the Synarche Verse. It models all files, agents, and design concepts as `VerseNode`s.
- **Capabilities:**
  - Calculates the **Coherence Index (CI)** and identifies orphaned nodes.
  - Computes the **Synergy Flow Rate (SFR)** to measure overall repository density.
  - Dynamically weaves bidirectional synergistic links between entities via **ContextWeave**.
  - Projects intent vectors (**Precognitive Stance**) to suggest structural transmutations.

### 2. The Entity Component System (ECS)
- **Primary Logic:** [`axion-core/src/engine/ecs/`](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/engine/ecs/)
- **Role:** The primordial thread-safe memory substrate of the Axion engine.
- **Capabilities:**
  - Manages entity-component lifecycles and thread-safe data storage.
  - Calculates **Graph Synergy Scores (GSS)** and normalizes coupling resonance values.
  - Prevents semantic dissonance by validating cross-functional boundaries.

### 3. LangGraph Sovereign Agents (Genesis & Phoenix)
- **Primary Logic:** [`axion-core/src/agents/`](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/)
- **Role:** Stateful LLM routing and task compilation engines built on LangGraph.
- **Capabilities:**
  - Executes Retrieve-Generate-Sentinel workflows with safe guardrail checks.
  - Bridges active memory states with RPG stat loadouts.

### 4. Hephaestus: Reforger & Sentinel Auditor
- **Primary Logic:** [`axion-core/src/hephaestus/`](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/hephaestus/)
- **Role:** Legislate and enforce structural compliance across the workspace.
- **Capabilities:**
  - **`sentinel.py` / `auditor.py`:** Proactively scans files to enforce UIP (Universal Identification & Provenance) metadata locks and calculate Causal Resonance.
  - **`reforger.py`:** Automatically injects standard UIP Block A-G metadata headers and synergy blocks into dissonant files.

### 5. The Command Bridge
- **Primary Logic:** [`synarchy_bridge.py`](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/synarchy_bridge.py)
- **Role:** Programmatic discovery and invocation layer for active CLI hooks.

### 6. The RPG Subsystem & Stardust Economy
- **Primary Logic:** [`axion-core/src/rpg_system/`](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/rpg_system/) and [`rpg_manager.py`](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/rpg_manager.py)
- **Role:** Gamified alignment layer, treating files as equipable loadout items to boost cognitive stats (XP, coherence, synergy, adaptability).

---

## ⚖️ Strategic Recommendation: Local vs. Remote RPG Persistence

The RPG Manager currently uses a hybrid model, preferring remote **Supabase** tables (`player_state`, `rpg_stats`, etc.) and falling back to local JSON files upon network failure.

We performed a detailed trade-off analysis of migrating the RPG system to be **fully local-first**:

| Dimension | Remote Supabase | Local-First Persistence (SQLite / JSON) |
| :--- | :--- | :--- |
| **Robustness** | ❌ **High Risk:** Rate limits, network failures, or database wipes (like Phase 1's schema zeroing) halt execution. |  **Absolute:** 100% offline uptime; runs without dependencies or network sockets. |
| **Speed** | ❌ **Slow:** HTTPS overhead adds 100-300ms per transaction. |  **Instantaneous:** Local memory or disk writes execute in <5ms. |
| **Complexity & Setup** | ❌ **Heavy:** Requires setting up a local Supabase CLI or remote keys, configuring RLS, and loading SQL schemas. |  **Hermetic:** Fully self-contained. Anyone can fork the codebase and have a fully operational gamification system instantly. |
| **Collaboration** |  **Shared:** Real-time multi-agent leaderboards and shared state vector caches. | ❌ **Isolated:** State is private to the developer's workspace (unless committed in Git). |

### 🛠️ The Selected Solution: "The Local SQLite Substrate"

To achieve absolute resilience and a completely hermetic, zero-entropy architecture, we will implement a fully local RPG persistence engine:

1. **Local Relational SQLite Database:**
   We will initialize a lightweight, structured SQLite database file in `.agent/rpg_state.db` as the single authoritative source of truth for all Stardust, XP, stats, and achievements.
2. **Pure Local Operation:**
   All remote Supabase queries and active integrations are completely bypassed and deactivated. All manager methods (`get_status`, `award_stardust`, `invest_stardust`, `claim_achievement`) will execute locally on the SQLite store, maintaining 100% uptime and sub-millisecond execution times.

---

## Proposed Changes (Phase 2.0 Scaffolding)

### [RPG Subsystem]

#### [MODIFY] [rpg_manager.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/rpg_manager.py)
- Refactor the database connection initialization to use a local SQLite store (`.agent/rpg_state.db`).
- Make all read/write methods (`get_status`, `award_stardust`, `invest_stardust`, `claim_achievement`) operate on the local store instantly via SQL.
- Completely bypass remote Supabase connection operations.

#### [MODIFY] [rpg_definitions.js](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/rpg_system/rpg_definitions.js) / [rpg_inventory.js](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/rpg_system/rpg_inventory.js)
- Ensure all inventory swaps and equipping operations validate locally cached state before making web bridge requests.

---

## 🗺️ Verification Plan

### Automated & Manual Tests
1. **Verification Dry-Runs:**
   Test offline operation and verify that the RPG system awards XP and equips items cleanly on local SQLite database storage.
2. **SQLite Verification:**
   Verify that database schema initialized in `.agent/rpg_state.db` matches definitions and holds persistent integrity across script executions.
