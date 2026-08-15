import { loadCanonicalEnemies, type CanonicalEnemy } from './graphLoader';

export interface BattleEvent {
  id: string;
  title: string;
  text: string;
  choices: { text: string; costLabel: string; effect: (engine: CombatEngine) => void }[];
}

export interface BattleState {
  innerFlame: number;       // Shared Health/Sanity (0 to 100)
  aegisShield: number;      // Serafina's shield buffer (0 to 100)
  exposedStacks: number;    // Garrett's Exposed debuff stacks
  enemyHealth: number;      // Current active enemy health
  enemyMaxHealth: number;   // Current active enemy max health
  enemyName: string;        // Active enemy name
  enemyCategory?: string;   // Canonical Category
  enemyDescription?: string;// Canonical Description
  enemyAbilities?: string[];// Canonical Abilities
  isStunned: boolean;       // Grounding Command active
  recoilPaused: boolean;    // Recoil pause active
  combatLog: string[];      // Recent lines of combat log
  victoryCount: number;     // Number of completed stages
  resonanceDrift: number;   // Spectrum: 0 (Nyx / Dark) <---> 50 (Equilibrium) <---> 100 (White Flame)
  darkModeActive: boolean;  // Dark Mode Stance toggle state
  activeEvent: BattleEvent | null; // Current pending moral dilemma choice
  hallucinationLevel: 'NONE' | 'MODERATE' | 'SEVERE'; // Psyche system threshold level
}

export class CombatEngine {
  private readonly state: BattleState;
  private readonly onStateChange: (state: BattleState) => void;
  private isRunning: boolean = false;
  private tickInterval: ReturnType<typeof setInterval> | null = null;
  private readonly passiveRegenBonus: number = 0; // Legacy talent modifier
  private readonly extraExposedStacks: number = 0; // Legacy talent modifier
  private readonly shieldAbsorbBonus: number = 1; // Legacy talent modifier (multiplier)

  private readonly enemiesList: CanonicalEnemy[] = [];


  constructor(
    onStateChange: (state: BattleState) => void,
    talents: string[] = []
  ) {
    this.onStateChange = onStateChange;

    // Load canonical enemies from the Knowledge Graph
    this.enemiesList = loadCanonicalEnemies();

    // Read active legacy talents
    if (talents.includes('talent-1')) this.passiveRegenBonus = 2; // Eternal Ember
    if (talents.includes('talent-2')) this.extraExposedStacks = 1; // Alerion Reflexes
    if (talents.includes('talent-3')) this.shieldAbsorbBonus = 1.3; // Warden's Grace
    if (talents.includes('talent-4')) this.shieldAbsorbBonus = 1.6; // Eldrin's Grace (Precision parry reduces recoil bleeding)

    this.state = this.getInitialState();
  }

  private getInitialState(): BattleState {
    const enemy = this.enemiesList[0] || {
      name: 'Creeping Doubt',
      maxHealth: 80,
      attackDamage: 8,
      category: 'Spite Manifestation',
      description: 'A low-level shadow that feeds on fear.',
      abilities: []
    };
    return {
      innerFlame: 100,
      aegisShield: 20,
      exposedStacks: 0,
      enemyHealth: enemy.maxHealth,
      enemyMaxHealth: enemy.maxHealth,
      enemyName: enemy.name,
      enemyCategory: enemy.category,
      enemyDescription: enemy.description,
      enemyAbilities: enemy.abilities,
      isStunned: false,
      recoilPaused: false,
      combatLog: ['The cycle begins now. [IGNITE]'],
      victoryCount: 0,
      resonanceDrift: 50,
      darkModeActive: false,
      activeEvent: null,
      hallucinationLevel: 'NONE'
    };

  }

  public start() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.tickInterval = setInterval(() => this.tick(), 1000);
  }

  public stop() {
    this.isRunning = false;
    if (this.tickInterval) {
      clearInterval(this.tickInterval);
      this.tickInterval = null;
    }
  }

  public triggerTap() {
    if (!this.isRunning) return;
    // Manual tapping to Kindle (adds Sparks / deals minor damage)
    this.state.enemyHealth = Math.max(0, this.state.enemyHealth - 5);
    this.addLog('You feed the spark manually, dealing 5 damage to the dark.');
    this.checkDefeated();
    this.onStateChange({ ...this.state });
  }

  // Active Ultimate: Garrett
  public triggerGroundingCommand(): boolean {
    if (!this.isRunning || this.state.isStunned) return false;
    this.state.isStunned = true;
    this.state.recoilPaused = true;
    this.addLog('Garrett: "Focus, Kaelen! Hold the line!" (Enemy Stunned, Recoil Paused)');
    this.onStateChange({ ...this.state });

    setTimeout(() => {
      this.state.isStunned = false;
      this.state.recoilPaused = false;
      this.addLog('Garrett\'s command fades. The enemy recovers.');
      this.onStateChange({ ...this.state });
    }, 3000);

    return true;
  }

  // Active Ultimate: Serafina
  public triggerWhispersOfTheDawn(): boolean {
    if (!this.isRunning) return false;
    this.state.innerFlame = 100;
    this.addLog('Serafina: "Let me carry the burden. Stand up!" (Inner Flame Restored)');
    this.onStateChange({ ...this.state });
    return true;
  }

  // Toggle Dark Mode Stance
  public toggleDarkMode() {
    if (!this.isRunning) return;
    this.state.darkModeActive = !this.state.darkModeActive;
    if (this.state.darkModeActive) {
      this.addLog('⚠️ Kaelen surrenders to the Shadow! Dark Mode Stance Active (+200% ATK, 3x Recoil Decay).');
    } else {
      this.addLog('🛡️ Kaelen regains focus and suppresses the Shadow.');
    }
    this.onStateChange({ ...this.state });
  }

  // Active Skill: Kaelen
  public triggerKaelenSkill() {
    this.toggleDarkMode();
  }


  // Resolve active moral dilemma event
  public resolveEvent(choiceIndex: number) {
    if (!this.state.activeEvent) return;
    const choice = this.state.activeEvent.choices[choiceIndex];
    if (choice) {
      choice.effect(this);
    }
    this.state.activeEvent = null;
    this.onStateChange({ ...this.state });
  }

  public modifyInnerFlame(amount: number) {
    this.state.innerFlame = Math.max(0, Math.min(100, this.state.innerFlame + amount));
  }

  public modifyResonanceDrift(amount: number) {
    this.state.resonanceDrift = Math.max(0, Math.min(100, this.state.resonanceDrift + amount));
  }

  private tick() {
    if (this.state.innerFlame <= 0) {
      this.handleDefeat();
      return;
    }

    this.updateHallucinationLevel();
    this.processSquadActions();

    if (this.checkDefeated()) return;

    this.processKaelenRecoil();

    if (this.state.innerFlame <= 0) {
      this.handleDefeat();
      return;
    }

    this.processEnemyTurn();

    if (!this.state.activeEvent && Math.random() < 0.08) {
      this.triggerRandomEvent();
    }

    this.onStateChange({ ...this.state });
  }

  private updateHallucinationLevel() {
    if (this.state.innerFlame < 10) {
      this.state.hallucinationLevel = 'SEVERE';
    } else if (this.state.innerFlame < 30) {
      this.state.hallucinationLevel = 'MODERATE';
    } else {
      this.state.hallucinationLevel = 'NONE';
    }
  }

  private processSquadActions() {
    // 1. Garrett Attacks
    const addedStacks = 1 + this.extraExposedStacks;
    this.state.exposedStacks += addedStacks;
    this.addLog(`Garrett strikes with Piercing Insight, applying ${addedStacks} [Exposed] stacks.`);

    // 2. Serafina Projects Shield
    this.state.aegisShield = Math.min(100, this.state.aegisShield + 5);
    if (this.passiveRegenBonus > 0) {
      this.state.innerFlame = Math.min(100, this.state.innerFlame + this.passiveRegenBonus);
    }

    // 3. Kaelen Attacks
    const baseDamage = this.state.darkModeActive ? 36 : 12;
    const multiplier = 1 + (this.state.exposedStacks * 0.4);
    const finalDmg = Math.floor(baseDamage * multiplier);

    this.state.enemyHealth = Math.max(0, this.state.enemyHealth - finalDmg);
    if (this.state.darkModeActive) {
      this.addLog(`Kaelen unleashes Oblivion Slash! Dealing ${finalDmg} dark damage!`);
      this.state.resonanceDrift = Math.max(0, this.state.resonanceDrift - 2);
    } else {
      this.addLog(`Kaelen strikes the Exposed gap, dealing ${finalDmg} damage!`);
      this.state.resonanceDrift = Math.min(100, this.state.resonanceDrift + 0.5);
    }
    this.state.exposedStacks = 0;
  }

  private processKaelenRecoil() {
    if (this.state.recoilPaused) return;

    let recoil = this.state.darkModeActive ? 30 : 10;
    if (this.state.innerFlame < 40) {
      recoil *= 1.8;
      this.addLog('Kaelen\'s Inner Flame is critical! Weight of the Oath increases Recoil volatility.');
    }

    const absorbed = Math.min(this.state.aegisShield, Math.floor(recoil * this.shieldAbsorbBonus));
    this.state.aegisShield -= absorbed;
    const bleedthrough = Math.max(0, recoil - absorbed);

    if (bleedthrough > 0) {
      this.state.innerFlame = Math.max(0, this.state.innerFlame - bleedthrough);
      this.addLog(`Inner Flame dims by ${bleedthrough} due to psychic Recoil.`);
    } else {
      this.addLog('Serafina\'s Aegis of Grace completely absorbs the Recoil.');
    }
  }

  private processEnemyTurn() {
    if (!this.state.isStunned) {
      const enemyDmg = this.state.enemyName === 'Ashen Abomination' ? 15 : 8;
      this.state.innerFlame = Math.max(0, this.state.innerFlame - enemyDmg);
      this.addLog(`The ${this.state.enemyName} attacks! Shared Inner Flame drops by ${enemyDmg}.`);
    } else {
      this.addLog(`The ${this.state.enemyName} is stunned and unable to strike.`);
    }
  }

  private triggerRandomEvent() {

    const events: BattleEvent[] = [
      {
        id: 'black_feather',
        title: 'The Black Feather',
        text: 'A shadow feather drifts down onto Oathbringer. The blade whispers for you to embrace it.',
        choices: [
          {
            text: 'Burn it in White Flame',
            costLabel: '+10 Inner Flame, +10 Resonance',
            effect: (eng) => {
              eng.modifyInnerFlame(10);
              eng.modifyResonanceDrift(10);
              eng.addLog('🔥 You burn the feather in White Flame. Hope flickers brighter.');
            }
          },
          {
            text: 'Let Oathbringer consume it',
            costLabel: '-10 Inner Flame, -20 Resonance (Nyx Shift)',
            effect: (eng) => {
              eng.modifyInnerFlame(-10);
              eng.modifyResonanceDrift(-20);
              eng.addLog('🌑 Oathbringer absorbs the feather. Nyx resonance flares!');
            }
          }
        ]
      },
      {
        id: 'whispering_sickness_echo',
        title: 'Whispers in the Ash',
        text: 'Voices of past wielders echo in your mind, questioning the Order\'s demands.',
        choices: [
          {
            text: 'Garrett: "Focus on the stance!"',
            costLabel: '+15 Shield Buffer',
            effect: (eng) => {
              eng.state.aegisShield = Math.min(100, eng.state.aegisShield + 15);
              eng.addLog('🛡️ Garrett grounds your focus, reinforcing the Aegis Shield.');
            }
          },
          {
            text: 'Serafina: "Hear their sorrow, then let go."',
            costLabel: '+15 Inner Flame',
            effect: (eng) => {
              eng.modifyInnerFlame(15);
              eng.addLog('✨ Serafina soothes the psychic strain. Inner Flame restored.');
            }
          }
        ]
      }
    ];

    const chosen = events[Math.floor(Math.random() * events.length)];
    this.state.activeEvent = chosen;
    this.addLog(`⚡ Moral Choice: ${chosen.title}`);
  }

  private checkDefeated(): boolean {
    if (this.state.enemyHealth <= 0) {
      this.handleVictory();
      return true;
    }
    return false;
  }

  private handleVictory() {
    this.state.victoryCount += 1;
    this.addLog(`✅ Victory! The ${this.state.enemyName} has collapsed into Ash.`);

    // Advance to next enemy in list
    const nextIndex = this.state.victoryCount % this.enemiesList.length;
    const nextEnemy = this.enemiesList[nextIndex];

    this.state.enemyName = nextEnemy.name;
    this.state.enemyMaxHealth = nextEnemy.maxHealth;
    this.state.enemyHealth = nextEnemy.maxHealth;
    this.state.enemyCategory = nextEnemy.category;
    this.state.enemyDescription = nextEnemy.description;
    this.state.enemyAbilities = nextEnemy.abilities;
    this.state.exposedStacks = 0;
    this.state.aegisShield = Math.min(100, this.state.aegisShield + 30); // Shield boost upon victory


    this.addLog(`A new threat emerges: ${nextEnemy.name} (${nextEnemy.maxHealth} HP).`);
    this.onStateChange({ ...this.state });
  }

  private handleDefeat() {
    this.stop();
    this.state.innerFlame = 0;
    this.addLog('❌ The Inner Flame has been extinguished. The darkness has claimed the spark.');
    this.onStateChange({ ...this.state });
  }

  private addLog(msg: string) {
    this.state.combatLog.unshift(msg); // Add to beginning of log
    if (this.state.combatLog.length > 20) {
      this.state.combatLog.pop();
    }
  }
}
