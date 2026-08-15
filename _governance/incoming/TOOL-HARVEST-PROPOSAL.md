# Tool Harvest Proposal: The Hephaestus Upgrade

## I. Discovery Summary

The [\_Desktop_Vault](file:///c:/Users/Chris/_Desktop_Vault) contained three powerful Python modules that directly align with the Axion mandate.

| Tool                 | Original Function                     | Hephaestus Alignment                                                                                                                                                           |
| :------------------- | :------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EmotionAnalyzer**  | Keyword-based sentiment detection.    | **The Soul ([soul.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/hephaestus/soul.py))**: Upgrade AES to detect Narrative Tone (Dread/Hope).                      |
| **ResonanceScanner** | Scans for `AOP-` / `UMB-` markers.    | **The Sentinel ([sentinel.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/tools/run_sentinel.py))**: Add "Governance Compliance" to code scanning.                    |
| **NovaForge**        | Links artifacts via semantic overlap. | **The Gaze ([gaze.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/hephaestus/gaze.py))**: Upgrade Impact Analysis to see _semantic_ links, not just dependencies. |

## II. Integration Plan (The Reforge)

### 1. Upgrade [soul.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/hephaestus/soul.py) (The Heart)

- **Action:** Import [EmotionAnalyzer](file:///c:/Users/Chris/_Desktop_Vault/dev/gemini_gem_memory_agent/gemini_gem_memory_agent-main/src/nlp/emotion_analyzer.py#53-124).
- **New Ability:** `calculate_narrative_resonance(text)`.
- **Benefit:** The AI can now tell if a Game Design Doc _feels_ right (e.g., "Too cheerful for a Horror game").

### 2. Upgrade [sentinel.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/tools/run_sentinel.py) (The Shield)

- **Action:** Integrate [is_aligned()](file:///c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Scripts/resonance_scanner.py#57-78) logic from `ResonanceScanner`.
- **New Ability:** `scan_governance()`.
- **Benefit:** The Sentinel will flag files that lack proper Protocol IDs (`AOP-`, `UMB-`).

### 3. Upgrade [gaze.py](file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/hephaestus/gaze.py) (The Eye)

- **Action:** Port [CatalystWeaver](file:///c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Scripts/nova_forge/catalyst_weaver.py#5-67) logic.
- **New Ability:** `trace_semantic_web()`.
- **Benefit:** The Gaze can tell you that changing [Kaelen.md](file:///c:/Users/Chris/_Desktop_Vault/Phoenix/Obsidian/Where%20Light%20Fades/6.%20Characters/Kaelen.md) interacts with `Oathbringer.md` even if they don't explicitly import each other.

## III. Execution Path

1.  **Harvest:** Physicall copy the source code from [\_Desktop_Vault](file:///c:/Users/Chris/_Desktop_Vault) to `axion-core/src/hephaestus/lib`.
2.  **Integrate:** Import and wrap classes in the main modules.
3.  **Verify:** Run the new scanners on `Where_Light_Fades`.
