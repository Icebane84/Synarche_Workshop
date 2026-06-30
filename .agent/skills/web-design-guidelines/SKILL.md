---
name: web-design-guidelines
description:
    Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility",
    "audit design", "review UX", or "check my site against best practices".
allowed-tools: Read, Glob, Grep, Bash
---

# Web Design Guidelines System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Visual Excellence** and **Inclusive Interaction** through **Accessibility Standards (WCAG 2.1)** and **Responsive Architecture**. This skill mandates a "Liquid-First" approach for verification, ensuring that every interface is legible, navigable, and beautiful on any device.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Web Design Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `scripts/design_checker.py` - Automated Responsive & Spacing Audit.
- `axe-core-cli` (npx) - Automated Accessibility Scan.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "Contrast-First" Mandate
**MANDATORY**: All text and meaningful UI elements MUST meet the WCAG 2.1 AA contrast ratio (4.5:1). Critical actions must aim for AAA (7:1).

### 2. 44px Touch Target
**MANDATORY**: Any element intended for touch interaction must have a minimum physical size of 44x44 CSS pixels.

### 3. Keyboard Sovereignty
Every interactive element MUST be reachable and operable via keyboard only, with a high-visibility focus indicator.

### 4. Fluidity Mandate
PROHIBITED: Hardcoded `px` for layout widths or font sizes. MANDATED: `rem`, `em`, `%`, and `clamp()` for fluid adaptation.

---
"Design is the face of the Sovereign. Clarity is its voice."
