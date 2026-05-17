"""ID: SEED-MEMORY-001
Objective: Seed the prs_db with initial memories for testing.
"""

from src.logic.memory.memory_system import MemorySystem


def seed():
    mem = MemorySystem()
    seeds = [
        ("The Phoenix Codex establishes the Supreme Law of the Synarche.", 1.0, ["law", "codex"]),
        ("Axion is the primary agent of the Synarche, governed by the Hierophant.", 0.9, ["agent", "axion"]),
        ("Gemini Gem provides the cognitive layer for emotional and semantic understanding.", 0.8, ["gemini", "cognition"]),
        ("Emerald City is a metaphor for the target architecture state.", 0.5, ["lore"]),
    ]
    
    for content, relevance, tags in seeds:
        print(f"Seeding: {content[:30]}...")
        mem.add_memory(content, relevance, tags)
    
    print("Seed Complete.")

if __name__ == "__main__":
    seed()
