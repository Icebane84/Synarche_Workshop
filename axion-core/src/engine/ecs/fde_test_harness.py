"""Artifact ID: CORE-FDE-TEST-001
Ethos: Verification through Execution.
"""

import copy


# --- PHASE 3: THE EXECUTOR ---
class DeterministicParallelExecutor:
    def execute_layer(self, layer, global_context):
        buffered_deltas = {}
        # Simulated Parallel Execution (Strict Isolation)
        for task in layer:
            safe_context = copy.deepcopy(global_context)
            buffered_deltas[task.execution_index] = task.compute_pure(safe_context)

        # Deterministic Commit & Conflict Detection
        seen_keys = set()
        for exec_index in sorted(buffered_deltas.keys()):
            delta = buffered_deltas[exec_index]
            for key, value in delta.get("writes", {}).items():
                if key in seen_keys:
                    raise RuntimeError(f"Collision on key: {key}")
                seen_keys.add(key)
                global_context[key] = value


# --- PHASE 5: THE ECS SYSTEM ---
class MovementSystem:
    def __init__(self):
        self.name = "MovementSystem"
        self.execution_index = 1

    def compute_pure(self, context):
        delta_writes = {"Transform": copy.deepcopy(context.get("Transform", {}))}
        transforms = delta_writes["Transform"]
        velocities = context.get("Velocity", {})
        inputs = context.get("inputs", {})

        for ent_id in transforms.keys():
            if ent_id in velocities:
                # Apply Input to Velocity
                p_input = inputs.get(ent_id, "NONE")
                if p_input == "DASH":
                    velocities[ent_id]["dx"] = 5
                elif p_input == "WALK":
                    velocities[ent_id]["dx"] = 1

                # Apply Velocity to Transform
                transforms[ent_id]["x"] += velocities[ent_id]["dx"]

        return {"writes": {"Transform": transforms, "Velocity": velocities}}


# --- PHASE 4: THE ROLLBACK CORE ---
class RollbackEngine:
    def __init__(self):
        self.executor = DeterministicParallelExecutor()
        self.state_buffer = {}  # Snapshot anchor
        self.input_log = {}  # Absolute truth
        self.current_frame = 0

    def get_inputs(self, frame):
        # Naive prediction: repeat last frame if missing
        if frame not in self.input_log:
            prev = self.input_log.get(frame - 1, {"player_1": "WALK"})
            self.input_log[frame] = copy.deepcopy(prev)
        return self.input_log[frame]

    def _simulate_frame(self, frame, context, inputs, compiled_graph):
        frame_context = {**context, "frame": frame, "inputs": inputs}
        for layer in compiled_graph:
            self.executor.execute_layer(layer, frame_context)
        context.update(frame_context)

    def step(self, context, compiled_graph):
        inputs = self.get_inputs(self.current_frame)
        self._simulate_frame(self.current_frame, context, inputs, compiled_graph)
        self.state_buffer[self.current_frame] = copy.deepcopy(context)

        print(
            f"Frame {self.current_frame} Complete | Pos X: {context['Transform']['player_1']['x']}"
        )
        self.current_frame += 1

    def handle_late_input(self, target_frame, actual_inputs, context, compiled_graph):
        print(
            f"\n[!] LATE NETWORK PACKET: Frame {target_frame} inputs = {actual_inputs}"
        )
        self.input_log[target_frame] = actual_inputs

        print(f"[ROLLBACK] Rewinding to Frame {target_frame - 1}...")
        restored_state = copy.deepcopy(self.state_buffer[target_frame - 1])

        print(
            f"[ROLLBACK] Fast-Forwarding {target_frame} -> {self.current_frame - 1}..."
        )
        for frame in range(target_frame, self.current_frame):
            inputs = self.input_log.get(frame)
            self._simulate_frame(frame, restored_state, inputs, compiled_graph)
            self.state_buffer[frame] = copy.deepcopy(restored_state)

        context.clear()
        context.update(restored_state)
        print(
            f"[ROLLBACK] Synchronized. Corrected Pos X: {context['Transform']['player_1']['x']}\n"
        )


# --- EXECUTION HARNESS ---
if __name__ == "__main__":
    # Initial State
    global_context = {
        "Transform": {"player_1": {"x": 0}},
        "Velocity": {"player_1": {"dx": 1}},
    }

    # Phase 2 Compiled Graph (1 Layer, 1 System)
    compiled_graph = [[MovementSystem()]]
    engine = RollbackEngine()

    print("--- INITIATING NORMAL SIMULATION ---")
    for _ in range(4):
        engine.step(global_context, compiled_graph)

    # FRAME 4: Late packet arrives. Player actually dashed on Frame 2.
    engine.handle_late_input(2, {"player_1": "DASH"}, global_context, compiled_graph)

    print("--- RESUMING NORMAL SIMULATION ---")
    engine.step(global_context, compiled_graph)
