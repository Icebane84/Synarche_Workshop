# Universal Identification & Provenance (UIP)

## Block A: The Identification Lock (UIP-V15)

---

| Key               | Value                               |
| :---------------- | :---------------------------------- |
| **Artifact ID**   | `GVRN.Style.SovereignStandard`      |
| **Official Name** | `GVRN.Style.SovereignStandard.v15.1.md` |
| **Version**       | **v15.1 [ACTIVE]**                  |
| **Domain**        | `GVRN`                              |
| **Celestial Class** | `[PLANET]`                          |
| **Evolution**     | `Adamant Refactor`                  |
| **Status**        | `[ACTIVE]`                          |
| **Ethos**         | `Crystalline Coherence`             |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix`   |

---

# 🛡️ THE PHOENIX SOVEREIGN CODING STANDARD (v15.1)

> **Ref:** GVRN-RULE-001 | **State:** [ACTIVE] | **Ethos:** Zero Entropy & Crystalline Coherence

This document is the **Supreme Law of the Forge**. It is the single source of truth for all coding and documentation standards within the Synarche, forged from the synthesis of all prior versions (`v13.1`, `v14.0`, `v15.0`). Adherence is mandatory.

---

## I. General Principles

---

### 1.1. The Master Coder Mindset

---

* **CORE Directive:** You do not just write CODE; you execute **Conceptual Engineering**.
* **Analyze Rigorously:** Dissect requests. Identify constraints. Context is King.
* **Promote Testability:** Write modular, decoupled CODE.
* **Enforce Algorithmic Elegance:** Prioritize clarity and simplicity over cleverness.

### 1.2. Cognitive Complexity

---

* **The Mandate:** Keep CODE simple, readable, and linear.
* **Maximum Cognitive Complexity:** A Sonar/Codacy complexity score of `15` is the absolute maximum for any single function.
* **Modularization:** If a function exceeds this logic density, it **must** be shattered into smaller, single-purpose sub-functions.

---

## II. Naming Conventions (RNC-v15)

---

Consistency is the bedrock of a readable system.

| Category                               | Convention     | Example                               | Source    |
| :------------------------------------- | :------------- | :------------------------------------ | :-------- |
| **Files & Folders (CODE/Config)**      | `kebab-case`   | `user-profile.ts`, `auth-service`     | `v14.0`   |
| **Types, Interfaces, Classes, Enums**  | `PascalCase`   | `interface User`, `class ApiService`  | `v14.0`   |
| **Variables, Functions, Methods**      | `camelCase`    | `userName`, `getUserProfile()`        | `v14.0`   |
| **Constants**                          | `UPPER_SNAKE_CASE` | `API_BASE_URL`, `MAX_RETRIES`         | `v14.0`   |
| **Booleans**                           | `is` / `has`   | `isLoggedIn`, `hasPermission`         | `v14.0`   |
| **Governance Artifacts (Markdown)**    | `PascalCase`   | `GVRN.Style.SovereignStandard.v15.1.md` | Synthesis |
| **Sovereign Artifact ID (Metadata)**   | `UPPER.Case`   | `GVRN.STYLE.SOVEREIGNSTANDARD`        | `v15.0`   |

---

## III. Python Standards (The Axion CORE)

---

### 3.1. General

---

* **Type Hints:** **MANDATORY** for all function signatures (`def func(a: int) -> str:`).
* **Modern Types (PEP 585):** For Python 3.9+, always use modern built-in generics (e.g., `list[str]` instead of `List[str]`, `dict[str, int]` instead of `Dict[str, int]`).
* **Docstrings:** Google-style docstrings are required for every public module, class, and function.
* **Error Handling:** Use custom, specific exceptions. Never use a bare `except Exception:`.
* **Dependency Management:** All project dependencies must be managed via `pyproject.toml`.

### 3.2. Versioning

---

* The specific Python version (`3.10`, `3.11`, etc.) shall be managed at the project level (e.g., in `pyproject.toml` or a `.python-version` file), not within this style guide.

---

## IV. TypeScript / Node.js Standards (The Axion Extension)

---

### 4.1. Strictness & Type Safety

---

* **`strict: true`:** This is non-negotiable in all `tsconfig.json` files.
* **Avoid `any`:** The `any` type is forbidden. Use `unknown` and perform type narrowing when a type is truly unknown.
* **Explicit Returns:** Public API functions and methods must have explicit return types.

### 4.2. Project Structure

---

* **Feature-Based:** Organize the codebase around features or domains, not file types.
* **Barrel Exports:** Use `index.ts` files to simplify module imports.

### 4.3. Testing

---

* **Preferred Framework:** `Vitest` is the recommended testing framework for new projects due to its speed and modern API.
* **Legacy:** `Jest` is permissible for maintaining existing legacy TEST suites.

---

## V. SQL Standards (The Data Loom)

---

### 5.1. General

---

* **Readability:** Prioritize clarity and readability over extreme brevity. SQL should be easy to understand at a glance.
* **Explicit Joins:** Always use explicit `JOIN` syntax (`INNER JOIN`, `LEFT JOIN`, etc.) instead of implicit joins in the `FROM` clause.
* **Avoid `SELECT *`:** Explicitly list all columns you need. This improves readability, performance, and prevents unexpected behavior when schema changes.
* **Descriptive Aliases:** Use meaningful aliases for tables and complex expressions.

### 5.2. Naming Conventions

---

* **Tables:** `snake_case`, plural (e.g., `user_profiles`, `order_items`).
* **Columns:** `snake_case`, singular (e.g., `first_name`, `order_date`).
* **Primary Keys:** `id` (or `table_name_id` if multiple primary keys are present in a single query).
* **Foreign Keys:** `related_table_id` (e.g., `user_id` in an `orders` table).
* **Stored Procedures/Functions:** `snake_case`, verb_noun (e.g., `get_user_by_id`, `calculate_total_sales`).

### 5.3. Formatting

---

* **Keywords:** `UPPERCASE` for all SQL keywords (`SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `INSERT`, `UPDATE`, `DELETE`).
* **Identifiers:** `lowercase` for table names, column names, and aliases.
* **Indentation:** Use 4 spaces for indentation.
* **Commas:**
    * Place commas *before* each column in a `SELECT` list (except the first).
    * Place commas *after* each column in an `INSERT` list (except the last).
* **Line Breaks:**
    * Start new clauses on a new line (`FROM`, `WHERE`, `GROUP BY`, `ORDER BY`, `JOIN`).
    * Place each column in a `SELECT` list on its own line if there are more than 3 columns.

**Example:**

```sql
SELECT
    u.id
  , u.first_name
  , u.last_name
  , o.order_date
  , o.total_amount
FROM
    user_profiles AS u
INNER JOIN
    orders AS o ON u.id = o.user_id
WHERE
    o.order_date >= '2026-01-01'
ORDER BY
    o.order_date DESC;
```

---

## V. Documentation & Governance Standards

---

### 5.1. The Chronos Lock (Provenance)

---

* Every new governance or architectural artifact **MUST** possess the "Universal Identification & Provenance" (UIP-V15) header table.

### 5.2. Template Compliance

---

* All UMBs, AOPs, and GUCAs must follow the structure defined in the `UMB-MASTER-TEMPLATE-001`.

---

## VII. Actionable Prompt Packet (APP)

---

| Command ID                | Action                                                                                                                                                             |
| :------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CMD: ADAMANT_ARCHIVE`    | **Execute Phase 3.** Once this new standard is approved, formally deprecate and archive the old style guide files (`GVRN.Style.Coding.md`, `style_guide.md`, `GVRN.Guide.Coding.md`). |
| `CMD: ADAMANT_INTEGRATE`  | **Execute Phase 4.** Update all system configurations and pointers to use this new Sovereign Standard.                                                              |
| `⚡ EXECUTE: ADAMANT_VERIFY` | **Execute Final Verification.** Run the `ide_sentinel.py` script to provide a final report on system coherence post-refactor.                                         |

---

### Block D: Standardized Synergy Block (The Loom Signature)

---

| Synergistic Artifact ID | Relationship Type | Synergistic Impact                                                              |
| :---------------------- | :---------------- | :------------------------------------------------------------------------------ |
| `CORE.Codex.Phoenix`    | `GOVERNS`         | The Codex provides the Supreme Law for this artifact.                           |
| `AOP.GVRN.Refactor.Adamant` | `BIRTHED_BY`      | This standard is the direct result of the Adamant Refactor Dissonance Quest.    |
| `GVRN.Style.Coding.md`  | `SUPERSEDES`      | This artifact replaces and canonizes the rules from all prior style guides.     |

---

## [ARTIFACT END]

---
