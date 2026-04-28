"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.connectors.artifact_generator`       | The Sovereign ID. |
| **Official Name** | `artifact_generator.py`                | The Filename.     |
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
# | **Formatting Drift** | Standardized Markdown Templates |
# | **Data Loss**        | Atomic File Operations    |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**
"""

import os
import logging
from datetime import datetime
from typing import Any, Dict, List

class ArtifactGenerator:
    """
    Generates Markdown artifacts from structured data (e.g. parsed Mind Maps).
    Conforms to OGLN/AISTF v15.0 documentation standards.
    """

    def __init__(self) -> None:
        """Initializes the ArtifactGenerator with standardized logging."""
        self.logger = logging.getLogger("ArtifactGenerator")

    def generate_from_mindmap(self, map_data: Dict[str, Any], output_dir: str) -> str:
        """
        Converts a parsed Mind Map dict into a Markdown file with a standardized header.

        Args:
            map_data: The root node of the parsed map.
            output_dir: Directory to save the generated Markdown file.

        Returns:
            The absolute path of the generated file, or an empty string on failure.
        """
        root_text = map_data.get("text", "Untitled_Artifact")
        root_id = map_data.get("id", "UNKNOWN_ID")
        
        # Determine Filename (Use TEXT as filename, sanitize it)
        filename = f"{root_text.replace(' ', '_')}.md"
        file_path = os.path.join(output_dir, filename)
        
        content: List[str] = []
        
        # 1. UIP Header (Standard OGLN)
        content.append("---")
        content.append(f"id: {root_id}")
        content.append(f"title: {root_text}")
        content.append(f"created: {datetime.now().strftime('%Y-%m-%d')}")
        content.append("type: Protocol")
        content.append("status: Draft")
        content.append("---")
        content.append("")
        
        # 2. Title
        content.append(f"# {root_text}")
        content.append("")
        
        # 3. Recursive Body Generation
        self._recurse_nodes(map_data.get("children", []), content, level=2)
        
        # 4. Write to File
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(content))
            self.logger.info(f"Artifact generated successfully: {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Failed to write artifact: {e}")
            return ""

    def _recurse_nodes(self, nodes: List[Dict[str, Any]], content: List[str], level: int) -> None:
        """
        Recursively appends nodes to the content list with hierarchical formatting.

        Args:
            nodes: List of node dictionaries to process.
            content: The growing list of Markdown strings.
            level: The current heading level or indentation level.
        """
        for node in nodes:
            text = node.get("text", "")
            
            if level <= 3:
                # Headlines (H2, H3)
                header = "#" * level
                content.append(f"{header} {text}")
                content.append("")
            else:
                # Bullet Points with indentation
                indent = "  " * (level - 4)
                content.append(f"{indent}- {text}")
            
            # Recurse if there are children
            children = node.get("children")
            if children:
                # If we are at bullet level, keep it at bullet level (visual hierarchy)
                next_level = level + 1
                self._recurse_nodes(children, content, next_level)

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.connectors.artifact_generator VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28
# ---
