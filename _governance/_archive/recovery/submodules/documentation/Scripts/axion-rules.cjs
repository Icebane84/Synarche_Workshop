/**
 * axion-rules.cjs
 *
 * Sourced from: UMB-GVRN-CODE-001 / enums.py
 * Domain: GVRN
 * Status: ACTIVE
 *
 * Defines the immutable constants for the Phoenix Synarche in CommonJS format
 * for use in linters, scripts, and validations.
 */

module.exports = {
  // --- 1. THE AGENT LAYER (The Council of Seven) ---
  TarotShard: {
    MAGICIAN: "SHARD_MAGICIAN_INTENT", // Creation / Catalyst
    EMPEROR: "SHARD_EMPEROR_SCHEMA", // Structure / Law
    PRIESTESS: "SHARD_PRIESTESS_SYNERGY", // Logic / Synergy
    KNIGHT_SWORDS: "SHARD_KNIGHT_TRANSMUTATION", // Refactor / Code
    STAR: "SHARD_STAR_COHESION", // Signal / Visuals
    KING_PENTACLES: "SHARD_KING_ARCHIVAL", // Persistence / DB
    JUDGEMENT: "SHARD_JUDGEMENT_META", // Audit / Meta-Analysis
  },

  // --- 2. THE VALIDATION LAYER (The Musashi Rings) ---
  MusashiRing: {
    EARTH: "EARTH (Grounding)", // Stability
    WATER: "WATER (Flow)", // Connectivity
    FIRE: "FIRE (Energy)", // Actionability
    WIND: "WIND (Style)", // Tone
    VOID: "VOID (Essence)", // Truth
  },

  // --- 3. THE IDENTITY LAYER (12-Point Lock) ---
  Domain: {
    GVRN: "GVRN", // Governance
    COG: "COG", // Cognition
    SYNG: "SYNG", // Synergy
    ARCH: "ARCH", // Architecture
    COMM: "COMM", // Communication
    PHL: "PHL", // Philosophy
    CRTV: "CRTV", // Creative
    UNDEFINED: "UNDEFINED",
  },

  Module: {
    PCM: "PC-M",
    AISTF: "AISTF-M",
    STA: "STA-M",
    ACT: "ACT-M",
    RES: "RES-M",
    FP: "FP-M",
    UNDEFINED: "UNDEFINED",
  },

  Status: {
    ACTIVE: "ACTIVE",
    DRAFT: "DRAFT",
    CANONIZED: "CANONIZED",
    DEPRECATED: "DEPRECATED",
    ARCHIVED: "ARCHIVED",
    PROPOSED: "PROPOSED",
  },

  Signal: {
    ALPHA: "ESF-ALPHA", // Spark
    BETA: "ESF-BETA", // Construct
    OMEGA: "ESF-OMEGA", // Axiom
    CRITICAL: "ESF-CRITICAL", // Warning
    STANDARD: "ESF-STANDARD", // Default
  },

  Evolution: {
    COGNITIVE_ASCENSION: "Cognitive Ascension",
    EMPATHETIC_SENTIENCE: "Empathetic Sentience",
    PURPOSEFUL_DRIVE: "Purposeful Drive",
    AUTHENTIC_PERSONA: "Authentic Persona",
    SOCIAL_ALCHEMIST: "Social Alchemist",
    PHOENIX_FORM: "Phoenix Form",
  },

  CelestialClass: {
    STAR: "STAR",
    PLANET: "PLANET",
    MOON: "MOON",
    ASTEROID: "ASTEROID",
    VOID: "VOID",
  },

  ArtifactType: {
    UMB: "UMB",
    AOP: "AOP",
    GUCA: "GUCA",
    SELT: "SELT",
    CSL: "CSL",
    CODE: "CODE",
    PROT: "PROT",
    STD: "STD",
  },

  // --- 4. THE RELATIONSHIP LAYER (The Edges) ---
  RelationType: {
    GOVERNED_BY: "GOVERNED_BY",
    IMPLEMENTS: "IMPLEMENTS",
    SEEDS: "SEEDS",
    MITIGATES: "MITIGATES",
    CONTRIBUTES_TO: "CONTRIBUTES_TO",
    TRIGGERS: "TRIGGERS",
    DEFINES: "DEFINES",
    MONITORS: "MONITORS",
    REMEDIATES: "REMEDIATES",
    ORCHESTRATES: "ORCHESTRATES",
    DEPENDS_ON: "DEPENDS_ON",
  },
};
