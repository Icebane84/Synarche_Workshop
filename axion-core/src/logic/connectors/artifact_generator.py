import os
import logging
from datetime import datetime

class ArtifactGenerator:
    """
    Generates Markdown artifacts from structured data (e.g. parsed Mind Maps).
    """

    def __init__(self):
        self.logger = logging.getLogger("ArtifactGenerator")

    def generate_from_mindmap(self, map_data: dict, output_dir: str) -> str:
        """
        Converts a parsed Mind Map dict into a Markdown file.
        
        Args:
            map_data (dict): The root node of the parsed map.
            output_dir (str): Directory to save the file.
            
        Returns:
            str: The absolute path of the generated file.
        """
        root_text = map_data.get("text", "Untitled_Artifact")
        root_id = map_data.get("id", "UNKNOWN_ID")
        
        # Determine Filename (Use TEXT as filename, sanitize it)
        filename = f"{root_text.replace(' ', '_')}.md"
        file_path = os.path.join(output_dir, filename)
        
        content = []
        
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
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(content))
            return file_path
        except Exception as e:
            self.logger.error(f"Failed to write artifact: {e}")
            return ""

    def _recurse_nodes(self, nodes, content, level):
        """
        Recursively appends nodes to content list.
        Level 2 = H2 (##)
        Level 3 = H3 (###)
        Level 4+ = Bullet points
        """
        for node in nodes:
            text = node.get("text", "")
            
            if level <= 3:
                # Headlines
                header = "#" * level
                content.append(f"{header} {text}")
                content.append("")
            else:
                # Bullet Points
                indent = "  " * (level - 4)
                content.append(f"{indent}- {text}")
            
            # Recurse
            if node.get("children"):
                # If we are at bullet level, keep it at bullet level (visual hierarchy)
                next_level = level + 1
                self._recurse_nodes(node["children"], content, next_level)
