"""
## **[ARTIFACT START]**
## **Block A: The Identification Lock (UIP-V15)**
| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.association.manager`                | The Sovereign ID. |
| **Official Name** | `association_manager.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |
## **[ARTIFACT END]**
"""

import logging
from collections import defaultdict
from typing import Any

log = logging.getLogger(__name__)

class AssociationManager:
    """Manage memory associations (Soft Links)."""

    STRENGTH_LEVELS = {"Weak": 0, "Moderate": 1, "Strong": 2}
    LEVEL_TO_STRENGTH = {v: k for k, v in STRENGTH_LEVELS.items()}

    def __init__(self, memory_system: Any = None) -> None:
        self.memory_system = memory_system
        self.links: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
        log.info("AssociationManager initialized.")

    def generate_citation_string(self, memories: list[dict[str, Any]]) -> str:
        if not memories:
            return ""
        citations = []
        for mem in memories:
            mem_id = mem.get("id", "Unknown ID")
            mem_type = mem.get("type", "Unknown Type")
            mem_content = mem.get("content", "No content available")
            citations.append(f"[{mem_id}] ({mem_type}): {mem_content[:100]}...")
        return "\n".join(citations)

    def trigger_tag_based_linking(self, memory_id: str, tags: list[str]) -> None:
        if not self.memory_system or not tags:
            return
        try:
            active_m_list = self.memory_system.storage.get_all_active()
            new_tags = set(tags)
            links_created = 0
            for other_mem in active_m_list:
                other_id = other_mem["id"]
                if other_id == memory_id: continue
                other_tags = set(other_mem.get("tags") or [])
                if new_tags.intersection(other_tags):
                    if self.add_soft_link(memory_id, other_id, "Thematic Connection", "Weak"):
                        links_created += 1
            if links_created > 0:
                log.info(f"Created {links_created} tag-based associations for memory {memory_id}.")
        except Exception as e:
            log.error(f"Failed to perform tag-based linking for {memory_id}: {e}")

    def _add_single_link(self, source_id: str, target_id: str, rel_type: str, strength: str) -> None:
        if strength not in self.STRENGTH_LEVELS:
            strength = "Weak"
        self.links[str(source_id)][str(target_id)] = {
            "relationship_type": rel_type,
            "strength": strength,
        }

    def add_soft_link(self, source_id: str, target_id: str, rel_type: str, initial_strength: str = "Weak") -> bool:
        if not source_id or not target_id or source_id == target_id:
            return False
        try:
            self._add_single_link(source_id, target_id, rel_type, initial_strength)
            self._add_single_link(target_id, source_id, rel_type, initial_strength)
            return True
        except Exception as e:
            log.exception(f"Failed to add link: {e}")
            return False

    def get_linked_memories(self, memory_id: str, min_strength: str = "Weak") -> list[tuple[str, str, str]]:
        linked_memories = []
        min_level = self.STRENGTH_LEVELS.get(min_strength, 0)
        m_id = str(memory_id)
        if m_id in self.links:
            for target_id, link_data in self.links[m_id].items():
                current_strength = link_data.get("strength", "Weak")
                if self.STRENGTH_LEVELS.get(current_strength, 0) >= min_level:
                    linked_memories.append((target_id, link_data.get("relationship_type", "Unknown"), current_strength))
        return linked_memories

    def save_to_dict(self) -> dict[str, Any]:
        return {k: dict(v) for k, v in self.links.items()}

    def load_from_dict(self, data: dict[str, Any]) -> None:
        self.links = defaultdict(dict, {k: dict(v) for k, v in data.items()})

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.association.manager VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 90aa32f0e9df1e2a
