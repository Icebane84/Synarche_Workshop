---
name: tailwind-patterns
description:
    Tailwind CSS v4 principles. CSS-First configuration, container queries, modern patterns, design token
    architecture.
allowed-tools: Read, Glob, Grep, Bash
---

# Tailwind Patterns System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Visual Identity** and **Dynamic Styling** through **v4 CSS-First Architecture** and **Utility-First Excellence**. This skill mandates a "Theme-First" approach for verification, ensuring that every UI element is structurally consistent, performant, and accessible.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Modern Tailwind Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `npx tailwindcss build` - Automated Theme Generation.
- `scripts/omega_audit.py` - Universal Cluster-Wide Health Check.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. "CSS-First" Mandate
**MANDATORY**: Use the v4 theme engine. Define all design tokens (colors, spacing) in `index.css` via CSS variables rather than JavaScript configuration.

### 2. Utility Taxonomy
**MANDATORY**: Group utility classes logically: `[Layout] [Box Model] [Typography] [Visuals] [Interactive]`. Prohibit chaotic or un-ordered strings.

### 3. Container-First Responsiveness
**MANDATORY**: Prioritize `@container` queries for modular components to ensure local layout stability across different viewports.

### 4. Accessibility Threshold (AA)
All styling must maintain a minimum 4.5:1 contrast ratio. Visible focus states are a blocking requirement for any interactive element.

---
"Identity is define by tokens. Speed is enabled by utilities. Build the Sovereign UI."
