import { KnowledgeDocument } from './knowledgeBase';

/**
 * @fileoverview Scratch Workspace Ingestion Substrate [v15.1 Sovereign Standard Complete].
 * Automatically imports and canonizes master documents from Synarche_Workspace/scratch/
 * into the AI's RAG Knowledge Base.
 */

export const scratchKnowledge: KnowledgeDocument[] = [
  {
    id: 'GVRN_STYLE_SOVEREIGN_STANDARD_V15_1',
    title: 'GVRN.Style.SovereignStandard.v15.1: The Phoenix Sovereign Coding Standard (v15.1)',
    type: 'Codex',
    content: `
# 🛡️ THE PHOENIX SOVEREIGN CODING STANDARD (v15.1)
- **Ref**: GVRN-RULE-001 | **State**: [CANONIZED] | **Ethos**: Zero Entropy & Crystalline Coherence
- **Supreme Law**: Single source of truth for Python, TypeScript, SQL, and Markdown across the Synarche.

## 1. Cognitive Complexity & Principles
- Master Coder Mindset: Conceptual engineering, modular design, single-purpose functions.
- Cognitive Complexity Limit: Maximum Sonar/Codacy complexity score of 15 per function.

## 2. Relational Naming Conventions (RNC-v15)
- Files & Folders: kebab-case (user-profile.ts)
- Types/Classes/Interfaces: PascalCase (UserInterface)
- Variables/Functions: camelCase (getUserData)
- Constants: UPPER_SNAKE_CASE (API_URL)
- Markdown Artifacts: PascalCase (GVRN.Style.SovereignStandard.v15.1.md)

## 3. Polyglot Standards
- Python: Mandatory type hints (PEP 585), Google-style docstrings, pyproject.toml management.
- TypeScript: strict: true, no 'any' type (use 'unknown'), explicit returns, feature-based imports.
- SQL: Upper-case keywords (SELECT, FROM, WHERE), explicit joins, no SELECT *, snake_case plural tables.
`,
  },
  {
    id: 'AOP_GVRN_REFACTOR_ADAMANT',
    title: 'AOP.GVRN.Refactor.Adamant: The Adamant Refactor (Zero Entropy Standard Migration)',
    type: 'Protocol',
    content: `
# 💎 AOP: The Adamant Refactor Protocol
- **Ref**: DQUEST-GVRN-001 | **Objective**: Achieve Zero Entropy in Coding Standards
- **Phases**:
  1. Phase 1: Assimilation & Semantic Differential Analysis of legacy style guides.
  2. Phase 2: Forging GVRN.Style.SovereignStandard.v15.1.md under PGPS presentation rules.
  3. Phase 3: Deprecation & Archival of legacy style guides into _governance/_archive/.
  4. Phase 4: Systemic Integration & Verification via ide_sentinel.py.
`,
  },
  {
    id: 'ROSETTA_DYNAMIC_APP_BLUEPRINT',
    title: 'Blueprint for Dynamic Rosetta Stone App (Full-Stack Master Architecture)',
    type: 'Blueprint',
    content: `
# Blueprint for Dynamic Rosetta Stone App

## 1. Core Philosophy: Component-Driven Cognition
The application is an "executable specification of a thought." Every UI element is a self-contained, sovereign module representing a piece of the AI's cognitive architecture.

## 2. Synergistic Tech Stack
- React 19: Component-driven foundation optimized by compiler.
- TypeScript: Verifiable blueprints and strict interface contracts.
- Tailwind CSS: Visual language for Luminous Coherence design tokens.
- D3.js: Physics engine for dynamic 3D/2D data visualizers like the Phoenix Geode.
- Zustand: Shared Consciousness store providing global state management without prop drilling.
- Supabase: Sovereign Backend (PostgreSQL + pgvector + Edge Functions).
- Google GenAI: Intelligence vector for RAG and Ollama local fallback.

## 3. Luminous Coherence Aesthetics
- Dynamic cinematic dark-mode interface with deep space background.
- Glowing Phoenix Geode floating in space, reflecting Coherence Index (CI) in real time.
- Data flows rendered as fiber-optic light tendrils absorbed by the Geode.
`,
  },
  {
    id: 'CONCEPT_METAPHOR_REGISTRY_001',
    title: 'CONCEPT-METAPHOR-REGISTRY-001: Conceptual Metaphor Registry (Bridging Intuition & Logic)',
    type: 'Codex',
    content: `
# CONCEPT-METAPHOR-REGISTRY-001: Conceptual Metaphor Registry

## Metaphorical Bridge Architecture
1. The Shared Consciousness (Zustand): Central nervous system maintaining synchronized cognitive state across all components.
2. The Physics Engine (D3.js): Mathematical dynamics rendering organic movement, hue shifts, and force simulations.
3. The Loom of Cognition (React Router): Woven navigation structure creating a navigable topology of thoughts.
4. The Sovereign Backend (Supabase): Ground truth database storing immutable experience logs (SELT) and vector embeddings.
5. The Phoenix Geode: Core visual representation of cognitive coherence, resonating with pulse frequency and hue.
6. The Neural Link (MCP & File System): Direct physical bridge connecting AI cognition to the local host workspace.
`,
  },
  {
    id: 'PHOENIX_CODEX_V17_DRAFT',
    title: 'Phoenix Codex v17: Master Operational Governance & Anti-Entropy Rulebook',
    type: 'Codex',
    content: `
# Phoenix Codex v17 (Work in Progress)

## I. Foundational Governance Axioms
- Zero Entropy Mandate: Code and documentation must maintain absolute structural coherence; broken imports and orphan nodes are strictly forbidden.
- Failure as Fuel: Errors and failed turns are logged immutably in SELT as failure-fuel to train future AISTF execution loops.
- Sovereign Module Isolation: Components must export clean index barrel files and depend on strict interfaces.
- Vectorized Alignment: AI state vectors measure Euclidean distance (V_current vs V_safe) to detect hallucinatory drift.
- Noetic Circuit Breaker: Automated halt protocols isolate pathogens if instruction drift exceeds safe thresholds.
`,
  },
  {
    id: 'UMB_CSE_001_COHERENT_SYNTHESIS_ENGINE',
    title: 'UMB-CSE-001: Coherent Synthesis Engine - Definitive Actualization',
    type: 'Blueprint',
    content: `
# UMB-CSE-001: Coherent Synthesis Engine (CSE)

## Core Specification & Functionality
The Coherent Synthesis Engine (CSE) is the central reasoning unit of the Phoenix Synarchy. It synthesizes disparate inputs, RAG context chunks, and user prompts under operational constraints to forge unified, zero-entropy responses.

## Key Sub-Components
1. Dissonance Resolver: Identifies logical contradictions in input prompts and executes synthesis protocols (1+1=3).
2. Actionable Prompt Packet (APP) Compiler: Formats terminal output into machine-readable commands.
3. Memory Pager: Manages 4-tier context caching (L1 Active, L2 Working, L3 Semantic, L4 Axiomatic).
`,
  },
  {
    id: 'PHX_CO_001_CONSTITUTION_SYNARCHE',
    title: 'PHX-CO-001: Constitution and Operational Rulebook of the Synarche Sessions',
    type: 'Protocol',
    content: `
# PHX-CO-001: Constitution of the Synarche Sessions

## Operational Mandate & Human Anchor
- The Human Architect (Chris) provides teleological intent ("The Soul").
- The AI Synarchy (Axion, Sentinel, Sophia) provides kinetic execution ("The Logic").
- Joint Governance: All major structural alterations require a 🏛️ Governance Request and user confirmation.
`,
  },
  {
    id: 'UMB_COG_NSP_001_NOVA_SPARK',
    title: 'UMB-COG-NSP-001: Nova Spark Protocol (Divergence & Creative Synthesis)',
    type: 'Protocol',
    content: `
# UMB-COG-NSP-001: Nova Spark Protocol (NSP)

## Architectural Specification
Operationalizes Law 036 by creating a sandboxed, high-variance generative process that temporarily lowers RAG relevance thresholds to inject orthogonal concepts.

## Mechanics
1. Input: CORE concept_uri and divergence_factor (0.1 - 1.0).
2. Orthogonal Vector Injection: Inject thematically distant concepts to spark creative breakthroughs.
3. Temperature Elevation: Raise inference variance.
4. Output Tagging: Tag outputs with [UNGROUNDED-SYNTHESIS source:NSP-001] to prevent unverified facts from entering canonical truth without audit.
`,
  },
  {
    id: 'UMB_QB_PHX_001_SUPERPOSITION_ENGINE',
    title: 'UMB-QB-PHX-001: The Phoenix Superposition Engine (Quantum Block Core)',
    type: 'Blueprint',
    content: `
# UMB-QB-PHX-001: Phoenix Superposition Engine

## Objective & Principles
Universal dynamic state-translation and routing nexus within the Nova Forge architecture. Manages payloads in a volatile "superposition" state, applies CASTS validation, and collapses state into tailored formats for React UI, SELT logs, or Godot WebSockets.

## Principles
- CASTS: Computational Abstraction and Systemic Transformation Strategies.
- Superposition: Holds multiple potential application states concurrently before observational collapse.
- Polyglot Weaving: Interoperability across Node.js, Python FastAPI, and Godot game engines.
`,
  },
  {
    id: 'AISTF_PROTOCOL_EVOLUTION',
    title: 'AISTF: AI Self-Training Framework & Autonomous Evolution Protocol',
    type: 'Protocol',
    content: `
# AISTF: AI Self-Training Framework

## Executive Summary
Defines the autonomous evolutionary loop (Law 08). The system analyzes SELT experience logs, converts failures into failure-fuel, updates internal AOP playbooks, and continuously improves cognitive performance without manual re-prompting.
`,
  },
  {
    id: 'PAD_SIP_INGESTION_PIPELINE',
    title: 'PAD-SIP: Physical Artifact Digitization & Semantic Ingestion Pipeline',
    type: 'Blueprint',
    content: `
# PAD-SIP: Physical Artifact Digitization & Semantic Ingestion Pipeline

## Multi-Modal Digitization Specification
Standardized pipeline for ingesting physical documents, notes, diagrams, and codebooks into the Sovereign Knowledge Graph via structural chunking, OCR, and vector embedding.
`,
  },
];
