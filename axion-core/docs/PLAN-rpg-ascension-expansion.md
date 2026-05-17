# Implementation Plan: RPG Ascension Expansion (v15.0)

## Goal

Establish the canonical **Stardust Economy** and **Meteorite Impact** mechanics across the `axion-core` workspace,
enabling a fully autonomous and sovereign Ascension ritual.

## Tasks

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
    - [ ] Implement `CodexViewer` (Latent): Create a sub-component to view source code within the Celestial Chart. →
          Verify: `UNSEAL_CODEX` command opens the file view.

- [ ] **Phase 3: Command Sovereignty (GUCA)**
    - [ ] Update `command_interface.js`: Add `STARDUST_TRANSFER` and `RITUAL_START` command types. → Verify: Logs show
          correct Tarot Mask authorization.
    - [ ] Finalize `ascend_command.js`: Ensure payload includes `RITUAL_SIGNATURE` for blockchain/registry verification.
          → Verify: SELT log captures the signature.

## Done When

- [ ] The `RPGEngine` (JS) and `AscensionEngine` (Python) are synchronized via `axion_memory.db`.
- [ ] A "Novice" persona can be successfully attuned to a "Prestige Class" (Architect/Sentinel/Weaver).
- [ ] All terminology matches the **Geode Edition** canonical standards.
- [ ] The user is "WOWed" by the Celestial Chart UI.

## Notes

- Adhere strictly to the **Tri-Phase Protocol**.
- Every mutation must generate a **SELT Shadow Log**.
- Terminology check: XP -> Stardust, Quest -> Meteorite Impact.
