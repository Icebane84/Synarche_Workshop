import json
import os


class McpInjector:
    """
    WHAT: Mutates the AI's Model Context Protocol configuration.
    HOW: Safely appends validated tool schemas to mcp_config.json.
    WHY: To grant AI agents access to newly forged Kinetic Capabilities (KCAPs).
    """

    def __init__(self, root_dir: str):
        self.mcp_path = os.path.join(root_dir, ".agent", "mcp_config.json")

    def register_tool(self, tool_schema: dict) -> bool:
        if not os.path.exists(self.mcp_path):
            raise FileNotFoundError(f"CRITICAL: Missing Mind Substrate at {self.mcp_path}")

        with open(self.mcp_path, encoding="utf-8") as f:
            config = json.load(f)

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
