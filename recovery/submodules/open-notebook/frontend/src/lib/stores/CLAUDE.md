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

# Stores Module

Zustand-based state management for authentication, modals, and application-level settings with localStorage persistence.

## Key Components

- **`auth-store.ts`**: Authentication state (token, isAuthenticated) with login, logout, auth checking, and Zustand persistence
- **Modal stores** (imported via hooks): Modal visibility and data state management
- **Settings persistence**: Auto-saves sensitive state (token, auth status) to localStorage via Zustand persist middleware

## Important Patterns

- **Zustand create + persist**: State + actions combined in single store; `persist` middleware auto-syncs to localStorage
- **Selective persistence**: `partialize` option limits what's saved (e.g., only `token` and `isAuthenticated`, not `isLoading`)
- **Hydration tracking**: `setHasHydrated()` marks when localStorage data loaded; used to avoid hydration mismatch in SSR
- **Auth caching**: 30-second cache on `checkAuth()` to avoid excessive API calls; stores `lastAuthCheck` timestamp
- **Network resilience**: Handles 401 globally in API interceptor; graceful degradation if API unreachable
- **API validation**: Uses actual API call (`/notebooks` endpoint) to validate token instead of parsing JWT

## Key Dependencies

- `zustand`: State management library
- `@/lib/config`: `getApiUrl()` for dynamic server discovery
- localStorage: Browser persistence API

## How to Add New Stores

1. Create new file (e.g., `settings-store.ts`)
2. Define interface extending store state and actions
3. Use `create<Interface>()(persist(...))`  for persistence, or plain `create<Interface>()` for ephemeral state:
   ```typescript
   export const useSettingsStore = create<SettingsState>()(
     persist((set) => ({
       theme: 'dark',
       setTheme: (theme) => set({ theme })
     }), {
       name: 'settings-storage'
     })
   )
   ```

## Important Quirks & Gotchas

- **Hydration mismatch**: Server-side rendered stores must check `hasHydrated` before rendering to prevent SSR mismatches
- **localStorage key collision**: Persist middleware uses `name` option as localStorage key; ensure unique per store
- **Token not validated**: `login()` only checks HTTP 200 response; doesn't decode or validate JWT structure
- **Auth check race condition**: Multiple simultaneous `checkAuth()` calls return early if one already in progress (`isCheckingAuth`)
- **Error messages from HTTP**: Shows 401/403/5xx status codes to user; helps with debugging but may leak info
- **Network timeout handling**: Network errors in `checkAuthRequired()` set `authRequired: null` (safe default); `login()` shows generic message
- **Logout doesn't invalidate session**: Client-side logout only clears local token; server session may still be valid
- **Double authentication**: Both `login()` and `checkAuth()` test same `/notebooks` endpoint; could be optimized with dedicated endpoint

## Testing Patterns

```typescript
// Mock store
const mockAuthStore = {
  isAuthenticated: true,
  token: 'test-token',
  checkAuth: vi.fn().mockResolvedValue(true),
  login: vi.fn().mockResolvedValue(true),
  logout: vi.fn()
}

// Test store mutations
act(() => store.setState({ theme: 'light' }))
expect(store.getState().theme).toBe('light')
```

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
