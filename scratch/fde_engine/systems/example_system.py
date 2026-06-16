# systems/example_system.py


class ExampleSystem:
    execution_index = 1

    def compute(self, world):
        count = 0

        for arch in world.registry._archetypes.values():
            count += len(arch.entity_ids)

        return {"mutations": {}, "log": f"Entities: {count} | Frame: {world.frame}"}
