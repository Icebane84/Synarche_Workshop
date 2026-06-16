---
command: "game_creation"
description: Orchestrate specialized subagents to design, prototype, and build games using the game-development skill tree.
---

# /game_creation - Game Design & Creation Orchestrator

$ARGUMENTS

---

## 🎮 Purpose

This workflow routes through the full **game-development skill tree** to take a game concept from idea to playable prototype. It orchestrates the GDD (Game Design Document), core loop design, platform selection, and code generation using specialized subagents.

---

## 🔴 CRITICAL RULES

1. **GDD First** — No code before a Game Design Document is approved.
2. **30-Second Loop** — Every game must have a validated core gameplay loop.
3. **Platform First** — Determine target platform before building (Web, 2D, 3D).
4. **Iterate** — Prototype → Playtest → Refine. Never ship a first draft.

---

## Phase 0: Concept Intake

Ask the user:

```
🎮 Game Creation Wizard

1. What is your game concept? (one sentence pitch)
2. What genre? (platformer / shooter / puzzle / RPG / strategy / other)
3. What platform? (web browser / desktop / mobile)
4. Multiplayer or single-player?
5. Art style? (pixel / cartoon / realistic / minimalist)
```

Wait for answers before proceeding.

---

## Phase 1: Game Design Document (GDD)

Use the `game-design` skill to generate a GDD with these sections:

| Section         | Content                             |
| --------------- | ----------------------------------- |
| **Pitch**       | One-sentence description            |
| **Core Loop**   | 30-second gameplay (ACTION→REWARD)  |
| **Mechanics**   | How all systems work                |
| **Progression** | How the player advances             |
| **Art Style**   | Visual direction & palette          |
| **Audio**       | Sound design direction              |
| **MVP Scope**   | Minimum features for first playable |

Output GDD to: `docs/GDD-{game-slug}.md`

---

## Phase 2: Core Loop Validation

Validate the 30-second loop before any code:

```
30-SECOND LOOP TEST:
1. ACTION  → What does the player DO?
2. FEEDBACK → What does the GAME respond with?
3. REWARD  → What does the player FEEL?
4. REPEAT  → Is there a reason to do it again?

✅ PASS: All 4 stages answered clearly
❌ FAIL: Redesign the loop
```

---

## Phase 3: Platform Routing

Route to the correct skill branch based on platform:

| Platform        | Skill Branch                                    | Tech Stack              |
| --------------- | ----------------------------------------------- | ----------------------- |
| **Web Browser** | `.agent/skills/dev/game-development/web-games/` | Phaser.js / Canvas API  |
| **2D Desktop**  | `.agent/skills/dev/game-development/2d-games/`  | Pygame / Godot GDScript |
| **3D Desktop**  | `.agent/skills/dev/game-development/`           | Three.js / Unity C#     |

---

## Phase 4: Prototype Generation

Orchestrate the following subagents:

1. **`game-developer`** → Core mechanics implementation
   - Player controller
   - Core loop systems
   - Basic collision / physics

2. **`frontend-specialist`** → UI & HUD
   - Main menu
   - HUD (health, score, timer)
   - Game over / win screens

3. **`performance-optimizer`** → Runtime optimization
   - Frame rate targets (60fps)
   - Asset loading strategy
   - Memory management

---

## Phase 5: Playtest Report

After prototype generation, produce:

```
🎮 PLAYTEST REPORT
==================
Game: {game-name}
Loop: {core-loop-summary}
Platform: {platform}

✅ Core loop functional
✅ Player controller responsive
✅ Win/loss conditions defined
⏳ Sound effects (pending)
⏳ Level 2+ content (pending)

Next: /enhance add sound effects
Next: /enhance build level 2
```

---

## Usage Examples

```
/game_creation pixel platformer in the browser
/game_creation top-down zombie shooter
/game_creation puzzle game like Sokoban
/game_creation idle clicker RPG
/game_creation multiplayer snake game
```

---

## Skill Tree Reference

```
.agent/skills/dev/game-development/
├── game-design/        ← GDD, core loop, player psychology
├── web-games/          ← Phaser.js, Canvas, browser games
├── 2d-games/           ← 2D engines, sprites, tilemaps
└── (performance-optimizer pinned from axion-core)
```

---

> **Remember:** Fun is discovered through iteration, not designed on paper. Ship the prototype. Playtest. Refine.
