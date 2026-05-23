"""Governance Stress Test: Law 26 & Catalyst Weaver Integration."""

import importlib.util
import os
import sys

# Ensure axion-core is in path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)


def test_law_26_hollow_check():
    print("--- [TEST] LAW 26: HOLLOW ARTIFACT DETECTION ---")
    content_hollow = "This is a random string of text with no intent."
    content_filled = "I intend to create a new governance protocol for memory mapping."

    try:
        from src.logic.nlp.nlp_engine import AxionCognition

        cog = AxionCognition()

        res_hollow = cog.process(content_hollow)
        res_filled = cog.process(content_filled)

        print(f"Hollow Intent: {res_hollow.get('user_intent_goal')}")
        print(f"Filled Intent: {res_filled.get('user_intent_goal')}")

        eff_hollow = res_hollow.get("magician_efficiency", 0)
        eff_filled = res_filled.get("magician_efficiency", 0)

        print(f"Hollow Efficiency: {eff_hollow}")
        print(f"Filled Efficiency: {eff_filled}")

        if eff_hollow < 1.0:
            print("[PASS] Hollow content flagged (Low Efficiency).")
        else:
            print("[FAIL] Hollow content not flagged.")

    except Exception as e:
        print(f"[ERROR] Law 26 test failed: {e}")


def test_weaver_nlp():
    print("\n--- [TEST] CATALYST WEAVER NLP INTEGRATION ---")
    try:
        weaver_path = os.path.join(
            BASE_DIR, "tools", "02_Forge", "GVRN.Tool.CatalystWeaver.py"
        )
        spec = importlib.util.spec_from_file_location("weaver", weaver_path)
        weaver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(weaver_mod)

        weaver = weaver_mod.CatalystWeaver("Test_Optimization_Bundle")
        test_content = "We need to optimize the memory retrieval loops for the High Priestess mask."

        weaver.extract_meta_tags(test_content)

        if weaver.bundle.meta_tags:
            print(f"[PASS] Weaver extracted tags: {weaver.bundle.meta_tags}")
        else:
            print("[FAIL] Weaver failed to extract tags.")
    except Exception as e:
        print(f"[ERROR] Weaver test failed: {e}")


if __name__ == "__main__":
    test_law_26_hollow_check()
    test_weaver_nlp()
