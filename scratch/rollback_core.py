"""
Artifact ID: CORE-FDE-ROLLBACK-013
Ethos: Time is a Shallow Pointer.
"""
class SnapshotBuffer:
    def __init__(self, size=60):
        self.buffer = {}
        self.size = size

    def save(self, frame, world):
        # FDE Upgraded: We no longer deepcopy the world. 
        # We ask the world for its optimized, shallow-pointer dictionary.
        self.buffer[frame] = world.snapshot()

        old = frame - self.size
        if old in self.buffer:
            del self.buffer[old]

    def load(self, frame):
        if frame not in self.buffer:
            raise RuntimeError(f"FDE Violation: Snapshot {frame} missing from buffer.")
        # Return the dictionary of pointers. No deepcopy needed.
        return self.buffer[frame]

class RollbackEngine:
    # ... (init and on_input remain the same) ...

    def rollback(self, target_frame, world):
        print(f"[ROLLBACK] Mismatch detected. Rewinding to frame {target_frame - 1}")

        # 1. Load the shallow pointer dictionary
        restored_snap = self.snapshots.load(target_frame - 1)

        # 2. Instruct the World to re-align its internal pointers
        world.restore(restored_snap)

        # 3. Resimulate forward
        for f in range(target_frame, self.current_frame + 1):
            world.current_inputs = self.input_log.get(f)
            self.scheduler.run_frame(world)
            self.snapshots.save(f, world)