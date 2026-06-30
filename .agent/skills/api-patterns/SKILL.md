---
id: UMB-API-001
name: API Design & Architecture
version: v2.1 [GOLD]
type: SKILL_LOGIC
status: [ACTIVE]
tags: ['#API', '#DESIGN', '#ARCHITECTURE', '#SOVEREIGN']
---

# 🧠 API DESIGN | UMB-API-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Infra.API            |
| **State**      | 🌟 GOLD STANDARD          |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V2.0-SOVEREIGN]          |

---

## 🎭 SOVEREIGN LOGIC

API design must prioritize consumer needs, developer experience (DX), and long-term evolvability. We avoid "one-size-fits-all" architectures by applying a context-aware selection process.

### Principles of API Architecture

1.  **Consumer-First**: Identify who will use the API and their specific constraints (e.g., mobile vs. web vs. server-to-server).
2.  **Resource-Oriented**: For REST, focus on nouns and relationships rather than actions.
3.  **Type Safety**: Prioritize end-to-end type safety (tRPC/GraphQL) for internal TypeScript-driven ecosystems.
4.  **Security by Default**: Implement rate-limiting, authentication, and validation at the gateway level.

---

## 🛠️ BLUEPRINT STANDARDS

### Selection Heuristics

- **[REST]**: Use for public-facing APIs or when maximum platform compatibility is required.
- **[GRAPHQL]**: Use for complex apps with multiple frontends needing flexible data sets.
- **[TRPC]**: Use for TypeScript monorepos to achieve zero-overhead type safety.
- **[GRPC]**: Use for high-performance internal microservice communication.

---

## 🔍 QUALITY CONSTRAINTS

- **[NO_VERBS]**: In REST, never use actions in endpoints (e.g., `/getUsers`). Use `GET /users`.
- **[CONSISTENT_ERRORS]**: Use a standardized error envelope across all endpoints.
- **[VERSIONING]**: Always plan for API evolution using URI or Header-based versioning.

---

`[OMNI-ARTIFACT-ANCHOR] ID: UMB-API-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
