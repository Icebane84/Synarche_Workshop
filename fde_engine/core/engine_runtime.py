"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-CORE-ENGINE_RUNTIME` | The Sovereign ID. |
| **Official Name** | `engine_runtime.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `CORE`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/core/engine_runtime.py`

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""


class EngineRuntime:
    def __init__(self, world, scheduler, rollback=None):
        self.world = world
        self.scheduler = scheduler
        self.rollback = rollback

    def tick(self, inputs):
        frame = self.world.frame

        # record inputs
        if self.rollback:
            for player, value in inputs.items():
                self.rollback.input_log.record(frame, player, value)

        self.world.current_inputs = inputs

        # simulate
        self.scheduler.run_frame(self.world)

        # snapshot AFTER simulation
        if self.rollback:
            self.rollback.snapshots.save(frame, self.world)
            self.rollback.current_frame = frame

        self.world.frame += 1
