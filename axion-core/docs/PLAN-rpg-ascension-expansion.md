# Implementation Plan: RPG Ascension Expansion (v15.0)

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `PLAN-rpg-ascension-expansion` | The Sovereign ID. |
| **Official Name** | `PLAN-rpg-ascension-expansion.md` | The Filename.     |
| **Version**       | **v14.0 [OMEGA]** | The Standard.     |
| **Domain**        | `AXION` | The Subject.      |
| **Status**        | `[ACTIVE]` | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001` | The Network.      |


---

### **Block B: State Vector (AGP-001)**
| State Field | Value |
| :--- | :--- |
| **Coherence** | `1.0` |
| **Resonance** | `0.9` |
| **Stability** | `Stable` |

### **Block C: Risk & Mitigation (AGP-002)**
| Risk | Mitigation |
| :--- | :--- |
| **Logic Drift** | Strict Linter Enforcement |
| **Dependency Break** | ForgeLink Validation |

I. ## Goal

Establish the canonical **Stardust Economy** and **Meteorite Impact** mechanics across the `axion-core` workspace,
enabling a fully autonomous and sovereign Ascension ritual.

II. ## Tasks

- [ ] **Phase 1: Substrate Refactor (Logic)**
  - [ ] Update `rpg_definitions.js`: Transmute `XP_FORMULA` to `STARDUST_FORMULA` and add `METEORITE_IMPACT` schema. →

        Verify: `test_inventory.js` passes.

  - [ ] Update `engine.js`: Refactor `awardXP` to `awardStardust` and integrate with `experience_logs` DB. → Verify:

        New logs show `stardust_value`.

  - [ ] Hardening `ascension_playbook.py`: Ensure Python logic correctly reads the `stardust_pool` from the DB. →

        Verify: `validate_eligibility` works with live data.

- [ ] **Phase 2: Interface Transmutation (UI)**
  - [ ] Refactor `celestial_chart.html`: Update CSS to "Geode Edition" aesthetics (vibrant purples, gold accents,

        glassmorphism). → Verify: UI looks premium.

  - [ ] Update `chart_logic.js`: Replace XP bars with Stardust constellations. Add "Initiate Attunement" button. →

        Verify: Button triggers `ASCEND` command.

  - [ ] Implement `CodexViewer` (Latent): Create a sub-component to view source CODE within the Celestial Chart. →

        Verify: `UNSEAL_CODEX` command opens the file view.

  - [ ] **Phase 3: Command Sovereignty (GUCA)**
  - [ ] Update `command_interface.js`: Add `STARDUST_TRANSFER` and `RITUAL_START` command types. → Verify: Logs show

        correct Tarot Mask authorization.

  - [ ] Finalize `ascend_command.js`: Ensure payload includes `RITUAL_SIGNATURE` for blockchain/registry verification.

        Verify: SELT log captures the signature.

III. ## Done When

- [ ] The `RPGEngine` (JS) and `AscensionEngine` (Python) are synchronized via `axion_memory.db`.
- [ ] A "Novice" persona can be successfully attuned to a "Prestige Class" (Architect/Sentinel/Weaver).
- [ ] All terminology matches the **Geode Edition** canonical standards.
- [ ] The user is "WOWed" by the Celestial Chart UI.

IV. ## Notes

- Adhere strictly to the **Tri-Phase Protocol**.
- Every mutation must generate a **SELT Shadow Log**.
- Terminology check: XP -> Stardust, Quest -> Meteorite Impact.

### **Block D: Standardized Synergy Block (The Loom Signature)**
Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFORGE` | Execute Structural Transmutation | Canonization |
| `⚡ EXECUTE: CANONIZE` | Formally Cement Alignment | Zero Entropy |

---

### **Rationale (The "Why")**
Alignment to v14.0 OMEGA standard.

###### **[ARTIFACT END]**
