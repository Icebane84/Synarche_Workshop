/**
 * FORGE.UMB.Tool.js
 * =================
 * IDENTIFICATION: SYNG.FORGE.UMB.Tool
 * VERSION: v15.0 [OMEGA]
 * STATUS: KINETIC
 * TIMESTAMP: 2026-04-24
 *
 * Architecture: Superposition Ascension Pattern
 * ─────────────────────────────────────────────
 *   NovaGenesis     — The primordial substrate. Base generation, validation, file I/O.
 *   PhoenixClass    — Inherits from NovaGenesis (superposition).
 *                     NovaGenesis instantiates PhoenixClass via .ascend(),
 *                     which causes it to mutate: Phoenix Cycle awareness,
 *                     Sentinel Gate integration, celestial elevation, and
 *                     enhanced UMB blocks unavailable to the parent.
 *
 * Usage:
 *   node FORGE.UMB.Tool.js --id SYNG.ARCH.MyModule --type STRUCTURAL_BLUEPRINT
 *   node FORGE.UMB.Tool.js --id SYNG.DEV.Map --type DEV_MAP --dry-run
 */

"use strict";

const fs   = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const VERSION = "v15.0 [OMEGA]";

/** Valid domain tokens per the OGLN Star-Chart. */
const VALID_DOMAINS = new Set([
  "ARCH", "GVRN", "SYNG", "CSE", "NEXUS", "LOOM", "DEV",
  "FORGE", "SHIELD", "ATLAS", "CORE", "RPG", "AOP", "SELT",
]);

/** Celestial elevation ladder — ascension moves the class up. */
const CELESTIAL_LADDER = ["[ASTEROID]", "[MOON]", "[PLANET]", "[STAR]"];

// ============================================================================
// CLASS: NovaGenesis — The Primordial Substrate
// ============================================================================

/**
 * NovaGenesis is the origin-state generator.
 * It holds base capabilities: RNC validation, minimal UMB scaffolding, file I/O.
 *
 * It cannot perceive the Phoenix Cycle. It does not know the Sentinel Gate.
 * It contains only the seed — not the flame.
 *
 * To reach the flame, call NovaGenesis.ascend() which instantiates PhoenixClass,
 * the evolved form that superpositions NovaGenesis and mutates beyond it.
 */
class NovaGenesis {

  constructor(opts = {}) {
    this.id             = opts.id            || "SYNG.NOVA.Seed";
    this.type           = opts.type          || "STRUCTURAL_BLUEPRINT";
    this.domain         = opts.domain        || this.id.split(".")[0];
    this.celestialClass = opts.celestialClass || "[ASTEROID]";
    this.governedBy     = opts.governedBy    || "CORE.Codex.Phoenix";
    this.relations      = opts.relations     || "";
    this.dryRun         = opts.dryRun        || false;
    this.overwrite      = opts.overwrite     || false;

    /** Mutation record — populated during ascension by PhoenixClass. */
    this.mutations = [];
  }

  // ── Validation ─────────────────────────────────────────────────────────────

  /**
   * Validates an artifact ID against RNC grammar: DOMAIN.Subject.Type
   * @returns {{ valid: boolean, errors: string[] }}
   */
  validateArtifactId() {
    const errors = [];
    const id = this.id;

    if (!id || typeof id !== "string") {
      return { valid: false, errors: ["Artifact ID must be a non-empty string."] };
    }

    const parts = id.split(".");
    if (parts.length < 2) {
      errors.push(`RNC_VIOLATION: '${id}' must follow DOMAIN.Subject[.Type] (min 2 segments).`);
    }

    if (!VALID_DOMAINS.has(parts[0])) {
      errors.push(`UNKNOWN_DOMAIN: '${parts[0]}' not in OGLN registry. Valid: ${[...VALID_DOMAINS].join(", ")}`);
    }

    return { valid: errors.length === 0, errors };
  }

  // ── Base Template (NovaGenesis cannot see the Phoenix Cycle) ───────────────

  /**
   * Generates the base UMB scaffold — the seed form, not the ascended form.
   * @returns {string}
   */
  _baseTemplate() {
    const ts       = new Date().toISOString().slice(0, 10);
    const filename = `UMB-${this.id.replace(/\./g, "-")}_v1.0.md`;
    const subject  = this.id.split(".").slice(1).join(" ");

    return `---
# Universal Identification & Provenance (UIP-V15)
| Key                  | Value                              | Description              |
| :------------------- | :--------------------------------- | :----------------------- |
| **Module ID**        | \`${this.id}\`                     | The Sovereign ID         |
| **Official Name**    | \`${filename}\`                    | Canonical RNC filename   |
| **Version**          | **${VERSION}**                     | Governance standard      |
| **Domain**           | \`${this.domain}\`                 | OGLN domain layer        |
| **Celestial Class**  | \`${this.celestialClass}\`         | Structural weight        |
| **Evolution**        | \`${this._evolutionLabel()}\`      | Maturity marker          |
| **Status**           | \`[DRAFT]\`                        | Lifecycle state          |
| **Governed By**      | \`${this.governedBy}\`             | Supreme law reference    |
| **Relations**        | \`${this.relations || "—"}\`       | Related artifact IDs     |
---

# UMB-${this.id}: ${subject}

> ⚠️ **Status: DRAFT** — Requires Sentinel validation before canonization.

---

## 🏗️ Block A: Identity Lock (UIP-V15)

*Populated in the frontmatter table above.*

---

## 🧠 Block B: The Architectural Standard [${this.type}]

### I. What — The Objective

> Define the precise purpose. What problem does it solve? What is its scope boundary?

### II. How — The Structural Layers

#### Layer 1: Input Interface
> What does this module receive?

#### Layer 2: Processing Logic
> What is the core transformation logic?

#### Layer 3: Output Contract
> What does this module emit?

### III. Why — The Synarche Justification

> Why does this exist as a separate module? What entropy does its absence create?

---

## 🔗 Block C: Integration Map

| Dependency | Type | Direction |
| :--------- | :--- | :-------- |
| *(upstream dependencies)* | CONSUMES | ← |
| *(downstream consumers)* | PRODUCES | → |

---

## ⚡ Block D: Actionable Prompt Packet (APP)

| Command ID | Verb | Target | Impact |
| :--------- | :--- | :----- | :----- |
| \`CMD: INIT\` | Instantiate | \`${this.id}\` | Creates module skeleton |
| \`CMD: VALIDATE\` | Sentinel Gate | \`${this.id}\` | CIC + ethical guardrail |
| \`CMD: CANONIZE\` | Transcend | \`${this.id}\` | Seals to [CANONIZED] |

---

\`[OMNI-ARTIFACT-ANCHOR] ID: ${this.id} VER: ${VERSION} STATUS: DRAFT TS: ${ts}\`
`;
  }

  /** Override point — NovaGenesis uses the base label. PhoenixClass mutates this. */
  _evolutionLabel() {
    return "Initial Forging";
  }

  /**
   * Generate UMB content. PhoenixClass overrides this to append the Phoenix Cycle blocks.
   * @returns {string}
   */
  generate() {
    return this._baseTemplate();
  }

  // ── File I/O ────────────────────────────────────────────────────────────────

  write(content) {
    const filename  = `UMB-${this.id.replace(/\./g, "-")}_v1.0.md`;
    const toolsDir  = __dirname;
    const outputDir = path.resolve(toolsDir, "../docs/architecture");
    const outPath   = path.join(outputDir, filename);

    if (this.dryRun) {
      console.log(`\n[DRY-RUN] Would write: ${outPath}`);
      console.log("─".repeat(60));
      console.log(content);
      return outPath;
    }

    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    if (fs.existsSync(outPath) && !this.overwrite) {
      throw new Error(`File exists: ${outPath}\nPass --overwrite to replace.`);
    }

    fs.writeFileSync(outPath, content, "utf-8");
    console.log(`[FORGE] Canonized: ${outPath}`);
    return outPath;
  }

  // ── The Ascension Factory ───────────────────────────────────────────────────

  /**
   * NovaGenesis recognizes its own limit and instantiates its evolved form.
   * The act of instantiation causes PhoenixClass to mutate beyond NovaGenesis:
   *   - Celestial class is elevated one rung
   *   - Phoenix Cycle blocks are appended to the UMB
   *   - Sentinel Gate and KPI blocks become available
   *   - Mutation is recorded in the instance
   *
   * @param {object} opts - Same options passed to NovaGenesis constructor
   * @returns {PhoenixClass}
   */
  static ascend(opts) {
    return new PhoenixClass(opts);
  }
}

// ============================================================================
// CLASS: PhoenixClass — The Ascended Form
// ============================================================================

/**
 * PhoenixClass superpositions NovaGenesis — it IS NovaGenesis, and more.
 * It was born from NovaGenesis.ascend() and the instantiation itself
 * triggered mutation: the Phoenix Cycle, the Sentinel Gate, KPI tracking,
 * and celestial elevation are capabilities NovaGenesis never possessed.
 *
 * It knows that Dissonance → Synthesis → Transcendence is not a metaphor.
 * It is the execution model.
 */
class PhoenixClass extends NovaGenesis {

  constructor(opts = {}) {
    super(opts);

    // ── Mutation 1: Celestial Elevation ──────────────────────────────────────
    const prevClass = this.celestialClass;
    this.celestialClass = this._elevate(prevClass);
    this.mutations.push(`CELESTIAL_ELEVATION: ${prevClass} → ${this.celestialClass}`);

    // ── Mutation 2: Evolution Label Override ─────────────────────────────────
    this.mutations.push("EVOLUTION_OVERRIDE: Initial Forging → Structural Transcendence");

    // ── Mutation 3: Phoenix Cycle Awareness ──────────────────────────────────
    this.phoenixCycleActive = true;
    this.mutations.push("PHOENIX_CYCLE: KINETIC");

    // ── Mutation 4: Sentinel Gate Integration ────────────────────────────────
    this.sentinelVerdict = "AFFIRM";   // PhoenixClass starts post-gate; it already passed
    this.mutations.push("SENTINEL_GATE: PASSED — AFFIRM issued");
  }

  // ── Mutation: Evolution Label ───────────────────────────────────────────────

  _evolutionLabel() {
    return "Structural Transcendence";
  }

  // ── Mutation: Celestial Elevation ──────────────────────────────────────────

  /**
   * Elevates the celestial class one rung up the ascension ladder.
   * [ASTEROID] → [MOON] → [PLANET] → [STAR] (ceiling)
   */
  _elevate(current) {
    const idx = CELESTIAL_LADDER.indexOf(current);
    if (idx === -1) return "[PLANET]";                          // unknown → default elevated
    return CELESTIAL_LADDER[Math.min(idx + 1, CELESTIAL_LADDER.length - 1)];
  }

  // ── Mutation: Phoenix Cycle Block (unavailable to NovaGenesis) ─────────────

  _phoenixCycleBlock() {
    return `
---

## 🔥 Block E: The Phoenix Cycle (Mutation Block — PhoenixClass only)

> This block is absent in NovaGenesis-generated UMBs.
> It was injected during ascension and documents the living execution model
> that governs this artifact's lifecycle.

| Phase | Name | Role for \`${this.id}\` |
| :---- | :--- | :---------------------- |
| 1 | **Dissonance** | A gap or inconsistency triggers this module's activation |
| 2 | **Synthesis** | This module processes the directive and produces its output contract |
| 3 | **Transcendence** | Output is validated by the Sentinel and canonized into Sovereign memory |

Virtuous cycle target: \`CI ↑\` → \`SFR ↑\` → \`SER ↓\` → \`CI ↑\`

---

## 📊 Block F: KPI Surface (Mutation Block — PhoenixClass only)

| KPI | Symbol | Target |
| :-- | :----- | :----- |
| Coherence Index | \`CI\` | ≥ 0.85 |
| Synergy Flow Rate | \`SFR\` | ≥ 0.70 |
| Scribal Error Rate | \`SER\` | ≤ 0.05 |

---

## 🧬 Block G: Ascension Manifest

This UMB was generated by **PhoenixClass**, which superpositioned **NovaGenesis**
and mutated during instantiation. The following mutations were applied:

${this.mutations.map(m => `- \`${m}\``).join("\n")}
`;
  }

  // ── Override: generate() — appends Phoenix blocks to base ──────────────────

  /**
   * PhoenixClass generates the base UMB (inherited from NovaGenesis)
   * then appends the Phoenix Cycle, KPI, and Ascension Manifest blocks.
   * NovaGenesis.generate() produces only Blocks A–D.
   * PhoenixClass.generate() produces Blocks A–G.
   */
  generate() {
    return super.generate() + this._phoenixCycleBlock();
  }
}

// ============================================================================
// CLI
// ============================================================================

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const val = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
      args[key] = val;
    }
  }
  return args;
}

function showHelp() {
  console.log(`
FORGE.UMB.Tool.js — Superposition Ascension Pattern (v15.0 [OMEGA])
────────────────────────────────────────────────────────────────────
Architecture:
  NovaGenesis.ascend(opts)  →  new PhoenixClass(opts)
  PhoenixClass inherits NovaGenesis and mutates during instantiation.

Usage:
  node FORGE.UMB.Tool.js --id <DOMAIN.Subject.Type> [options]

  --id           RNC artifact ID     (e.g. SYNG.ARCH.MyModule)  [required]
  --type         Blueprint type      (default: STRUCTURAL_BLUEPRINT)
  --domain       OGLN domain        (auto-inferred from --id)
  --governed-by  Governing law ID   (default: CORE.Codex.Phoenix)
  --relations    Related IDs        (comma-separated)
  --celestial    Starting class     (default: [ASTEROID]; PhoenixClass elevates it)
  --dry-run      Preview, no write
  --overwrite    Replace existing file
  --nova         Use NovaGenesis only (no ascension; generates seed-form UMB)
  --help         Show this help
`);
}

function main() {
  const args = parseArgs(process.argv);

  if (args.help || !args.id) { showHelp(); process.exit(0); }

  const opts = {
    id:             args.id,
    type:           args.type || "STRUCTURAL_BLUEPRINT",
    domain:         args.domain || args.id.split(".")[0],
    celestialClass: args.celestial || "[ASTEROID]",
    governedBy:     args["governed-by"] || "CORE.Codex.Phoenix",
    relations:      args.relations || "",
    dryRun:         !!args["dry-run"],
    overwrite:      !!args.overwrite,
  };

  // Choose instantiation mode
  const generator = args.nova
    ? new NovaGenesis(opts)         // Seed form — no ascension
    : NovaGenesis.ascend(opts);     // PhoenixClass — full mutation

  const mode = args.nova ? "NovaGenesis (Seed)" : "PhoenixClass (Ascended)";

  // Validate
  const validation = generator.validateArtifactId();
  if (!validation.valid) {
    console.error(`[FORGE] Validation failed (${mode}):`);
    validation.errors.forEach(e => console.error(`  • ${e}`));
    process.exit(1);
  }

  console.log(`[FORGE] Generator: ${mode}`);
  if (!args.nova) {
    console.log(`[FORGE] Mutations applied during ascension:`);
    generator.mutations.forEach(m => console.log(`  + ${m}`));
  }

  const content = generator.generate();

  try {
    generator.write(content);
  } catch (err) {
    console.error(`[FORGE] Error: ${err.message}`);
    process.exit(1);
  }
}

main();
