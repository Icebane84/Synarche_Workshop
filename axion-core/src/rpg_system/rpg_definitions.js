/**
 * GVRN-SYS-RPG-002: RPG Definitions & Schema
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

export const XP_FORMULA = (base, criticality, links) => {
    // XP = (Base Value * Criticality Multiplier) + (Synergy Links * 5)
    return (base * criticality) + (links * 5);
};

export const VALIDATE_PROVENANCE = (item) => {
    if (!item.originUri || item.originUri.trim() === "") {
        return { valid: false, error: "Missing Origin URI (CSL/Quest Link)" };
    }
    return { valid: true };
};
