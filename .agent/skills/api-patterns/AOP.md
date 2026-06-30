---
id: AOP-API-001
name: API Operational Playbook
version: v2.1 [GOLD]
type: OPERATIONAL_PLAYBOOK
status: [ACTIVE]
tags: ['#AOP', '#PROCESS', '#API', '#ARCH']
---

# 📖 API PLAYBOOK | AOP-API-001

| Field          | Metadata                  |
| :------------- | :------------------------ |
| **Provenance** | Genesis Stamp: 2026-03-30 |
| **Domain**     | NOVA.Infra.API            |
| **State**      | ⚡ OPERATIONAL            |
| **Audit**      | Musashi (Pass)            |
| **Integrity**  | [V15.0-OMEGA]             |

---

## 🏗️ SYSTEMIC PROCESSES

### 1. API Style Selection (Decision Matrix)

Identify the consumer before choosing the protocol:

| Consumer | Recommended Protocol | Key Benefit |
| :--- | :--- | :--- |
| **Public / Broad** | REST + OpenAPI | Maximum interoperability |
| **Complex Frontend** | GraphQL | Optimized data fetching (No overfetching) |
| **TS Monorepo** | tRPC | Automated end-to-end type safety |
| **Microservices** | gRPC | High-throughput, low-latency binary serialization |

### 2. REST Resource Architecture

Follow the "Nouns-Only" ritual for endpoint design:
- ✅ `GET /users/123/posts` (Shallow, hierarchical)
- ❌ `POST /create-user` (Verb in endpoint)
- ✅ Use lowercase with hyphens for multi-word resources (`/user-profiles`).

### 3. Response & Error Standardization

Every API response must use a consistent envelope:
```json
{
  "success": true,
  "data": { ... },
  "message": "Protocol Sync Complete",
  "meta": { "pagination": { ... } }
}
```
**HTTP Status Consistency**:
- `201 Created`: successful POST.
- `422 Unprocessable Entity`: validation failures (semantics).
- `429 Too Many Requests`: rate limit threshold hit.

---

## 🔍 ACTIONABLE HEURISTICS

- **[VERSIONING]**: Default to URI versioning (e.g., `/v1/users`) unless header-based versioning is explicitly requested.
- **[IDEMPOTENCY]**: Ensure `PUT` and `DELETE` operations are idempotent.
- **[SECURITY]**: Always validate the `Authorization: Bearer <JWT>` header before executing service-layer logic.

---

`[OMNI-ARTIFACT-ANCHOR] ID: AOP-API-001 VER: v2.1 [GOLD] DOMAIN: MIND STATUS: [ACTIVE]`
