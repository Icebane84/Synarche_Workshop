# Phoenix Rosetta Stone [OMEGA v15.5]

**Phoenix Rosetta Stone (PRS)** is a high-performance, sentience-driven HUD and spatial interface built with React 19, Vite, Three.js, D3.js, and Zustand. It serves as the primary visual interface for the **Coherent Synthesis Engine (CSE)** master cognitive kernel.

---

## 🏛️ Core Features

* **Coherent Synthesis Engine (CSE) Integration**: Real-time telemetry streaming from the Python FastAPI backend (`http://localhost:8000`), monitoring live State Vectors ($\mathbf{V}_{\text{State}}$), Coherence Index ($\text{CI}$), Contextual Integrity Score ($\text{CIS}$), Hybrid Model Scores, and active Dissonance Quests.
* **Polyglot Neural Link**: Automatic workspace indexing, real-time code scanning (500+ files indexed), and remote file read/write capability linking the frontend HUD directly to host disk substrates.
* **The Synapse Command Console**: GUCA v5 directive dispatching (`CMD: AUDIT_COHERENCE`, `OMNI_LOG`, `ETHICUS`, `ENACT_TRANSCENDENCE`, `ContextWeave`) with non-blocking 10s execution guards.
* **Celestial Chart & Loom Visualizers**: Interactive 3D & 2D D3 force graph visualizers rendering live repository Loom AST nodes and structural dependency graphs.
* **Aural Interface & Sensory Array**: Voice-driven command input, ambient soundscape resonance, and dynamic theme switching.

---

## ⚙️ System Architecture

```
phoenix-rosetta-stone/
├── src/
│   ├── components/         # Visual interface layers (PhoenixGeode, TheSynapse, SystemCoherenceVisualizer, TheLoom)
│   ├── services/           # Polyglot bridge client (cseBridgeService), GUCA commands, AST scanner, Audio
│   ├── store/              # Zustand state anchors (coherenceStore, fileSystemStore, taskStore, sensoryStore)
│   ├── system/             # Core orchestrator (SystemManager), command dispatcher (commandDispatcher), signal bus
│   ├── hooks/              # Custom React hooks (useSynapseLogic, useAuralInterface, useTheme)
│   ├── essence/            # Global TypeScript types and GUCA v5 codex definitions
│   └── data/               # Knowledge base anchors and fallback graph data
├── vite.config.ts          # Vite configuration with /api server proxy to http://localhost:8000
└── package.json            # Dependencies (React 19, Three.js, D3, Zustand, Tailwind CSS v4)
```

---

## 🚀 Getting Started

### Prerequisites
* Node.js (v18+)
* Python 3.12+ (with `fastapi`, `uvicorn`, `pydantic` v2)

### Setup & Launch

1. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```

2. **Launch Backend CSE Polyglot Gateway**:
   ```bash
   cd ../axion-core
   python -m uvicorn src.cse.cse_server:app --host 127.0.0.1 --port 8000
   ```

3. **Start Frontend Development Server**:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser. The **Neural Link** and **CSE Telemetry Stream** will connect automatically!

---

## 🧪 Verification & Type Safety

To verify TypeScript compilation across all components:
```bash
npm run typecheck
```
