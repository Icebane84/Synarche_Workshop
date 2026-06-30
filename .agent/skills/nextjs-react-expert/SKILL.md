---
name: react-best-practices
description:
    React and Next.js performance optimization from Vercel Engineering. Use when building React components, optimizing
    performance, eliminating waterfalls, reducing bundle size, reviewing code for performance issues, or implementing
    server-side optimizations.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js & React Performance System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Vercel-Grade Performance**, **Waterfall Elimination**, and **Bundle Hygiene** across the React ecosystem. This skill prevents the use of barrel imports, sequential data-fetching, and unprotected server actions. It mandates modern (Next.js 16+) component-level caching.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Performance Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🛠️ Validation Scripts
- `scripts/react_performance_checker.py` - Automated Performance Audit. Usage: `python scripts/react_performance_checker.py <project_path>`.

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. Waterfall Elimination Mandate
**PROHIBITED**: Sequential `await` calls in React Server Components or API routes unless data is co-dependent. Mandate `Promise.all` or parallel component composition.

### 2. Barrel Import Avoidance
**PROHIBITED**: Importing from "barrel" (`index.ts`) files in app code. Mandate direct imports or `optimizePackageImports` in `config/`.

### 3. Server Action Security
Every `"use server"` function **MUST** verify authentication and authorization *locally*. No reliance on page-level guards.

### 4. Caching & PPR [Next.js 16+]
Leverage `use cache`, `cacheLife`, and `cacheTag` for granular component-level control. Partial Pre-Rendering (PPR) is the expected standard.

---
"Performance is a debt. Pay it early, or the users will pay for it later."
