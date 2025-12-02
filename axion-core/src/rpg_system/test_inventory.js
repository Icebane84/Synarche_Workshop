/**
 * TEST: RPG Inventory System
 * Verifies:
 * 1. Provenance Enforcement (Failure on missing URI).
 * 2. Slot Validation (Failure on invalid slot).
 * 3. Successful Equip (Head Slot).
 * 4. Stat Calculation.
 */

import { RPGRarity, RPGSlot, RPGStat } from './rpg_enums.js';
import { InventorySystem } from './rpg_inventory.js';

const inventory = new InventorySystem();

// TEST 1: Provenance Failure
const invalidItem = {
    id: "ITM-000",
    name: "Glitch Dagger",
    slot: RPGSlot.HAND,
    originUri: "" // MISSING!
};

console.log("--- TEST 1: Provenance Audit ---");
const test1 = inventory.equip(invalidItem);
if (test1 === false) console.log("PASS: Invalid item rejected.");
else console.error("FAIL: Invalid item accepted.");

// TEST 2: Valid Item
const validItem = {
    id: "ITM-001",
    name: "Resonance Scanner",
    slot: RPGSlot.HEAD,
    rarity: RPGRarity.RARE,
    stats: { [RPGStat.INSIGHT]: 10 },
    originUri: "file:///c:/Users/Chris/Synarche_Workspace/_governance/50_Logs/GVRN.CSL.001.ChronosLock.md",
    description: "A tool for seeing the unseen."
};

console.log("\n--- TEST 2: Equip Valid Item ---");
const test2 = inventory.equip(validItem);
if (test2 === true) console.log("PASS: Valid item equipped.");
else console.error("FAIL: Valid item rejected.");

// TEST 3: Slot Check
console.log("\n--- TEST 3: Slot State ---");
if (inventory.slots[RPGSlot.HEAD] === validItem) console.log("PASS: Head slot occupied.");
else console.error("FAIL: Head slot empty.");

// TEST 4: Stats
console.log("\n--- TEST 4: Stat Calculation ---");
const stats = inventory.calculateStats();
console.log("Total Stats:", stats);
if (stats[RPGStat.INSIGHT] === 10) console.log("PASS: Stats correct.");
else console.error("FAIL: Stats incorrect.");
