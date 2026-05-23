"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.association.manager`                | The Sovereign ID. |
| **Official Name** | `association_manager.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Logic Drift**      | Strict Linter Enforcement |
# | **Semantic Decay**   | Axiomatic Compass Audit   |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List, Tuple

# Configure logging for this module
log = logging.getLogger(__name__)


class AssociationManager:
    """Manages memory associations (Soft Links) within the cognitive system.
    Supports thematic linking, strength tracking, and persistence mapping.
    """

    STRENGTH_LEVELS: Dict[str, int] = {"Weak": 0, "Moderate": 1, "Strong": 2}
    LEVEL_TO_STRENGTH: Dict[int, str] = {v: k for k, v in STRENGTH_LEVELS.items()}

    def __init__(self, memory_system: Any = None) -> None:
        """Initializes the AssociationManager.

        Args:
            memory_system: Reference to the parent memory system for cross-memory lookups.

        """
        self.memory_system = memory_system
        self.links: Dict[str, Dict[str, Dict[str, str]]] = defaultdict(dict)
        log.info("AssociationManager initialized.")

    def generate_citation_string(self, memories: List[Dict[str, Any]]) -> str:
        """Generates a human-readable citation string from a list of memory objects.

        Args:
            memories: List of memory dictionaries.

        Returns:
            A formatted string suitable for logging or display.

        """
        if not memories:
            return ""
        citations = []
        for mem in memories:
            mem_id = mem.get("id", "Unknown ID")
            mem_type = mem.get("type", "Unknown Type")
            mem_content = mem.get("content", "No content available")
            citations.append(f"[{mem_id}] ({mem_type}): {mem_content[:100]}...")
        return "\n".join(citations)

    def trigger_tag_based_linking(self, memory_id: str, tags: List[str]) -> None:
        """Automatically creates links between memories based on shared tags.

        Args:
            memory_id: The ID of the memory to link from.
            tags: The list of tags associated with the memory.

        """
        if not self.memory_system or not tags:
            return
        try:
            active_m_list = self.memory_system.storage.get_all_active()
            new_tags = set(tags)
            links_created = 0
            for other_mem in active_m_list:
                other_id = other_mem["id"]
                if other_id == memory_id:
                    continue
                other_tags = set(other_mem.get("tags") or [])
                if new_tags.intersection(other_tags):
                    if self.add_soft_link(
                        memory_id, other_id, "Thematic Connection", "Weak"
                    ):
                        links_created += 1
            if links_created > 0:
                log.info(
                    f"Created {links_created} tag-based associations for memory {memory_id}."
                )
        except Exception as e:
            log.error(f"Failed to perform tag-based linking for {memory_id}: {e}")

    def _add_single_link(
        self, source_id: str, target_id: str, rel_type: str, strength: str
    ) -> None:
        """Internal method to add a unidirectional link between two memories.

        Args:
            source_id: Origin memory ID.
            target_id: Target memory ID.
            rel_type: Type of relationship.
            strength: Strength level of the link.

        """
        if strength not in self.STRENGTH_LEVELS:
            strength = "Weak"
        self.links[str(source_id)][str(target_id)] = {
            "relationship_type": rel_type,
            "strength": strength,
        }

    def add_soft_link(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        initial_strength: str = "Weak",
    ) -> bool:
        """Adds a bidirectional soft link between two memories.

        Args:
            source_id: First memory ID.
            target_id: Second memory ID.
            rel_type: The nature of the association.
            initial_strength: The starting strength of the association.

        Returns:
            True if the link was successfully created, False otherwise.

        """
        if not source_id or not target_id or source_id == target_id:
            return False
        try:
            self._add_single_link(source_id, target_id, rel_type, initial_strength)
            self._add_single_link(target_id, source_id, rel_type, initial_strength)
            return True
        except Exception as e:
            log.exception(
                f"Failed to add soft link between {source_id} and {target_id}: {e}"
            )
            return False

    def get_linked_memories(
        self, memory_id: str, min_strength: str = "Weak"
    ) -> List[Tuple[str, str, str]]:
        """Retrieves all memories associated with a given memory ID.

        Args:
            memory_id: The ID of the memory to query.
            min_strength: The minimum strength threshold for retrieved links.

        Returns:
            A list of (target_id, relationship_type, strength) tuples.

        """
        linked_memories = []
        min_level = self.STRENGTH_LEVELS.get(min_strength, 0)
        m_id = str(memory_id)
        if m_id in self.links:
            for target_id, link_data in self.links[m_id].items():
                current_strength = link_data.get("strength", "Weak")
                if self.STRENGTH_LEVELS.get(current_strength, 0) >= min_level:
                    linked_memories.append(
                        (
                            target_id,
                            link_data.get("relationship_type", "Unknown"),
                            current_strength,
                        )
                    )
        return linked_memories

    def save_to_dict(self) -> Dict[str, Any]:
        """Serializes the current link state to a dictionary.

        Returns:
            A dictionary representation of the association links.

        """
        return {k: dict(v) for k, v in self.links.items()}

    def load_from_dict(self, data: Dict[str, Any]) -> None:
        """Loads the link state from a dictionary.

        Args:
            data: The dictionary representation of the links to load.

        """
        self.links = defaultdict(dict, {k: dict(v) for k, v in data.items()})


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.association.manager VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 90aa32f0e9df1e2a
# ---
