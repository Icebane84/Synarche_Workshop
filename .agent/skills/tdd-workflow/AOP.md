# AOP: TDD & Agent A/B/C Playbook [v15.0]

## 🏗️ THE TRIPLE-PASS PROTOCOL (AGENT A/B/C)
**Eliminating Implementation Bias.**

### 🔴 RED Phase: Specification (Agent A) [CRITICAL]
- **Goal**: Define expected behavior via a failing test.
- **Rules**: Agent A is PROHIBITED from editing production code.
- **Output**: A new test file (e.g., `tests/ui_feature.test.ts`) that precisely describes the requirement.
- **Fail Early**: Verify that the test actually fails before proceeding to GREEN.

### 🟢 GREEN Phase: Implementation (Agent B) [CRITICAL]
- **Goal**: Pass the Agent A test with minimal code.
- **Rules**: Agent B is PROHIBITED from refactoring or optimizing. YAGNI (You Aren't Gonna Need It) is the only logic allowed.
- **Output**: Minimal functional code that makes the test turn green.

### 🔵 REFACTOR Phase: Optimization (Agent C) [CRITICAL]
- **Goal**: Align the GREEN code with OMEGA v15.0 performance/security standards.
- **Rules**: Agent C is PROHIBITED from changing behavior. All Agent A tests MUST remain green.
- **Output**: Hardened, professional-grade code (Bundle size optimized, RSC-compliant, typed).

---

## 🏰 DECOMPOSITION PROTOCOL (TDD PRE-WORK)
**Before starting any new feature/refactor, perform this scan:**
```
UI/TASK: [Task Name]
├── SPEC: [What is the failing test for Agent A?] (RED check)
├── MINIMAL: [What is the simplest way to pass?] (GREEN check)
├── HARDEN: [How do we optimize for OMEGA standards?] (REFACTOR check)
└── AUDIT: [Does /omega_audit pass?] (Final check)
```

---

## 📜 ASSERTION STANDARDS (MANDATORY)
1. **Behavior-Based**: Test what the user/system *does*, not the internal implementation.
2. **Deterministic**: No `wait()` or random values in tests.
3. **Atomic**: Tests must run independently with their own isolated state.

---
**Protocol**: "Spec first. Pass second. Harden always. Trust the cycle."
