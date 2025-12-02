"""
HARVESTED LOGIC: Sanity & Resonance System
Origin: Ashen Oath Inner Flame Echoes (script.js)
Purpose: Prototype the mathematical model for the 3rd Person Game.
"""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP


import time


class PsycheSystem:
    def __init__(self):
        self.sanity = 100.0
        self.resonance = 50.0  # 0 = Light, 100 = Shadow

        # Configuration (Harvested from gameConfig)
        self.PASSIVE_DRAIN = 0.2
        self.RESONANCE_DRIFT_RATE = 0.1
        self.SANITY_RECOVERY_ON_RESOLVE = 2.0

        # World State (Simulated)
        self.structures = {
            "sanctum": 0,  # Pulls to Light
            "spire": 0,  # Pulls to Shadow
        }

        self.resources = {"faith": 0, "doubt": 0, "resolve": 0}

    def update(self, delta_time: float = 1.0):
        """
        Runs one tick of the psyche simulation.
        """
        # 1. Calculate Drain
        drain = self.PASSIVE_DRAIN
        # Spire penalty
        drain += self.structures["spire"] * 0.1

        # Apply Drain
        self.sanity = max(0.0, self.sanity - drain)

        # 2. Calculate Resonance Drift
        pull = 0.0
        # Light Pull (Sanctum)
        pull -= self.structures["sanctum"] * 1.0
        # Shadow Pull (Spire)
        pull += self.structures["spire"] * 1.0

        # Apply Drift
        self.resonance += pull * self.RESONANCE_DRIFT_RATE
        self.resonance = max(0.0, min(100.0, self.resonance))

        # 3. Trigger Hallucinations?
        hallucination_level = "None"
        if self.sanity < 10:
            hallucination_level = "SEVERE"
        elif self.sanity < 30:
            hallucination_level = "MODERATE"

        return {
            "sanity": self.sanity,
            "resonance": self.resonance,
            "hallucination": hallucination_level,
        }

    def interact(self, action: str):
        """
        Simulates player action.
        """
        if action == "pray":
            self.resources["faith"] += 1
            print(f"Action: Prayed. Faith: {self.resources['faith']}")

        elif action == "focus":
            self.resources["resolve"] += 1
            self.sanity = min(100.0, self.sanity + self.SANITY_RECOVERY_ON_RESOLVE)
            print(f"Action: Focused. Sanity Restored. Current: {self.sanity:.2f}")

        elif action == "build_spire":
            if self.resources["doubt"] >= 10:
                self.resources["doubt"] -= 10
                self.structures["spire"] += 1
                print("Action: Built Spire (Resonance will drift to Shadow)")
            else:
                print("Not enough Doubt.")


# --- Text-Based Simulation ---
if __name__ == "__main__":
    system = PsycheSystem()
    print("--- Ashen Oath Logic Prototype ---")
    print(f"Initial Sanity: {system.sanity}")

    # Simulate a player building a Spire and waiting
    system.resources["doubt"] = 20  # Cheat
    system.interact("build_spire")

    for i in range(10):
        state = system.update()
        print(
            f"Tick {i + 1}: Sanity={state['sanity']:.2f} | Resonance={state['resonance']:.2f} | Effect={state['hallucination']}"
        )
        time.sleep(0.1)
