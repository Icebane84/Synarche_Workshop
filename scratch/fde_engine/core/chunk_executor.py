"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-CORE-CHUNK_EXECUTOR` | The Sovereign ID. |
| **Official Name** | `chunk_executor.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `CORE`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""

# core/chunk_executor.py

import concurrent.futures


class ArchetypeChunk:
    def __init__(self, archetype, start, end):
        self.archetype = archetype
        self.start = start
        self.end = end


class ChunkExecutor:
    def __init__(self, max_workers=4, chunk_size=256):
        self.max_workers = max_workers
        self.chunk_size = chunk_size

    def execute_layer(self, layer, world):
        futures = {}
        results = {}

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as pool:
            for task in layer:
                system = task.system

                # 1. get matching archetypes
                arches = system.query(world)

                # 2. split into chunks
                for arch in arches:
                    total = len(arch.entity_ids)

                    for i in range(0, total, self.chunk_size):
                        chunk = ArchetypeChunk(arch, i, min(i + self.chunk_size, total))

                        future = pool.submit(system.compute_chunk, world, chunk)
                        futures[future] = task.execution_index

            # 3. collect results
            for f in concurrent.futures.as_completed(futures):
                idx = futures[f]
                delta = f.result()

                if idx not in results:
                    results[idx] = {"mutations": {}}

                self._merge(results[idx], delta)

        return results

    def _merge(self, master, delta):
        for comp, updates in delta.get("mutations", {}).items():
            master["mutations"].setdefault(comp, {}).update(updates)
