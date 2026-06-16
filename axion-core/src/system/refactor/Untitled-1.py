"""
artifact_anchor:
  id: CORE.UNTITLED-1.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""


class CompiledGraph:
    def __init__(self, tasks):
        self.tasks = tasks
        self.layers = []

    def build(self):
        remaining = set(self.tasks)
        resolved = set()

        while remaining:
            layer = [t for t in remaining if all(d in resolved for d in t.deps)]

            if not layer:
                raise RuntimeError("Cycle detected")

            # deterministic ordering inside layer
            layer = sorted(layer, key=lambda t: t.name)

            self.layers.append(layer)

            for t in layer:
                remaining.remove(t)
                resolved.add(t)


class LayeredScheduler:
    def __init__(self, compiled_graph):
        self.graph = compiled_graph

    def execute(self, context):
        for i, layer in enumerate(self.graph.layers):
            print(f"[LAYER {i}]")

            for task in layer:
                print(f"  → {task.name}")
                task.run(context)
