import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.engine.deterministic import DeterministicEngine, ResonanceDomain, Task


# Define mock component types
class MotionData:
    pass


class CombatData:
    pass


def test_resonance_alignment():
    """Validates that the ResonanceAuditor correctly identifies and blocks
    unauthorized cross-domain data access.
    """
    print("--- [START] RESONANCE ALIGNMENT VALIDATION ---")

    engine = DeterministicEngine()

    # 1. Register component domains
    engine.resonance_registry.register(MotionData, ResonanceDomain.MOTION)
    engine.resonance_registry.register(CombatData, ResonanceDomain.COMBAT)

    # 2. Define a System in the MOTION domain
    def motion_system(ctx):
        print(f"[{ctx['frame']}] MotionSystem executing...")
        e = ctx["state"]["entities"].create_entity()

        # VALID ACCESS: Motion system adding Motion data
        ctx["state"]["components"].add_component(e, MotionData())
        print("Successfully added MotionData (Authorized)")

        # INVALID ACCESS: Motion system adding Combat data
        try:
            print("Attempting to add CombatData (Unauthorized)...")
            ctx["state"]["components"].add_component(e, CombatData())
            # If we reach here, the test failed
            raise AssertionError("Dissonant access was NOT blocked!")
        except RuntimeError as e:
            print(f"Caught Expected Dissonance: {e}")

    # Create the task with MOTION domain authority
    task_motion = Task("Physics_System", motion_system, domain=ResonanceDomain.MOTION)

    engine.register_task(task_motion)
    engine.initialize()

    print("\nRunning Engine Step...")
    engine.step()

    print("\n--- [SUCCESS] Resonance Alignment validated. ---")


if __name__ == "__main__":
    try:
        test_resonance_alignment()
    except Exception as e:
        print(f"\n[FAILURE] Resonance Validation Failed: {e}")
        sys.exit(1)
