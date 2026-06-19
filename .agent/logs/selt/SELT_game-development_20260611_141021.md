## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                                        | Description       |
| :---------------- | :------------------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.SELT.GameDev.Enhance.SidechainDucking` | The Sovereign ID. |
| **Official Name** | `SELT_game-development_20260611_141021.md`   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**                            | The Standard.     |
| **Domain**        | `GVRN`                                       | The Subject.      |
| **Status**        | `[ACTIVE]`                                   | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix`            | The Network.      |

---

## **Block B: State Vector (AGP-001)**

| State Field   | Value    |
| :------------ | :------- |
| **Coherence** | `1.0`    |
| **Resonance** | `1.0`    |
| **Stability** | `Stable` |

---

### **Block C: Risk & Mitigation (AGP-002)**

| Risk               | Mitigation                |
| :----------------- | :------------------------ |
| **Logic Drift**    | Strict Linter Enforcement |
| **Semantic Decay** | Axiomatic Compass Audit   |

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
| :---------------------- | :---------------- | :---------------------------------------------- |
| `CORE.Codex.Phoenix`    | `GOVERNS`         | Provides the supreme law and ethical framework. |

---

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: GVRN.SELT.GameDev.Enhance.SidechainDucking VER: v15.0 [OMEGA] DOMAIN: GVRN STATUS: [ACTIVE] TS: 2026-06-11 HASH: OMEGA-V15`

###### **[ARTIFACT START]**

# SELT Shadow Log: Game Development Enhancements Phase 3 (Sidechain Audio Ducking)

### Dissonance & Deconstruction:

- **Dissonance (Explosion Audio Clutter):** Per the `game-audio` guidelines, an explosion should briefly duck other audio elements (like BGM and ambient beats) by -3 to -6 dB to preserve mix clarity and maximize impact. Without this sidechain ducking, the bass-heavy explosion conflicts with the arpeggiator notes and kick-drum sequence, creating a muddy frequency collision.
- **Synthesis:** Implement a dynamic BGM multiplier `bgmVolumeMultiplier` on the `AudioSynthManager` class. Duck this multiplier to `0.35` immediately upon an explosion, then smoothly ramp it back to `1.0` over 300ms. Apply this multiplier to BGM notes and beats to create a professional sidechain compression effect.

### Actions:

- **Action 1:** Declare `bgmVolumeMultiplier` in `AudioSynthManager`.
- **Action 2:** Modulate `bgmVolumeMultiplier` inside `playExplosionTone()`, scheduling smooth recovery.
- **Action 3:** Incorporate `bgmVolumeMultiplier` in BGM note & drum volume calculations.
- **Action 4:** Validate that all unit tests still pass.

###### **[ARTIFACT END]**
