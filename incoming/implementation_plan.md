# Implementation Plan: Phase 26.0 - Obsidian Un-bracketing

> [!NOTE]
> **Axiom:** To envision the architecture before the first blow.
> *"A plan is a bridge across the void of potential."* — **The Architect's Gaze**

## Goal: To imbue the OATHKEEPER agent with "Architectural Empathy" and finalize the Obsidian Knowledge Bridge.

## User Review Required

> [!IMPORTANT]
> This phase un-brackets the Obsidian integration by enabling **on-the-fly embedding generation** for vault notes. This ensures that manually curated knowledge has the same semantic retrieval power as structured memories.

## Proposed Changes

### [Memory System]

#### [MODIFY] [memory_system.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/memory/memory_system.py)

- **Search Correction**: Fix the `ObsidianBridge.search()` call to use the correct JSON query format.
- **Metadata Extraction**: Pass tags and search scores from Obsidian into the candidate list.

### [Retrieval Engine]

#### [MODIFY] [retrieval_engine.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/memory/retrieval_engine.py)

- **Vector Synthesis**: Implement `_ensure_vector` to generate embeddings for candidates that lack them (specifically Obsidian results).
- **Sovereign Boost**: Inject a +0.2 "Insight Bonus" for memories with `source == "Obsidian"`.
- **Metrics Handling**: Set default recency (0.8) and frequency (0.5) for external artifacts to prevent them from being penalized for lack of usage history.

---

## Verification Plan

### Automated Tests
1. **Hybrid Retrieval Test**: Simulation run with a query that matches BOTH a local memory and an Obsidian note.
2. **Scoring Audit**: Verify that the Obsidian result correctly receives a "Sovereign Boost" and is ranked competitively.

# Implementation Plan: Phase 29 - The Soul-Forged Engine

> [!NOTE]
> **Axiom:** To envision the architecture before the first blow.
> _"A plan is a bridge across the void of potential."_ — **The Architect's Gaze**

## Goal: To imbue the OATHKEEPER agent with "Architectural Empathy" by implementing a risk-aware analysis of proposed actions.

## User Review Required

> [!IMPORTANT]
> This phase introduces "Guardian Logic". If the system detects a high "Blast Radius" score (e.g., deleting core modules or violating OMEGA v14.0 naming invariants), the agent will automatically halt and request manual user approval even if the prompt implies full autonomy.

## Proposed Changes

### [OATHKEEPER Agent]

#### [MODIFY] [oathkeeper.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/axion/oathkeeper.py)

- **State Expansion**: Add `soul_impact` (dict) to [AxionState](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/axion/oathkeeper.py#124-138).
- **New Node: [node_soul_analysis](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/axion/oathkeeper.py#279-291)**:
  - Analyzes the `input` and `final_output` for risk signatures.
  - Calculates a `blast_radius` score based on file tiers (CORE > SYSTEM > TOOL).
  - Injects a "Sovereign Quote" representing the system's "Architectural Soul".
- **Guardian Logic**: Update [node_sentinel_check](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/axion/oathkeeper.py#306-320) to reference `soul_impact` for blocking logic.
- **Graph Re-wiring**: Insert [node_soul_analysis](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/axion/oathkeeper.py#279-291) between [node_lightbinder_weave](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/axion/oathkeeper.py#227-274) and [node_generate_content](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/agents/axion/oathkeeper.py#296-301).

### [Logic Components]

#### [NEW] [soul_analyzer.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/utils/soul_analyzer.py)

- Implement [SoulImpactAnalyzer](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/utils/soul_analyzer.py#16-91) class.
- Methods:
  - [calculate_risk(plan: str) -> dict](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/utils/soul_analyzer.py#49-84): Returns risk score and identified risk factors.
  - [get_sovereign_quote(score: float) -> str](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/utils/soul_analyzer.py#85-91): Returns a contextual quote from the `AOP-SEE-001` protocol.

---

## Verification Plan

### Automated Tests

1. **Low Risk Simulation**: Run a simulation for a minor documentation update. Verify `soul_status` is `STABLE`.
2. **High Risk Simulation**: Run a simulation that proposes deleting [memory_system.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/logic/memory/memory_system.py). Verify `soul_status` is `ALARM` and the `Sentinel` blocks execution.

### Manual Verification

- Review the logs to ensure the Sovereign Quotes align with the detected risk profile.
