# GUCA: Rust Professional Command Registry [v15.0]

## 🛠️ Audit Commands

### 🔍 Memory & Safety
- `/audit_ownership` - Scan for unnecessary clones and redundant moves.
- `/verify_safety_invariants` - Check all `unsafe` blocks for mandatory `// SAFETY:` documentation.
- `/check_lifetime_elision` - Analyze complex structs for lifetime clarity and elision opportunities.

### 🚀 Performance & Async
- `/audit_async_blocking` - Scan for blocking I/O or long-running sync tasks in `async` contexts.
- `/verify_zero_cost` - Check for unnecessary `dyn Trait` usage and vtable overhead.
- `/check_simd_hotpaths` - Identify computational loops for vectorization candidates.

### 🛡️ Quality & Tools
- `/audit_rust_security` - Run `cargo audit` and `cargo deny` for dependency health.
- `/verify_error_strategy` - Check for correct `thiserror` vs `anyhow` usage across modules.
- `/run_clippy_extreme` - Execute `cargo clippy -- -D warnings -A clippy::all -W clippy::pedantic`.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: These commands are to be executed as part of the **Rust Pre-Work Validation** or **High-Performance Audit** phases of any Rust task. Use with the **AOP.md** playbook as authority.
