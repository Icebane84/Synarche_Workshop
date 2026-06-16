import pytest
from src.engine.ecs.compiler import ECSSystemCompiler
from src.engine.ecs.resonance import ResonanceRegistry, ResonanceDomain
from src.engine.ecs.world import World
from src.engine.scheduling.layered_scheduler import LayeredScheduler
from src.system.refactor.parallel_executor_v2 import DeterministicParallelExecutor


class MockECSSystem:
    def __init__(self, name, execution_index, reads=None, writes=None, accumulates=None):
        self.name = name
        self.execution_index = execution_index
        self.reads = reads or set()
        self.writes = writes or set()
        self.accumulates = accumulates or set()
        self.called = False
        self.context_received = None

    def compute(self, world, entities):
        self.called = True
        self.context_received = world
        # Return a structured delta packet
        return {
            "writes": {f"{self.name}_output": "success"}
        }


def test_ecs_compiler_dependency_resolution():
    # Setup ResonanceRegistry and register systems
    registry = ResonanceRegistry()

    # System A (execution_index=1): writes to 'pos'
    sys_a = MockECSSystem("SystemA", 1, writes={"pos"})
    # System B (execution_index=2): reads 'pos', writes to 'vel'
    sys_b = MockECSSystem("SystemB", 2, reads={"pos"}, writes={"vel"})
    # System C (execution_index=3): reads 'vel'
    sys_c = MockECSSystem("SystemC", 3, reads={"vel"})

    registry.register_system(sys_a)
    registry.register_system(sys_b)
    registry.register_system(sys_c)

    # Pull from registry and compile
    systems = registry.get_systems()
    assert len(systems) == 3

    compiler = ECSSystemCompiler(systems)
    graph = compiler.compile()
    graph.build()

    # Verify dependency layers
    assert len(graph.layers) == 3
    # Layer 0: SystemA
    assert graph.layers[0][0].name == "SystemA"
    # Layer 1: SystemB (depends on A)
    assert graph.layers[1][0].name == "SystemB"
    # Layer 2: SystemC (depends on B)
    assert graph.layers[2][0].name == "SystemC"


def test_ecs_scheduler_execution_with_world():
    # Setup resonance registry and systems
    registry = ResonanceRegistry()
    sys_a = MockECSSystem("SystemA", 1, writes={"pos"})
    sys_b = MockECSSystem("SystemB", 2, reads={"pos"}, writes={"vel"})

    registry.register_system(sys_a)
    registry.register_system(sys_b)

    # Compile systems into graph
    systems = registry.get_systems()
    compiler = ECSSystemCompiler(systems)
    graph = compiler.compile()
    graph.build()

    # Run scheduler
    executor = DeterministicParallelExecutor(max_workers=2)
    scheduler = LayeredScheduler(graph, executor)

    world = World()
    context = {"world": world}

    scheduler.execute(context)

    # Assert systems were executed
    assert sys_a.called
    assert sys_b.called
    assert context.get("SystemA_output") == "success"
    assert context.get("SystemB_output") == "success"
