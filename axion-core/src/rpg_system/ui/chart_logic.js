/**
 * UI Controller for Celestial Chart
 * Bridges the HTML view with the RPGEngine.
 */

import { RPGEngine } from '../engine.js';
import { RPGRarity, RPGSlot, RPGStat } from '../rpg_enums.js';

// Init Engine
const engine = new RPGEngine();

// Mock Data (Since we don't have persistence yet)
const mockItems = [
    {
        id: 'ITM-001',
        name: 'Resonance Scanner',
        slot: RPGSlot.HEAD,
        rarity: RPGRarity.RARE,
        stats: { [RPGStat.INSIGHT]: 10 },
        originUri: 'file:///c:/Users/Chris/Synarche_Workspace/_governance/50_Logs/GVRN.CSL.001.ChronosLock.md',
        description: 'See the hidden synergy strings.',
    },
    {
        id: 'ITM-SPL-001',
        name: 'Chronos Lock (Spell)',
        slot: RPGSlot.HAND,
        rarity: RPGRarity.EPIC,
        stats: { [RPGStat.ORDER]: 15 },
        originUri: 'file:///c:/Users/Chris/Synarche_Workspace/_governance/50_Logs/GVRN.CSL.001.ChronosLock.md',
        description: 'Freeze time on a file.',
    },
    {
        id: 'TPL-001',
        name: 'CSL v11.9 (Omega)',
        slot: RPGSlot.TEMPLATE,
        rarity: RPGRarity.LEGENDARY,
        stats: { [RPGStat.COHERENCE]: 25 },
        originUri: 'file:///c:/Users/Chris/Synarche_Workspace/_governance/templates/CSL%20Template.md',
        description: 'The Sovereign Standard.',
    },
];

// Equip Mock Items
mockItems.forEach((item) => {
    engine.equipItem(item);
});

// Render UI
function renderUI() {
    const inventory = engine.inventory;
    const stats = engine.getStats();

    // 1. Render Stats
    const statsPanel = document.getElementById('stats-panel');
    statsPanel.innerHTML = '';
    for (const [stat, value] of Object.entries(stats)) {
        const row = document.createElement('div');
        row.className = 'stat-row';
        row.innerHTML = `<span>${stat}</span> <span style="color: gold;">+${value}</span>`;
        statsPanel.appendChild(row);
    }

    // 2. Render Slots
    for (const [slotName, item] of Object.entries(inventory.slots)) {
        const slotEl = document.getElementById(`slot-${slotName}`);
        if (!slotEl) continue;

        // Clear previous item (keep label)
        const label = slotEl.querySelector('.slot-label');
        slotEl.innerHTML = '';
        slotEl.appendChild(label);

        if (item) {
            const itemCard = document.createElement('div');
            itemCard.className = 'item-card';
            itemCard.dataset.provenance = 'true';
            itemCard.innerHTML = `
                ${item.name}
                <div class="provenance-tooltip">
                    <strong>Origin:</strong><br>
                    <a href="${item.originUri}" style="color:cyan;">${item.originUri.split('/').pop()}</a><br>
                    <em>"${item.description}"</em>
                </div>
            `;
            slotEl.appendChild(itemCard);
        }
    }
}

// Initial Render
document.addEventListener('DOMContentLoaded', renderUI);
