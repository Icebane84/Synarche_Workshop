"""Artifact ID: CORE-FDE-DAG-009
Ethos: Time is Directed; Data is Typed.
"""

from collections import defaultdict
from typing import List, Set, Type


class SystemSignature:
    """The strictly enforced contract for all FDE Systems."""

    name: str = "Unknown"
    execution_index: int = 0
    reads: Set[Type] = set()
    writes: Set[Type] = set()
    accumulates: Set[Type] = set()


class DAGCompiler:
    """Compiles deterministic parallel layers from System read/write signatures."""

    def __init__(self, systems: List[SystemSignature]):
        self.systems = systems
        self._validate_system_integrity()

    def _validate_system_integrity(self) -> None:
        """Fail-fast validation to ensure no ambiguous temporal states exist."""
        seen_indices = set()
        for s in self.systems:
            if s.execution_index in seen_indices:
                raise RuntimeError(
                    f"FDE Violation: Duplicate execution_index {s.execution_index} detected on '{s.name}'. "
                    "All systems must possess a unique temporal anchor."
                )
            seen_indices.add(s.execution_index)

            # Ensure a system doesn't declare a component in multiple conflicting modes
            intersection = s.writes & s.accumulates
            if intersection:
                raise RuntimeError(
                    f"FDE Violation: '{s.name}' cannot both write and accumulate {intersection}"
                )

    def build_graph(self):
        graph = defaultdict(set)  # node -> set(dependents)
        indegree = {s: 0 for s in self.systems}

        for a in self.systems:
            for b in self.systems:
                if a == b:
                    continue

                if self._depends(a, b):
                    graph[a].add(b)
                    indegree[b] += 1

        return graph, indegree

    def _depends(self, a: SystemSignature, b: SystemSignature) -> bool:
        """Determines if A must completely execute before B can begin."""
        # Temporal Directive: Edges can ONLY flow forward in time.
        if a.execution_index >= b.execution_index:
            return False

        # Semantic Data Overlaps
        write_read = a.writes & b.reads
        read_write = a.reads & b.writes
        write_write = a.writes & b.writes

        # Accumulate interactions
        write_accum = a.writes & b.accumulates
        accum_write = a.accumulates & b.writes
        read_accum = a.reads & b.accumulates
        accum_read = a.accumulates & b.reads

        # NOTE: (a.accumulates & b.accumulates) is explicitly EXCLUDED.
        # They can safely run in parallel.

        return bool(
            write_read
            or read_write
            or write_write
            or write_accum
            or accum_write
            or read_accum
            or accum_read
        )

    def compile_layers(self) -> List[List[SystemSignature]]:
        graph, indegree = self.build_graph()

        # Deterministic chronological baseline
        systems_sorted = sorted(self.systems, key=lambda s: s.execution_index)

        layers = []
        remaining = set(systems_sorted)

        while remaining:
            # Find all nodes whose prerequisites have fully executed
            ready = [s for s in systems_sorted if s in remaining and indegree[s] == 0]

            if not ready:
                raise RuntimeError(
                    "FDE Violation: Unresolvable cyclic dependency detected in System logic."
                )

            # Enforce absolute internal layer ordering
            ready.sort(key=lambda s: s.execution_index)
            layers.append(ready)

            for s in ready:
                remaining.remove(s)
                for neighbor in graph[s]:
                    indegree[neighbor] -= 1

        return layers
