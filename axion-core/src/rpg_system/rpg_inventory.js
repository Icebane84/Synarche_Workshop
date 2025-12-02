/**
 * GVRN-SYS-RPG-003: Inventory System
 * Manages the Avatar's Loadout and "Four Slot" Archetype.
 */

import { VALIDATE_PROVENANCE } from './rpg_definitions.js';
import { RPGSlot } from './rpg_enums.js';

export class InventorySystem {
    constructor() {
        this.slots = {
            [RPGSlot.HEAD]: null,
            [RPGSlot.BODY]: null,
            [RPGSlot.HAND]: null,
            [RPGSlot.CORE]: null,
            [RPGSlot.TEMPLATE]: null
        };
        this.backpack = []; // Un-equipped items
    }

    /**
     * Equips an item to the appropriate slot.
     * Enforces Provenance Validation before equipping.
     * @param {Object} item
     */
    equip(item) {
        // 1. Audit Provenance
        const audit = VALIDATE_PROVENANCE(item);
        if (!audit.valid) {
            console.error(`[RPG] Equip Failed: ${audit.error} for item ${item.name}`);
            return false;
        }

        // 2. Validate Slot
        if (!this.slots.hasOwnProperty(item.slot)) {
            console.error(`[RPG] Equip Failed: Invalid slot ${item.slot}`);
            return false;
        }

        // 3. Equip (Swap if occupied)
        const previousItem = this.slots[item.slot];
        if (previousItem) {
            this.backpack.push(previousItem);
        }

        this.slots[item.slot] = item;
        console.log(`[RPG] Equipped ${item.name} to ${item.slot}. (Origin: ${item.originUri})`);
        return true;
    }

    /**
     * Unequips an item from a slot.
     * @param {string} slot
     */
    unequip(slot) {
        if (this.slots[slot]) {
            this.backpack.push(this.slots[slot]);
            this.slots[slot] = null;
            return true;
        }
        return false;
    }

    /**
     * Returns the current total stat bonuses from all equipped items.
     */
    calculateStats() {
        let totalStats = {};
        for (const slot in this.slots) {
            const item = this.slots[slot];
            if (item && item.stats) {
                for (const stat in item.stats) {
                    totalStats[stat] = (totalStats[stat] || 0) + item.stats[stat];
                }
            }
        }
        return totalStats;
    }
}
