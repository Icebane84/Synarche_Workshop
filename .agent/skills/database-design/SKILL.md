---
id: UMB-DAT-001
name: Database Design & Architecture
version: v2.1 [GOLD]
type: SKILL_LOGIC
status: [ACTIVE]
tags: ['#DATABASE', '#SCHEMA', '#DATA_MODELING', '#SOVEREIGN']
---

# 🧠 DATABASE DESIGN | UMB-DAT-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Data.Design          |
| **State**      | 🌟 GOLD STANDARD          |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V2.0-SOVEREIGN]          |

---

## 🎭 SOVEREIGN LOGIC

Database design is the foundation of application integrity and performance. We prioritize relational correctness (Normalization), efficient retrieval (Indexing), and safe schema evolution (Migrations) over ad-hoc data storage.

### Principles of Data Architecture

1.  **Normalization over Denormalization**: Separate tables for repeated data to ensure update consistency, unless read performance is a proven bottleneck.
2.  **Primary Key Strategy**: Use UUID/ULID for distributed systems and security, and auto-increment for simple, local datasets.
3.  **Temporal Awareness**: Every table must include `created_at` and `updated_at` (using `TIMESTAMPTZ`).
4.  **Referential Integrity**: Always use Foreign Keys with explicit `ON DELETE` behavior (CASCADE, SET NULL, RESTRICT).

---

## 🛠️ BLUEPRINT STANDARDS

### Relationship Heuristics

- **[1:1]**: One-to-One. Use for extension data. Separate table with a shared Primary Key.
- **[1:N]**: One-to-Many. The child table must hold the Foreign Key of the parent.
- **[M:N]**: Many-to-Many. Requires a Junction Table (Associative Table) to link both entities.

---

## 🔍 QUALITY CONSTRAINTS

- **[NO_GHOST_SCHEMAS]**: Never suggest a schema without defining Primary Keys and Foreign Key constraints.
- **[NO_SELECT_STAR]**: Avoid `SELECT *` in production code. Explicitly list required columns.
- **[INDEX_STRATEGY]**: Every table must have an indexing strategy defined in the schema design.

---

`[OMNI-ARTIFACT-ANCHOR] ID: UMB-DAT-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
