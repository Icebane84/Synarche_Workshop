"""Artifact ID: CORE-FDE-ECS-005
Ethos: Data is contiguous; Logic is stateless.
"""

from typing import Any, Dict, List


class SystemTask:
    """Base class for all ECS Systems.
    Functions as a Task node in the CompiledGraph.
    """

    def __init__(self, name: str, execution_index: int, required_components: List[str]):
        self.name = name
        self.execution_index = execution_index
        self.required_components = required_components
        self.deps = []  # Used by CompiledGraph to determine Layering

    def compute_pure(self, read_only_context: Dict[str, Any]) -> Dict[str, Any]:
        """The Map phase. Must be overridden by specific systems.
        Returns a structured delta packet: {"writes": {}, "accumulate": {}}.
        """
        raise NotImplementedError


class MovementSystem(SystemTask):
    def __init__(self, execution_index: int):
        super().__init__(
            name="MovementSystem",
            execution_index=execution_index,
            required_components=["Transform", "Velocity"],
        )

    def compute_pure(self, context: Dict[str, Any]) -> Dict[str, Any]:
        delta_writes = {"Transform": {}}

        transforms = context.get("Transform", {})
        velocities = context.get("Velocity", {})

        # 1. Query: Find intersection of entities with both components
        active_entities = set(transforms.keys()).intersection(velocities.keys())

        # 2. Compute logic
        for ent_id in active_entities:
            pos = transforms[ent_id]
            vel = velocities[ent_id]

            new_x = pos["x"] + vel["dx"]
            new_y = pos["y"] + vel["dy"]

            # 3. Buffer the write
            delta_writes["Transform"][ent_id] = {"x": new_x, "y": new_y}

        # 4. Emit structured packet
        return {"writes": delta_writes}
