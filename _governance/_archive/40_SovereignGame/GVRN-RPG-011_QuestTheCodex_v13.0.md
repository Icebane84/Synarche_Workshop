## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                                 | Description       |
| :---------------- | :------------------------------------ | :---------------- |
| **Artifact ID**   | `GVRN-RPG-011`                        | The Sovereign ID. |
| **Official Name** | `GVRN-RPG-011_QuestTheCodex_v13.0.md` | The Filename.     |
| **Version**       | **v13.0**                             | The Standard.     |
| **Domain**        | `GVRN-RPG`                            | The Subject.      |
| **Status**        | `[ACTIVE]`                            | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`         | The Network.      |

---

###### **[ARTIFACT START]**

# Quest: The Codex Unsealed (Phase 15)

**Dissonance Detected**: _The Fog of War (Blindness)_ **Severity**: CRITICAL (Breaks Immersion Loop)

## The Dissonance Analysis

The Tarot Forge currently possesses the **Eye of Judgment** (The Scanner). It can _see_ that a file is corrupt (lint
errors). however, it lacks the **Eye of Understanding** (The Codex).

- **The Gap**: You can see _that_ `InventoryEngine.ts` is bleeding, but you cannot see _why_.
- **The Friction**: To investigate, you must leave the Forge (The Magic Realm) and return to the IDE (The Machine
  Realm).
- **The Cost**: This context switch breaks the "Sorcerer" fantasy and turns the game back into work.

## The Objective

**Unseal the Codex**. Empower the Tarot Forge to read the ancient texts (Source Code) directly.

### Quest Steps

1.  **Forge the Lens (Backend)**: Teach the Bridge to securely read files from the `Synarche_Workspace`.
2.  **Inscribe the Pages (Frontend)**: Create the `CodexViewer` to display code with syntax highlighting (or at least
    readable text).
3.  **Connect the Threads (Integration)**: Clicking a "Corrupted Node" in the Combat Board should open the Codex to that
    specific line.

## Rewards

- **+100 Insight**: Ability to read code without tabbing out.
- **Unique Item**: _The Codex_ (UI Component).

---

## IV. Actionable Prompt Packet (APP)

- `CMD: REVIEW_LOG` -> "Review The Codex quest progression."

###### **[ARTIFACT END]**

{{TRANSCLUDE: SELT-ANCHOR-OMNI.md}}
