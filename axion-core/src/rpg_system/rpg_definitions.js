/**
 * GVRN-SYS-RPG-002: RPG Definitions & Schema [GEODE EDITION]
 * Defines the core data structures for the Gamification Layer.
 */


/**
 * @typedef {Object} RPGItem
 * @property {string} id - Unique Identifier (e.g., ITM-001)
 * @property {string} name - Display Name
 * @property {string} type - Item Type (from Enum)
 * @property {string} rarity - Rarity (from Enum)
 * @property {string} slot - Equip Slot (from Enum)
 * @property {Object} stats - Stat bonuses { [Stat]: value }
 * @property {string} originUri - Link to CSL/Quest (REQUIRED for Provenance)
 * @property {string} description - Lore/Reasoning
 */

/**
 * @typedef {Object} MeteoriteImpact
 * @property {string} id - Impact Identifier (e.g., IMP-001)
 * @property {string} title - The Challenge Title
 * @property {number} stardust_value - The potential harvestable Stardust
 * @property {string} csl_uri - The corresponding CSL Log URI
 */

export const STARDUST_FORMULA = (base, energy_level, synergy_count) => {
    // Stardust = (Base Value * Energy Level) + (Synergy Count * 13)
    // 13 is the Fibonacci prime for Geode resonance.
    return (base * energy_level) + (synergy_count * 13);
};

export const VALIDATE_PROVENANCE = (item) => {
    if (!item.originUri || item.originUri.trim() === "") {
        return { valid: false, error: "Missing Origin URI (CSL/Quest Link) - Sovereign Breach!" };
    }
    return { valid: true };
};

