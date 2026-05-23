"""Artifact ID: CORE-FDE-ECS-SCH-001
Ethos: Logic Must Be Bound.
"""

from typing import Any, Dict, List

from .ecs_hardened_core import apply_ecs_delta


class SystemTask:
    """Wrapper that forces an ECS System to behave like a DAG Task."""

    def __init__(self, system_instance):
        self.system = system_instance
        self.name = system_instance.name
        self.execution_index = system_instance.execution_index

    def compute_pure(self, world_read_only) -> Dict[str, Any]:
        """Executes the System's logic without allowing direct mutation."""
        entities = self.system.query(world_read_only)
        return self.system.compute(world_read_only, entities)


class ECSScheduler:
    """Binds the DAG layers to the Phase 3 Deterministic Parallel Executor."""

    def __init__(self, executor, layers: List[List[SystemTask]]):
        self.executor = executor
        self.layers = layers

    def run_frame(self, world) -> None:
        """Executes the entire compiled graph for a single frame."""
        for _layer_index, layer in enumerate(self.layers):
            buffered_deltas = {}

            # 1. Execute the horizontal band in parallel
            for task in layer:
                # In a real multi-threading environment, the executor handles this.
                # For this binding, we simulate the executor's pure requirement.
                delta_packet = task.compute_pure(world)
                buffered_deltas[task.execution_index] = delta_packet

            # 2. Deterministic Commit Phase
            seen_mutations = set()
            for exec_index in sorted(buffered_deltas.keys()):
                delta = buffered_deltas[exec_index]
                apply_ecs_delta(world, delta, seen_mutations)
