---
id: SKILL-I18-001
name: i18n & Localization
version: v2.1 [GOLD]
type: SYSTEM_PRINCIPLES
status: [ACTIVE]
tags: ['#I18N', '#L10N', '#SOVEREIGN']
---

# 🌐 i18n & LOCALIZATION | SKILL-I18-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Engineering.i18n     |
| **State**      | ⚡ ACTIVE                 |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC PRINCIPLES

### 1. The i18n Standard

All user-facing strings must be **Abstracted** into translation keys. No raw text is allowed in components or logic.

- **Internationalization (i18n)**: Making the application codebase translatable.
- **Localization (L10n)**: Providing target-specific translations (locale files).
- **RTL (Right-to-Left)**: Core support for Arabic, Hebrew, etc., using logical CSS.

### 2. Formatting & Pluralization

Always use the **Intl API** for regional formatting.

- **Dates**: `Intl.DateTimeFormat(locale).format(date)`.
- **Numbers**: `Intl.NumberFormat(locale).format(number)`.
- **Plurals**: Use ICU Message Format to handle complex plurality rules (especially in Slavic/Arabic languages).

---

## 🔍 GATEWAY NAVIGATION PROTOCOL (GNP)

Navigate the i18n system using these canonical files:

| File                 | Status          | Context                             |
| :------------------- | :-------------- | :---------------------------------- |
| [INDEX.md](INDEX.md) | 🔴 **REQUIRED** | Gateway for the cluster.            |
| [AOP.md](AOP.md)     | 🔴 **REQUIRED** | Operational Playbook (RTL/Logical). |
| [GUCA.md](GUCA.md)   | ⚪ Optional     | Command Registry (Scripts/Audit).   |
| [SELT.md](SELT.md)   | ⚪ Optional     | Experience Log (Gold Standard).     |

---

## ⚡ ACTIONABLE HEURISTICS

- **[LOGICAL_CSS]**: Use `margin-inline-start` instead of `margin-left`.
- **[KEY_NAMESPACING]**: Group keys by domain (e.g., `common:cancel`, `auth:login`).
- **[ZERO_HARDCODING]**: Run `geo-audit --hardcoded` before every merge.

---

`[OMNI-ARTIFACT-ANCHOR] ID: SKILL-I18-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
