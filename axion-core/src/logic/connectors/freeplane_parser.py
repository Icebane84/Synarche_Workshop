import logging
import os
from typing import Any, Dict, List, Optional

from lxml import etree


class FreeplaneParser:
    """
    Parses Freeplane (.mm) XML files into structured dictionaries.
    Extracts Nodes (Topics), Attributes, and Links.
    """

    def __init__(self):
        self.logger = logging.getLogger("FreeplaneParser")

    def parse_mindmap(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parses a Freeplane .mm file and returns a structured representation.
        
        Args:
            file_path (str): Path to the .mm file.
            
        Returns:
            dict: Structured representation of the mind map (Root Node).
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return None

        try:
            tree = etree.parse(file_path)
            root_element = tree.getroot()
            
            # The root of the XML is <map>, its first child is the Root Node
            map_root_node = root_element.find("node")
            if map_root_node is None:
                self.logger.error("Invalid Mind Map: No root node found.")
                return None
                
            return self._parse_node(map_root_node)

        except Exception as e:
            self.logger.error(f"Failed to parse mind map: {e}")
            return None

    def _parse_node(self, node_element) -> Dict[str, Any]:
        """
        Recursively parses a node element.
        """
        node_data = {
            "id": node_element.get("ID"),
            "text": node_element.get("TEXT"),
            "attributes": {},
            "children": [],
            "links": []
        }

        # Parse Attributes
        for attr in node_element.findall("attribute"):
            name = attr.get("NAME")
            value = attr.get("VALUE")
            if name:
                node_data["attributes"][name] = value

        # Parse Links (arrowlink)
        for link in node_element.findall("arrowlink"):
            target = link.get("DESTINATION")
            if target:
                node_data["links"].append(target)

        # Recurse Children
        for child in node_element.findall("node"):
            node_data["children"].append(self._parse_node(child))

        return node_data
