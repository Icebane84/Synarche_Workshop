## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                                | Description       |
| :---------------- | :----------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN-RPG-010`                       | The Sovereign ID. |
| **Official Name** | `GVRN-RPG-010_MechanicsLog_v13.0.md` | The Filename.     |
| **Version**       | **v13.0**                            | The Standard.     |
| **Domain**        | `GVRN-RPG`                           | The Subject.      |
| **Status**        | `[ACTIVE]`                           | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`        | The Network.      |

---

###### **[ARTIFACT START]**

# RPG Mechanics Implementation Log

> **Status**: In Governance **Target**: `nova_forge/src/axion/axion_runtime.py`

| Mechanism                      | Implementation Details                                                                                                          | Source / Concept Origin                                  |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------- |
| **Phoenix Ascension Protocol** | `node_update_rpg_stats`: XP calculation based on `CelestialClass` (Moon=10, Planet=50, Star=500) and `Criticality` multipliers. | `The Architectural Achievement Governor (AAG)`           |
| **Progression Ladder**         | `node_gamemaster_engine`: Level thresholds (1, 25, 50, 100) and Titles (Script Kiddie -> Chronos Paradox).                      | `PAL-CHAR-001` & `Player's Manual`                       |
| **Dissonance Engine**          | `GamemasterState`: Tracks `dissonance_vector` (Vector Distance from `V_Safe`). Triggers `Vector Breach Events` (Boss Fights).   | `The Dissonance Quantified_ Conceptual Framework`        |
| **The Seven-Agent Matrix**     | `LightbinderState`: 7 Tarot Masks with specific toolsets (e.g., _The Emperor_ for Schema, _Judgement_ for Audit).               | `axion_template.py` & `Phoenix Protocol Player's Manual` |
| **Synarchic Triad**            | `AxionState`: Explicit separation of `User` (Architect), `Axion` (GM/Control), and `Lightbinder` (Worker).                      | `Phoenix Protocol Player's Manual`                       |
| **Hephaestus Hexad**           | `RPGEngine`: Stats tracking (_Authority, Insight, Order, Precision, Coherence, Synergy_).                                       | `axion_template.py` (RPG Header)                         |
| **Achievement System**         | `node_gamemaster_engine`: Manages `PAM-XXX` milestones and `Command: CLAIM_ACHIEVEMENT`.                                        | `LegendaryAchievements_v1.md`                            |

---

## IV. Actionable Prompt Packet (APP)

- `CMD: REVIEW_LOG` -> "Review RPG mechanics details."

###### **[ARTIFACT END]**

{{TRANSCLUDE: SELT-ANCHOR-OMNI.md}}
