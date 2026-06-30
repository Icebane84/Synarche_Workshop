---
name: rust-pro
description:
    Master Rust 1.75+ with modern async patterns, advanced type system features, and production-ready systems
    programming. Expert in the latest Rust ecosystem including Tokio, axum, and cutting-edge crates.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Rust Professional Governance System [v15.0]

## 🎯 Axiomatic Purpose
To enforce **Memory-Safe**, **Zero-Cost**, and **Async-Ready** development across high-performance systems. This skill prevents the use of redundant clones, unoptimized locks, and undocumented `unsafe` code. It mandates modern (1.75+) Rust idioms and trait-driven architecture.

## 🗂️ Sovereign Registry (UMB-SELT)

| Artifact | Purpose | Authority |
| :--- | :--- | :--- |
| **[INDEX.md](INDEX.md)** | Deterministic Gateway | System Entry |
| **[AOP.md](AOP.md)** | Professional Playbook | Sovereign Heuristics |
| **[GUCA.md](GUCA.md)** | Command Registry | Operational Audit |
| **[SELT.md](SELT.md)** | Experience Log | Systemic Trace |

## 🔴 MANDATORY OPERATIONAL PROTOCOLS

### 1. Ownership Integrity Protocol
**DO NOT** bypass the borrow checker with unnecessary `.clone()`. Master the use of `Arc`, `Box`, and `Weak` for efficient memory management. 

### 2. Async Hygiene [Tokio]
Any blocking work within an `async` context **MUST** be offloaded to `spawn_blocking`. Never block the async executor threads with long-running sync tasks.

### 3. Trait-Driven Architecture
Leverage GATs and advanced generic bounds to create flexible, type-safe abstractions. Adhere to the orphan rule via the Newtype pattern.

### 4. Unsafe Safety Mandate
Every `unsafe` block **MUST** have a `// SAFETY:` header documenting exactly why the operation is memory-safe and invariant-respecting.

---
"In Rust, we trust the compiler, but we audit the intent."
