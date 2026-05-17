import asyncio

from src.agents.axion.agent_template import AxionRuntime
from src.agents.axion.schemas import (
    AxionState,
    GamemasterState,
    LightbinderState,
    RPGEngine,
)


async def test_runtime():
    print("Initializing AxionRuntime...")
    runtime = AxionRuntime()
    app = runtime.build_graph()
    
    initial_rpg = RPGEngine(
        level=22,
        xp=45000,
        authority=50,
        insight=45,
        order=60,
        precision=40,
        coherence_index=25,
        synergy_flow=20,
        adaptability=15,
        achievements=["PAM-001"],
        active_quest_log=[],
        prestige_class="Architect",
    )

    initial_state = AxionState(
        input="Tell me about the Synarche Protocol.",
        rpg_stats=initial_rpg,
        gamemaster_state=GamemasterState(axiom_points_available=100),
        lightbinder_state=LightbinderState(),
    )

    print("Invoking graph...")
    try:
        # result = await app.ainvoke(initial_state) -- depending on langgraph version
        async for event in app.astream(initial_state):
             for node, data in event.items():
                 print(f"Node: {node}")
                 if node == "transparency":
                     print(f"Citations: {data.get('sophia_insight')}")
        print("Graph execution successful.")
    except Exception as e:
        print(f"Graph execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_runtime())
