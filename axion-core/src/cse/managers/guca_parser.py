"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-CSE-PAR-002`            | The Sovereign ID. |
| **Official Name**   | `guca_parser.py`              | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-CSE`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Command Clarity (Law 34)**
> Implemented from Blueprint `GVRN.REG.GucaParser.md`.
> Ethos: Precision through Extraction.
"""

import ast
import os
from typing import Any, Dict, Optional


class GucaParser:
    """
    WHAT: Extracts Genesis Universal Command Architecture (GUCA) from KCAPs.
    HOW: Uses Python's AST (Abstract Syntax Tree) to read docstrings safely without executing code.
    WHY: To ensure only strictly formatted, Phoenix-compliant tools are registered.
    """

    def __init__(self, root_dir: str):
        self.skills_dir = os.path.join(root_dir, ".agent", "skills")

    def extract_capability(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Extracts the GUCA capability schema from a Python skill file.
        
        Args:
            filename (str): The name of the file to parse within the skills directory.
            
        Returns:
            Optional[Dict[str, Any]]: The extracted tool schema if compliant, else None.
        """
        filepath = os.path.join(self.skills_dir, filename)
        if not os.path.exists(filepath) or not filename.endswith(".py"):
            return None

        try:
            with open(filepath, encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)
        except (SyntaxError, IOError):
            return None

        # Extract module-level docstring
        docstring = ast.get_docstring(tree)
        if not docstring or "WHAT:" not in docstring:
            return None  # Fails Phoenix compliance

        # Construct the MCP-compatible schema (simplified for abstraction)
        tool_schema = {
            "name": filename.replace(".py", ""),
            "description": docstring.split("HOW:")[0].strip().replace("WHAT:", "").strip(),
            "inputSchema": {
                "type": "object",
                "properties": {},  # Would be parsed dynamically in a full implementation
                "required": [],
            },
        }
        return tool_schema
