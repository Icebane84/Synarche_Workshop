# GUCA: Node.js Command Registry [v15.0]

## 🛠️ Audit Commands

### 🔍 API & Architecture
- `/audit_route_layer` - Scan for business logic leaks in controllers.
- `/verify_layered_structure` - Check Controller-Service-Repository separation.
- `/validate_zod_schemas` - Ensure all input boundaries have Zod/Valibot validation.

### 🚀 Performance & Runtime
- `/check_event_loop` - Scan for blocking `Sync` methods and heavy CPU operations.
- `/audit_async_patterns` - Verify parallel execution via `Promise.all`.
- `/check_node_v22` - Analyze for Node.js 22+ feature compatibility (`--experimental-strip-types`, `node --test`).

### 🛡️ Security Guardrails
- `/audit_backend_security` - Check for parameterized queries, password hashing, and rate limiting.
- `/verify_secrets_storage` - Ensure no secrets are hardcoded in the codebase.
- `/check_cors_policy` - Validate CORS configuration and security headers (Helmet).


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: These commands are to be executed as part of the **Backend Pre-Work Validation** or **Security Post-Mortem** phases of any Node.js task. Use with the **AOP.md** playbook as authority.
