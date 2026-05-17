"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-CORE-ROLLBACK_CORE` | The Sovereign ID. |
| **Official Name** | `rollback_core.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `CORE`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""
# core/rollback_core.py

import copy


class InputLog:
    def __init__(self):
        self.log = {}
        self.predicted = set()

    def record(self, frame, player, value, predicted=False):
        self.log.setdefault(frame, {})[player] = value

        if predicted:
            self.predicted.add(frame)
        elif frame in self.predicted:
            self.predicted.remove(frame)

    def get(self, frame):
        return self.log.get(frame, {})

    def mismatch(self, frame, player, actual):
        predicted = self.log.get(frame, {}).get(player)
        return predicted != actual


class SnapshotBuffer:
    def __init__(self, size=120):
        self.buffer = {}
        self.size = size

    def save(self, frame, world):
        self.buffer[frame] = copy.deepcopy(world)

        old = frame - self.size
        if old in self.buffer:
            del self.buffer[old]

    def load(self, frame):
        if frame not in self.buffer:
            raise RuntimeError("Snapshot missing")
        return copy.deepcopy(self.buffer[frame])


class RollbackEngine:
    def __init__(self, executor, scheduler, input_log, snapshot_buffer):
        self.executor = executor
        self.scheduler = scheduler
        self.input_log = input_log
        self.snapshots = snapshot_buffer
        self.current_frame = 0

    def on_input(self, frame, player, actual_input, world):
        mismatch = self.input_log.mismatch(frame, player, actual_input)

        self.input_log.record(frame, player, actual_input, predicted=False)

        if mismatch:
            self.rollback(frame, world)

    def rollback(self, target_frame, world):
        print(f"[ROLLBACK] to frame {target_frame}")

        restored = self.snapshots.load(target_frame - 1)

        # overwrite world
        world.__dict__.update(restored.__dict__)

        # replay
        for f in range(target_frame, self.current_frame + 1):
            world.current_inputs = self.input_log.get(f)
            self.scheduler.run_frame(world)

            self.snapshots.save(f, world)
