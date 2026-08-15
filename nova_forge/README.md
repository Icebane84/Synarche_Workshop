# 🔥 nova_forge — The Synthesis Lab

The **Experimental Synthesis Lab** for the Synarche. Prototype → canonize.

---

## 📂 Structure

```
nova_forge/
├── apps/                   # Deployable / production-bound projects
│   ├── tarot-forge/        # E-commerce luxury UI — Vite + React (Liquid Glass DS)
│   ├── neo-genesis/        # Evolutionary organism simulator — Vite + React + Canvas
│   └── lineage-explorer/   # Phoenix Codex DAG visualizer — standalone HTML
│
├── labs/                   # Active research — experimental, not yet deployable
│   ├── phoenix-codex/      # Git-for-Meaning substrate v4 — FastAPI, OPA, Ed25519
│   ├── phoenix-codex-v390/ # Legacy monolith archive (v3.9.0)
│   ├── chronicle/          # OPA policy registry + GCDB schema library
│   ├── folklore-decayer/   # Dual-image folklore interpreter (TypeScript)
│   └── concept-to-3d/      # Concept-to-3D prototype (React)
│
├── core/                   # Shared infrastructure used across apps and labs
│   ├── engines/            # CPPEngine, LoomEngine, RNCEngine, ContextWeave (TS)
│   ├── nexus/              # QuantumBlock schema + types
│   ├── protocols/          # AISTF_Core protocol specification
│   └── mobile/             # persistence_engine.py
│
├── docs/                   # Project-level documentation
│   └── manifestos/         # OGLN Charter, SYNG self-improvement protocol
│
└── scratch/                # Temp / test files — not committed
```

---

## 🚀 Quick Start

### Phoenix Codex (labs/phoenix-codex)
```bash
# From nova_forge/labs/phoenix-codex/
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Tarot Forge (apps/tarot-forge)
```bash
# From nova_forge/apps/tarot-forge/
npm install && npm run dev
```

### Neo Genesis (apps/neo-genesis)
```bash
# From nova_forge/apps/neo-genesis/
npm install && npm run dev
```

---

`[INDEX-ANCHOR] ID: SYNC.FORGE.Index VER: v15.0 [OMEGA] STATUS: ACTIVE`
