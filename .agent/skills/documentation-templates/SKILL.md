---
id: UMB-DOC-001
name: Documentation Templates & Standards
version: v2.1 [GOLD]
type: SKILL_LOGIC
status: [ACTIVE]
tags: ['#DOCUMENTATION', '#TEMPLATES', '#STANDARDS', '#SOVEREIGN']
---

# 🧠 DOCUMENTATION | UMB-DOC-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Doc.Templates        |
| **State**      | 🌟 GOLD STANDARD          |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V2.0-SOVEREIGN]          |

---

## 🎭 SOVEREIGN LOGIC

Documentation is the bridge of coherence between developers, users, and AI agents. We prioritize scannability, clear
hierarchy, and machine-readability over verbose, long-form explanations.

### Principles of Structural Clarity

1.  **Scannability First**: Use headers (H1-H3), bullet points, and tables to make information digestible at a glance.
2.  **Examples over Theory**: Show, don't just tell. Every template must include a baseline implementation example.
3.  **Progressive Disclosure**: Start with a summary/one-liner. Provide deeper technical details in nested sections or
    separate files.
4.  **Machine-Readability**: Format data structures, API contracts, and decision records (ADRs) to be easily parsed by
    AI agents (e.g., using explicit YAML frontmatter or JSON blocks).

---

## 🛠️ BLUEPRINT STANDARDS

### Template Hierarchy

- **[README]**: Title, Quick Start (<5 min), Features, Configuration, API Reference, License.
- **[API_REF]**: Endpoint, Description, Parameters, Response (200/4xx), Example.
- **[ADR]**: Status, Context, Decision, Consequences (Trade-offs).
- **[CODE]**: JSDoc/TSDoc for public APIs. Focus on "Why" (Business Logic) over "What" (Obvious code).

---

## 🔍 QUALITY CONSTRAINTS

- **[NO_TUTORIALS]**: Templates are starting points. Avoid conversational text that clutters the technical intent.
- **[NO_STALE_DOCS]**: Outdated documentation is a critical risk. If code changes, the documentation must be updated in
  the same task.

---

`[OMNI-ARTIFACT-ANCHOR] ID: UMB-DOC-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
