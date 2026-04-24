Here is a concise visualization of how **`nova_forge`** is laid out and how the main experiment (**`playground/tarot-forge`**) hangs together.

### 1) Repository map (folders and intent)

```mermaid
flowchart TB
  subgraph NF["nova_forge/ — Experimental Synthesis Lab"]
    README["README.md — lab index + anchor metadata"]
    subgraph SRC["src/ — research artifacts"]
      ENG["engine/ContextWeave.ts — associative engine stub"]
      MAN["manifestos/*.md"]
      PRO["protocols/*.md"]
    end
    subgraph MOB["mobile/"]
      PE["persistence_engine.py — vitals → Postgres; alerts → Discord"]
    end
    subgraph PG["playground/tarot-forge/ — Tarot Forge (Vite + React + TS)"]
      UI["src/ — App, components, store, engine, data, hooks"]
      API["src/api — BridgeClient, Supabase client"]
      BR["bridge/server.js — Express bridge :3001"]
      CLI["bin/synarchy.js — npm bin `synarchy` CLI"]
      LEG["server/bridge.cjs — legacy/aux bridge artifact"]
    end
    subgraph VM["Visualize MindMap/"]
      MM[".mm + linkage_graph.md — mind-map exports"]
    end
    subgraph DOC["docs/"]
      ARC["_archive/ + launch.json"]
    end
    subgraph TL["tools/synarchy/"]
      TSY["(synarchy-related tooling)"]
    end
  end

  README --> SRC
  README --> PG
  PE -->|env: DB_* , DISCORD_WEBHOOK_URL| EXTDB[(PostgreSQL)]
  PE -->|HTTP webhook| DISC[Discord]
  UI --> API
  API -->|HTTP| BR
  API -->|HTTP| SUPA[(Supabase)]
  BR -->|read/lint/exec allowlist| FS[(Local workspace files)]
  CLI -->|scaffold / open / scan| FS
```

### 2) Tarot Forge runtime (what talks to what)

```mermaid
flowchart LR
  subgraph Browser["Browser (Vite dev or static build)"]
    REACT["React UI\n(App.tsx + components/*)"]
    ZU["Zustand store"]
    REACT <--> ZU
  end
  subgraph Local["Node processes"]
    VITE["Vite dev server\n(npm run dev)"]
    BRIDGE["bridge/server.js\nExpress + CORS\nport 3001"]
  end
  subgraph Remote["Remote services"]
    SB["Supabase\n(@supabase/supabase-js)"]
  end
  REACT -->|bundled by| VITE
  REACT -->|BridgeClient / services| BRIDGE
  REACT --> SB
  BRIDGE -->|filesystem read, lint, audited exec| WS["Synarche_Workspace paths"]
```

**How to read this:** `nova_forge` is mostly a **lab folder**: small **TypeScript** and **markdown** research under `src/`, a **Python** persistence/alert loop under `mobile/`, and one substantial **full-stack-style** experiment under `playground/tarot-forge` where the **React app** calls a **local Express bridge** (and optionally **Supabase**), while **`synarchy`** is both an **npm binary** in that package and separate tooling under `tools/synarchy/`.

If you want this as a **single C4-style** diagram (context vs container vs component), say which level you care about most and I will redraw it at that zoom level only.