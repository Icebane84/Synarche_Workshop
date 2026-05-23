"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-CSE-MGR-001`            | The Sovereign ID. |
| **Official Name**   | `mcp_injector.py`             | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-CSE`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Kinetic Capability (Law 33)**
> Implemented from Blueprint `GVRN.REG.McpInjector.md`.
> Ethos: Empowerment through Capability.
"""

import json
import os
from typing import Any


class McpInjector:
    """WHAT: Mutates the AI's Model Context Protocol configuration.
    HOW: Safely appends validated tool schemas to mcp_config.json.
    WHY: To grant AI agents access to newly forged Kinetic Capabilities (KCAPs).
    """

    def __init__(self, root_dir: str) -> None:
        self.mcp_path = os.path.join(root_dir, ".agent", "mcp_config.json")

    def register_tool(self, tool_schema: dict[str, Any]) -> bool:
        """Registers a new tool schema into the MCP configuration.

        Args:
            tool_schema (Dict[str, Any]): The JSON-serializable schema of the tool to register.

        Returns:
            bool: True if the tool was successfully registered, False if it already existed.

        Raises:
            FileNotFoundError: If the mcp_config.json file is missing.
            IOError: If the file cannot be read or written.

        """
        if not os.path.exists(self.mcp_path):
            raise FileNotFoundError(
                f"CRITICAL: Missing Mind Substrate at {self.mcp_path}"
            )

        try:
            with open(self.mcp_path, encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise IOError(f"CRITICAL: Failed to parse MCP config: {e!s}") from e

        # Ensure "tools" array exists
        if "mcp.tools" not in config:
            config["mcp.tools"] = []

        # Prevent duplicate registration
        if any(tool.get("name") == tool_schema["name"] for tool in config["mcp.tools"]):
            return False  # Tool already exists

        config["mcp.tools"].append(tool_schema)

        with open(self.mcp_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        return True
