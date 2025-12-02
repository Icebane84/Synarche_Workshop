"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-MINTSEED-001`            | The Sovereign ID. |
| **Official Name** | `mint_seed.py`                 | The Filename.     |
| **Version**       | **v14.0**                      | The Standard.     |
| **Domain**        | `AXION`                        | The Subject.      |
| **Evolution**     | **Kinetic Ascension [25.0]**   | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |.

## Sovereign Ethos
This tool is the Transmutation Engine. It converts static artifacts into kinetic seeds
for the Cognitive Loom. Every seed minted must be pure, traceable, and secure.

"The seed of the future is forged in the fires of the past."
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console

console = Console()

# --- Sovereign Exceptions ---


class ForgeError(Exception):
    """Base exception for all Forge Toolkit errors."""

    pass


class SovereigntyViolationError(ForgeError):
    """Raised when a path resolution attempts to leave the Workspace Sanctuary."""

    pass


class IntegrityError(ForgeError):
    """Raised when metadata or rendering integrity is compromised."""

    pass


class ArtifactTransmuter:
    """The Seed Minter (v14.0) - Markdown to Mindmap Transmuter."""

    def __init__(self, workspace_root: str, strict: bool = False) -> None:
        self.workspace = os.path.abspath(workspace_root).replace("\\", "/")
        self.strict = strict
        self.audit_log: list[dict[str, Any]] = []

        # Log initialization
        self.audit_log.append(
            {"type": "engine_init", "workspace": self.workspace, "timestamp": datetime.now().isoformat()}
        )

    def _safe_path_resolve(self, path: str, check_exists: bool = True) -> str:
        """Ensures the resolved path stays within the Workspace Sanctuary."""
        abs_path = os.path.abspath(path).replace("\\", "/")

        # Cross-platform commonpath check
        try:
            # We normalize everything to forward slashes for comparison
            ws_norm = self.workspace.rstrip("/")
            abs_norm = abs_path.rstrip("/")

            common = os.path.commonpath([ws_norm, abs_norm]).replace("\\", "/")
            if common != ws_norm:
                raise SovereigntyViolationError(
                    f"Path Traversal Attempt: {path}. The Forge remains within the Sanctuary."
                )
        except ValueError:
            # Handles different drives on Windows
            raise SovereigntyViolationError(f"Cross-Drive Traversal Blocked: {path}")

        if check_exists and not os.path.exists(abs_path):
            raise FileNotFoundError(f"Vault Object Missing: {path}")

        return abs_path

    def clean_text(self, text: str) -> str:
        """Removes markdown bold/italic clutter for cleaner node titles."""
        # Strip Bold/Italic/Backticks
        text = re.sub(r"\*\*|\*|`", "", text)
        # Strip Links [text](path) -> text
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
        return text.strip()

    def parse_block_a_identity(self, content: str) -> list[str]:
        """Extracts Key Metadata from Block A (The Identification Lock)."""
        identity_nodes = []

        # Flexible patterns (accounts for optional formatting around keys)
        patterns = {
            "ID": r"\|?\s*\*?\*?Artifact ID\*?\*?\s*\|\s*(.*?)\s*\|",
            "Version": r"\|?\s*\*?\*?Version\*?\*?\s*\|\s*(.*?)\s*\|",
            "Class": r"\|?\s*\*?\*?Celestial Class\*?\*?\s*\|\s*(.*?)\s*\|",
            "Status": r"\|?\s*\*?\*?Status\*?\*?\s*\|\s*(.*?)\s*\|",
        }

        icons = {"ID": "🆔", "Version": "🚩", "Class": "⚖️", "Status": "🔋"}

        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                val = self.clean_text(match.group(1))
                if val:
                    identity_nodes.append(f"- {icons[key]} {key}: {val}")

        return identity_nodes

    def parse_block_d_synergy(self, content: str) -> list[str]:
        """Extracts Relationships from Block D (The Loom Signature)."""
        synergy_nodes = set()

        # Find the synergy block section
        marker = re.search(
            r"##\s*Block D|###\s*Block D|Standardized Synergy Block|Loom Signature", content, re.IGNORECASE
        )
        if marker:
            # Look ahead for relevant artifacts until next major section
            chunk = content[marker.end() : marker.end() + 3000]
            chunk_end = re.search(r"\n#|---", chunk)
            chunk = chunk[: chunk_end.start()] if chunk_end else chunk

            # Extract everything that looks like an Artifact ID and relationship
            # Format 1: | ID | Rel Type |
            for match in re.finditer(r"\|\s*([A-Z0-9][-A-Z0-9_\.]+[A-Z0-9])\s*\|\s*([A-Z_]+)\s*\|", chunk):
                target, rel = match.groups()
                synergy_nodes.add(f"- 🔗 {target} ({rel})")

            # Format 2: ID, Rel Type, Impact
            for match in re.finditer(r"([A-Z0-9][-A-Z0-9_\.]+[A-Z0-9]),\s*([A-Z_]+)\s*,", chunk):
                target, rel = match.groups()
                if rel not in ["ID", "TYPE", "impact"]:
                    synergy_nodes.add(f"- 🔗 {target} ({rel})")

        return sorted(list(synergy_nodes))

    def parse_commands(self, content: str) -> list[str]:
        """Extracts CMD: prompts and Actionable Prompt Packets."""
        command_nodes = set()

        # Inline commands
        for cmd in re.findall(r"`(CMD:.*?)`", content):
            command_nodes.add(f"- ⚡ {self.clean_text(cmd)}")

        # Table-based prompts
        for cmd in re.findall(r"\|\s*`?(CMD:.*?)`?\s*\|", content):
            command_nodes.add(f"- ⚡ {self.clean_text(cmd)}")

        return sorted(list(command_nodes))

    def parse_structure(self, content: str) -> list[str]:
        """Parses the headers into a simplified hierarchy, skipping metadata blocks."""
        structure_nodes = []
        lines = content.split("\n")

        skip_keywords = ["Block A", "Block D", "Identification Lock", "Synergy", "APP", "Actionable Prompt Packet"]

        for line in lines:
            line = line.strip()
            if line.startswith("##") and not any(kw in line for kw in skip_keywords):
                text = self.clean_text(line.replace("#", ""))
                if text:
                    structure_nodes.append(f"- 📂 {text}")

        return structure_nodes

    def process_file(self, filepath: Path) -> str:
        """Reads a file and converts it into a Mindmap Node Tree string."""
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Determine Root Title
        title_match = re.search(r"^#\s+(.*)", content, re.MULTILINE)
        root_title = self.clean_text(title_match.group(1)) if title_match else filepath.stem

        self.audit_log.append(
            {
                "type": "file_transmutation",
                "filename": filepath.name,
                "title": root_title,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Assemble logic branches
        tree = [f"# {root_title}"]

        identity = self.parse_block_a_identity(content)
        if identity:
            tree.append("## 🧬 Identity Protocol")
            tree.extend(identity)

        commands = self.parse_commands(content)
        if commands:
            tree.append("## ⚡ Actionable Commands")
            tree.extend(commands)

        synergy = self.parse_block_d_synergy(content)
        if synergy:
            tree.append("## 🕸️ Neural Network")
            tree.extend(synergy)

        structure = self.parse_structure(content)
        if structure:
            tree.append("## 📜 Archive Structure")
            tree.extend(structure)

        return "\n".join(tree) + "\n\n"

    def execute(self, input_path: str, output_path: str) -> None:
        """Orchestrates the transmutation of multiple artifacts into a single seed file."""
        try:
            abs_input = self._safe_path_resolve(input_path)
            abs_output = self._safe_path_resolve(output_path, check_exists=False)

            # Case 1: Input is a directory
            if os.path.isdir(abs_input):
                md_files = list(Path(abs_input).glob("*.md"))
                if not md_files:
                    raise ForgeError(f"No Markdown Artifacts found in {input_path}")

                console.print(f"[cyan]Found {len(md_files)} artifacts. Initiating Minting...[/cyan]")

                buffer = []
                for file in md_files:
                    buffer.append(self.process_file(file))

                final_content = "".join(buffer)

            # Case 2: Input is a single file
            else:
                final_content = self.process_file(Path(abs_input))

            # Write the minted seed
            output_dir = os.path.dirname(abs_output)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            with open(abs_output, "w", encoding="utf-8") as f:
                f.write(final_content.strip() + "\n")

            console.print(f"[bold green]✅ SUCCESS.[/bold green] Mindmap seed minted at: [bold]{output_path}[/bold]")
            self.audit_log.append({"type": "mint_success", "output": output_path})

        except Exception as e:
            self.audit_log.append({"type": "mint_failure", "error": str(e)})
            console.print(f"[bold red]MINTING FAILED:[/bold red] {e}")
            raise

    def save_audit_log(self) -> None:
        """Writes the process trace to a machine-readable JSON log."""
        log_dir = os.path.join(self.workspace, "_governance", "50_Logs", "Forge_Audit")
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"mint_seed_{timestamp}.json")

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.audit_log, f, indent=4)

        console.print(f"[dim]Audit trace saved to: {log_file}[/dim]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Minter (v14.0) - Artifact Transmutation Engine")
    parser.add_argument("--input", required=True, help="Input directory or single Markdown file")
    parser.add_argument("--output", help="Output Mindmap Seed filename (default: Nicemind_Import_Master.md)")
    parser.add_argument("--strict", action="store_true", help="Fail strictly on resolution errors")

    args = parser.parse_args()

    output_file = args.output or "Nicemind_Import_Master.md"

    # Calculate Workspace Root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    transmuter = ArtifactTransmuter(workspace_root=workspace_root, strict=args.strict)

    try:
        transmuter.execute(args.input, output_file)
    finally:
        transmuter.save_audit_log()


if __name__ == "__main__":
    main()
