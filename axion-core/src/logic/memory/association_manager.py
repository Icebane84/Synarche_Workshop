"""LOGIC-ASSOC-MGR-001: Memory Association Manager.

## Genesis Stamp: 2026-03-07 | Domain: LOGIC | State: ACTIVE

# I. Universal Identification & Provenance (UIP-V13)

| Key | Value |
| :--- | :--- |
| **Artifact ID** | `LOGIC-ASSOC-MGR-v1.0` |
| **Version** | **v1.0** |
| **Status** | `[ACTIVE]` |
| **Provenance** | `Date Reforged: 2026-03-07` |
| **Domain** | `LOGIC` |
| **Evolution** | **Cognitive Ascension** |
| **Celestial Class** | `[MOON]` |
| **Status (State)** | `[ACTIVE]` |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001` |

---

# II. Axiomatic Governance & Purpose
To manage Soft Links (thematic and causal associations) between memory entries, enabling graph-based navigation of the Axion Memory System.

# III. The Architectural Spine
- **Attributes**: `links` (defaultdict)
- **Methods**: `add_soft_link`, `get_linked_memories`, `update_link_strength`

# V. Systemic Relationships & Impact
- `MemorySystem`: Uses this to retrieve related memories during query cycles.
- `axion_template.py`: Benefits from expanded context retrieval.

# VI. RPG Framework Integration
- **Synergy Bonus**: Activating highly linked memories yields a +5 Synergy bonus.

# VII. Actionable Prompt Packet
- "Visualize the network of associations for Memory ID 42."
"""

import logging
from collections import defaultdict
from typing import Any

log = logging.getLogger(__name__)


class AssociationManager:
    """Manage memory associations (Soft Links).

    Handle the creation, retrieval, and updating of thematic and causal
    associations between memory entries.
    """

    STRENGTH_LEVELS = {"Weak": 0, "Moderate": 1, "Strong": 2}
    LEVEL_TO_STRENGTH = {v: k for k, v in STRENGTH_LEVELS.items()}

    def __init__(self, memory_system: Any = None) -> None:
        """Initialize the AssociationManager.

        :param memory_system: The parent MemorySystem instance.
        """
        self.memory_system = memory_system
        # Bidirectional links: self.links[source_id][target_id] = {'type': str, 'strength': str}
        self.links: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
        log.info("AssociationManager initialized.")

    def generate_citation_string(self, memories: list[dict[str, Any]]) -> str:
        """Generate a formatted citation string for the used memories."""
        if not memories:
            return ""

        citations = []
        for mem in memories:
            mem_id = mem.get("id", "Unknown ID")
            mem_type = mem.get("type", "Unknown Type")
            mem_content = mem.get("content", "No content available")
            citations.append(f"[{mem_id}] ({mem_type}): {mem_content[:100]}...")  # Truncate content for brevity
        return "\n".join(citations)

    def trigger_tag_based_linking(self, memory_id: str, tags: list[str]) -> None:
        """Trigger automatic linking between memories sharing common tags."""
        if not self.memory_system or not tags:
            return

        try:
            # Note: This is an expensive operation for very large memory systems.
            # In a production environment, this would be handled asynchronously.
            active_m_list = self.memory_system.storage.get_all_active()
            new_tags = set(tags)
            links_created = 0

            for other_mem in active_m_list:
                other_id = other_mem["id"]
                if other_id == memory_id:
                    continue

                other_tags = set(other_mem.get("tags") or [])
                shared = new_tags.intersection(other_tags)

                if shared:
                    # Create a bidirectional thematic link
                    if self.add_soft_link(memory_id, other_id, "Thematic Connection", "Weak"):
                        links_created += 1

            if links_created > 0:
                log.info(f"Created {links_created} tag-based associations for memory {memory_id}.")
        except Exception as e:
            log.error(f"Failed to perform tag-based linking for {memory_id}: {e}")

    def _add_single_link(self, source_id: str, target_id: str, rel_type: str, strength: str) -> None:
        """Add a unidirectional link to the internal graph."""
        if strength not in self.STRENGTH_LEVELS:
            strength = "Weak"
        self.links[str(source_id)][str(target_id)] = {"relationship_type": rel_type, "strength": strength}

    def add_soft_link(self, source_id: str, target_id: str, rel_type: str, initial_strength: str = "Weak") -> bool:
        """Add a bidirectional soft link between two memory entries."""
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
                current_level = self.STRENGTH_LEVELS.get(current_strength, 0)
                if current_level >= min_level:
                    linked_memories.append((target_id, link_data.get("relationship_type", "Unknown"), current_strength))

        return linked_memories

    def save_to_dict(self) -> dict:
        return {k: dict(v) for k, v in self.links.items()}

    def load_from_dict(self, data: dict):
        self.links = defaultdict(dict, {k: dict(v) for k, v in data.items()})
