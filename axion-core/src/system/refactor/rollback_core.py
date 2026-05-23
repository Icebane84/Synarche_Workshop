"""Artifact ID: CORE-FDE-ROLLBACK-004
Ethos: Time is fluid; State is absolute.
"""

import copy
from typing import Any


class InputLog:
    def __init__(self):
        self._log = {}  # {frame_number: {"p1": input, "p2": input}}
        self._predicted_frames = set()

    def record_input(
        self, frame: int, player_id: str, input_data: Any, is_predicted: bool = False
    ):
        if frame not in self._log:
            self._log[frame] = {}
        self._log[frame][player_id] = input_data

        if is_predicted:
            self._predicted_frames.add(frame)
        elif frame in self._predicted_frames:
            self._predicted_frames.remove(frame)

    def verify_and_get_mismatch(
        self, frame: int, player_id: str, actual_input: Any
    ) -> bool:
        """Returns True if the actual input contradicts our prediction."""
        predicted = self._log.get(frame, {}).get(player_id)
        return predicted != actual_input


class StateSnapshotBuffer:
    def __init__(self, max_frames: int = 60):
        self.max_frames = max_frames
        self._buffer = {}  # {frame_number: deep_copied_context}
        self.latest_verified_frame = 0

    def save_snapshot(self, frame: int, context: dict[str, Any]):
        # Must be a deep copy to ensure the FDE anchor cannot be mutated
        self._buffer[frame] = copy.deepcopy(context)

        # Cleanup old frames to prevent memory leaks
        if frame - self.max_frames in self._buffer:
            del self._buffer[frame - self.max_frames]

    def load_snapshot(self, frame: int) -> dict[str, Any]:
        if frame not in self._buffer:
            raise RuntimeError(f"CRITICAL: Rollback frame {frame} dropped from buffer.")
        return copy.deepcopy(self._buffer[frame])


class ResimulationEngine:
    def __init__(
        self, executor, input_log: InputLog, state_buffer: StateSnapshotBuffer
    ):
        self.executor = executor  # Phase 3 DeterministicParallelExecutor
        self.input_log = input_log
        self.state_buffer = state_buffer
        self.current_frame = 0

    def handle_network_input(
        self,
        target_frame: int,
        player_id: str,
        actual_input: Any,
        current_context: dict[str, Any],
        task_layer: list[Any],
    ):
        """Triggered when delayed remote input arrives."""
        mismatch = self.input_log.verify_and_get_mismatch(
            target_frame, player_id, actual_input
        )

        # Update the log with the absolute truth
        self.input_log.record_input(
            target_frame, player_id, actual_input, is_predicted=False
        )

        if mismatch:
            self._execute_rollback(target_frame, current_context, task_layer)
        else:
            # Prediction was correct. Mark snapshot as verified.
            self.state_buffer.latest_verified_frame = max(
                self.state_buffer.latest_verified_frame, target_frame
            )

    def _execute_rollback(
        self, target_frame: int, context: dict[str, Any], task_layer: list[Any]
    ):
        """The Time Machine."""
        print(
            f"[ROLLBACK] Mismatch at Frame {target_frame}. Initiating Resimulation..."
        )

        # 1. Rewind: Load the state from right before the mismatch
        restored_state = self.state_buffer.load_snapshot(target_frame - 1)

        # 2. Fast-Forward: Replay from the target_frame up to the current_frame
        for frame_to_simulate in range(target_frame, self.current_frame + 1):
            # Inject the historical/corrected inputs for this specific frame into the context
            restored_state["current_inputs"] = self.input_log._log.get(
                frame_to_simulate, {}
            )

            # 3. Recompute: Feed the state through the strict Phase 3 Executor
            self.executor.execute_layer(task_layer, restored_state)

            # Re-save the corrected snapshots as we step forward
            self.state_buffer.save_snapshot(frame_to_simulate, restored_state)

        # 4. Finalize: Mutate the live context to the corrected present state
        context.clear()
        context.update(restored_state)
        print(f"[ROLLBACK] Frame {self.current_frame} successfully synchronized.")
