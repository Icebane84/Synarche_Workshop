class LawValidator:
    """Enforces zero-entropy state validation and runtime invariants."""

    @staticmethod
    def validate_world(world) -> bool:
        """Verifies that entity registry and archetype indices remain 100% coherent."""
        reg = world.registry
        for eid, (sig, row) in reg._entity_index.items():
            if eid not in reg.alive:
                raise ValueError(f"State Dissonance: Entity {eid} in index but not marked alive.")
            if sig not in reg._archetypes:
                raise ValueError(f"State Dissonance: Archetype signature {sig} missing from registry.")
            arch = reg._archetypes[sig]
            if row >= arch.size:
                raise ValueError(f"State Dissonance: Row index {row} exceeds archetype size {arch.size}.")
            if arch.entity_ids[row] != eid:
                raise ValueError(f"State Dissonance: Row {row} eid mismatch ({arch.entity_ids[row]} != {eid}).")
        return True

