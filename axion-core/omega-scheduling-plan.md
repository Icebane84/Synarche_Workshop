# Task: OMEGA v15.1 - Scheduling Core Integration (TDD)

## Goal

Implement the `CompiledGraph` and `LayeredScheduler` blueprints using TDD to unify ECS and Superposition engine
execution.

## Tasks

- [ ] **Phase 1: Scheduling Core (TDD)**
    - [ ] Task 1.1: Create `tests/engine/scheduling/test_graph.py` (RED) → Verify: `pytest` fails.
    - [ ] Task 1.2: Implement `src/engine/scheduling/compiled_graph.py` (GREEN) → Verify: `pytest` passes.
    - [ ] Task 1.3: Refactor `CompiledGraph` for OMEGA v15.0 compliance (REFACTOR) → Verify: Tests stay green.
    - [ ] Task 1.4: Create `tests/engine/scheduling/test_scheduler.py` (RED) → Verify: `pytest` fails.
    - [ ] Task 1.5: Implement `src/engine/scheduling/layered_scheduler.py` (GREEN) → Verify: `pytest` passes.

- [ ] **Phase 2: ECS Integration**
    - [ ] Task 2.1: Implement `src/engine/ecs/compiler.py` using `DAGCompiler` logic.
    - [ ] Task 2.2: Update `engine_v2.py` to use `LayeredScheduler`.

- [ ] **Phase 3: Final Verification**
    - [ ] Task 3.1: Run `sentinel.py` audit.
    - [ ] Task 3.2: Verify 0-violation state.

## Done When

- [ ] `CompiledGraph` handles dependency layering and cycle detection.
- [ ] `LayeredScheduler` executes tasks in deterministic order.
- [ ] `engine_v2.py` successfully initializes with the new scheduler.
