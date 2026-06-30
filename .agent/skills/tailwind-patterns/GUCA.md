# GUCA: Tailwind Command Registry [v15.0]

## 🛠️ Styling & Performance Commands

### 🔍 CSS Analysis
- `/audit_css_size` - Check `index.css` and generated bundle size.
  - **Automation**: `npx tailwind-cli build --content src/**/*; ls -lh dist/*.css`
- `/verify_token_mapping` - Audit class usage against the v4 CSS Variable theme.
- `/check_unused_classes` - Identify potential dead-code utilities.

### ⚡ Build & Theme
- `/run_tailwind_build` - Execute the v4 theme generation engine.
- `/verify_container_queries` - Test layout behavior with `@container`.
- `/check_fluid_typography` - Audit usage of `rem/clamp` vs hardcoded `px`.
  - **Automation**: `python scripts/style_checker.py <dir>`

### 🛡️ Final Verification
- `/audit_visual_consistency` - Compare UI snapshots across breakpoints.
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

### 🚀 Reporting
- `/generate_style_report` - Pass/Fail/Accessibility metrics for the UI.
- `/audit_contrast_failures` - Identify WCAG 2.1 AA/AAA contrast failure.

---
**Usage**: Styling commands must be executed as part of the visual audit loop. No UI is Sovereign without a passing Theme Audit.
