/*
artifact_anchor:
  id: CORE.RPG_ENUMS.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

/**
 * GVRN-SYS-RPG-001: RPG Enums
 * Mirrors the Sovereign Enums for the Extension Layer.
 */

export const RPGStat = {
    AUTHORITY: "Authority",
    INSIGHT: "Insight",
    ORDER: "Order",
    PRECISION: "Precision",
    COHERENCE: "Coherence",
    TRANSPARENCY: "Transparency"
};

export const RPGRole = {
    ARCHITECT: "Architect",
    SENTINEL: "Sentinel",
    WEAVER: "Weaver"
};

export const RPGSlot = {
    HEAD: "Head",       // The Lens (Analysis)
    BODY: "Body",       // The Plate (Governance)
    HAND: "Hand",       // The Tool (Execution)
    CORE: "Core",       // The Heart (Seeds)
    TEMPLATE: "Template" // The Pattern (High-Fidelity)
};

export const RPGRarity = {
    COMMON: "Common",
    UNCOMMON: "Uncommon",
    RARE: "Rare",
    EPIC: "Epic",
    LEGENDARY: "Legendary",
    ARTIFACT: "Artifact",
    ANOMALOUS: "Anomalous"
};
