# Phoenix HUD — Supabase Backend Control Center

**Scope**: Full-replacement UI — specialized Supabase admin HUD with Realtime

---

## Goal

Build a production-quality personal backend HUD for the Synarche Supabase instance. Full read/write control over all 19
tables, live Realtime streaming, two-user context (Chris / Axion), and a Pro-Max dark command-center aesthetic.

---

## Design: AI-Native × HUD / Sci-Fi FUI (STT-43 × STT-51)

- **Palette**: Deep black `#000000` base, celestial blue `#77B5FE` primary accent, amber `#F59E0B` for Chris context,
  indigo `#6366F1` for Axion context
- **Motion**: Streaming data tickers, pulse-on-insert, slide-in panels, 200–300ms ease-out
- **Layout**: Fixed left nav sidebar + main content area + live activity rail (right)
- **No**: glassmorphism as hero, mesh gradients, purple backgrounds, scanlines as wallpaper

---

## Architecture

```
phoenix-rosetta-stone/src/
├── core/
│   ├── supabase.ts          ← re-export @synarche/supabase
│   ├── useUserContext.ts    ← Chris/Axion switcher (Zustand)
│   └── hooks/
│       ├── useRealtime.ts   ← generic Supabase Realtime hook
│       ├── usePlayerState.ts
│       ├── useMemoryFeed.ts
│       ├── useActionLog.ts
│       └── useNotifications.ts
├── components/
│   ├── layout/
│   │   ├── AppShell.tsx     ← root layout (sidebar + main + rail)
│   │   ├── Sidebar.tsx      ← icon nav with active state
│   │   ├── UserSwitcher.tsx ← Chris ↔ Axion pill toggle
│   │   └── ActivityRail.tsx ← live action_log ticker (right)
│   ├── views/
│   │   ├── Dashboard/       ← Overview: live KPIs, system status
│   │   ├── MemoryPalace/    ← memory_entries CRUD + vector search
│   │   ├── RPGCommand/      ← player_state, rpg_stats, stardust, achievements
│   │   ├── KnowledgeForge/  ← knowledge_base CRUD
│   │   ├── Chronicle/       ← conversation_history + episodes
│   │   └── Notifications/   ← notifications feed + mark-read
│   └── ui/
│       ├── DataTable.tsx    ← reusable sortable/filterable table
│       ├── StatBar.tsx      ← animated RPG stat bar
│       ├── LivePill.tsx     ← animated domain/state pill
│       └── Toast.tsx        ← achievement/notification toast
└── App.tsx                  ← Router + AppShell
```

---

## Phases

### Phase 1 — Foundation (Tokens + Layout + Router)

- [ ] `index.css` — design token CSS vars (elevations, motion, type scale)
- [ ] `App.tsx` — React Router with 6 routes
- [ ] `AppShell.tsx` — sidebar + main + rail grid
- [ ] `Sidebar.tsx` — icon nav (Dashboard/Memory/RPG/Knowledge/Chronicle/Notifs)
- [ ] `UserSwitcher.tsx` — Chris ↔ Axion toggle with color context
- [ ] `useUserContext.ts` — Zustand store for active user_id

### Phase 2 — Data Layer (Hooks + Realtime)

- [ ] `core/supabase.ts` — phoenix-scoped re-export
- [ ] `useRealtime.ts` — generic hook: `useRealtime(table, event, callback)`
- [ ] `usePlayerState.ts` — fetch + Realtime on `rpg_stats`
- [ ] `useMemoryFeed.ts` — paginated `memory_entries` + INSERT subscription
- [ ] `useActionLog.ts` — live streaming `axiom_action_log`
- [ ] `useNotifications.ts` — `notifications` with unread count badge

### Phase 3 — Dashboard View

- [ ] KPI cards: XP, Level, Stardust, Coherence Index (live from rpg_stats)
- [ ] System status indicator: last action_log entry + timestamp
- [ ] Recent memories strip: last 5 `memory_entries`
- [ ] Active notifications badge

### Phase 4 — Memory Palace View

- [ ] Sortable table: `memory_entries` (domain, state, layer, activation_score)
- [ ] Filter bar: domain dropdown, state filter, layer filter, text search
- [ ] Row actions: Edit content, Archive (state→Archived), Delete
- [ ] Insert panel: add new memory with domain/layer/content
- [ ] Live highlight: new rows flash on Realtime INSERT

### Phase 5 — RPG Command View

- [ ] `player_state` card: XP progress bar, Level, Prestige score
- [ ] `rpg_stats` radar: 7 stats as animated bars + numeric
- [ ] Stardust ledger table: `stardust_ledger` with EARNED/SPENT filter
- [ ] Achievements grid: earned vs locked, stardust/XP rewards shown
- [ ] Quick actions: +XP, +Stardust, grant achievement

### Phase 6 — Knowledge Forge View

- [ ] Searchable `knowledge_base` table with metadata preview
- [ ] Inline edit: click row → edit content/metadata
- [ ] Insert: title + content + metadata JSON editor
- [ ] History panel: `knowledge_history` for selected entry

### Phase 7 — Chronicle + Notifications

- [ ] `conversation_history`: grouped by session_id, sender color-coded
- [ ] `episodes`: phase badge, memory_count, coherence_delta
- [ ] Notifications: unread feed, mark-as-read, link to discovered_insights

### Phase 8 — Activity Rail + Polish

- [ ] `ActivityRail.tsx`: live stream of `axiom_action_log` entries
- [ ] `Toast.tsx`: fires on new achievement / notification via Realtime
- [ ] `prefers-reduced-motion` pass on all animations
- [ ] Keyboard navigation on all interactive elements

---

## Done When

- [ ] All 6 views render with live Supabase data
- [ ] Realtime subscriptions active (rpg_stats, memory_entries, action_log, notifications)
- [ ] Chris ↔ Axion switcher changes data context throughout
- [ ] CRUD operations work (create, edit, delete) on memory_entries + knowledge_base
- [ ] `npm run typecheck` → 0 errors
- [ ] No hardcoded values — all data from Supabase
