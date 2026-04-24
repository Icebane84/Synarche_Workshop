import ast
import os


class GucaParser:
    """
    WHAT: Extracts Genesis Universal Command Architecture (GUCA) from KCAPs.
    HOW: Uses Python's AST (Abstract Syntax Tree) to read docstrings safely without executing code.
    WHY: To ensure only strictly formatted, Phoenix-compliant tools are registered.
    """

    def __init__(self, root_dir: str):
        self.skills_dir = os.path.join(root_dir, ".agent", "skills")

    def extract_capability(self, filename: str) -> dict | None:
        filepath = os.path.join(self.skills_dir, filename)
        if not os.path.exists(filepath) or not filename.endswith(".py"):
            return None

        with open(filepath, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=filepath)

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
