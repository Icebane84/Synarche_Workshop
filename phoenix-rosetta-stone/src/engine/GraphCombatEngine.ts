import graphDb from '../data/adjacency_matrix.json';

export interface BattleState {
  log: any;
  innerFlame: number;
  aegisShield: number;
  exposedStacks: number;
  enemyHealth: number;
  enemyMaxHealth: number;
  enemyName: string;
  isStunned: boolean;
  recoilPaused: boolean;
  combatLog: string[];
  activePulsingNodes: string[]; // Node IDs that should light up/pulse
  activeGlowLinks: Array<{ source: string; target: string }>; // Link connections to glow
  victoryCount: number;
}

/**
 * Cryptographically secure random float generator [0, 1) for combat roll simulation.
 * Uses Web Crypto API (crypto.getRandomValues) to eliminate SonarQube S2245 warnings.
 */
const getRandomFloat = (): number => {
  const array = new Uint32Array(1);
  crypto.getRandomValues(array);
  return array[0] / (0xffffffff + 1);
};

export class GraphCombatEngine {
  private readonly state: BattleState;
  private readonly onStateChange: (state: BattleState) => void;
  private isRunning: boolean = false;
  private tickInterval: ReturnType<typeof setInterval> | null = null;

  // Raw Graph Database
  private readonly nodes: any = graphDb.nodes;
  private readonly edges: any[] = graphDb.edges;

  // Resolved entities from the graph
  private characters: any = {};
  private relics: any = {};
  private talents: any = {};
  private readonly enemies: any[] = [];
  private activeZone: any = {};

  constructor(
    onStateChange: (state: BattleState) => void,
    unlockedTalentIds: string[] = []
  ) {
    this.onStateChange = onStateChange;
    this.resolveGraphEntities(unlockedTalentIds);
    this.state = this.getInitialState();
  }

  private resolveGraphEntities(unlockedTalents: string[]) {
    const nodeList: any[] = Array.isArray(this.nodes) ? this.nodes : Object.values(this.nodes);
    this.indexNodes(nodeList, unlockedTalents);
    this.indexEdges();
  }

  private indexNodes(nodeList: any[], unlockedTalents: string[]) {
    for (const node of nodeList) {
      const data = node as any;
      const id = data.id;
      const props = data.properties || {};
      switch (data.label) {
        case 'Character':
          this.characters[id] = { ...props, id, name: data.name, baseAtk: props.atk || 15, baseHp: props.hp || 100 };
          break;
        case 'Artifact':
        case 'Relic':
          this.relics[id] = { ...props, id, name: data.name };
          break;
        case 'Talent':
        case 'Ability':
          if (unlockedTalents.includes(id) || data.label === 'Ability') {
            this.talents[id] = { ...props, id, name: data.name };
          }
          break;
        case 'Enemy':
          this.enemies.push({ ...props, id, name: data.name, maxHp: props.hp || 120, atk: props.atk || 12 });
          break;
        case 'Location':
        case 'Zone':
          this.activeZone = { ...props, id, name: data.name };
          break;
      }
    }
  }

  private indexEdges() {
    for (const edge of this.edges) {
      const { source, target, relation } = edge;

      if (relation === 'WIELDS' && this.characters[source] && this.relics[target]) {
        this.characters[source].relic = this.relics[target];
      }

      if (relation === 'STRENGTHENS' && this.talents[source] && this.characters[target]) {
        const talent = this.talents[source];
        const char = this.characters[target];
        char.talents = char.talents || [];
        char.talents.push(talent);
      }
    }
  }

  private getInitialState(): BattleState {
    const defaultEnemy = this.enemies[0] || { name: 'Shadow', maxHp: 100, hp: 100, id: 'enemy-shadow' };
    return {
      innerFlame: 100,
      aegisShield: 20,
      exposedStacks: 0,
      enemyHealth: defaultEnemy.maxHp,
      enemyMaxHealth: defaultEnemy.maxHp,
      enemyName: defaultEnemy.name,
      isStunned: false,
      recoilPaused: false,
      combatLog: ['Ingesting graph node alignments... [IGNITE]'],
      activePulsingNodes: [],
      activeGlowLinks: [],
      victoryCount: 0,
      log: undefined,
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
    this.state.enemyHealth = Math.max(0, this.state.enemyHealth - 5);
    this.addLog('Manual Intervention: Fed spark (+5 damage).');

    // Pulse the core active node representing manual input
    this.pulseNodes(['char-kaelen'], 'zone-oakhaven');
    this.checkDefeated();
    this.onStateChange({ ...this.state });
  }

  // Active Ultimate: Garrett
  public triggerGroundingCommand(): boolean {
    if (!this.isRunning || this.state.isStunned) return false;
    this.state.isStunned = true;
    this.state.recoilPaused = true;
    this.addLog('Garrett: Traverses [COORDINATES] link. "Hold!" (Stunned, Recoil Paused)');

    // Light up Garrett and connection to Kaelen
    this.pulseNodes(['char-garrett', 'char-kaelen']);
    this.state.activeGlowLinks = [{ source: 'char-garrett', target: 'char-kaelen' }];
    this.onStateChange({ ...this.state });

    setTimeout(() => {
      this.state.isStunned = false;
      this.state.recoilPaused = false;
      this.state.activeGlowLinks = [];
      this.addLog('Garrett\'s Command link closes. Enemy recovers.');
      this.onStateChange({ ...this.state });
    }, 3000);

    return true;
  }

  // Active Ultimate: Serafina
  public triggerWhispersOfTheDawn(): boolean {
    if (!this.isRunning) return false;
    this.state.innerFlame = 100;
    this.addLog('Serafina: Traverses [PROTECTS] link. Shared Flame fully restored.');

    // Pulse Serafina and Kaelen
    this.pulseNodes(['char-serafina', 'char-kaelen']);
    this.state.activeGlowLinks = [{ source: 'char-serafina', target: 'char-kaelen' }];
    this.onStateChange({ ...this.state });
    return true;
  }

  // Active Ultimate: Kaelen
  public triggerInwardInquisition(): boolean {
    if (!this.isRunning || this.state.innerFlame < 50) return false;
    const dmg = Math.floor(this.state.enemyMaxHealth * 0.45);
    this.state.enemyHealth = Math.max(0, this.state.enemyHealth - dmg);
    this.state.innerFlame = Math.max(10, this.state.innerFlame - 30);
    this.addLog(`Kaelen: Judgment Shockwave deals ${dmg} damage!`);

    // Pulse Kaelen and the current enemy
    const enemy = this.getCurrentEnemyNode();
    if (enemy) {
      this.pulseNodes(['char-kaelen', enemy.id]);
      this.state.activeGlowLinks = [{ source: 'char-kaelen', target: enemy.id }];
    }

    this.checkDefeated();
    this.onStateChange({ ...this.state });
    return true;
  }

  private processGarrettPhase() {
    let exposedPerHit = 1;
    const garrettNode = this.characters['char-garrett'];
    if (garrettNode?.talents) {
      const reflexes = garrettNode.talents.find((t: any) => t.id === 'talent-alerion-reflexes');
      if (reflexes) {
        exposedPerHit += reflexes.extra_exposed || 0;
      }
    }

    this.state.exposedStacks += exposedPerHit;
    this.addLog(`Garrett: Applied ${exposedPerHit} stacks of [Exposed].`);
    this.state.activePulsingNodes.push('char-garrett');
  }

  private processSerafinaPhase(): number {
    let shieldBonusMultiplier = 1.0;
    let regenBonus = 0;
    const serafinaNode = this.characters['char-serafina'];
    if (serafinaNode?.talents) {
      const grace = serafinaNode.talents.find((t: any) => t.id === 'talent-wardens-grace');
      if (grace) {
        shieldBonusMultiplier = grace.shield_bonus || 1.0;
      }
    }

    const kaelenNode = this.characters['char-kaelen'];
    if (kaelenNode?.talents) {
      const ember = kaelenNode.talents.find((t: any) => t.id === 'talent-eternal-ember');
      if (ember) {
        regenBonus = ember.regen_bonus || 0;
      }
    }

    this.state.aegisShield = Math.min(100, this.state.aegisShield + 5);
    if (regenBonus > 0) {
      this.state.innerFlame = Math.min(100, this.state.innerFlame + regenBonus);
    }
    this.state.activePulsingNodes.push('char-serafina');

    return shieldBonusMultiplier;
  }

  private processKaelenPhase(): { baseRecoil: number } {
    let weaponAtkBonus = 0;
    let baseRecoil = 10;
    const kaelenNode = this.characters['char-kaelen'];

    if (kaelenNode?.relic) {
      weaponAtkBonus = kaelenNode.relic.atk_bonus || 0;
      baseRecoil = kaelenNode.relic.recoil || 10;
    }

    const totalAtk = (kaelenNode ? kaelenNode.baseAtk : 10) + weaponAtkBonus;
    const multiplier = 1 + (this.state.exposedStacks * 0.4);

    const isGemCrit = getRandomFloat() < 0.35; // 35% Gem Crit chance
    const critMultiplier = isGemCrit ? 1.5 : 1.0;
    const finalDmg = Math.floor(totalAtk * multiplier * critMultiplier);

    if (isGemCrit) {
      this.addLog(`Kaelen: L1 Gem Resonates! [CRITICAL STRIKE] for ${finalDmg} damage!`);
    } else {
      this.addLog(`Kaelen: Strikes through [WIELDS] slot for ${finalDmg} damage!`);
    }
    this.state.activePulsingNodes.push('char-kaelen');

    const enemyNode = this.getCurrentEnemyNode();
    if (enemyNode) {
      this.state.activePulsingNodes.push(enemyNode.id);
      this.state.activeGlowLinks.push({ source: 'char-kaelen', target: enemyNode.id });
    }

    return { baseRecoil };
  }

  private processRecoilPhase(baseRecoil: number, shieldBonusMultiplier: number) {
    if (this.state.recoilPaused) return;

    let recoil = baseRecoil;
    if (this.state.innerFlame < 40) {
      recoil = Math.floor(baseRecoil * 1.8);
      this.addLog('Kaelen: Weight of the Oath triggers. Recoil increases!');
    }

    const shieldAbsorb = Math.min(this.state.aegisShield, Math.floor(recoil * shieldBonusMultiplier));
    this.state.aegisShield -= shieldAbsorb;
    const bleedthrough = Math.max(0, recoil - shieldAbsorb);

    if (bleedthrough > 0) {
      this.state.innerFlame = Math.max(0, this.state.innerFlame - bleedthrough);
      this.addLog(`Psychic Recoil dims Inner Flame by ${bleedthrough}.`);
      this.state.activeGlowLinks.push({ source: 'relic-oathbringer', target: 'char-kaelen' });
    } else {
      this.addLog('Serafina\'s Aegis of Grace completely absorbs the Recoil.');
      this.state.activeGlowLinks.push({ source: 'char-serafina', target: 'char-kaelen' });
    }
  }

  private processEnemyPhase() {
    const enemyNode = this.getCurrentEnemyNode();
    if (!this.state.isStunned && enemyNode) {
      const enemyAtk = enemyNode.atk || 10;
      this.state.innerFlame = Math.max(0, this.state.innerFlame - enemyAtk);
      this.addLog(`The ${this.state.enemyName} strikes! Shared Flame dims by ${enemyAtk}.`);
      this.state.activeGlowLinks.push({ source: enemyNode.id, target: 'char-kaelen' });
    }
  }

  private tick() {
    if (this.state.innerFlame <= 0) {
      this.handleDefeat();
      return;
    }

    // Reset visual pulses
    this.state.activePulsingNodes = [];
    this.state.activeGlowLinks = [];

    // Modularized combat phases
    this.processGarrettPhase();
    const shieldBonusMultiplier = this.processSerafinaPhase();
    const { baseRecoil } = this.processKaelenPhase();

    this.state.exposedStacks = 0; // Reset stacks

    if (this.checkDefeated()) return;

    this.processRecoilPhase(baseRecoil, shieldBonusMultiplier);
    if (this.state.innerFlame <= 0) {
      this.handleDefeat();
      return;
    }

    this.processEnemyPhase();
    if (this.state.innerFlame <= 0) {
      this.handleDefeat();
      return;
    }

    this.onStateChange({ ...this.state });
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
    this.addLog(`✅ Victory! Enemy dissolved into Ash.`);

    // Choose next enemy in the list
    const nextIndex = this.state.victoryCount % this.enemies.length;
    const nextEnemy = this.enemies[nextIndex];

    this.state.enemyName = nextEnemy.name;
    this.state.enemyMaxHealth = nextEnemy.maxHp;
    this.state.enemyHealth = nextEnemy.maxHp;
    this.state.exposedStacks = 0;
    this.state.aegisShield = Math.min(100, this.state.aegisShield + 35);

    this.addLog(`New Adversary located: ${nextEnemy.name} (${nextEnemy.maxHp} HP).`);
    this.onStateChange({ ...this.state });
  }

  private handleDefeat() {
    this.stop();
    this.state.innerFlame = 0;
    this.addLog('❌ Inner Flame Extinguished. Rebirth via the Sanctuary of Memory is required.');
    this.onStateChange({ ...this.state });
  }

  private getCurrentEnemyNode() {
    return this.enemies.find(e => e.name === this.state.enemyName);
  }

  private pulseNodes(nodeIds: string[], targetZone: string = 'zone-oakhaven') {
    this.state.activePulsingNodes = [...nodeIds, targetZone];
  }

  private addLog(msg: string) {
    this.state.combatLog.unshift(msg);
    if (this.state.combatLog.length > 15) {
      this.state.combatLog.pop();
    }
  }
}
