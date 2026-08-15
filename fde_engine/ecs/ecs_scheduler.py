from typing import Any, List
from fde_engine.core.chunk_executor import ChunkExecutor
from fde_engine.ecs.commit_layer import CommandCommitter


class SystemTask:
    def __init__(self, system):
        self.system = system
        self.execution_index = getattr(system, "execution_index", 0)


class ECSScheduler:
    def __init__(self, executor: ChunkExecutor = None, layers: List[List[SystemTask]] = None):
        self.executor = executor or ChunkExecutor()
        self.layers = layers or []
        self.committer = CommandCommitter()

    def run_frame(self, world) -> None:
        reg = world.registry
        for layer in self.layers:
            results = self.executor.execute_layer(layer, world)
            # Apply state mutations deterministically
            for _idx, delta in results.items():
                for comp_type, updates in delta.get("mutations", {}).items():
                    for eid, val in updates.items():
                        if eid in reg._entity_index:
                            sig, row = reg._entity_index[eid]
                            if sig in reg._archetypes and comp_type in reg._archetypes[sig].columns:
                                reg._archetypes[sig].columns[comp_type][row] = val

