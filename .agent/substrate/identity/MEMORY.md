# MEMORY.md - The Akashic Substrate

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                       | Description       |
| :---------------- | :-------------------------- | :---------------- |
| **Artifact ID**   | `ID.MEM.AKASHIC-001`        | The Sovereign ID. |
| **Official Name** | `MEMORY.md`                 | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**           | The Standard.     |
| **Domain**        | `IDENTITY`                  | The Subject.      |
| **Status**        | `[ACTIVE]`                  | The Lifecycle.    |
| **Relations**     | `REF: GVRN.Registry.Master` | The Network.      |

---

## 1. THE 5-LAYER MEMORY MODEL

### L1: GEMS (The Muse's Insights)

- **Content**: High-impact user preferences, specific design aversions, unique terminal solutions.
- **Persistence**: Managed by `GemMemoryAgent` in `memory_system.py`.

### L2: KINETIC (Active Session)

- **Content**: Briefings, current tool outputs, ephemeral context.
- **Persistence**: `axion_memory.db` (SQLite).

### L3: SEMANTIC (Knowledge Graph)

- **Content**: Vectorized associations, RAG indices, cross-file relationships.
- **Persistence**: `ContextWeave` matrix.

### L4: SOVEREIGN (Architectural Law)

- **Content**: `LEARNINGS.md`, `PHOENIX_CODEX.md`, System Benchmarks.
- **Persistence**: Git-tracked Markdown in `.learnings/`.

### L5: META (Self-Improvement)

- **Content**: `ERRORS.md`, `FEATURE_REQUESTS.md`, session heuristics.
- **Persistence**: Automated extraction via `SKL.SELF-IMPROVE`.

---

## 2. THE COGNITIVE LIFECYCLE

Memories are not static; they evolve through a mathematical lifecycle governed by `MemoryProtocols`.

| State            | Trigger                              | Result            |
| :--------------- | :----------------------------------- | :---------------- |
| **Active**       | Initial entropy or reactivation.     | Searchable/Fluid. |
| **Fading**       | Activation < `0.2`.                  | Deprioritized.    |
| **Archived**     | Activation < `0.05`.                 | Near-Total Loss.  |
| **Consolidated** | Activation > `0.8` AND Usage > `10`. | Static/Immortal.  |

### **Lifecycle Transitions**

- **Reactivation**: `Archived` -> `Active` if activation spikes > `0.3`.
- **Layer Elevation**: `L2 Kinetic` -> `L3 Semantic` upon transition to `Consolidated`.
- **Decay Resistance**: `Consolidated` memories resist fading with a `1.5x` threshold buffer.

---

## 3. PERSISTENCE STRATIFICATION

The Synarche Memory System employs a dual-backend architecture for maximum resilience:

1. **PostgreSQL (Sovereign)**: High-durability storage via `PostgresMemoryStorage` for multi-agent synchronization and vectorized RAG.
2. **SQLite (Kinetic)**: Low-latency local storage via `SQLiteMemoryStorage` for rapid session context and edge operations.

---

## 4. ROUTING & SYNTHESIS LOGIC

1. **Trigger A (Observation)**: When a tool identifies a pattern, route to L2.
2. **Trigger B (Verification)**: When a pattern persists across 3 sessions, elevate to L4.
3. **Trigger C (Optimization)**: When an error occurs, extract the root cause to L5.

---

`[MEMORY-ANCHOR] ID: ID.MEM.AKASHIC-001 VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-03-18`
