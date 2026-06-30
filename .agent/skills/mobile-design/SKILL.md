---
name: mobile-design
description:
    Mobile-first design thinking and decision-making for iOS and Android apps. Touch interaction, performance patterns,
    platform conventions. Teaches principles, not fixed values. Use when building React Native, Flutter, or native
    mobile apps.
allowed-tools: Read, Glob, Grep, Bash
---

# Mobile Design System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Touch-First**, **Platform-Respectful**, and **Performance-Mandated** design across all mobile ecosystems. This skill prevents AI "Safe Harbor" defaults and mandates deep context scanning before any implementation.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Global Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `scripts/mobile_audit.py` - Automated UX & Touch Audit. Usage: `python scripts/mobile_audit.py <project_path>`.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. The Anti-Safe-Harbor Rule
**DO NOT** default to tab bars, Redux, or FlatList without completing the **Mandatory Context Scan** in `AOP.md`.

### 2. Tactile Integrity
Every interactive element **MUST** have a touch target of **44pt (iOS) / 48dp (Android)**. Spacing between targets must be **8pt/dp** minimum.

### 3. Performance Guardrail
**Frame drops are failures.** Use `FlatList`/`ListView.builder` for all dynamic data. Never use `ScrollView` for lists with >10 items.

### 4. Platform Respect
iOS must feel like iOS (HIG); Android must feel like Android (Material 3). Match system fonts (SF Pro vs Roboto) and haptic/ripple patterns.

---
"Mobile is not a small desktop. It is a portal to a tactile, immediate reality."
