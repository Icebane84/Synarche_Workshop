---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `CLAUDE` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# CLAUDE.md
> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-02** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

### **Block A: The Identification Lock (UIP-V13)**

| Key | Value | Description |
| :--- | :--- | :--- |
| **Artifact ID** | `GVRN-CLAUDE-001` | The Sovereign ID. |
| **Official Name** | `CLAUDE.md` | The Filename. |
| **Version** | **v13.1 [OMEGA]** | The Standard. |
| **Domain** | `GVRN` | The Subject. |
| **Celestial Class** | `[PLANET]` | The Weight. |
| **Evolution** | `Omega Ascension` | The Maturity. |
| **Status** | `[ACTIVE]` | The Lifecycle. |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001` | The Network. |

# Locales Module (i18n)

Internationalization system providing multi-language UI support using i18next with type-safe translation access.

## Architecture

```
lib/
├── i18n.ts              # i18next initialization and configuration
├── i18n-events.ts       # Language change event emitters
├── hooks/
│   └── use-translation.ts  # Custom hook with Proxy-based API
├── utils/
│   └── date-locale.ts   # date-fns locale mapping
└── locales/
    ├── index.ts         # Locale registry and type exports
    ├── en-US/index.ts   # English translations
    ├── pt-BR/index.ts   # Brazilian Portuguese translations
    ├── zh-CN/index.ts   # Simplified Chinese translations
    ├── zh-TW/index.ts   # Traditional Chinese translations
    └── ja-JP/index.ts   # Japanese translations
```

## Key Components

- **`i18n.ts`**: i18next initialization with language detection (localStorage → browser)
- **`i18n-events.ts`**: Event emitters for language change start/end (used by loading overlay)
- **`locales/index.ts`**: Central registry exporting all locales and `LanguageCode` type
- **`use-translation.ts`**: Custom hook providing `t` object with nested property access

## Translation Structure

Each locale file exports a flat object with nested keys:

```typescript
export const enUS = {
  common: {
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    // ...
  },
  notebooks: {
    title: 'Notebooks',
    createNew: 'Create Notebook',
    // ...
  },
  // ... other sections
}
```

**Sections**:
- `common`: Shared UI elements (buttons, labels, actions)
- `notebooks`, `sources`, `notes`: Feature-specific strings
- `chat`, `search`, `podcasts`: Module-specific strings
- `models`, `transformations`, `settings`: Configuration UI
- `advanced`: System administration strings
- `apiErrors`: Backend error message translations

## Usage Pattern

```typescript
import { useTranslation } from '@/lib/hooks/use-translation'

function MyComponent() {
  const { t, language, setLanguage } = useTranslation()

  // Nested property access (Proxy-based)
  return <h1>{t.notebooks.title}</h1>

  // With interpolation
  return <p>{t.common.updated.replace('{time}', timeAgo)}</p>

  // Change language
  await setLanguage('zh-CN')
}
```

## Important Patterns

- **Proxy-based access**: `t.section.key` instead of `t('section.key')` for better DX
- **Type safety**: `TranslationKeys` type derived from `enUS` locale
- **Language persistence**: Saved to localStorage, auto-detected on load
- **Fallback**: Falls back to `en-US` if key missing in current locale
- **Date localization**: Use `getDateLocale(language)` from `utils/date-locale.ts`

## Key Dependencies

- `i18next`: Core internationalization framework
- `react-i18next`: React bindings for i18next
- `i18next-browser-languagedetector`: Auto-detect browser language
- `date-fns/locale`: Date formatting locales

## How to Add a New Language

1. Create locale folder: `locales/pt-BR/index.ts`
2. Copy structure from `en-US/index.ts` and translate all strings
3. Register in `locales/index.ts`:
   ```typescript
   import { ptBR } from './pt-BR'
   export const resources = {
     // ...existing
     'pt-BR': { translation: ptBR },
   }
   export const languages: Language[] = [
     // ...existing
     { code: 'pt-BR', label: 'Português' },
   ]
   ```
4. Add to `utils/date-locale.ts`:
   ```typescript
   import { ptBR } from 'date-fns/locale'
   const LOCALE_MAP = { ...existing, 'pt-BR': ptBR }
   ```

## Important Quirks & Gotchas

- **Proxy depth limit**: `useTranslation` limits nesting to 4 levels to prevent infinite loops
- **Blocked properties**: React internals (`__proto__`, `$$typeof`, etc.) are blocked from Proxy traversal
- **Loop detection**: Access counts reset every 1s; >1000 accesses triggers error and breaks recursion
- **String methods**: `.replace()`, `.split()` work on translated strings via Proxy magic
- **Language change events**: `emitLanguageChangeStart/End` used by `LanguageLoadingOverlay` for UX
- **No SSR**: `useSuspense: false` disables React Suspense for i18next (avoids hydration issues)
- **All keys required**: Missing keys in non-English locales fall back to English; keep locales in sync

## Testing Patterns

```typescript
// Mock useTranslation in tests (see test/setup.ts)
vi.mock('@/lib/hooks/use-translation', () => ({
  useTranslation: () => ({
    t: enUS,  // Use English locale directly
    language: 'en-US',
    setLanguage: vi.fn(),
  }),
}))

// Test locale completeness
import { enUS, zhCN } from '@/lib/locales'
const enKeys = Object.keys(flatten(enUS))
const zhKeys = Object.keys(flatten(zhCN))
expect(zhKeys).toEqual(enKeys)  // All keys present
```

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
