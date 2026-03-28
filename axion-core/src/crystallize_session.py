"""
⚡ CRYSTALLIZE: Session L4 Memory Canonization
VERSION: v15.0 [OMEGA]
DOMAIN: CORE.LOGIC.MEMORY
"""

import asyncio
import os
import sys
from pathlib import Path

from logic.memory.memory_system import MemorySystem

# Anchor to axion-core
ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR / "src"))


async def crystallize():
    print("Initiating Crystallization Sequence...")

    # 1. Load Distillates
    distillate_path = Path(
        r"C:\Users\Chris\.gemini\antigravity\brain\d0961d9f-38fa-4015-8e8d-69ecf7c881a6\crystalline_distillates_XXXVI.md"
    )
    if not distillate_path.exists():
        print(f"Error: Distillate not found at {distillate_path}")
        return

    with open(distillate_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. Initialize Memory System
    mem_sys = MemorySystem()

    # 4. Canonize to L4 Sovereign Layer
    memory_id = mem_sys.add_memory(
        content=content,
        domain="SovereignSynthesis",
        relevance=1.0,
        confidence=1.0,
        tags=["OMEGA-V15", "CrystallineDistillate", "CognitiveLoom", "PhaseXXXVI"],
        source="crystalline_distillates_XXXVI.md",
        layer=4,  # LAYER_SOVEREIGN
    )

    if memory_id != -1:
        print(
            f"SUCCESS: Crystalline Distillate canonized to L4 Memory (ID: {memory_id})"
        )
        print("Divine Bridge: Cloud mirroring initiated via MemorySystem hooks.")
    else:
        print("FAILURE: Crystallization failed at the substrate level.")


if __name__ == "__main__":
    asyncio.run(crystallize())
