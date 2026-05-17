from core.engine_runtime import EngineRuntime
from core.parallel_executor import DeterministicParallelExecutor
from dag.dag_compiler import DAGCompiler
from ecs.ecs_scheduler import ECSScheduler, SystemTask
from ecs.world import World
from systems.example_system import ExampleSystem
from core.chunk_executor import ChunkExecutor


def main():
    world = World()

    systems = [ExampleSystem()]
    compiler = DAGCompiler(systems)
    layers = compiler.compile_layers()

    wrapped = [[SystemTask(s) for s in layer] for layer in layers]

    executor = ChunkExecutor(max_workers=4, chunk_size=128)

    scheduler = ECSScheduler(executor, wrapped)

    engine = EngineRuntime(world, scheduler)

    for _ in range(5):
        engine.tick({})


if __name__ == "__main__":
    main()
# demo/bootstrap.py


def main():
    world = World()

    # spawn test entities
    world.spawn({})
    world.spawn({})
