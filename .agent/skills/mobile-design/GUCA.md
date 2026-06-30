# GUCA: Mobile Design Command Registry [v15.0]

## 🛠️ Audit Commands

### 🔍 UI/UX Compliance
- `/audit_mobile_ui` - Perform full UI/UX scan for touch target size and thumb zone compliance.
- `/check_platform_conventions` - Verify HIG (iOS) vs Material 3 (Android) adherence.
- `/validate_accessibility` - Check Dynamic Type, VoiceOver, and TalkBack semantics.

### 🚀 Performance Guardrails
- `/audit_list_performance` - Verify FlatList/ListView.builder/FlashList implementation.
- `/check_animation_fps` - Analyze animation logic for native driver support.
- `/monitor_memory` - Check for common mobile memory leak patterns (timers, listeners).

### 📐 Tactile Synthesis
- `/decompose_screen` - Run the mandatory Component Decomposition Protocol for a specific screen.
- `/verify_haptics` - Audit haptic feedback patterns for consistency and intensity.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: These commands are to be executed as part of the **Pre-Work Validation** or **In-Depth Audit** phases of any mobile-related ticket. Use with the **AOP.md** playbook as authority.
