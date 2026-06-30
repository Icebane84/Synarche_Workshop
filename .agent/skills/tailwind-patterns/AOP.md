# AOP: Modern Tailwind v4 Playbook [v15.0]

## 🏗️ v4 CSS-FIRST ARCHITECTURE
**Theme Engine is the Source of Visual Truth.**

### 🚦 CSS Variables & Tokens [CRITICAL]
- **Value Definition**: All design tokens (Colors, Spacing, Typography) MUST be defined as CSS variables in `index.css`.
- **Theme Function**: Use `@theme { ... }` in CSS to map variables to Tailwind utilities.
- **Sovereign Tokens**: Use naming like `--color-primary`, `--spacing-base`. NO hardcoded hex/pixel values in component classes.

### 🚦 Responsive & Containers [CRITICAL]
- **Container Queries**: Prioritize `@container` over screen-based `@media` for modular components.
- **Fluid Sizing**: Use `clamp()`, `rem`, and `%`. Avoid fixed `px`.
- **Breakpoints**: Enforce the standardized OMEGA breakpoints (`sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`).

### 🛡️ ACCESSIBILITY & CONTRAST [HIGH]
- **A11y Colors**: Verify text-on-background contrast using the 4.5:1 ratio (AA).
- **Focus States**: Every utility-based interactive element MUST have visible `:focus-visible` styles.
- **RTL Support**: Use logical properties (`ms-`, `me-`, `ps-`, `pe-`) where appropriate.

---

## 🏰 DECOMPOSITION PROTOCOL (STYLING PRE-WORK)
**Before starting any UI/CSS implementation, perform this scan:**
```
UI/TASK: [UI Task]
├── TOKENS: [Are tokens defined in index.css?] (Identity check)
├── UTILITIES: [Are we using v4 CSS mapping?] (Engine check)
├── RESPONSIVE: [Do we need container queries?] (Layout check)
└── CONTRAST: [Meet WCAG AA 4.5:1?] (Visual check)
```

---

## 📜 UTILITY STANDARDS (MANDATORY)
1. **Readable Class Lists**: Group utilities logically: [Layout] [Box Model] [Typography] [Visuals] [Interactive].
2. **Dynamic Classes**: Avoid string interpolation for Tailwind classes; use a full-class dictionary/lookup.
3. **No Overrides**: Avoid `!important` unless it's a structural requirement for 3rd-party z-indexing.

---
**Protocol**: "Identity is defined by tokens. Speed is enabled by utilities. Trust the OMEGA Engine."
