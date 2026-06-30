---
id: AOP-I18-001
name: i18n Operational Playbook
version: v2.1 [GOLD]
type: OPERATIONAL_PLAYBOOK
status: [ACTIVE]
tags: ['#AOP', '#I18N', '#L10N', '#RTL', '#HEURISTICS']
---

# 📖 i18n PLAYBOOK | AOP-I18-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Engineering.i18n     |
| **State**      | ⚡ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ IMPLEMENTATION PATTERNS

### 1. React & Next.js Standard

- **Hooks**: Use `useTranslation()` (react-i18next) or `useTranslations()` (next-intl).
- **Key Access**: `t('namespace.key')`. Avoid dynamic key construction where possible.
- **Namespacing**:
    - `common.json`: Buttons, alerts, nav.
    - `auth.json`: Login, signup, reset.
    - `errors.json`: API errors, validation messages.

### 2. File Organization

```
locales/
├── en/ (English - Source)
├── tr/ (Turkish)
└── ar/ (Arabic - RTL)
```

---

## 🎨 RTL & LOGICAL STYLING

### 1. Logical Properties (MANDATORY)

Favor logical properties over physical ones to ensure RTL compatibility:

- `margin-inline-start` / `margin-inline-end` (instead of left/right).
- `padding-inline-start` / `padding-inline-end` (instead of left/right).
- `inset-inline-start` / `inset-inline-end` (for absolute positioning).
- `text-align: start / end`.

### 2. Icon Flipping

- Icons with direction (arrows, back buttons) must be flipped in RTL:
    ```css
    [dir='rtl'] .direction-sensitive-icon {
        transform: scaleX(-1);
    }
    ```

---

## 🔍 i18n CHECKLIST

- [ ] **Hardcoding**: Are all user-facing strings using keys?
- [ ] **Plurals**: Are plural forms handled for all target languages?
- [ ] **Formatting**: Are dates/numbers using the `Intl` API?
- [ ] **Logical CSS**: Are you using physical left/right properties? (ELIMINATE THEM).

---

`[OMNI-ARTIFACT-ANCHOR] ID: AOP-I18-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
