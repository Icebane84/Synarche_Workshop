# ecs/ecs_scheduler.py

from typing import Set


def apply_delta(world, delta, seen: Set):
    reg = world.registry

    # Mutations
    for comp_type, updates in delta.get("mutations", {}).items():
        for eid, value in updates.items():
            key = (comp_type, eid)
            if key in seen:
                raise RuntimeError("Determinism violation: double write")

            seen.add(key)

            sig, row = reg._entity_index[eid]
            arch = reg._archetypes[sig]

            arch.columns[comp_type][row] = value


class SystemTask:
    def __init__(self, system):
        self.system = system
        self.execution_index = system.execution_index

    def compute_pure(self, world):
        return self.system.compute(world)


class ECSScheduler:
    def __init__(self, executor, layers):
        self.executor = executor
        self.layers = layers

    def run_frame(self, world):
        for layer in self.layers:
            results = self.executor.execute_layer(layer, world)

            seen = set()

            for _, delta in sorted(results.items()):
                apply_delta(world, delta, seen)
