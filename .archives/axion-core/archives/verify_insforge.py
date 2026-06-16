import asyncio
import sys
from pathlib import Path

# Add Synarche_Workspace to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.agents.axion.insforge_client import insforge


async def verify_substrate():
    print("--- 🏛️ SYNARCHE INSFORGE SUBSTRATE VERIFICATION ---")

    if not insforge.enabled:
        print("❌ Error: InsForge client is not enabled. Check .env credentials.")
        return

    # 1. Test Database Connectivity
    print("\n[DB] Testing connectivity...")
    result = await insforge.query_db("SELECT count(*) FROM artifacts")
    if "error" in result:
        print(f"❌ DB Query Failed: {result['error']}")
    else:
        print(f"✅ DB Connected. Artifact count: {result[0]['count']}")

    # 2. Verify Core Artifacts
    print("\n[ARTIFACTS] Verifying mission-critical artifacts...")
    artifacts = await insforge.get_artifacts()
    artifact_ids = [a["artifact_id"] for a in artifacts]
    required = [
        "GVRN.SOUL.PhoenixPrime",
        "SYNC.ROOT.Entryway",
        "SYNG.TASK.ActiveMission",
    ]

    for aid in required:
        if aid in artifact_ids:
            print(f"✅ Found Authoritative Artifact: {aid}")
        else:
            print(f"❌ Missing Critical Artifact: {aid}")

    # 3. Verify Agents
    print("\n[AGENTS] Verifying Kinetic Shard alignment...")
    result = await insforge.query_db("SELECT agent_id, name, status FROM agents")
    if "error" in result:
        print(f"❌ Agent Query Failed: {result['error']}")
    else:
        for agent in result:
            print(
                f"✅ Agent Registered: {agent['name']} ({agent['agent_id']}) -> {agent['status']}"
            )

    print("\n--- ✅ SUBSTRATE VERIFICATION COMPLETE ---")


if __name__ == "__main__":
    asyncio.run(verify_substrate())
