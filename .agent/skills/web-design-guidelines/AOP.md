# AOP: Web Design Playbook [v15.0]

## 🏗️ UI ARCHITECTURE & ACCESSIBILITY
**User-First Design is a Structural Property.**

### 🚦 Accessibility (A11y) [CRITICAL]
- **Contrast**: Minimum 4.5:1 ratio for standard text (WCAG AA). 7:1 for enhanced (WCAG AAA).
- **Semantics**: Use appropriate HTML5 elements (`<article>`, `<aside>`, `<mark>`).
- **Interaction**: Every interactive element MUST be keyboard-navigable and have a visible focus state.
- **Form Labels**: Every `<input>` MUST have a corresponding `<label>` or `aria-label`.

### 🚦 Responsive & Fluid [CRITICAL]
- **Mobile First**: Design for small screens first. Use `@media (min-width: ...)` for expansion.
- **Touch Targets**: Minimum 44x44px for touch-interactive elements.
- **Fluid Layouts**: Use `clamp()`, `rem`, and `%` for sizing. Avoid fixed `px` for layout containers.
- **Overflow**: Ensure no horizontal scrolling on mobile (max-width: 100%).

### 🛡️ TYPOGRAPHY & SPACING [HIGH]
- **Font Scale**: Use a logical font scale (e.g., 1.25 Modular Scale).
- **Line Height**: Minimum 1.5 for body text to ensure readability.
- **Consistency**: Maintain a consistent spacing system (e.g., multiples of 4px or 8px).

---

## 🏰 DECOMPOSITION PROTOCOL (DESIGN PRE-WORK)
**Before starting any UI implementation, perform this scan:**
```
UI/TASK: [Task Name]
├── CONTRAST: [Meet WCAG AA 4.5:1?] (Visual check)
├── MOBILE: [44px touch targets?] (Interaction check)
├── LAYOUT: [Fluid clamp / rem used?] (Responsive check)
└── A11Y: [Aria-labels & Focus states?] (Inclusive check)
```

---

## 📜 COLOR SYSTEM (MANDATORY)
1. **Primary**: High-saturation for action.
2. **Surface**: Neutral for background.
3. **Status**: Red/Amber/Green for feedback.
4. **Contrast Overlay**: Always check on-dark vs on-light visibility.

---
**Protocol**: "Design is the identity of the Sovereign. Contrast is the clarity of the truth."
