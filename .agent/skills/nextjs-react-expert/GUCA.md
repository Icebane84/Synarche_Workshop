# GUCA: React & Next.js Command Registry [v15.0]

## 🛠️ Audit Commands

### 🔍 Performance & Waterfalls
- `/audit_waterfalls` - Scan for sequential `await` calls in RSC, API routes, and Server Actions.
- `/verify_parallel_fetching` - Check for `Promise.all` or `better-all` usage in data layers.
- `/check_suspense_boundaries` - Validate strategic placement of `<Suspense>` for PPR.

### 📦 Bundle & Imports
- `/check_barrel_imports` - Scan for `import { x } from 'library'` in app code.
- `/audit_bundle_bloat` - Identify components > 20KB that are NOT using `next/dynamic`.
- `/verify_optimize_packages` - Check `next.config.js` for `optimizePackageImports`.

### 🛡️ Security & RSC
- `/audit_action_security` - Verify auth/authz checks inside all `"use server"` functions.
- `/check_rsc_serialization` - Scan for bloated props (e.g., passing 50 fields when only 1 is used).
- `/verify_react_cache` - Check for per-request deduplication of DB/Auth calls.

### 🚀 Next.js 16+ Specifics
- `/audit_cache_directives` - Scan for `use cache`, `cacheLife`, and `cacheTag` usage.
- `/check_ppr_readiness` - Verify `cacheComponents` flag in `next.config.ts`.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: These commands are to be executed as part of the **React Pre-Work Validation** or **In-Depth Performance Audit** phases of any project. Use with the **AOP.md** playbook as authority.
