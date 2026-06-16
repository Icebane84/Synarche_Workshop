import os
import sys

# Adjust path to find tool_router in sibling directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from tools.tool_router import ToolRouter


def test_router():
    router = ToolRouter()

    print("--- Testing The Council of Seven Routing ---")

    # --- 1. THE EMPEROR (Validation) ---
    print("\n👑 The Emperor (Structure)")

    # Valid ID
    res = router.route_update("Artifact ID", "GVRN-LEX-002")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid ID: {res['value']}")

    # Invalid ID
    res = router.route_update("Artifact ID", "bad_id_format")
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Invalid ID: {res['msg']}")

    # Valid Version
    res = router.route_update("Version", "v13.0")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Version: {res['value']}")

    # Invalid Version
    res = router.route_update("Version", "13.0")  # Missing 'v'
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Invalid Version: {res['msg']}")

    # --- 2. THE STAR (Signal) ---
    print("\n🌟 The Star (Tone)")

    # Valid Signal (Value Check)
    res = router.route_update("Signal", "ESF-OMEGA")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Signal: {res['value']}")

    # Invalid Signal
    res = router.route_update("Signal", "ESF-GARBAGE")
    assert res["status"] == "ERROR"
    assert res["governor"] == "STAR"
    print(f"🛡️ Blocked Invalid Signal: {res['msg']}")

    # --- 3. THE PRIESTESS (Domain) ---
    print("\n🔮 The High Priestess (Domain)")

    # Valid Domain
    res = router.route_update("Domain", "GVRN")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Domain: {res['value']}")

    # Invalid Domain
    res = router.route_update("Domain", "PIZZA")
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Invalid Domain: {res['msg']}")

    # --- 4. THE MAGICIAN (Intent) ---
    print("\n🎩 The Magician (Origin)")
    res = router.route_update(
        "Module", "ACT"
    )  # Correct Enum key (ACT is in Module?) Check ACT-M vs keys
    # Enum definition: ACT = "ACT-M". Keys are ACT.
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Module: {res['value']}")

    res = router.route_update("Module", "FAKE_MODULE")
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Invalid Module: {res['msg']}")

    res = router.route_update("Catalyst", "Start")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Catalyst: {res['value']}")

    res = router.route_update("Catalyst", "No")  # Too short
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Short Catalyst: {res['msg']}")

    # --- 5. THE KNIGHT OF SWORDS (Action) ---
    print("\n⚔️ The Knight of Swords (Action)")
    res = router.route_update("Genesis Seed", "Refactor the core logic")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Seed: {res['value']}")

    res = router.route_update("Genesis Seed", "..")
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Bad Seed: {res['msg']}")

    # --- 6. THE KING OF PENTACLES (Time) ---
    print("\n💰 The King of Pentacles (Time)")
    res = router.route_update("Created", "2026-01-29")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Date: {res['value']}")

    res = router.route_update("Created", "2026/01/29")  # Wrong format
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Bad Date: {res['msg']}")

    # --- 7. JUDGEMENT (Integrity) ---
    print("\n⚖️ Judgement (Integrity)")

    # Valid Hash (Real)
    valid_hash = "sha256:" + "a" * 64
    res = router.route_update("Integrity Hash", valid_hash)
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Hash: {res['value'][:20]}...")

    # Valid Hash (Placeholder)
    res = router.route_update("Integrity Hash", "[AUTO-GEN-SHA256]")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Placeholder: {res['value']}")

    # Invalid Hash
    res = router.route_update("Integrity Hash", "bad_hash")
    assert res["status"] == "ERROR"
    print(f"🛡️ Blocked Invalid Hash: {res['msg']}")

    # Audit Status
    res = router.route_update("Musashi Audit", "PASS")
    assert res["status"] == "VALIDATED"
    print(f"✅ Valid Audit: {res['value']}")

    print("\n🎉 All Verification Tests Passed!")


if __name__ == "__main__":
    test_router()
