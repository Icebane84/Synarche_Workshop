"""Artifact ID: CORE-FDE-EXEC-003-V2
Ethos: Concurrency bounded by Absolute Order and Explicit Conflict.
"""

import concurrent.futures
import copy
from typing import Any, Dict, List


class DeterministicParallelExecutor:
    """Executes a pre-compiled layer of independent tasks.
    Enforces Strict Isolation, Structured Deltas, and Conflict Detection.
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def execute_layer(self, layer: List[Any], global_context: Dict[str, Any]) -> None:
        buffered_deltas = {}

        # PHASE 1: PARALLEL COMPUTATION (STRICT ISOLATION)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as pool:
            future_to_task = {}
            for task in layer:
                # 1. Enforce strict read-only via deepcopy (Correctness over Speed)
                safe_context = copy.deepcopy(global_context)
                future = pool.submit(task.compute_pure, safe_context)
                future_to_task[future] = task

            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    delta_packet = future.result()
                    # 2. Use stable execution IDs, not names
                    buffered_deltas[task.execution_index] = delta_packet
                except Exception as exc:
                    raise RuntimeError(
                        f"Task {task.execution_index} ({task.name}) failed: {exc}"
                    )

        # PHASE 2: DETERMINISTIC MERGE & CONFLICT DETECTION
        seen_keys = set()

        for exec_index in sorted(buffered_deltas.keys()):
            delta = buffered_deltas[exec_index]
            self._apply_delta_to_context(global_context, delta, seen_keys, exec_index)

    def _apply_delta_to_context(
        self,
        context: Dict[str, Any],
        delta: Dict[str, Any],
        seen_keys: set,
        exec_index: int,
    ) -> None:
        if not delta:
            return

        writes = delta.get("writes", {})
        accumulate = delta.get("accumulate", {})

        # 3. Process Strict Writes (Fail-fast on conflict)
        for key, value in writes.items():
            if key in seen_keys:
                raise RuntimeError(
                    f"Determinism violation: Task {exec_index} attempted multiple writes to '{key}'"
                )
            seen_keys.add(key)
            context[key] = value

        # 4. Process Accumulations (Order-independent math)
        for key, val in accumulate.items():
            # Example: Safe concurrent accumulation of "damage_taken"
            context[key] = context.get(key, 0) + val
