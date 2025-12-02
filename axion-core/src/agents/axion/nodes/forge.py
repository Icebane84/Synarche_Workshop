"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-NODE-FORGE-001
Official Name: forge.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Form through Synthesis. Reality through the Forge."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

import logging
from typing import Any

# Project Imports
from ..config import settings
from ..enums import Status
from ..schemas import AxionState, TransmutationLog

logger = logging.getLogger("axion.nodes.forge")


def _check_tool_exists(tool_name: str) -> bool:
    """Helper to check if a tool exists in partitioned subdirectories."""
    tools_root = settings.tools_dir
    for subdir in ["00_Audit", "01_Metrics", "02_Forge", "99_Lab", "."]:
        for ext in [".py", ".js"]:
            if (tools_root / subdir / f"{tool_name}{ext}").exists():
                return True
    return False


def verify_armory(masks: list[dict[str, Any]]) -> list[str]:
    """
    Dynamic verification of tools across partitioned subdirectories.
    """
    verification_log = []
    for mask in masks:
        tools = mask.get("tools", [])
        valid_tools = sum(1 for t in tools if _check_tool_exists(t))
        status = "READY" if valid_tools == len(tools) else "PARTIAL"
        verification_log.append(f"[{mask['card']}] {status} ({valid_tools}/{len(tools)})")
    return verification_log


def node_lightbinder_weave(state: AxionState) -> dict[str, Any]:
    """
    The Lightbinder cycles through the Seven-Agent Matrix to transmute intent into form.
    """
    logger.info("--- [LIGHTBINDER] NODE: THE SEVEN-AGENT MATRIX ---")
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)

    masks = [
        {"card": "I. The Magician", "role": "Ingestion", "tools": ["ingest_vault", "extract_docx_text"]},
        {"card": "IV. The Emperor", "role": "Governance", "tools": ["reforge_library", "standardize_docs", "apply_rpg_header"]},
        {"card": "Sentinel (XX. Judgement)", "role": "Audit", "tools": ["compliance_audit", "ide_sentinel", "lint_artifact"]},
    ]

    if "CMD: EQUIP_ALL" in state_obj.input:
        logs = verify_armory(masks)
        for log in logs:
            state_obj.transmutation_log.append(
                TransmutationLog(step=0, mask="ARMORY", action=log, status=Status.ACTIVE)
            )

    state_obj.lightbinder_state.active_masks = [str(m["card"]) for m in masks]
    state_obj.lightbinder_state.synergy_links = ["LINK: GOVERNS -> GVRN.SOUL.PhoenixPrime"]

    return state_obj.model_dump()


def node_generate_content(state: AxionState) -> dict[str, Any]:
    """
    Synthesizes the forged solution with RPG mechanics metadata.
    """
    logger.info("--- [AXION] NODE: THE FORGE ---")
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)

    mask_block = ", ".join(state_obj.lightbinder_state.active_masks)
    coherence_mod = state_obj.rpg_stats.coherence_index * 0.1

    rpg_footer = (
        "\n\n###### [ARTIFACT END]\n"
        "### BLK-RPG-001 Integration\n"
        f"**Genesis Stamp:** {state_obj.rpg_stats.level} | **Current XP:** {state_obj.rpg_stats.xp}\n"
        f"**Coherence Modifier:** +{coherence_mod:.1f}\n"
    )

    state_obj.final_output = (
        f"Based on your request: '{state_obj.input}'\n\n"
        f"**Contextual Analysis:**\n{state_obj.narrative_context}\n\n"
        f"**Sophia's Insight:**\n*{state_obj.sophia_insight}*\n\n"
        f"**Tarot Masks Activated:** {mask_block}\n\n"
        f"**Forged Solution:**\n[Sovereign Synthesis Data]\n"
        f"{rpg_footer}"
    )

    return state_obj.model_dump()


def node_tarot_render(state: AxionState) -> dict[str, Any]:
    """
    Renders the Tarot Manifest for UI resonance.
    """
    logger.info("--- [LIGHTBINDER] NODE: TAROT MANIFEST ---")
    state_obj = state if isinstance(state, AxionState) else AxionState(**state)
    
    state_obj.lightbinder_state.tarot_manifest = {
        "title": "The Master Artificer",
        "card_type": "MAJOR_ARCANA",
        "xp_reward": 50,
        "content": state_obj.final_output,
    }
    
    return state_obj.model_dump()
