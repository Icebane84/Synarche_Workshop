# AOP: Global Testing & Performance Playbook [v15.0]

## 🏗️ TESTING ARCHITECTURE & HEALTH
**Vitality is the Primary Structural Property.**

### 🚦 Unit Testing [CRITICAL]
- **Isolation**: Test individual functions/logic in isolation. Use `mocks` for all external dependencies (APIs, Stores).
- **Edge Cases**: Mandate testing for `null`, `undefined`, `empty-string`, and `large-payload` inputs.
- **Pure Logic**: Prioritize testing of business logic in `src/services/` or `src/utils/`.

### 🚦 Performance Auditing [CRITICAL]
- **Memory Leaks**: Verify that components/services clean up Event Listeners and Timers on unmount.
- **Execution Speed**: Logic in critical paths (Rendering, Data Mapping) must execute in under **10ms**.
- **Bundle Size**: No single component should exceed **50kB** (min+gz). Use dynamic imports for large libraries.

### 🛡️ INTEGRATION & MOCKING [HIGH]
- **Service Mocks**: Use `vitest.mock()` to intercept global service calls during tests.
- **Store Sync**: Verify that state changes in `taskStore` or `userStore` propagate correctly to subscribers.
- **Error Propagation**: Test that failed service calls are handled gracefully by the UI (Sovereign Recovery).

---

## 🏰 DECOMPOSITION PROTOCOL (TESTING PRE-WORK)
**Before starting any production logic, perform this scan:**
```
UI/TASK: [Logic Task]
├── UNIT: [What are the 3-5 critical test cases?] (Behavior check)
├── EDGE: [What happens on invalid input?] (Safety check)
├── PERF: [Is this logic on the critical render path?] (Performance check)
└── MOCK: [What external services need isolation?] (Boundary check)
```

---

## 📜 ASSERTION STANDARDS (MANDATORY)
1. **Behavioral Accuracy**: Assert on the result (the "What"), not the implementation (the "How").
2. **Determinism**: No network calls or random values in Unit/Integration tests.
3. **Fail-Fast**: Tests must fail immediately and clearly on regression.

---
**Protocol**: "Health is the only foundation of execution. Verify the Sovereign."
