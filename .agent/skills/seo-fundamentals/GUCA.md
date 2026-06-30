# GUCA: SEO Command Registry [v15.0]

## 🛠️ Audit & Validation Commands

### 🔍 Metadata & Structure
- `/simulate_crawl` - Simulated crawl of the project directory.
  - **Automation**: `python scripts/seo_crawler.py <dir>`
- `/check_heading_hierarchy` - Verify single H1 and H2-H4 flow.
- `/verify_meta_tags` - Check for unique titles/descriptions across routes.

### ⚡ Core Web Vitals
- `/audit_cls_shift` - Identify elements without explicit dimensions.
- `/verify_lcp_priority` - Scan for above-the-fold image preloading.
  - **Automation**: `bash scripts/vitals_audit.sh <url>`
- `/check_fid_delay` - Identify main-thread blocking JS tasks.

### 🛡️ Schema & Semantics
- `/validate_json_ld` - Verify `schema.org` syntax for Organization/Product.
- `/check_aria_landmarks` - Ensure `<main>`, `<nav>`, `<header>` are used.

### 🚀 Reporting
- `/generate_seo_audit` - Auto-generation of visibility score (1-100).
- `/audit_keyword_density` - Check for keyword-stuffing vs authority.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: commands must be executed within the target project context. Technical SEO is a blocking requirement for any Production-ready branch.
