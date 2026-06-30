---
id: AOP-DAT-001
name: Database Design Operational Playbook
version: v2.1 [GOLD]
type: OPERATIONAL_PLAYBOOK
status: [ACTIVE]
tags: ['#AOP', '#PROCESS', '#DATABASE', '#SCHEMA']
---

# 📖 DATABASE DESIGN PLAYBOOK | AOP-DAT-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Data.Design          |
| **State**      | ⚡ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC PROCESSES

### 1. The Schema Design Ritual (MANDATORY)

Before writing any SQL or ORM code, define the following:

- **Entity Model**: List all tables, primary keys (UUID/ULID preferred), and required columns.
- **Relationship Map**: Define 1:1, 1:N, and M:N links. Specify `ON DELETE` behavior.
- **Index Plan**: Identify columns for filtering, sorting, and joining.
- **Temporal Tracking**: Add `created_at` and `updated_at` (TIMESTAMPTZ).

### 2. Database Selection Matrix (2025)

Choose the optimal database based on context:

| Context | Recommended Database | Key Benefit |
| :--- | :--- | :--- |
| **Full Relational** | PostgreSQL (Neon/Supabase) | Robust features, pgvector |
| **Edge / Low-Latency** | Turso (Edge SQLite) | Near-zero latency |
| **Simple / Local** | SQLite | Embedded, zero-config |
| **Global Scale** | PlanetScale / CockroachDB | Distributed consensus |

### 3. Normalization Heuristics

- **Normalize (L1-L3)**: When data is repeated across rows or updates require multiple changes.
- **Denormalize**: Only when read performance is critical and the data rarely changes (e.g., historical logs).

---

## 🔍 ACTIONABLE HEURISTICS

- **[PROTECTION]**: Always use `EXPLAIN ANALYZE` on complex queries during development.
- **[LIMITS]**: Avoid storing large binary data (BLOBs) in the relational database. Use [Supabase Storage](file:///c:/Users/Chris/_Desktop_Vault/dev/rosetta-stone_-the-phoenix-protocol-(cast)/.agent/skills/app-builder/AOP.md) or S3.
- **[MIGRATIONS]**: Schema changes must be incremental and versioned (e.g., `drizzle-kit` or `prisma migrate`).

---

`[OMNI-ARTIFACT-ANCHOR] ID: AOP-DAT-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
