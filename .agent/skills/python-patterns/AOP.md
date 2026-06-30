# AOP: Python Systems & Modern Architecture [v15.0]

## 🛠️ THE PYTHONIC CHOICE (2025)
**STOP. Do not default to Flask or Django. Analyze the service intent and concurrency requirements.**

### 🚦 Framework Decision Tree
| Target | Choice | Rationale |
| :--- | :--- | :--- |
| **API-First / Microservice** | **FastAPI** | Async-native, Pydantic validation, ultra-fast performance. |
| **Full-Stack / Admin-Rich** | **Django** | Batteries-included, built-in Admin, robust ecosystem. |
| **Simple Script / Mini-API** | **Flask** | Minimal, low overhead (but no native async). |
| **AI/ML API Serving** | **FastAPI** | High concurrency for model orchestration. |

---

## 🏗️ TYPE SAFETY & VALIDATION (PYDANTIC V2)
**Python is dynamic, but your interfaces MUST be static.**

### 🛡️ The Type Integrity Protocol
1. **Pydantic v2**: Use for ALL request bodies, response models, and environment configurations.
2. **Strict Hinting**: Function parameters and return values **MUST** be typed. Use `Union` (`|`), `Optional`, and `Generic` typing.
3. **Data Classes**: Use `pydantic.BaseModel` instead of standard `dataclasses` for runtime validation.

### 📐 Project Structure Standards
- **Feature-Based**: Organize by `users/`, `billing/`, `core/` for large apps.
- **Layer-Based**: `routes/`, `services/`, `models/`, `schemas/` for medium APIs.

---

## ⚡ CONCURRENCY & PERFORMANCE

### ⚖️ The I/O vs CPU Rule
- **I/O-Bound (Waiting for DB/Network)**: Use `async def`.
- **CPU-Bound (Computing/ML/Crypto)**: Use `def` + `multiprocessing` or offload to background workers.
- **Async Hygiene**: NEVER use blocking libraries (e.g., `requests`) in `async` code. Use `httpx` or `aiohttp`.

### 🔄 Background Orchestration
- **In-Process**: `FastAPI.BackgroundTasks` (Simple fire-and-forget).
- **Distributed**: **Celery** (Complex workflows, retries) or **ARQ** (Redis-based async).

---

## 🚨 DJANGO & FASTAPI SPECIFICS

### 🐍 Django 5.0+ Governance
- **Fat Models, Thin Views**: Move logic into model managers or services.
- **Query Optimization**: Mandate `select_related()` (FK) and `prefetch_related()` (M2M) to kill N+1 queries.
- **Async Views**: Use only for external I/O or WebSockets.

### ⚡ FastAPI Wisdom
- **Dependency Injection**: Use `Depends()` for DB sessions, security, and shared logic.
- **Native Doc Alignment**: Leverage Pydantic descriptions for automatic OpenAPI documentation.

---

## 🧪 DECOMPOSITION PROTOCOL (PRE-WORK)
**Before starting any Python implementation, perform this analysis:**
```
PYTHON TASK: [Task Name]
├── FRAMEWORK: [FastAPI / Django / Flask]
├── CONCURRENCY: [Async (I/O) / Sync (CPU)]
├── TYPE STRATEGY: [Pydantic Models / Type Hints]
├── ARCHITECTURE: [By Layer / By Feature]
├── BACKGROUND: [Task Queue Choice]
└── TESTING: [Pytest Fixtures / Async Mocking]
```

---
> 🔴 **Remember:** Code quality in Python is proportional to the explicitness of its types and the correctness of its concurrency models.
