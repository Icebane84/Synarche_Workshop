/* =========================================
   GAME CONFIGURATION & DATA
   ========================================= */

let gameState = {
    resources: { faith: 0, doubt: 0, resolve: 0 },
    lifetime: { faith: 0, doubt: 0, resolve: 0 },
    structures: { sanctum: 0, spire: 0, regimen: 0, censer: 0 },
    research: {},
    unlockedLore: [], 
    prestige: { echoes: 0, timesAscended: 0, upgrades: {} },
    sanity: 100,
    resonance: 50,
    heartstone: { unlocked: false, active: false, level: 1, purification: 0, corruption: 0 },
    darkModeActive: false,
    gameWon: false
};

const gameConfig = {
    manualClickValue: 1,
    sanityRecoveryOnResolve: 2,
    sanityPassiveDrain: 0.2,
    resonanceDriftRate: 0.1,
    prestigeUnlockThreshold: 1000, 

    structures: {
        sanctum: { name: "Hallowed Chapel", desc: "A place of Order. Generates Faith.", baseCost: { faith: 10 }, output: { faith: 1 }, resonancePull: 1, costScaling: 1.5 },
        spire: { name: "Obsidian Shard", desc: "A conduit for Nyx. Generates Doubt.", baseCost: { doubt: 10 }, output: { doubt: 1 }, resonancePull: -1, sanityPenalty: 0.1, costScaling: 1.5 },
        regimen: { name: "Sentinel's Drill", desc: "Garrett's training methods. Generates Resolve.", baseCost: { faith: 5, doubt: 5 }, output: { resolve: 0.5 }, costScaling: 1.5 },
        censer: { name: "Serafina's Ward", desc: "Soothing incense. Restores Sanity.", baseCost: { faith: 100, resolve: 20 }, output: { sanity: 0.1 }, costScaling: 1.5 }
    },

    heartstoneConfig: {
        unlockThreshold: 500,
        baseMaxIntegrity: 100,
        corruptionRate: 2,
        costFaith: 50,
        costResolve: 25,
        purifyAmt: 10
    },

    loreData: {
        "lore_origin": { title: "I. The Great Sundering", text: "The world is a broken puzzle..." },
        "lore_eldrin": { title: "II. The Fallen Paladin", text: "Eldrin was the Order's greatest hero..." },
        "lore_valerius": { title: "III. The Mentor's Shadow", text: "Valerius speaks of 'necessary evils'..." },
        "lore_oathbringer": { title: "IV. The Cursed Blade", text: "Oathbringer is not just steel..." },
        "lore_prophecy": { title: "V. The Sundered Blade", text: "The prophecy speaks of a choice..." }
    },

    researchData: {
        "innerFlame": { name: "Kindle Inner Flame", desc: "+50% Faith gen.", cost: { faith: 50 }, unlocksLore: "lore_origin" },
        "whisperNetwork": { name: "Listen to the Wind", desc: "+50% Doubt gen.", cost: { doubt: 50 }, unlocksLore: "lore_oathbringer" },
        "ritualClarity": { name: "Lorekeeper's Heritage", desc: "Unlocks 'Serafina's Ward'.", cost: { faith: 200, resolve: 50 }, unlocksLore: "lore_eldrin" },
        "mentalFortress": { name: "The Sentinel's Gambit", desc: "Sanity drain reduced by 20%.", cost: { resolve: 150 }, unlocksLore: "lore_valerius" },
        "lumenAttunement": { name: "Heartstone Resonance", desc: "Resonance shifts 50% faster.", cost: { faith: 100, doubt: 100 }, unlocksLore: "lore_prophecy" },
        "voidTouched": { name: "Void-Touched Tempering", desc: "Oathbringer generates +1 resource per click for every 10 Obsidian Shards.", cost: { faith: 150, doubt: 150 } },
        "litanyLost": { name: "Litany of the Lost", desc: "Hallowed Chapels produce +0.5 Resolve/sec.", cost: { faith: 300 } },
        "cognitiveDissonance": { name: "Cognitive Dissonance", desc: "+1% Doubt gen for every 1% missing Sanity.", cost: { doubt: 500 } },
        "serafinaTincture": { name: "Serafina's Tinctures", desc: "Serafina's Wards are 2x effective.", cost: { faith: 200, resolve: 200 } },
        "watcherEye": { name: "The Watcher's Eye", desc: "10% chance for 5x Critical Clicks.", cost: { resolve: 400 } },
        "archGeometry": { name: "Architectural Geometry", desc: "Reduces Chapel cost scaling to 1.4.", cost: { faith: 1000 } },
        "shadowBargain": { name: "Shadow Bargain", desc: "Unlocks Dark Mode Toggle (Triple production, 5x Sanity Drain).", cost: { doubt: 1000 } },
        "leylineMapping": { name: "Leyline Mapping", desc: "Heartstone Rituals fill 20% faster.", cost: { faith: 750, doubt: 750 } },
        "eldrinRegret": { name: "Eldrin's Regret", desc: "Obsidian Shards produce Faith instead of Doubt (50% rate).", cost: { resolve: 2000 } },
        "ascendantEcho": { name: "The Ascendant's Echo", desc: "Retain 10% of structures after Ascension.", cost: { faith: 5000, doubt: 5000, resolve: 5000 } }
    },

    prestigeUpgrades: {
        "ancestralMemory": { name: "Eldrin's Memory", desc: "+10% Global Production.", baseCost: 1, costScaling: 2, effect: (l) => 1 + (l * 0.10) },
        "mentalResilience": { name: "Guardian's Blood", desc: "-5% Sanity Drain.", baseCost: 2, costScaling: 2, effect: (l) => Math.max(0.1, 1 - (l * 0.05)) },
        "lumenMastery": { name: "Shadow Integration", desc: "+10% Drift Speed.", baseCost: 1, costScaling: 1.5, effect: (l) => 1 + (l * 0.10) }
    },

    eventData: [
        {
            id: "black_feather",
            title: "The Black Feather",
            text: "You wake from a nightmare. On your pillow lies a single, perfect black feather.",
            trigger: (gs) => gs.sanity < 60 && gs.resources.doubt > 20,
            choices: [
                { text: "Burn it.", costLabel: "-10 Resolve, +5 Sanity", effect: (gs) => { gs.resources.resolve -= 10; gs.sanity += 5; return "It burns with a sickly green flame."; } },
                { text: "Keep it.", costLabel: "+30 Doubt, -10 Sanity", effect: (gs) => { gs.resources.doubt += 30; gs.sanity -= 10; return "Oathbringer hums in approval."; } }
            ]
        }
    ]
};

/* =========================================
   INITIALIZATION & START
   ========================================= */

// Start Logic Fixed: Loop won't start until user clicks
let gameInterval;

function startGame() {
    const overlay = document.getElementById('start-overlay');
    if(overlay) {
        overlay.style.opacity = '0';
        setTimeout(() => { overlay.style.display = 'none'; }, 1000);
    }

    if (typeof audio !== 'undefined') {
        try { audio.init(); } catch(e) { console.warn("Audio failed to init", e); }
    }

    if (!gameInterval) {
        gameInterval = setInterval(gameTick, 1000);
        logEvent("You step into the void...", "system");
        updateUI(); // Immediate update
    }
}

/* =========================================
   CORE MECHANICS & VISUALS
   ========================================= */

function manualGather(resourceType, event) {
    let amount = gameConfig.manualClickValue;
    
    if (gameState.research['voidTouched']) {
        const bonus = Math.floor(gameState.structures.spire / 10);
        amount += bonus;
    }

    let isCrit = false;
    if (gameState.research['watcherEye'] && Math.random() < 0.10) {
        amount *= 5;
        isCrit = true;
    }

    addResources(resourceType, amount);

    if (resourceType === 'resolve') {
        modifySanity(gameConfig.sanityRecoveryOnResolve);
    }
    
    if (typeof audio !== 'undefined') audio.playClick(resourceType);

    if (event) {
        let text = `+${amount}`;
        if (isCrit) text += " CRIT!";
        spawnFloatingText(event.clientX, event.clientY, text, resourceType);
    }
    updateUI();
}

function spawnFloatingText(x, y, text, type) {
    const el = document.createElement('div');
    el.className = 'floating-text';
    el.innerText = text;
    if (type === 'faith') el.style.color = 'var(--col-faith)';
    if (type === 'doubt') el.style.color = 'var(--col-doubt)';
    if (type === 'resolve') el.style.color = 'var(--col-resolve)';
    
    // Position fixed to mouse + scroll
    el.style.left = (x + window.scrollX + 10) + 'px';
    el.style.top = (y + window.scrollY - 20) + 'px';
    
    document.body.appendChild(el);
    setTimeout(() => { el.remove(); }, 1000);
}

function addResources(type, amount) {
    if (isNaN(amount)) amount = 0;
    gameState.resources[type] += amount;
    gameState.lifetime[type] += amount;
}

function modifySanity(amount) {
    gameState.sanity += amount;
    if (gameState.sanity > 100) gameState.sanity = 100;
    if (gameState.sanity < 0) gameState.sanity = 0;
}

function toggleDarkMode() {
    gameState.darkModeActive = !gameState.darkModeActive;
    updateUI();
    const btn = document.getElementById('btn-dark-mode');
    if(btn) {
        btn.style.backgroundColor = gameState.darkModeActive ? "#9b59b6" : "transparent";
        btn.style.color = gameState.darkModeActive ? "#000" : "#9b59b6";
    }
    logEvent(gameState.darkModeActive ? "You embrace the shadow." : "You suppress the darkness.", "system");
}

/* =========================================
   BUILDINGS & RESEARCH
   ========================================= */

function getCost(structureKey) {
    const owned = gameState.structures[structureKey];
    const base = gameConfig.structures[structureKey].baseCost;
    let scaling = gameConfig.structures[structureKey].costScaling;
    if (structureKey === 'sanctum' && gameState.research['archGeometry']) {
        scaling = 1.4;
    }
    let currentCost = {};
    for (let res in base) {
        currentCost[res] = Math.floor(base[res] * Math.pow(scaling, owned));
    }
    return currentCost;
}

function buyBuilding(structureKey) {
    const cost = getCost(structureKey);
    for (let res in cost) if (gameState.resources[res] < cost[res]) return;
    for (let res in cost) gameState.resources[res] -= cost[res];
    
    gameState.structures[structureKey]++;
    if (typeof audio !== 'undefined') audio.playClick('build');
    updateUI();
}

function buyResearch(researchId) {
    if (gameState.research[researchId]) return;
    const item = gameConfig.researchData[researchId];
    if (researchId === 'cognitiveDissonance' && gameState.sanity < 50) {
        alert("Not enough Sanity."); return;
    }
    for (let res in item.cost) if (gameState.resources[res] < item.cost[res]) return;
    
    for (let res in item.cost) gameState.resources[res] -= item.cost[res];
    if (researchId === 'cognitiveDissonance') gameState.sanity -= 50;

    gameState.research[researchId] = true;
    logEvent(`Discovery: ${item.name}`, "research");
    if (item.unlocksLore) unlockLore(item.unlocksLore);
    if (typeof audio !== 'undefined') audio.playClick('faith');

    checkUnlocks();
    renderResearch();
    updateUI();
}

/* =========================================
   HEARTSTONE LOGIC
   ========================================= */

function checkHeartstoneUnlock() {
    if (!gameState.heartstone.unlocked && gameState.lifetime.faith > gameConfig.heartstoneConfig.unlockThreshold) {
        gameState.heartstone.unlocked = true;
        const hsSection = document.getElementById('heartstone-section');
        if(hsSection) hsSection.style.display = 'block';
        logEvent("You feel the pulse of a corrupted Heartstone nearby...", "lore");
    } else if (gameState.heartstone.unlocked) {
        const hsSection = document.getElementById('heartstone-section');
        if(hsSection) hsSection.style.display = 'block';
    }
}

function startHeartstoneEncounter() {
    if (gameState.heartstone.active) return;
    gameState.heartstone.active = true;
    gameState.heartstone.purification = 0;
    gameState.heartstone.corruption = 0;
    
    document.getElementById('btn-hs-start').style.display = 'none';
    document.getElementById('hs-active-controls').style.display = 'flex';
    document.getElementById('hs-status-text').innerText = "THE RITUAL HAS BEGUN.";
    document.getElementById('hs-icon').innerText = "🔥";
    if (typeof audio !== 'undefined') audio.playClick('doubt');
}

function channelHeartstone(type) {
    if (!gameState.heartstone.active) return;
    let mult = gameState.research['leylineMapping'] ? 1.2 : 1.0;
    const costFaith = Math.floor(gameConfig.heartstoneConfig.costFaith * Math.pow(1.2, gameState.heartstone.level));
    const costResolve = Math.floor(gameConfig.heartstoneConfig.costResolve * Math.pow(1.2, gameState.heartstone.level));

    if (type === 'faith') {
        if (gameState.resources.faith >= costFaith) {
            gameState.resources.faith -= costFaith;
            gameState.heartstone.purification += gameConfig.heartstoneConfig.purifyAmt * mult;
            spawnFloatingText(window.innerWidth/2, window.innerHeight/2, "PURIFIED!", "faith");
        }
    } else if (type === 'resolve') {
        if (gameState.resources.resolve >= costResolve) {
            gameState.resources.resolve -= costResolve;
            gameState.heartstone.purification += (gameConfig.heartstoneConfig.purifyAmt * 1.5) * mult;
            spawnFloatingText(window.innerWidth/2, window.innerHeight/2, "STRIKE!", "resolve");
        }
    }
    updateUI();
}

function heartstoneTick() {
    if (!gameState.heartstone.active) return;
    const maxIntegrity = Math.floor(gameConfig.heartstoneConfig.baseMaxIntegrity * Math.pow(1.5, gameState.heartstone.level));
    const corruptionRate = gameConfig.heartstoneConfig.corruptionRate * gameState.heartstone.level;
    gameState.heartstone.corruption += corruptionRate;

    if (gameState.heartstone.purification >= maxIntegrity) {
        endHeartstone(true);
    } else if (gameState.heartstone.corruption >= maxIntegrity) {
        endHeartstone(false);
    }
}

function endHeartstone(victory) {
    gameState.heartstone.active = false;
    document.getElementById('btn-hs-start').style.display = 'inline-block';
    document.getElementById('hs-active-controls').style.display = 'none';

    if (victory) {
        gameState.heartstone.level++;
        logEvent(`Heartstone Purified! Level ${gameState.heartstone.level} Reached.`, "good");
        document.getElementById('hs-status-text').innerText = "Purified.";
        document.getElementById('hs-icon').innerText = "💎"; 
        gameState.sanity += 20; 
        
        checkTrueEndingConditions();
        
    } else {
        logEvent("The Ritual Failed.", "bad");
        document.getElementById('hs-status-text').innerText = "FAILED.";
        document.getElementById('hs-icon').innerText = "☠️"; 
        gameState.sanity -= 30; 
        gameState.resources.faith = 0; 
    }
    
    gameState.heartstone.purification = 0;
    gameState.heartstone.corruption = 0;
    updateUI();
}

/* =========================================
   GAME LOOP
   ========================================= */

function calculateProduction() {
    let prod = { faith: 0, doubt: 0, resolve: 0 };
    prod.faith += gameState.structures.sanctum * gameConfig.structures.sanctum.output.faith;
    
    if (gameState.research['eldrinRegret']) {
        prod.faith += (gameState.structures.spire * gameConfig.structures.spire.output.doubt) * 0.5;
    } else {
        prod.doubt += gameState.structures.spire * gameConfig.structures.spire.output.doubt;
    }
    
    if(gameState.structures.regimen > 0) {
        prod.resolve += gameState.structures.regimen * gameConfig.structures.regimen.output.resolve;
    }

    if (gameState.research['litanyLost']) prod.resolve += gameState.structures.sanctum * 0.5;
    if (gameState.research['innerFlame']) prod.faith *= 1.5;
    if (gameState.research['whisperNetwork']) prod.doubt *= 1.5;

    if (gameState.research['cognitiveDissonance']) {
        const missingSanity = 100 - gameState.sanity;
        prod.doubt *= (1 + (missingSanity * 0.01));
    }
    if (gameState.darkModeActive) {
        prod.faith *= 3;
        prod.doubt *= 3;
        prod.resolve *= 3;
    }

    let multiplier = 1;
    if (gameState.heartstone.level > 1) multiplier += (gameState.heartstone.level - 1) * 0.5;
    const prestigeMult = gameConfig.prestigeUpgrades['ancestralMemory'].effect(gameState.prestige.upgrades['ancestralMemory'] || 0);
    multiplier *= prestigeMult;

    prod.faith *= multiplier;
    prod.doubt *= multiplier;
    prod.resolve *= multiplier;

    const sanityMult = 0.2 + (0.8 * (gameState.sanity / 100));
    prod.faith *= sanityMult;
    prod.doubt *= sanityMult;
    prod.resolve *= sanityMult;

    return prod;
}

function gameTick() {
    // WRAPPED IN TRY-CATCH TO PREVENT CRASHES STOPPING THE GAME LOOP
    try {
        const production = calculateProduction();
        addResources('faith', production.faith);
        addResources('doubt', production.doubt);
        addResources('resolve', production.resolve);

        heartstoneTick();
        checkHeartstoneUnlock();

        let drain = gameConfig.sanityPassiveDrain;
        drain += gameState.structures.spire * gameConfig.structures.spire.sanityPenalty;
        if (gameState.research['mentalFortress']) drain *= 0.8;
        const drainMult = gameConfig.prestigeUpgrades['mentalResilience'].effect(gameState.prestige.upgrades['mentalResilience'] || 0);
        drain *= drainMult;
        if (gameState.darkModeActive) drain *= 5;

        modifySanity(-drain);

        let censerHeal = gameConfig.structures.censer.output.sanity;
        if (gameState.research['serafinaTincture']) censerHeal *= 2;
        if (gameState.structures.censer > 0) modifySanity(gameState.structures.censer * censerHeal);

        let resonancePull = 0;
        resonancePull += gameState.structures.sanctum * gameConfig.structures.sanctum.resonancePull;
        if (!gameState.research['eldrinRegret']) {
            resonancePull += gameState.structures.spire * gameConfig.structures.spire.resonancePull;
        }
        let driftRate = gameConfig.resonanceDriftRate;
        if (gameState.research['lumenAttunement']) driftRate *= 1.5;
        const driftMult = gameConfig.prestigeUpgrades['lumenMastery'].effect(gameState.prestige.upgrades['lumenMastery'] || 0);
        driftRate *= driftMult;

        gameState.resonance += resonancePull * driftRate;
        if (gameState.resonance > 100) gameState.resonance = 100;
        if (gameState.resonance < 0) gameState.resonance = 0;

        if (typeof audio !== 'undefined') audio.updateAtmosphere(gameState.sanity, gameState.resonance);
        
        // Visual effects (safeguarded)
        updateAtmosphereVisuals();
        
        triggerRandomEvent();
        checkUnlocks();
        
        if (Date.now() % 30000 < 1000) saveGame();
        
        updateUI();
    } catch (e) {
        console.error("Game Tick Error:", e);
    }
}

function updateAtmosphereVisuals() {
    const root = document.documentElement;
    if (gameState.resonance > 60) {
        root.style.setProperty('--bg-gradient-center', '#4f4220'); 
    } else if (gameState.resonance < 40) {
        root.style.setProperty('--bg-gradient-center', '#3d2a45'); 
    } else {
        root.style.setProperty('--bg-gradient-center', '#222'); 
    }

    const pulseOverlay = document.getElementById('sanity-pulse');
    if (pulseOverlay) { // Safety check
        if (gameState.sanity < 30) {
            pulseOverlay.style.opacity = 1;
            pulseOverlay.classList.add('pulse-active');
        } else {
            pulseOverlay.style.opacity = 0;
            pulseOverlay.classList.remove('pulse-active');
        }
    }
}

function updateUI() {
    document.getElementById('res-faith').innerText = Math.floor(gameState.resources.faith);
    document.getElementById('res-doubt').innerText = Math.floor(gameState.resources.doubt);
    document.getElementById('res-resolve').innerText = Math.floor(gameState.resources.resolve);

    const prod = calculateProduction();
    document.getElementById('rate-faith').innerText = prod.faith.toFixed(1);
    document.getElementById('rate-doubt').innerText = prod.doubt.toFixed(1);
    document.getElementById('rate-resolve').innerText = prod.resolve.toFixed(1);

    updateStructureUI('sanctum', ['faith']);
    updateStructureUI('spire', ['doubt']);
    updateStructureUI('regimen', ['faith', 'doubt']);
    updateStructureUI('censer', ['faith', 'resolve']);

    const sanityBar = document.getElementById('bar-sanity');
    if (sanityBar) {
        sanityBar.style.width = gameState.sanity + "%";
        document.getElementById('val-sanity').innerText = Math.floor(gameState.sanity);
        if (gameState.sanity > 50) sanityBar.style.backgroundColor = "var(--col-sanity)";
        else if (gameState.sanity > 25) sanityBar.style.backgroundColor = "#e67e22";
        else sanityBar.style.backgroundColor = "#c0392b";
    }

    const resPercent = gameState.resonance;
    const resMarker = document.getElementById('marker-resonance');
    if (resMarker) resMarker.style.left = resPercent + "%";
    
    applyHallucinations();
    
    if (gameState.heartstone.unlocked) {
        const maxIntegrity = Math.floor(gameConfig.heartstoneConfig.baseMaxIntegrity * Math.pow(1.5, gameState.heartstone.level));
        document.getElementById('hs-level').innerText = gameState.heartstone.level;
        document.getElementById('hs-name').innerText = gameState.heartstone.active ? "RITUAL ACTIVE" : "Corrupted Heartstone";
        const purPct = Math.min(100, (gameState.heartstone.purification / maxIntegrity) * 100);
        const corPct = Math.min(100, (gameState.heartstone.corruption / maxIntegrity) * 100);
        document.getElementById('bar-purification').style.width = purPct + "%";
        document.getElementById('bar-corruption').style.width = corPct + "%";
        const costFaith = Math.floor(gameConfig.heartstoneConfig.costFaith * Math.pow(1.2, gameState.heartstone.level));
        const costResolve = Math.floor(gameConfig.heartstoneConfig.costResolve * Math.pow(1.2, gameState.heartstone.level));
        document.getElementById('cost-hs-faith').innerText = costFaith;
        document.getElementById('cost-hs-resolve').innerText = costResolve;
    }
    
    const echoEl = document.getElementById('val-echoes');
    if (echoEl) echoEl.innerText = gameState.prestige.echoes;
    const pendingEl = document.getElementById('val-pending-echoes');
    if (pendingEl) pendingEl.innerText = calculatePendingEchoes();
}

function updateStructureUI(key, costTypes) {
    const countEl = document.getElementById(`count-${key}`);
    if (!countEl) return;
    countEl.innerText = gameState.structures[key];
    const cost = getCost(key);
    costTypes.forEach(type => {
        const el = document.getElementById(`cost-${key}-${type}`);
        if(el) el.innerText = cost[type];
    });
}

function applyHallucinations() {
    const body = document.body;
    if (gameState.sanity < 10) body.className = 'hallucinating-severe';
    else if (gameState.sanity < 30) body.className = 'hallucinating';
    else body.className = '';
}

/* =========================================
   TRUE ENDING & IMPORT/EXPORT
   ========================================= */

function checkTrueEndingConditions() {
    if (gameState.heartstone.level >= 5 && !gameState.gameWon) {
        document.getElementById('fusion-container').style.display = 'block';
    }
}

function attemptFusion() {
    if (gameState.resources.faith >= 5000 && gameState.resources.doubt >= 5000 && gameState.resources.resolve >= 5000) {
        gameState.gameWon = true;
        logEvent("KAELEN AND ELDRIN FUSE. THE CYCLE IS BROKEN.", "ending");
        alert("YOU HAVE ACHIEVED THE TRUE ENDING. Kaelen and Eldrin are one. The Shadow Self is bound. The world begins to heal.");
        
        gameState.prestige.echoes += 100; 
        prestige();
    } else {
        logEvent("You are not yet ready for the fusion.", "bad");
    }
}

function exportSave() {
    const saveString = btoa(JSON.stringify(gameState));
    navigator.clipboard.writeText(saveString).then(() => {
        alert("Save copied to clipboard!");
    });
}

function importSave() {
    const saveString = prompt("Paste your save string here:");
    if (saveString) {
        try {
            const decoded = atob(saveString);
            const parsed = JSON.parse(decoded);
            gameState = parsed;
            saveGame();
            location.reload();
        } catch (e) {
            alert("Invalid save string!");
        }
    }
}

/* =========================================
   UTILITIES
   ========================================= */

function checkUnlocks() {
    if (gameState.research['ritualClarity']) {
        const censerEl = document.getElementById('container-censer');
        if (censerEl && censerEl.style.display === 'none') {
            censerEl.style.display = 'flex';
            logEvent("Unlocked: Serafina's Ward", "system");
        }
    }
    if (gameState.research['shadowBargain']) {
        document.getElementById('btn-dark-mode').style.display = 'inline-block';
    }
    const totalLifetime = gameState.lifetime.faith + gameState.lifetime.doubt + gameState.lifetime.resolve;
    const ascensionBtn = document.getElementById('btn-tab-ascension');
    const shouldShowAscension = totalLifetime >= gameConfig.prestigeUnlockThreshold || gameState.prestige.timesAscended > 0;
    if (shouldShowAscension && ascensionBtn.style.display === 'none') {
        ascensionBtn.style.display = 'inline-block';
        if (gameState.prestige.timesAscended === 0) logEvent("A path to Ascension reveals itself...", "prestige");
    }
}

function unlockLore(loreId, silent=false) {
    if (!gameState.unlockedLore.includes(loreId)) {
        gameState.unlockedLore.push(loreId);
        if(!silent) logEvent("Codex Entry Decrypted.", "lore");
        renderCodex(); 
    }
}

function renderCodex() {
    const container = document.getElementById('codex-container');
    if (!container) return;
    container.innerHTML = '';
    for (let id in gameConfig.loreData) {
        const data = gameConfig.loreData[id];
        const isUnlocked = gameState.unlockedLore.includes(id);
        const entry = document.createElement('div');
        if (isUnlocked) {
            entry.className = "codex-entry";
            entry.innerHTML = `<h4>${data.title}</h4><p>${data.text}</p>`;
        } else {
            entry.className = "codex-locked";
            entry.innerText = "Fragment Encrypted...";
        }
        container.appendChild(entry);
    }
}

function renderPrestigeUpgrades() {
    const container = document.getElementById('prestige-upgrades-container');
    if (!container) return;
    container.innerHTML = '';
    for (let key in gameConfig.prestigeUpgrades) {
        const upg = gameConfig.prestigeUpgrades[key];
        const level = gameState.prestige.upgrades[key] || 0;
        const cost = getPrestigeUpgradeCost(key);
        const canAfford = gameState.prestige.echoes >= cost;
        const card = document.createElement('div');
        card.className = "research-card upgrade-card";
        card.innerHTML = `<h4>${upg.name} (Lvl ${level})</h4><p>${upg.desc}</p><div class="research-cost" style="color: var(--col-prestige);">Cost: ${cost} Echoes</div><button onclick="buyPrestigeUpgrade('${key}')" ${canAfford ? '' : 'disabled'} style="border-color: var(--col-prestige); color: var(--col-prestige);">Upgrade</button>`;
        container.appendChild(card);
    }
}

function switchTab(tabName) {
    const contents = document.getElementsByClassName('tab-content');
    for(let c of contents) c.style.display = 'none';
    document.getElementById(`tab-${tabName}`).style.display = 'block';
    const btns = document.getElementsByClassName('nav-btn');
    for(let b of btns) b.classList.remove('active');
    
    if(tabName === 'sanctum') btns[0].classList.add('active');
    if(tabName === 'research') btns[1].classList.add('active');
    if(tabName === 'codex') btns[2].classList.add('active');
    if(tabName === 'ascension') document.getElementById('btn-tab-ascension').classList.add('active');

    if (tabName === 'ascension') renderPrestigeUpgrades();
    if (tabName === 'research') renderResearch();
    if (tabName === 'codex') renderCodex();
}

function logEvent(text, type="system") {
    const log = document.getElementById('event-log');
    if (!log) return;
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.innerText = text;
    log.insertBefore(entry, log.firstChild);
    if (log.children.length > 20) log.removeChild(log.lastChild);
}

function saveGame() {
    localStorage.setItem('ashenOathSave', JSON.stringify(gameState));
}

function loadGame() {
    const savedGame = localStorage.getItem('ashenOathSave');
    if (savedGame) {
        const parsedGame = JSON.parse(savedGame);
        gameState = { ...gameState, ...parsedGame };
        // Deep merge resources/structures to ensure new fields are caught
        if (parsedGame.resources) gameState.resources = { ...gameState.resources, ...parsedGame.resources };
        if (parsedGame.structures) gameState.structures = { ...gameState.structures, ...parsedGame.structures };
        if (parsedGame.heartstone) gameState.heartstone = { ...gameState.heartstone, ...parsedGame.heartstone };
        if (parsedGame.prestige) gameState.prestige = { ...gameState.prestige, ...parsedGame.prestige };
    }
    checkUnlocks();
    checkTrueEndingConditions(); 
    switchTab('sanctum');
    updateUI();
}

function resetGame() {
    if(confirm("HARD RESET: Wipe everything including prestige?")) {
        localStorage.removeItem('ashenOathSave');
        location.reload();
    }
}