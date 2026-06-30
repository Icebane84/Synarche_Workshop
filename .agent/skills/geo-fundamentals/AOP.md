---
id: AOP-GEO-001
name: GEO Operational Playbook
version: v2.1 [GOLD]
type: OPERATIONAL_PLAYBOOK
status: [ACTIVE]
tags: ['#AOP', '#GEO', '#AI_SEARCH', '#HEURISTICS']
---

# 📖 GEO PLAYBOOK | AOP-GEO-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Engineering.GEO      |
| **State**      | ⚡ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🤖 AI SEARCH HEURISTICS

### 1. Citation Triggers (What to Include)

- **Original Data**: Statistics, case studies, and internal research.
- **Expert Quotes**: Attributed insights from named professionals.
- **Structured Lists**: Comparison tables, step-by-step guides, and TL;DR summaries.
- **Direct Answers**: Clearly defined "What is X?" statements at the top of the content.

### 2. Entity Management

- **Brand Consistency**: Ensure the name, URL, and description are identical across Wikipedia, LinkedIn, and the main
  site.
- **Author E-E-A-T**: Every article must have a bio, social links, and credentials (schema).
- **Knowledge Graph**: Submit site to relevant industry directories to solidify entity nodes.

---

## 🏗️ TECHNICAL IMPLEMENTATION

### 1. Schema Protocol (MANDATORY)

- **Article**: Include `datePublished`, `dateModified`, and `author`.
- **FAQPage**: Use for direct Q&A blocks related to the primary topic.
- **Person**: Define the author as a distinct entity with `jobTitle` and `sameAs`.

### 2. Crawler Configuration

- **Robots.txt**: Explicitly ALLOW `GPTBot`, `Claude-Web`, `PerplexityBot`, and `CCBot`.
- **Performance**: Maintain LCP < 2.5s and CLS < 0.1 to ensure crawlers don't time out.

---

## 🔍 GEO CHECKLIST

- [ ] **TL;DR**: Is there a summary block at the top?
- [ ] **Citation Bait**: Are there at least 3 original stats or expert quotes?
- [ ] **Schema**: Have you verified the `FAQPage` and `Person` schema?
- [ ] **Recency**: Is the "Last Updated" timestamp current?

---

`[OMNI-ARTIFACT-ANCHOR] ID: AOP-GEO-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
