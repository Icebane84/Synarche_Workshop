/**
 * GVRN-SYS-RPG-004: The RPG Engine
 * The central nervous system for the Gamification Layer.
 */

import { XP_FORMULA } from './rpg_definitions.js';
import { InventorySystem } from './rpg_inventory.js';

export class RPGEngine {
    constructor() {
        this.inventory = new InventorySystem();
        this.currentXP = 0;
        this.level = 1;
    }

    /**
     * Calculates XP gain for a completed Quest or CSL.
     * @param {number} baseValue - Base XP of the task.
     * @param {number} criticality - Multiplier (1-3).
     * @param {number} synergyLinks - Number of synergistic connections.
     */
    awardXP(baseValue, criticality, synergyLinks) {
        const gain = XP_FORMULA(baseValue, criticality, synergyLinks);
        this.currentXP += gain;
        console.log(`[RPG] Gained ${gain} XP! Total: ${this.currentXP}`);
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
