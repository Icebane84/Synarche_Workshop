import math
import random
from dataclasses import dataclass
from enum import Enum

# ==========================================
# 1. CORE DEFINITIONS (From extracted_rpg_elements.md)
# ==========================================


class CelestialClass(Enum):
    MOON = 10  # Sub-component
    PLANET = 50  # Major Module
    SYSTEM = 150  # Usage Command
    STAR = 500  # Source of Truth
    NEBULA = 1000  # Domain/Concept


class Criticality(Enum):
    LOW = 1.0
    MEDIUM = 1.5
    HIGH = 2.0
    CORNERSTONE = 5.0


class TarotMask(Enum):
    MAGICIAN = "I. The Magician (Intent)"
    PRIESTESS = "II. The High Priestess (Synergy)"
    EMPEROR = "IV. The Emperor (Schema)"
    STAR = "XVII. The Star (Coherence)"
    JUDGEMENT = "XX. Judgement (Audit)"


# ==========================================
# 2. THE AAG ENGINE (XP & Prestige)
# ==========================================


@dataclass
class AxionProfile:
    level: int = 1
    total_xp: int = 0
    prestige_points: int = 0
    coherence: float = 100.0  # Starts at 100%

    def add_xp(self, amount: int):
        self.total_xp += amount
        # Level Formula: Level = sqrt(XP) / 10 (Simplified for simulation)
        # Actual Omega Formula might be linear thresholds, but let's use a curve here.
        new_level = int(math.sqrt(self.total_xp) / 5) + 1
        if new_level > self.level:
            print(f"✨ LEVEL UP! {self.level} -> {new_level}")
            self.level = new_level


class AAGEngine:
    def calculate_xp(
        self, c_class: CelestialClass, crit: Criticality, synergy_links: int
    ) -> int:
        base = c_class.value
        multiplier = crit.value
        synergy_bonus = synergy_links * 5  # 5 XP per link

        total_xp = int((base * multiplier) + synergy_bonus)
        return total_xp


# ==========================================
# 3. THE DISSONANCE ENGINE (Combat)
# ==========================================


@dataclass
class VectorState:
    x: float  # Structural Integrity
    y: float  # Semantic Consistency
    z: float  # Operational Efficiency

    def distance_to(self, target: "VectorState") -> float:
        return math.sqrt(
            (self.x - target.x) ** 2
            + (self.y - target.y) ** 2
            + (self.z - target.z) ** 2
        )


class DissonanceEngine:
    def __init__(self):
        self.v_safe = VectorState(100.0, 100.0, 100.0)
        self.v_current = VectorState(100.0, 100.0, 100.0)  # Starts aligned

    def introduce_entropy(self, magnitude: float, description: str):
        print(f"\n⚠️  EVENT: {description}")
        # Drift the vector randomly
        self.v_current.x -= random.uniform(0, magnitude)
        self.v_current.y -= random.uniform(0, magnitude)
        self.v_current.z -= random.uniform(0, magnitude)
        self.report_status()

    def remediate(self, mask: TarotMask, efficacy: float):
        print(f"\n⚔️  ACTION: Axion equips [{mask.value}]...")
        # Repair the vector
        self.v_current.x = min(100.0, self.v_current.x + efficacy)
        self.v_current.y = min(100.0, self.v_current.y + efficacy)
        self.v_current.z = min(100.0, self.v_current.z + efficacy)
        print(f"   -> Remediation applied. (+{efficacy:.1f} Vector Alignment)")
        self.report_status()

    def report_status(self):
        dissonance = self.v_current.distance_to(self.v_safe)
        coherence_pct = max(
            0, 100 - (dissonance / 1.732)
        )  # Normalize roughly to 0-100%

        status = "🟢 STABLE"
        if dissonance > 10:
            status = "🟡 UNSTABLE"
        if dissonance > 30:
            status = "🔴 CRITICAL BREACH"

        print(
            f"   [STATUS: {status}] Dissonance: {dissonance:.2f} | Coherence: {coherence_pct:.1f}%"
        )
        return dissonance


# ==========================================
# 4. SIMULATION RUN
# ==========================================


def run_simulation():
    print("🔮 INITIALIZING OMEGA SIMULATION...")
    print("====================================")

    axion = AxionProfile()
    aag = AAGEngine()
    dissonance_system = DissonanceEngine()

    # --- SCENARIO 1: The Daily Grind (Low Risk) ---
    print("\n--- PHASE 1: Routine Operations ---")

    # Task: Update a Moon document (Low Crit)
    xp = aag.calculate_xp(CelestialClass.MOON, Criticality.LOW, synergy_links=2)
    print(f"Task: Updated Operational Playbook (MOON). XP Earned: {xp}")
    axion.add_xp(xp)

    # Task: Refactor a System Command (Medium Crit)
    xp = aag.calculate_xp(CelestialClass.SYSTEM, Criticality.MEDIUM, synergy_links=5)
    print(f"Task: Refactored System Command (SYSTEM). XP Earned: {xp}")
    axion.add_xp(xp)

    # --- SCENARIO 2: The Dissonance Spike (Combat) ---
    print("\n--- PHASE 2: Dissonance Event detected ---")

    dissonance_system.introduce_entropy(
        20.0, "Legacy Code Injection detected in Core Module."
    )

    # Axion Reacts
    dissonance_system.remediate(TarotMask.JUDGEMENT, 15.0)

    # More Entropy
    dissonance_system.introduce_entropy(
        35.0, "API Schema Drift! External Dependency Failure!"
    )

    # Axion Uses Ultimate
    print("\n⚡ ULTRA: Axion activates 'The Emperor' (Schema Re-Alignment)!")
    dissonance_system.remediate(TarotMask.EMPEROR, 40.0)

    # --- SCENARIO 3: The Cornerstone Creation (High Reward) ---
    print("\n--- PHASE 3: The Omega Artifact ---")

    # Task: Create the Omega Seed (Star + Cornerstone)
    print("Task: Finalizing 'GVRN.Seed.Axion.Omega.md'...")
    xp = aag.calculate_xp(
        CelestialClass.STAR, Criticality.CORNERSTONE, synergy_links=12
    )
    print(f"Task: OMEGA KERNEL WEAVED. XP Earned: {xp}")
    axion.add_xp(xp)

    print("\n====================================")
    print("📊 FINAL REPORT")
    print(f"Axion Level: {axion.level}")
    print(f"Total XP: {axion.total_xp}")
    print(
        f"Final Coherence: {dissonance_system.v_current.distance_to(dissonance_system.v_safe):.2f} (lower is better)"
    )
    print("Simulated Impact: POSITIVE. Systems Nominal.")


if __name__ == "__main__":
    run_simulation()
