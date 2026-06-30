---
description: Execute the Agent A/B/C Triple-Pass TDD Cycle
---

## 🏗️ TDD Cycle: Triple-Pass Protocol

Follow these steps to implement any new feature or refactor under OMEGA v15.0 governance.

### 🔴 Phase 1: RED (Agent A - Specifier)
1. **Understand**: Read the `UI/TASK` requirements.
2. **Decompose**: Perform a **Decomposition Protocol** scan using `AOP.md`.
3. **Spec**: Create a new test file (e.g., `src/features/feature.test.ts`).
4. **Verify**: Run the test to ensure it fails.
// turbo
5. Command: `npx vitest run src/features/feature.test.ts --expect-fail`

### 🟢 Phase 2: GREEN (Agent B - Implementer)
1. **Pass**: Edit the target production file.
2. **Minimal**: Write only enough code to pass the test. Do not optimize.
3. **Verify**: Run the test to ensure it passes.
// turbo
4. Command: `npx vitest run src/features/feature.test.ts`

### 🔵 Phase 3: REFACTOR (Agent C - Optimizer)
1. **Align**: Refactor the code for OMEGA v15.0 standards (Performance, Bundle size, Types).
2. **Harden**: Ensure no behavior was changed.
3. **Verify All**: Run the master audit script.
// turbo
4. Command: `python scripts/omega_audit.py`

### 🛡️ Final Verification
5. Update `SELT.md` in the relevant skill folder with the new trace.
6. Commit the changes and close the task.

---
"The test is the specification. Trust the cycle."
