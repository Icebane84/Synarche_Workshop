# AOP: Mobile Design & Tactical Implementation [v15.0]

## 🧠 THE MOBILE CORE (ANTI-SAFE-HARBOR)
**STOP. Before writing a single line of mobile code, you MUST scan the project context. The "AI Safe Harbor" (defaulting to tab bars, Redux, and FlatList without thinking) is FORBIDDEN.**

### 🔍 MANDATORY CONTEXT SCAN
1. **Project Type**: E-Commerce? Social? SaaS? Utility? Media? (Each has a different navigation DNA).
2. **Platform Target**: iOS-First? Android-First? Cross-Platform? (Respect the specific platform conventions).
3. **Connectivity**: Offline-First? (Mandates caching/sync strategy).
4. **Hardware**: Low-end support? (Mandates extreme memory management).

---

## 🎨 TACTILE GOVERNANCE (THUMB PSYCHOLOGY)

### 📐 Fitts' Law for Touch
- **Minimum Target**: **44pt** (iOS) / **48dp** (Android) / **44px** (WCAG).
- **Target Spacing**: **8pt/dp** minimum between adjacent interactive elements.
- **Visual vs. Hit Area**: Element icons can be 24px, but the **Touch Area** must be extended to 44-48px using padding.

### 🤳 The Thumb Zone Map
- **EASY (Bottom Center/Right)**: Primary CTAs, Tab Bars, FABs.
- **OK (Middle)**: Content, secondary actions.
- **HARD (Top/Stretch)**: Navigation, Settings, Destructive actions (Safe-by-hard-reach).

---

## 🚀 PERFORMANCE MANDATE (THE 16.67ms BUDGET)
**Frame drops are failures. A janky app is a broken app.**

### 📋 List Optimization (MANDATORY)
| ❌ NEVER DO THIS | ✅ ALWAYS DO THIS |
| :--- | :--- |
| `ScrollView` with items.map() | `FlatList` (RN) or `ListView.builder` (Flutter). |
| Using `index` as key. | Using stable `item.id`. |
| Re-creating `renderItem` every render. | Using `useCallback` + `React.memo`. |
| Massive image components in items. | Image caching + Resizing (2-3x retina max). |

### 🎞️ Animation Governance
- **React Native**: Always use `useNativeDriver: true` for transform/opacity. For complex logic, use **Reanimated 3**.
- **Flutter**: Use `const` constructors everywhere. Avoid `Opacity` widget; use `FadeTransition`.
- **Target**: 60 FPS minimum; 120 FPS for ProMotion devices.

---

## 📱 PLATFORM DIFFERENTIATION

### 🍏 iOS (HIG)
- **Navigation**: Tab bar (3-5 items), Edge-swipe back is MANDATORY.
- **Typography**: SF Pro. Support **Dynamic Type** (MANDATORY).
- **Haptics**: Use `selection`, `impact`, and `notification` variants for a premium feel.
- **Layout**: Safe Area Insets (status bar, home indicator) must be respected.

### 🤖 Android (Material 3)
- **Navigation**: Bottom nav (3-5 items) or Navigation Rail (Tablets).
- **Typography**: Roboto. Use **sp** for text, **dp** for layout.
- **Haptics**: Every touchable element needs a **Ripple Effect** (12% opacity).
- **Layout**: 8dp baseline grid. Support **Dynamic Color** (Material You).

---

## 🚦 DECISION TREES

### Navigation Selection
- **3-5 destinations?** → Bottom Tab Bar.
- **6+ destinations?** → Drawer or "More" menu hybrid.
- **Deep hierarchical drill-down?** → Stack Navigation.
- **Tablet support?** → Navigation Rail.

### State Selection (React Native)
- **Simple page state?** → Local `useState`.
- **Modest shared state?** → `Zustand` or `Jotai`.
- **Server state/Caching?** → `TanStack Query`.
- **Complex enterprise logic?** → `Redux` (only if requested).

---

## 🧪 DECOMPOSITION PROTOCOL (PRE-WORK)
**Before designing any mobile screen, perform this analysis:**
```
SCREEN: [Screen Name]
├── PRIMARY ACTION: [Main Action → Thumb Zone Check]
├── TOUCH TARGETS: [44-48px Audit]
├── LIST LOGIC: [Virtualization Strategy]
├── STATE: [Local/Global/Server Choice]
├── PLATFORM: [iOS vs Android Convention Check]
└── PERFORMANCE: [Any heavy components? Memoization?]
```

---
> 🔴 **Remember:** Passing the checklist is NOT enough. Creating a tactile, responsive, and platform-compliant experience is the only path to OMEGA validation.
