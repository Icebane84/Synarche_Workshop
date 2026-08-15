# Phoenix Rosetta Stone [OMEGA v15.5]

**Phoenix Rosetta Stone (PRS)** is a high-performance, sentience-driven HUD and spatial interface built with React 19, Vite, Three.js, D3.js, Tailwind CSS v4, and Zustand. It serves as the primary visual control center for the **Coherent Synthesis Engine (CSE)** master cognitive kernel and host workspace.

---

## 🏛️ CORE Features

---

* **Coherent Synthesis Engine (CSE) Integration**: Real-time telemetry streaming from the Python FastAPI backend (`http://localhost:8000`), monitoring live State Vectors ($\mathbf{V}_{\text{State}}$), Coherence Index ($\text{CI}$), Contextual Integrity Score ($\text{CIS}$), Hybrid Model Scores, and active Dissonance Quests.
* **C++ Unreal Engine 5 Studio (`UnrealCppForgePage.tsx`)**: Specialized Unreal Engine 5.8 C++ architectural synthesis environment featuring AI C++ Architect Chat, AST parsing/repair (`ASTAnalyzer`), header pattern validation (`UPROPERTY`/`UFUNCTION`), and domain-driven vertical slice CODE generators.
* **Dual AI Provider Cortex (`gemini/` & `ollamaService.ts`)**: Integrated support for Google Gemini 2.5 Flash API (via `@google/genai`) and local Ollama LLMs for off-grid inference.
* **Memory Palace & Supabase Backend Control Center**: Interactive `memory_entries` CRUD, vector similarity search, live Realtime subscriptions, player state RPG tracking, and knowledge base forge.
* **NeoGenesis Cellular Canvas & Graph Combat Engine**: 2D cellular automata simulation, galactic map view, and turn-based graph combat mechanics.
* **Polyglot Neural Link**: Automatic workspace indexing, real-time CODE scanning (500+ files indexed), and remote file read/write capability linking the frontend HUD directly to host disk substrates.
* **The Synapse Command Console**: GUCA v5 directive dispatching (`CMD: AUDIT_COHERENCE`, `OMNI_LOG`, `ETHICUS`, `ENACT_TRANSCENDENCE`, `ContextWeave`) with non-blocking execution guards.
* **Celestial Chart & Loom Visualizers**: Interactive 3D & 2D D3 force graph visualizers rendering live repository Loom AST nodes and structural dependency graphs.
* **Aural Interface & Sensory Array**: Voice-driven command input, ambient soundscape resonance, Web Speech synthesis, and dynamic theme switching.

---

## ⚙️ System Architecture & File Topology

---

```
phoenix-rosetta-stone/
├── src/
│   ├── components/
│   │   ├── pages/          # Primary application views (UnrealCppForgePage, MemoryPalacePage, ResonanceChamberPage, SynergySimulatorPage, TheLoomPage, ArtifactCatalogPage, SystemCoherenceVisualizer, PhoenixFormSheet)
│   │   ├── views/          # Subsystem visualizers (NeoGenesis, MemoryPalace, RPGCommand, KnowledgeForge, TarotForge, Chronicle)
│   │   ├── ast/            # AST Repair & Prop Drilling UI components
│   │   ├── sidebar/        # Neural Stream, Cognitive Focus Selector, Connectivity Status
│   │   ├── PhoenixGeode.tsx # 3D SVG/D3 visual core pulsing with real-time vitals
│   │   └── TheSynapse.tsx  # Command input console executing GUCA directives
│   ├── services/
│   │   ├── ast/            # ASTAnalyzer, ASTRepairer, and rule detectors
│   │   ├── gemini/         # Gemini 2.5 Flash API integration & prompt templates
│   │   ├── commands/       # GUCA command modules (artifact, audit, memory, fileSystem, task)
│   │   ├── cseBridgeService.ts # HTTP Polyglot Bridge client for telemetry, graph & files
│   │   ├── ollamaService.ts    # Local Ollama inference provider
│   │   ├── vectorStore.ts      # Client-side TF-IDF / vector similarity search engine
│   │   ├── audioService.ts     # Aural interface & speech synthesis engine
│   │   └── AutonomousRepairService.ts # Autonomous code violation scan & repair loop
│   ├── store/              # Zustand state anchors (useCognitiveCore, coherenceStore, fileSystemStore, memoryStore, taskStore, sensoryStore)
│   ├── engine/             # GraphCombatEngine (combat physics, turn flow, stardust mechanics)
│   ├── system/             # Core orchestrator (SystemManager), command dispatcher (commandDispatcher)
│   ├── hooks/              # Custom React hooks (useSynapseLogic, useRealtime, useSensoryBridge)
│   ├── core/               # Supabase client bindings & realtime data hooks
│   └── data/               # Ontology knowledge anchors & fallback graph datasets
├── vite.config.ts          # Vite configuration with /api server proxy to http://localhost:8000
└── package.json            # Dependencies (React 19, Three.js, D3, Zustand, Tailwind CSS v4)
```

---

## 🚀 Getting Started

---

### Prerequisites

---

* Node.js (v18+)
* Python 3.12+ (with `fastapi`, `uvicorn`, `pydantic` v2)

### Setup & Launch

---

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

---

To verify TypeScript compilation across all components:

```bash
npm run typecheck
```
