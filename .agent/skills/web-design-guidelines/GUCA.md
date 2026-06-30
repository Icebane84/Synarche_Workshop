# GUCA: Design Command Registry [v15.0]

## 🛠️ Visual & Interaction Audit Commands

### 🔍 Accessibility (A11y)
- `/audit_a11y_contrast` - Scan for WCAG 2.1 AA/AAA contrast failure.
  - **Automation**: `npx axe-core-cli <url>`
- `/check_aria_labels` - Verify presence of labels on all interactive elements.
- `/verify_focus_states` - Test keyboard navigation and focus visibility.

### ⚡ Responsive & Layout
- `/check_mobile_targets` - Identify touch targets < 44x44px.
- `/verify_fluid_typography` - Scan for `px` usage in font-size vs `rem/clamp`.
  - **Automation**: `python scripts/design_checker.py <dir>`
- `/check_overflow_mobile` - Verify no horizontal scrolling on 320px width.

### 🛡️ Typography & Spacing
- `/audit_font_hierarchy` - Verify logical font scale and line-height.
- `/check_spacing_consistency` - Identify "magic numbers" vs 8px grid system.

### 🚀 Reporting
- `/generate_design_report` - Auto-generation of UI/UX consistency score.
- `/audit_visual_regression` - Compare current UI vs canonical mockups.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: Design audit commands must be executed within the UI context. Visual Excellence is a blocking requirement for any Frontend-ready branch.
