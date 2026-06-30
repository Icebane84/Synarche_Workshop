# AOP: Node.js Backend & Systems Implementation [v15.0]

## 🛠️ THE RUNTIME CHOICE (2025)
**STOP. Do not default to Express. Analyze the deployment target and performance requirements.**

### 🚦 Framework Decision Tree
| Target | Choice | Rationale |
| :--- | :--- | :--- |
| **Edge / Serverless** | **Hono** | Zero dependency, < 1ms cold start, native TS. |
| **High-Perf API** | **Fastify** | 2-3x faster than Express, schema-based, DI ready. |
| **Enterprise / Team** | **NestJS** | Structured, Opinionated, Angular-style DI. |
| **Legacy / Mature** | **Express** | Largest ecosystem, but slowest performance. |

---

## 🏗️ ARCHITECTURAL GOVERNANCE

### 🏰 The Layered Mandate
**Business logic MUST NOT reside in controllers.**
1. **Controller Layer**: Handles HTTP (params, query, body), calls Service, returns response.
2. **Service Layer**: Pure business logic, framework-agnostic. Calls Repository.
3. **Repository Layer**: Data access only (Prisma, Drizzle, Kysely).

### 🛡️ Validation & Security
- **Fail-at-Gate**: Use **Zod** or **Valibot** to validate all incoming requests at the Controller boundary.
- **SQL Integrity**: **NEVER** use string concatenation for SQL. Use parameterized queries or safe ORMs.
- **Secrets**: Environment variables only. No hardcoding in `config/` files.

---

## 🚀 PERFORMANCE & ASYNC PROTOCOLS

### ⚖️ The Event Loop Rule
- **I/O-Bound**: Use `async/await`.
- **CPU-Bound**: Offload to **Worker Threads** or external microservices.
- **Blocking**: Any `Sync` method (e.g., `fs.readFileSync`) is **PROHIBITED** in production code.

### 🔄 Async Orchestration
- **Sequential**: `await a(); await b();`
- **Parallel Independent**: `Promise.all([a(), b()])`
- **Partial Failure**: `Promise.allSettled()`

---

## 🚨 ERROR & QUALITY STANDARDS

### 🩺 Centralized Error Handling
- Throw custom `ApiError` classes with defined `statusCode`.
- Handle all errors in a global middleware.
- **Log**: Full stack trace, context, user metadata.
- **Response**: Programmatic error code + user message. No internal traces.

### 🧪 Testing Strategy
- **Unit**: Business logic (Vitest/node:test).
- **Integration**: API endpoints (Supertest).
- **E2E**: Critical paths (Playwright).
- **Native**: Use `node --test` for dependency-free runners in Node.js 22+.

---

## 🧪 DECOMPOSITION PROTOCOL (PRE-WORK)
**Before starting any backend implementation, perform this analysis:**
```
BACKEND TASK: [Task Name]
├── FRAMEWORK: [Hono / Fastify / NestJS / Express]
├── RUNTIME: [Node 22+ / Bun / Deno]
├── ARCHITECTURE: [Controller / Service / Repo Layout]
├── VALIDATION: [Zod / Valibot Schema]
├── SECURITY: [Auth / Rate-Limit / SQL-Check]
└── PERFORMANCE: [Async / Event Loop Check]
```

---
> 🔴 **Remember:** Code quality in Node.js is proportional to the health of the event loop. Protect it at all costs.
