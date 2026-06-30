# AOP: Next.js & React Performance Playbook [v15.0]

## 🛠️ THE PERFORMANCE HIERARCHY
**DO NOT micro-optimize until you have eliminated waterfalls and bloat.**

### 🚦 Waterfall Elimination [CRITICAL]
- **Defer Await**: Only `await` when the data is strictly necessary for the next line.
- **Parallel Independent**: Use `Promise.all([fetch1(), fetch2()])` for non-dependent data.
- **Dependency Chains**: Use `better-all` or start promises early: `const a = fetchA(); const b = a.then(fetchB); await Promise.all([a, b])`.
- **Composition Parallelism**: Move fetches into sub-components. Components in the same row/layout fetch simultaneously.
- **Next.js 16 `after()`**: Use for non-UI logic (logging, analytics) to prevent response blocking.

---

## 📦 BUNDLE & CLIENT OPTIMIZATION [CRITICAL]

### 🛡️ The Barrel Protocol
- **PROHIBITED**: Importing from "barrel" index files (e.g., `import { X } from 'lucide-react'`).
- **MANDATORY**: Direct imports (`import X from 'lucide-react/icons/x'`) or `optimizePackageImports` in `next.config.js`.

### 🗜️ Code Splitting
- **`next/dynamic`**: Use for ALL components > 20KB or those below the fold (editors, charts, maps).
- **Conditional Loading**: Wrap client-only heavy modules in `typeof window !== 'undefined'` checks.

---

## 🖥️ SERVER COMPONENTS & ACTIONS [HIGH]

### 🏰 Server Governance
- **Boundary Serialization**: Minimize props passed across the RSC boundary. Pass `userId` instead of the whole `user` object.
- **Action Security**: **Authenticate and Authorize** inside the `"use server"` function itself. It is a public API endpoint.
- **Deduplication**: Use `React.cache()` for DB/Auth work inside a single request.

---

## 🚀 CACHING & NEXT.JS 16+ [CRITICAL]

### ⚖️ Component-Level Caching
- **`use cache`**: Apply to granular functions or components. No more segment-level `revalidate`.
- **`cacheLife`**: Choose your profile: `seconds`, `minutes`, `hours`, `days`, `weeks`, `max`.
- **`cacheTag`**: Label your data for selective purging (`revalidateTag`).

### ⚡ Partial Pre-Rendering (PPR)
- **MANDATORY**: Wrap dynamic cache components in `<Suspense>` boundaries. Static shells must render immediately while dynamic chunks stream.

---

## 🧪 DECOMPOSITION PROTOCOL (PRE-WORK)
**Before starting any React/Next.js implementation, perform this analysis:**
```
UI TASK: [Task Name]
├── WATERFALLS: [Sequential await check]
├── BUNDLE: [Dynamic import / Barrel check]
├── RSC: [Serialization / Security check]
├── CACHING: [use cache / cacheLife choice]
├── HYDRATION: [ssr: false / skeleton choice]
└── RE-RENDERS: [Memoization / Hook check]
```

---
> 🔴 **Remember:** Performance is not a feature; it is a structural property. Eliminate waterfalls, then ship less JS, then cache.
