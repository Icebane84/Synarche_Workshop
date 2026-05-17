/**
 * GVRN-SYS-RPG-004: The RPG Engine [GEODE EDITION]
 * The central nervous system for the Gamification Layer.
 */

import { STARDUST_FORMULA } from './rpg_definitions.js';
import { InventorySystem } from './rpg_inventory.js';

export class RPGEngine {
    constructor() {
        this.inventory = new InventorySystem();
        this.stardust_pool = 0;
        this.prestige_level = 0;
        this.persona_class = "Novice";
    }

    /**
     * Harvests Stardust from a completed Meteorite Impact.
     * @param {number} base_energy - Base energy of the task.
     * @param {number} energy_level - Multiplier (1-10).
     * @param {number} resonance_links - Number of synergistic connections.
     */
    awardStardust(base_energy, energy_level, resonance_links) {
        const gain = STARDUST_FORMULA(base_energy, energy_level, resonance_links);
        this.stardust_pool += gain;
        // Telemetry Capture: [SYNA-RPG-HEART]
        return gain;
    }

    /**
     * Wrapper for equipping items via the Engine.
     * @param {Object} item
     */
    equipItem(item) {
        return this.inventory.equip(item);
    }

    /**
     * Gets the current avatar stats.
     */
    getStats() {
        return this.inventory.calculateStats();
    }
}

