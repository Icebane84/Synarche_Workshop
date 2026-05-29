# Phase 2: Extraction Engine
# Extracts embedded YAML frontmatter / anchor metadata blocks

import os
import re
import ast
import yaml
import textwrap

class ArtifactParser:
    def __init__(self):
        # Split string literals to prevent the parser from matching its own source code definition!
        self.anchor_regex = re.compile(
            r"(?:<!-- prettier-ignore -->\s*\n|// prettier-ignore\s*\n)?"
            r"(?:<!--\s*\n|/\*\s*\n|\"\"\"\s*\n|'''\s*\n|---\s*\n)?"
            r"artifact_" + r"anchor:(?:[ \t]*\n)?(.*?)(?:-->|\"\"\"|'''|\*/|---|\Z)",
            re.DOTALL
        )

    def parse_python_ast(self, content: str) -> tuple[dict, str, str]:
        """Parses Python module-level docstrings using grammar-aware AST."""
        try:
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            if docstring and "artifact_" + "anchor:" in docstring:
                match = self.anchor_regex.search(docstring)
                if match:
                    anchor_yaml = textwrap.dedent(match.group(1))
                    data = yaml.safe_load(anchor_yaml) or {}
                    
                    # Locate raw string block in Python content for exact replacement
                    raw_block_match = re.search(r'(""".*?"""|\'\'\'.*?\'\'\')', content, re.DOTALL)
                    raw_block = raw_block_match.group(1) if raw_block_match else ""
                    return data, docstring, raw_block
        except Exception:
            pass
        return None, "", ""

    def extract_anchor(self, file_path: str, content: str) -> tuple[dict, str, str]:
        """Extracts YAML anchor data, parsed docstring/text, and raw text block from a file."""
        filename = os.path.basename(file_path)
        _, ext = os.path.splitext(filename)
        
        # AST first for Python
        if ext == ".py":
            data, docstring, raw_block = self.parse_python_ast(content)
            if data:
                return data, docstring, raw_block

        # Fallback to regex token parsing
        match = self.anchor_regex.search(content)
        if match:
            anchor_text = match.group(1)
            dedented_yaml = textwrap.dedent(anchor_text)
            try:
                data = yaml.safe_load(dedented_yaml) or {}
                return data, anchor_text, match.group(0)
            except Exception:
                pass
                
        return None, "", ""
