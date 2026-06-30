# SELT: Node.js Experience Log & Trace [v15.0]

## 📅 Session Logs

### 🏗️ 2026-03-30 (Batch 4 Rollout)
- **Status**: Canonized Batch 4 (Node.js).
- **Synthesis**: Standardized Hono vs Fastify vs NestJS selection matrix in `AOP.md`.
- **Integrity**: Enforced **Layered Architecture** and **Zod Validation** as top-level governance.
- **Audit**: Updated command registry in `GUCA.md`.

## 📍 Systemic Discoveries

### 🧠 Performance Expansion
- **Discovery**: Widespread use of `Express` for edge/serverless contexts, causing high cold start times.
- **Remediation**: Injected **Hono** as the mandatory default for Edge/Serverless in `AOP.md`.
- **Discovery**: Blocking sync methods (`fs.readFileSync`) found in high-traffic APIs.
- **Remediation**: Implemented the **Event Loop Rule**: `Sync` methods are prohibited in production code.

## 🚧 Historical Dissonance
- **Issue**: SQL Injection risks in legacy service layers.
- **Legacy Pattern**: Use of string concatenation for dynamic queries.
- **Correction**: Prohibited string concatenation for SQL. Mandated parameterized queries and schema validation at the Controller boundary.

---
**Protocol**: This log MUST be updated after every backend audit or implementation task to maintain Zero Entropy in Node.js governance.
