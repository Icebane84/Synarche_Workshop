# AOP: Rust Professional Implementation [v15.0]

## 🛠️ THE RUST 1.75+ MANDATE
**Rust is a contract between the developer and the compiler. Ownership and Lifetimes are the ink.**

### 🦾 Ownership & Memory Governance
1. **Ownership**: Default to Move semantics. Explicitly `clone()` only when necessary.
2. **Borrowing**: Prefer immutability. Use `Cell`/`RefCell` or `Mutex`/`RwLock` only for interior mutability.
3. **Smart Pointers**:
   - `Box`: Heap allocation.
   - `Arc`: Thread-safe reference counting.
   - `Rc`: Single-thread reference counting.
   - `Weak`: Break reference cycles.

---

## 🏗️ ADVANCED ARCHITECTURAL HYGIENE

### 🏰 Trait-Driven Design
1. **Generic Associated Types (GATs)**: Use for advanced async/iterator patterns.
2. **Orphan Rule**: Navigate via Newtype pattern where necessary.
3. **Marker Traits**: Use `Send` and `Sync` to enforce thread safety at compile time.
4. **Type Erasure**: Use `dyn Trait` for dynamic dispatch only when necessary (vtable overhead).

### 🛡️ Error Handling Protocol
- **Libraries**: Use `thiserror` for precise, machine-readable error variants.
- **Applications**: Use `anyhow` for context-rich error reporting and quick propagation.
- **Panic**: Prohibited in production code. Use `Result<T, E>` and `Option<T>` for all recoverable paths.

---

## ⚡ ASYNC & CONCURRENCY [TOKIO]

### ⚖️ The Async Rule
- **I/O-Bound**: Use `async/.await` with **Tokio** runtime.
- **CPU-Bound**: Use `tokio::task::spawn_blocking` or external thread pools (Rayon).
- **Blocking**: **Never** sleep the main thread or perform blocking I/O in an async context. Use `tokio::time::sleep`.

### 🔄 Concurrency Patterns
- **Tasks**: `tokio::spawn` for independent work.
- **Channels**: `mpsc` for single-producer-multi-consumer (queues), `broadcast` for events.
- **Select**: Use `tokio::select!` for multi-signal orchestration.

---

## 🏎️ PERFORMANCE & SYSTEMS SECRETS

### ⚡ Zero-Cost Protocol
- **SIMD**: Use `portable-simd` for vector operations.
- **Inlining**: Use `#[inline]` liberally for small, hot-path functions.
- **Caching**: Ensure cache-locality by using contiguous memory (`Vec`) over fragmented pointers.

### 🛡️ Unsafe Code Safety
- Every `unsafe` block **MUST** be accompanied by a `// SAFETY: ...` comment documenting the invariants that prevent UB.

---

## 🧪 DECOMPOSITION PROTOCOL (PRE-WORK)
**Before starting any Rust implementation, perform this analysis:**
```
RUST TASK: [Task Name]
├── RUNTIME: [Tokio / None]
├── OWNERSHIP: [Move / Arc / Box strategy]
├── TRAITS: [GATs / Generic Bounds / Marker Traits]
├── ERROR: [thiserror / anyhow choice]
├── PERFORMANCE: [SIMD / Inlining / Zero-cost targets]
└── SAFETY: [Unsafe check / Safety Invariants]
```

---
> 🔴 **Remember:** Rust is about making the impossible unrepresentable. Let the type system do the heavy lifting.
