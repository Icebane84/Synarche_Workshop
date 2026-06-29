"""HARVESTED LOGIC: Sanity & Resonance System
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
        # Structure-specific modifiers
        self.SPIRE_DRAIN_PENALTY = 0.1
        self.SANCTUM_PULL_STRENGTH = 1.0
        self.SPIRE_PULL_STRENGTH = 1.0
        # Data-driven hallucination thresholds (sanity, level name)
        # Sorted from most severe to least severe.
        self.HALLUCINATION_THRESHOLDS = [
            (10, "SEVERE"),
            (30, "MODERATE"),
        ]

        # World State (Simulated)
        self.structures = {
            "sanctum": 0,  # Pulls to Light
            "spire": 0,  # Pulls to Shadow
        }

        self.resources = {"faith": 0, "doubt": 0, "resolve": 0}

    def update(self, delta_time: float = 1.0) -> dict:
        """Runs one tick of the psyche simulation."""
        # 1. Calculate Drain
        drain = self.PASSIVE_DRAIN
        # Spire penalty
        drain += self.structures["spire"] * self.SPIRE_DRAIN_PENALTY

        # Apply Drain
        self.sanity = max(0.0, self.sanity - drain)

        # 2. Calculate Resonance Drift
        pull = 0.0
        # Light Pull (Sanctum)
        pull -= self.structures["sanctum"] * self.SANCTUM_PULL_STRENGTH
        # Shadow Pull (Spire)
        pull += self.structures["spire"] * self.SPIRE_PULL_STRENGTH

        # Apply Drift
        self.resonance += pull * self.RESONANCE_DRIFT_RATE
        self.resonance = max(0.0, min(100.0, self.resonance))

        # 3. Determine Hallucination Level (Data-Driven)
        hallucination_level = "None"
        for threshold, level in self.HALLUCINATION_THRESHOLDS:
            if self.sanity < threshold:
                hallucination_level = level
                break  # First match wins

        return {
            "sanity": self.sanity,
            "resonance": self.resonance,
            "hallucination": hallucination_level,
        }

    # --- Resource & Structure Interaction Methods ---

    def pray(self, amount: int = 1):
        """Increases the 'faith' resource."""
        self.resources["faith"] += amount
        print(f"Action: Prayed. Faith increased to: {self.resources['faith']}")

    def embrace_doubt(self, amount: int = 5, sanity_cost: float = 2.0):
        """Gain 'doubt' at the cost of sanity."""
        self.resources["doubt"] += amount
        self.sanity = max(0.0, self.sanity - sanity_cost)
        print(f"Action: Embraced doubt. Gained {amount} doubt, lost {sanity_cost} sanity.")

    def focus_resolve(self):
        """Increases 'resolve' and recovers a small amount of sanity."""
        self.resources["resolve"] += 1
        self.sanity = min(100.0, self.sanity + self.SANITY_RECOVERY_ON_RESOLVE)
        print(f"Action: Focused. Sanity Restored. Current: {self.sanity:.2f}")

    def build_spire(self, cost: int = 10):
        """Consumes 'doubt' to build a Spire, pulling Resonance to Shadow."""
        if self.resources["doubt"] >= cost:
            self.resources["doubt"] -= cost
            self.structures["spire"] += 1
            print(f"Action: Built Spire (cost: {cost} doubt). Total: {self.structures['spire']}.")
        else:
            print(f"Action Failed: Not enough Doubt to build Spire. Have {self.resources['doubt']}, need {cost}.")

    def build_sanctum(self, cost: int = 10):
        """Consumes 'faith' to build a Sanctum, pulling Resonance to Light."""
        if self.resources["faith"] >= cost:
            self.resources["faith"] -= cost
            self.structures["sanctum"] += 1
            print(f"Action: Built Sanctum (cost: {cost} faith). Total: {self.structures['sanctum']}.")
        else:
            print(f"Action Failed: Not enough Faith to build Sanctum. Have {self.resources['faith']}, need {cost}.")

    def interact(self, action: str, **kwargs):
        """
        Simulates a player action by dispatching to a specific method.
        Useful for text-based commands or simple event systems.
        """
        action_map = {
            "pray": self.pray,
            "focus": self.focus_resolve,
            "build_spire": self.build_spire,
            "build_sanctum": self.build_sanctum,
            "embrace_doubt": self.embrace_doubt,
        }
        method = action_map.get(action)
        if method:
            method(**kwargs)
        else:
            print(f"Unknown action: {action}")


# --- Text-Based Simulation ---
if __name__ == "__main__":
    system = PsycheSystem()
    print("--- Ashen Oath Logic Prototype ---")
    print(f"Initial State: Sanity={system.sanity:.2f}, Resonance={system.resonance:.2f}")
    print("-" * 20)

    # Simulate a player building a Spire and waiting
    print(">> Scenario 1: Embracing the Shadow")
    system.resources["doubt"] = 20  # Cheat to give resources
    system.build_spire()
    system.embrace_doubt()

    for i in range(5):
        state = system.update()
        print(
            f"  Tick {i + 1}: Sanity={state['sanity']:.2f} | Resonance={state['resonance']:.2f} | Effect={state['hallucination']}"
        )
        time.sleep(0.1)

    print("-" * 20)
    print(">> Scenario 2: Seeking the Light")
    # Reset state for second scenario for clarity
    system.sanity = 80.0
    system.resonance = 50.0
    system.resources["faith"] = 15
    print(f"State Reset: Sanity={system.sanity:.2f}, Resonance={system.resonance:.2f}")

    system.build_sanctum()
    system.pray()
    system.focus_resolve()

    for i in range(5):
        state = system.update()
        print(
            f"  Tick {i + 1}: Sanity={state['sanity']:.2f} | Resonance={state['resonance']:.2f} | Effect={state['hallucination']}"
        )
        time.sleep(0.1)
