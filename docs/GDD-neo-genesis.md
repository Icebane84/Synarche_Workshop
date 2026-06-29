# Game Design Document: NEO-GENESIS EVOLUTION

> **Artifact ID**: `GDD-NEO-GENESIS-001` **Evolution Stage**: `STANDALONE ENGINE V1.0` **Package Location**:
> [`nova_forge/prototypes/neo-genesis`](file:///c:/Users/Chris/Synarche_Workspace/nova_forge/prototypes/neo-genesis)
> **Status**: `[CANONIZED STANDALONE ENGINE]`

---

## 🌌 1. Pitch

---

_NEO-GENESIS EVOLUTION_ is a single-player evolutionary simulation strategy game where players guide an alien species
from a microscopic single-celled organism swimming in primordial soup, through tribal and planetary stages, all the way
to an interstellar galactic empire.

---

## 🔄 2. CORE Gameplay Loop (30-Second Loop)

---

```plaintext
[ HARVEST BIO-ENERGY ] ──> [ MUTATE & EVOLVE ] ──> [ EXPAND DOMINION ] ──> [ UNLOCK NEW ERA ]
       ▲                                                                          │
       └──────────────────────────────────────────────────────────────────────────┘
```

1. **ACTION**: Player harvests Bio-Mass (organelle ingestion, resource gathering, planetary terraforming) and assigns
   Mutation Points.
2. **FEEDBACK**: Organism / species dynamically mutates visual traits (flagella, armor plating, neural networks,
   hyperdrives) and increases stats (Adaptability, Aggression, Intelligence, Energy).
3. **REWARD**: Immediate physical evolution unlocked, unlocking new biomes, rivals, and expansion vectors.
4. **REPEAT**: Advance to higher evolutionary stages (Cellular ➔ Aquatic ➔ Tribal ➔ Global Empire ➔ Interstellar
   Starfarer).

---

## ⚙️ 3. Mechanics & Evolutionary Eras

---

### Stage I: Primordial Cell (Microscopic Phase)

---

- **Controls/Interface**: Canvas-based micro-organism swimming.

- **Goal**: Consume nutrients, avoid predators, collect 100 DNA points to split and evolve cilia/membranes.

### Stage II: Tribal & Planetary Civilization

---

- **Controls/Interface**: Strategy grid / territorial map.

- **Goal**: Manage pop growth, build habitats, balance ecology vs. industry.

### Stage III: Interstellar Galaxy

---

- **Controls/Interface**: Galactic star map.

- **Goal**: Dispatch starships, colonize exoplanets, build Dyson swarms.

---

## 🎨 4. Art Style & Visual Direction

---

- **Aesthetic**: **Dark Modern Neon Glassmorphism mixed with Retro Pixel Art**.

- **Palette**: Deep void darks (`#0a0b10`), glowing cyan (`#00f0ff`), neon purple (`#a855f7`), and bio-amber
  (`#f59e0b`).
- **UI Elements**: Translucent blurred glass panels (`backdrop-blur-md`), pulsing neon borders, pixel-rendered creature
  sprites and planetary icons.

---

## 🎵 5. Audio Direction

---

- **Atmosphere**: Ambient synthwaves transitioning from deep aquatic echoes to cosmic electronic soundscapes.

---

## 🚀 6. MVP Scope for First Playable

---

For our initial interactive prototype inside `phoenix-rosetta-stone`:

1. **Stage I (Cellular Phase)**: Interactive canvas / Grid simulator where players control a cell, absorb Bio-Mass,
   collect DNA points, and trigger live mutations.
2. **Evolution Chamber**: Interactive glassmorphic UI upgrade panel to spend DNA points on Adaptability, Speed, and
   Armor.
3. **Stage Transition**: Reaching 100% Evolutionary Readiness unlocks the **Tribal / Planetary Phase**!
