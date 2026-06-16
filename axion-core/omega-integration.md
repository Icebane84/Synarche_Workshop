# Omega Module Integration Plan

## Goal

Synchronize the newly relocated OMEGA modules (ECS, Logging, Refactor) with the Synarche Master Registry and hook them
into the Coherent Synthesis Engine (CSE).

## Tasks

- [x] Task 1: Expose Interfaces → Verify: `__init__.py` files exist in `engine/ecs`, `phoenix/logging`, and
      `system/refactor`.
- [x] Task 2: Register ECS Core → Verify: Add `src/engine/ecs/*.py` entries to `GVRN.Master.Registry.yaml`.
- [x] Task 3: Register Logging Suite → Verify: Add `src/phoenix/logging/*.py` entries to `GVRN.Master.Registry.yaml`.
- [x] Task 4: Register Refactor Suite → Verify: Add `src/system/refactor/*.py` entries to `GVRN.Master.Registry.yaml`.
- [x] Task 5: Hook EthicalLogger into CSE → Verify: `engine_v2.py` imports and uses `EthicalLogger`.
- [x] Task 6: Hook ECSScheduler into CSE → Verify: `engine_v2.py` executes audit tasks via the scheduler.
- [x] Task 7: Final Governance Audit → Verify: Run `python -m hephaestus.sentinel` from `src` and confirm 0 dissonance for new modules.

## Done When

- [x] All new modules are registered in the Master Registry.
- [x] The CSE uses the new logging and scheduling frameworks.
- [x] The Sentinel audit returns a clean state for the relocated directories (Resonance optimized).

## Notes

- Circular imports in `hephaestus/__init__.py` cause warnings but do not block execution.
- Registry updates should follow the established YAML schema.
