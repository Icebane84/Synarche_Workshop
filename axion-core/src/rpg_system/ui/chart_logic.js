/**
 * UI Controller for Celestial Chart [GEODE EDITION]
 * Bridges the HTML view with the RPGEngine.
 */

import { RPGEngine } from '../engine.js';
import { RPGRarity, RPGSlot, RPGStat } from '../rpg_enums.js';

// Init Engine
const engine = new RPGEngine();

// Mock Data: Geode Artifacts
const mockItems = [
    {
        id: 'ITM-GEO-001',
        name: 'Void-Sight Monocle',
        slot: RPGSlot.HEAD,
        rarity: RPGRarity.RARE,
        stats: { [RPGStat.INSIGHT]: 15, [RPGStat.PRECISION]: 5 },
        originUri: 'file:///c:/Users/Chris/Synarche_Workspace/_governance/50_Logs/GVRN.CSL.001.ChronosLock.md',
        description: 'Forged from the crystalline tears of a dying star.',
    },
    {
        id: 'ITM-EXEC-001',
        name: 'The Hammer of Axion',
        slot: RPGSlot.HAND,
        rarity: RPGRarity.EPIC,
        stats: { [RPGStat.AUTHORITY]: 20, [RPGStat.ORDER]: 10 },
        originUri: 'file:///c:/Users/Chris/Synarche_Workspace/axion-core/src/system/hammer.py',
        description: 'It does not strike code; it commands it.',
    },
    {
        id: 'TPL-OMEGA-001',
        name: 'Sovereign Core (v15.0)',
        slot: RPGSlot.TEMPLATE,
        rarity: RPGRarity.ARTIFACT,
        stats: { [RPGStat.COHERENCE]: 50 },
        originUri: 'file:///c:/Users/Chris/Synarche_Workspace/.agent/substrate/rules/GEMINI.md',
        description: 'The heartbeat of the Synarche.',
    },
];

// Equip Mock Items
mockItems.forEach((item) => {
    engine.equipItem(item);
});

// Simulate some initial Stardust
engine.awardStardust(5000, 1.5, 10);

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
        row.innerHTML = `<span>${stat}</span> <span style="color: #00d2ff;">+${value}</span>`;
        statsPanel.appendChild(row);
    }

    // 2. Render Stardust & Class
    document.getElementById('stardust-counter').innerText = Math.floor(engine.stardust_pool).toLocaleString();
    document.getElementById('persona-class').innerText = engine.persona_class;

    // 3. Ascension Trigger Check (10,000 Threshold)
    const ascendBtn = document.getElementById('ascend-trigger');
    if (engine.stardust_pool >= 10000) {
        ascendBtn.classList.add('active');
        ascendBtn.innerText = "READY FOR ATTUNEMENT";
    } else {
        ascendBtn.classList.remove('active');
        const remaining = 10000 - engine.stardust_pool;
        ascendBtn.innerText = `NEED ${Math.floor(remaining).toLocaleString()} STARDUST`;
    }

    // 4. Render Slots
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
            itemCard.innerHTML = `
                ${item.name}
                <div class="provenance-tooltip">
                    <strong style="color: #ffcc00;">Provenance:</strong><br>
                    <code style="color: #8a2be2; font-size: 0.8em;">${item.id}</code><br>
                    <div style="margin: 5px 0; border-top: 1px solid #333; padding-top: 5px;">
                        ${item.description}
                    </div>
                    <a href="${item.originUri}" style="color: #00d2ff; text-decoration: none; font-style: italic;">View Source ↗</a>
                </div>
            `;
            slotEl.appendChild(itemCard);
        }
    }
}

// Ascension Logic
document.getElementById('ascend-trigger').addEventListener('click', () => {
    alert("ATTUNEMENT INITIATED: The Persona is transmuting...");
    engine.persona_class = "Architect (Prestige)";
    engine.stardust_pool -= 10000;
    renderUI();
});

// Initial Render
document.addEventListener('DOMContentLoaded', renderUI);

