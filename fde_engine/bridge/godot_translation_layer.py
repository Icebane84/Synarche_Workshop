from typing import Any, Dict
from fde_engine.systems.movement_system import Position, Velocity


class GodotTranslationLayer:
    """Translates FDE simulation state into Godot visual/rendering node state payload."""

    @staticmethod
    def export_render_nodes(world) -> Dict[int, dict]:
        """Extracts position and velocity for rendering nodes."""
        nodes = {}
        for sig, arch in world.registry._archetypes.items():
            if Position in sig:
                positions = arch.columns[Position]
                velocities = arch.columns.get(Velocity)
                for i in range(arch.size):
                    eid = arch.entity_ids[i]
                    p = positions[i]
                    v = velocities[i] if velocities else None
                    nodes[eid] = {
                        "position": {"x": p.x, "y": p.y} if p else None,
                        "velocity": {"dx": v.dx, "dy": v.dy} if v else None,
                    }
        return nodes

