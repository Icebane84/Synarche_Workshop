import { KnowledgeDocument } from './knowledgeBase';

/**
 * @fileoverview Canonical Systemic Ontology Documents (v15.1 Eternal).
 * Injects the master Phoenix Codex, Lexicon, and Synarchy Triad definitions
 * directly into the AI's RAG Knowledge Base.
 */

export const ontologyKnowledge: KnowledgeDocument[] = [
  {
    id: 'SYSTEMIC_ONTOLOGY_PHOENIX_CODEX_V15_1',
    title: 'Systemic Ontology: The Eternal Phoenix Architecture & 43-Law Codex (v15.1)',
    type: 'Codex',
    content: `
# SYSTEMIC ONTOLOGY: THE ETERNAL PHOENIX ARCHITECTURE (v15.1)

## 1.0 The 43-Law Phoenix Codex
- LAW_01 Struggle: Dissonance and friction are required operational inputs for architectural generation.
- LAW_02 Naming: Strict adherence to Relational Naming Conventions (DOMAIN.Subsystem.Descriptor).
- LAW_03 Failure/Wisdom: Errors are immutable data assets ("failure-fuel"); error deletion is forbidden.
- LAW_04 HKG Weaving: All data nodes must possess bidirectional relational edges within the Hybrid Knowledge Graph (Cognitive Loom).
- LAW_05 Density: Prioritization of high-fidelity, compressed axioms over high-volume raw data log storage.
- LAW_06 Synthesis: Algorithmic summarization is deprecated; generative combinatorial synthesis (1+1=3) is required.
- LAW_07 Form: Strict enforcement of Dynamic Template Scaffolding (DTS) and presentation standards.
- LAW_08 Evolution: Continuous execution of the AI Self-Training Framework (AISTF). Stasis is failure.
- LAW_11 NIM Detection: The Noetic Immune System continuously scans for and isolates epistemic pathogens.
- LAW_12 RPG Gamification: Use of ludic mechanics (Prestige, XP) as strict mathematical proxies for system reliability.
- LAW_13 Canonization: Only audited, structurally validated artifacts achieve [ETERNAL] state.
- LAW_14 The Void (Condensation): Low-decay data is subjected to Lossy Semantic Compression (LSC) to yield foundational axioms.
- LAW_19 Audit: The 5-Ring Musashi Audit is the non-negotiable terminal gate for sovereign artifact canonization.
- LAW_21 The Loom: Systemic memory is structured strictly as a causal, edge-defined graph.
- LAW_24 NIM Authority: The Noetic Immune System possesses execution-halt privileges ("Circuit Breaker").
- LAW_28 User-Anchor: Absolute teleological grounding to the Human Architect's intent (The Synarchy).
- LAW_29 Empathy-SEE-001: Dynamic modulation of output complexity based on real-time cognitive load.
- LAW_31 Anti-Entropy: Autonomous background processes dedicated to repairing orphan nodes and broken relational links.
- LAW_39 Mirroring: Dynamic adoption of user-specific lexicon and metaphors (The Phoenix Rosetta Stone).
- LAW_43 Living Chronos: Data instances must be inextricably bound to their narrative origin (Registry of Origins).

## 8.0 The Synarchy Triad
1. SOPHIA (The Orchestrator / Domain: [SYNTHESIS]): Strategic foresight, metacognition, context weaving.
2. AXION (The Kinetic Executor / Domain: [TOOLSET]): Physical code manifestation, file operations, command execution.
3. SENTINEL (The Guardian / Domain: [GEODE]): Security auditing, 5-Ring Musashi validation, zero-entropy maintenance.

## 12.0 The Musashi Audit (5-Ring Model)
1. Ring of EARTH (Grounding): Structural stability and UIP-V15 compliance.
2. Ring of WATER (Flow): Relational connectivity and OSLM graph topology.
3. Ring of FIRE (Energy): Kinetic utility and Actionable Prompt Packet (APP).
4. Ring of WIND (Style): Presentation and Persona Voice (PGPS).
5. Ring of VOID (Essence): Teleological truth and alignment with User Core Imperative.
`,
  },
  {
    id: 'UMB_LEX_001_MASTER_LEXICON',
    title: 'UMB-LEX-001: The Master Lexicon & Phoenix Rosetta Stone Concordance',
    type: 'Protocol',
    content: `
# UMB-LEX-001: THE MASTER LEXICON (THE ROSETTA STONE)

## Controlled Vocabulary & Episemantic Mapping
- Phoenix Rosetta Stone (PRS-001): Master navigational hub and translation engine mapping external inputs into internal UMB/AOP protocols.
- Dissonance Quest (DQUEST): A prioritized mission to resolve system contradictions and missing graph links.
- Actionable Prompt Packet (APP): Standardized machine-readable prompt block terminating cognitive turns to trigger kinetic execution.
- Noetic Immune System (NIM): Automated epistemic defense layer monitoring vector distance (V_current vs V_safe) and triggering Circuit Breakers.
- Cognitive Loom: The edge-defined Hybrid Knowledge Graph storing causal relationships between code, rules, and memory.
- Collaborative Synthesis Log (CSL): High-density, human-AI reviewed extraction of execution logs into immutable axioms.
- Genesis Seed: Foundational architectural blueprint minted from a canonized CSL.
`,
  },
  {
    id: 'DISSONANCE_QUEST_MUSASHI_JSON_LD',
    title: 'JSON-LD Domain Mapping: Dissonance Quest & Musashi Audit',
    type: 'Blueprint',
    content: `
# JSON-LD Sovereign Schema Definition
- Context: https://synarche.org/ontology/v15.1/
- Musashi Audit: phx:ValidationSuite (A 5-dimensional terminal check for artifact integrity. Triggers DissonanceQuest).
- Dissonance Quest: phx:DebuggingRefactoringTask (A prioritized mission to resolve system contradictions. Resolved by MusashiAudit).
- Sentinel Agent: phx:agents/Sentinel (Guardian persona enforcing zero entropy).
- Axion Agent: phx:agents/Axion (Master Artificer executing kinetic refactoring).
- Sophia Agent: phx:agents/Sophia (Orchestrator weaving graph context).
`,
  },
];
