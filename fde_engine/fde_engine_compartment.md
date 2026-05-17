# fde_engine/
│
├── gvrn/                              # NEW: The Phoenix Governance Layer
│   ├── law_validator.py               # Enforces zero-entropy state validation
│   ├── selt_logger.py                 # Immutable telemetry and Dissonance tracking
│
├── core/
│   ├── engine_runtime.py              # Main loop (S(n+1) = F(S(n), I(n)))
│   ├── chunk_executor.py              # UPGRADED: Replaces naive parallel_executor (Phase 6+)
│   ├── rollback_core.py               # Time machine (Phase 4)
│   ├── delta_packet.py                # NEW: Strict DAMP schemas for mutation payloads
│
├── ecs/
│   ├── entity_registry.py             # Deterministic ID generation
│   ├── archetype_storage.py           # Contiguous columnar arrays (O(1) queries)
│   ├── world.py                       # The immutable snapshot container
│   ├── commit_layer.py                # O(1) swap-and-pop data migration bottleneck
│   ├── ecs_scheduler.py               # DAG-to-Executor mapping
│
├── dag/
│   ├── dag_compiler.py                # Graph compilation
│   ├── system_signature.py            # NEW: The required Read/Write/Accumulate contract
│
├── systems/
│   ├── base_system.py                 # Pure function templates
│   ├── movement_system.py             # Logic exemplar
│   ├── input_system.py                # Deterministic input injection
│
├── bridge/                            # NEW: Preparation for Ashen Oath
│   ├── godot_translation_layer.py     # Stub: Maps FDE state to Godot visual/rendering state
│
├── demo/
│   ├── fde_test_harness.py            # The physical execution bootstrap
│
└── docs/
    ├── PRS_INDEX.md                   # NEW: Rosetta Stone navigational mapping
    └── README.md

    Input → Predict → Simulate → Snapshot
           ↓
   Mismatch? → Rollback → Resimulate