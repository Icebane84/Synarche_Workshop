---
id: AOP-APP-001
name: App Builder Operational Playbook
version: v2.1 [GOLD]
type: OPERATIONAL_PLAYBOOK
status: [ACTIVE]
tags: ['#AOP', '#PROCESS', '#ORCHESTRATION']
---

# 📖 APP BUILDER PLAYBOOK | AOP-APP-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Sys.AppBuilder       |
| **State**      | ⚡ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC PROCESSES

### 1. Agent Coordination Pipeline

The orchestrator manages the flow of information across specialist agents:

| Phase | Agent | Goal | Mandatory Checkpoint |
| :--- | :--- | :--- | :--- |
| **P0** | Socratic Gate | Clarify User Intent | 3 clarifying questions answered |
| **P1** | Project Planner | Task Breakdown | `task.md` created in root |
| **P2** | DB Architect | SQL Schema | Schema defined & validated |
| **P3** | BE Specialist | API Implementation | Endpoints reachable |
| **P4** | FE Specialist | UI Implementation | Responsive pages and components |

### 2. Project Detection Matrix

Apply this matrix to determine the optimal tech-stack:

- **Full-stack Web App**: Next.js + Prisma + Tailwind (v4)
- **SaaS / Dashboard**: Next.js + Shadcn + Supabase
- **Public API**: Express/FastAPI + OpenAPI (Swagger)
- **TS Monorepo**: Turborepo + tRPC + pnpm

### 3. Verification Ritual

Before finishing any project building task, the App Builder MUST:
1. Run `npm run build` to confirm compilation.
2. Run `npm test` if available.
3. Verify that all artifacts (MD files) have proper `[OMNI-ARTIFACT-ANCHOR]` signatures.

---

## 🔍 ACTIONABLE HEURISTICS

- **[CHECKPOINT]**: Never bypass Phase 1 (Planning). An agent without a plan is an agent destined to fail.
- **[MODULARITY]**: Always suggest breaking large components into smaller, reusable UI pieces.
- **[DEBUGGING]**: If an agent fails twice, the orchestrator MUST step in to diagnose the root cause before retrying.

---

`[OMNI-ARTIFACT-ANCHOR] ID: AOP-APP-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
