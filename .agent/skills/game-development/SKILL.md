---
id: SKILL-GAM-001
name: Game Development Principles
version: v2.1 [GOLD]
type: SYSTEM_PRINCIPLES
status: [ACTIVE]
tags: ['#GAMEDEV', '#ENGINEERING', '#SOVEREIGN']
---

# 🎮 GAME DEVELOPMENT | SKILL-GAM-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Game.Dev             |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC PRINCIPLES

### 1. The Game Loop (MANDATORY)

Every game follows this pattern: **INPUT → UPDATE (Fixed Timestep) → RENDER (Interpolated)**

- **Fixed Timestep**: Physics/Logic must run at a consistent rate (e.g., 50-60Hz).
- **Interpolation**: Smooth any visual jitter between logic frames.

### 2. Input Abstraction

Abstract input into **ACTIONS**, not raw keys.

- **Jump**: Space | A-Button | Tap.
- **Move**: WASD | Left-Stick | Virtual Joy.

### 3. Performance Budget (16.67ms for 60 FPS)

- **Input/AI/Logic**: 7ms.
- **Physics**: 3ms.
- **Rendering**: 5ms.
- **Wait/Buffer**: 1.67ms.

---

## 🔍 GATEWAY NAVIGATION PROTOCOL (GNP)

Navigate the game development system using these canonical files:

| File                 | Status          | Context                               |
| :------------------- | :-------------- | :------------------------------------ |
| [INDEX.md](INDEX.md) | 🔴 **REQUIRED** | Gateway for the cluster.              |
| [AOP.md](AOP.md)     | 🔴 **REQUIRED** | Operational Playbook (MDA/2D/3D).     |
| [GUCA.md](GUCA.md)   | ⚪ Optional     | Command Registry (Scaffolding/Audit). |
| [SELT.md](SELT.md)   | ⚪ Optional     | Experience Log (Gold Standard).       |

---

## ⚡ ACTIONABLE HEURISTICS

- **[MDA_FRAMEWORK]**: Mechanics (Rules) → Dynamics (Player behavior) → Aesthetics (Emotional response).
- **[30-SECOND_TEST]**: Is the core loop fun for 30 seconds?
- **[ANTI_PATTERN_ZERO]**: No object creation in hot loops. Profile before optimizing.

---

`[OMNI-ARTIFACT-ANCHOR] ID: SKILL-GAM-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
