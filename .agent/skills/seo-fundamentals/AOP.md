# AOP: SEO & Semantic Playbook [v15.0]

## 🏗️ SEMANTIC ARCHITECTURE
**Structure Defines Authority.**

### 🚦 Heading Hierarchy [CRITICAL]
- **Single H1**: Every page MUST have exactly one `<h1>` containing the primary keyword/context.
- **Logical Flow**: Use `<h2>` for major sections, `<h3>` for subsections. Do NOT skip levels for styling.
- **Main Landmark**: Wrap main content in `<main id="main-content">` to facilitate accessibility and crawling.

### 🚦 Meta & Social [CRITICAL]
- **Uniqueness**: Every route MUST have a unique `<title>` (under 60 chars) and `<meta description>` (under 160 chars).
- **Open Graph**: Mandate `og:title`, `og:description`, `og:image`, and `og:type` for all social previews.
- **Canonical Tags**: ALWAYS include `<link rel="canonical" href="...">` to prevent duplicate content indexing.

### 🛡️ CORE WEB VITALS [HIGH]
- **LCP (Largest Contentful Paint)**: Prioritize "Above the Fold" images using `preloading` or `priority` in Next.js/Vite.
- **CLS (Cumulative Layout Shift)**: Set explicit `width` and `height` for images/vids. Avoid dynamic layout injection without skeletons.
- **FID/INP**: Keep JS execution under 100ms for interaction-heavy components.

---

## 🏰 DECOMPOSITION PROTOCOL (SEO PRE-WORK)
**Before starting any UI/Page implementation, perform this scan:**
```
UI/TASK: [Task Name]
├── TITLES: [Unique title & meta description?] (Auth check)
├── HEADINGS: [H1-H3 hierarchy check?] (Semantic check)
├── IMAGES: [Alt text & dimensions?] (Accessibility check)
└── VITALS: [LCP/CLS check?] (Performance check)
```

---

## 📜 DATA STRUCTURE (JSON-LD)
Mandate schema-org JSON-LD for:
1. `Organization` / `SoftwareApplication` / `Product`.
2. `BreadcrumbList`.
3. `FAQPage` (if applicable).

---
**Protocol**: "Semantics first. Styling second. Visibility always."
