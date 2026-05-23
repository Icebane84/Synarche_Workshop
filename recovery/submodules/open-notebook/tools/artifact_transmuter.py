import os
import re
from pathlib import Path

# ==========================================
# PHOENIX PROTOCOL PARSER & TRANSMUTER
# ==========================================
# DIRECTIVE: Convert GVRN/SYNG Markdown Artifacts into Nicemind-Optimized Import Format.
# TARGET: NiceMind (Header = Node, Bullet = Child Node)
# ==========================================


class ArtifactTransmuter:
    def __init__(self, source_path, output_file):
        self.source_path = Path(source_path)
        self.output_file = Path(output_file)
        self.buffer = []

    def log(self, message):
        print(f"[CODEX_MINT] {message}")

    def clean_text(self, text):
        """Removes markdown bold/italic clutter for cleaner node titles."""
        text = text.replace("**", "").replace("*", "").replace("`", "").strip()
        return text

    def parse_block_a_identity(self, content):
        """Extracts Key Metadata from Block A (The Identification Lock)."""
        identity_nodes = []

        # Regex to find the ID and Version within the pipe table
        # Handles optional markdown formatting in keys (keywords may be bolded)
        id_match = re.search(
            r"\|\s*[*]*Artifact ID[*]*\s*\|\s*(.*?)\s*\|", content, re.IGNORECASE
        )
        ver_match = re.search(
            r"\|\s*[*]*Version[*]*\s*\|\s*(.*?)\s*\|", content, re.IGNORECASE
        )
        status_match = re.search(
            r"\|\s*[*]*Status[*]*\s*\|\s*(.*?)\s*\|", content, re.IGNORECASE
        )
        class_match = re.search(
            r"\|\s*[*]*Celestial Class[*]*\s*\|\s*(.*?)\s*\|", content, re.IGNORECASE
        )

        if id_match:
            identity_nodes.append(f"- 🆔 ID: {self.clean_text(id_match.group(1))}")
        if ver_match:
            identity_nodes.append(
                f"- 🚩 Version: {self.clean_text(ver_match.group(1))}"
            )
        if class_match:
            identity_nodes.append(
                f"- ⚖️ Class: {self.clean_text(class_match.group(1))}"
            )
        if status_match:
            identity_nodes.append(
                f"- 🔋 Status: {self.clean_text(status_match.group(1))}"
            )

        return identity_nodes

    def parse_block_d_synergy(self, content):
        """Extracts Relationships from Block D (The Loom Signature)."""
        synergy_nodes = []

        # Look for Block D header
        # Updated to handle markdown bolding e.g. ### **Block D
        # Also handles plain ### Block D
        block_d_start = re.search(r"###\s*[*]*Block D", content, re.IGNORECASE)
        if block_d_start:
            # Extract text after Block D until the next header or EOF
            post_header = content[block_d_start.end() :]
            end_match = re.search(r"\n#", post_header)
            block_content = (
                post_header[: end_match.start()] if end_match else post_header
            )

            # Parse CSV-like lines or Table lines
            lines = block_content.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Cleanup simple CSV format: ID, Relationship, Description
                # e.g. CORE-CODEX-001, GOVERNS, The Codex provides...
                if (
                    "," in line
                    and not line.startswith("|")
                    and not line.startswith("Synergistic")
                ):
                    parts = line.split(",")
                    if len(parts) >= 2:
                        target = self.clean_text(parts[0])
                        rel_type = self.clean_text(parts[1])
                        synergy_nodes.append(f"- 🔗 {target} ({rel_type})")

                # Cleanup Table format
                elif "|" in line and "---" not in line and "Synergistic" not in line:
                    parts = [p for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        target = self.clean_text(parts[0])
                        rel_type = self.clean_text(parts[1])
                        synergy_nodes.append(f"- 🔗 {target} ({rel_type})")

        return synergy_nodes

    def parse_commands(self, content):
        """Extracts CMD: prompts and Actionable Prompt Packets."""
        command_nodes = []

        # Regex for inline commands
        raw_commands = re.findall(r"`(CMD:.*?)`", content)
        for cmd in raw_commands:
            command_nodes.append(f"- ⚡ {self.clean_text(cmd)}")

        # Regex for Table based APP (Actionable Prompt Packet)
        # We look for lines containing `CMD:` inside pipes
        table_commands = re.findall(r"\|\s*`?(CMD:.*?)`?\s*\|", content)
        for cmd in table_commands:
            if f"- ⚡ {self.clean_text(cmd)}" not in command_nodes:
                command_nodes.append(f"- ⚡ {self.clean_text(cmd)}")

        return list(set(command_nodes))  # Remove duplicates

    def parse_structure(self, content):
        """Parses the headers into a simplified hierarchy, skipping metadata blocks."""
        structure_nodes = []
        lines = content.split("\n")

        for line in lines:
            line = line.strip()
            # Catch Headers, but skip the specific Blocks we parsed separately to avoid duplication
            # This ensures only the actual "Content" of the artifact makes it to the Structure branch
            if line.startswith("##") and not any(
                x in line
                for x in ["Block A", "Block D", "Identification Lock", "Synergy"]
            ):
                line.count("#")
                text = self.clean_text(line.replace("#", ""))
                # Nicemind formatting: Just text. Hierarchy is handled by parent grouping later.
                # For this parser, we will treat H2/H3 as generic content nodes
                structure_nodes.append(f"- 📂 {text}")

        return structure_nodes

    def process_file(self, filepath):
        """Reads a file and converts it into a Mindmap Node Tree."""
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        filename = filepath.stem
        # Try to find the real Title (# Title)
        title_match = re.search(r"^#\s+(.*)", content, re.MULTILINE)
        root_title = self.clean_text(title_match.group(1)) if title_match else filename

        self.log(f"Transmuting: {root_title}")

        # --- BUILD THE NODE TREE ---

        # 1. ROOT NODE (The File Name/Title)
        # In Markdown for Nicemind, H1 is a Central Topic
        tree = [f"# {root_title}"]

        # 2. IDENTITY BRANCH (From Block A)
        identity = self.parse_block_a_identity(content)
        if identity:
            tree.append("## 🧬 Identity Protocol")
            tree.extend(identity)

        # 3. COMMANDS BRANCH (Extracted CMDs)
        commands = self.parse_commands(content)
        if commands:
            tree.append("## ⚡ Actionable Commands")
            tree.extend(commands)

        # 4. NETWORK BRANCH (From Block D / Relations)
        synergy = self.parse_block_d_synergy(content)
        if synergy:
            tree.append("## 🕸️ Neural Network")
            tree.extend(synergy)

        # 5. STRUCTURE BRANCH (Remaining Headers)
        structure = self.parse_structure(content)
        if structure:
            tree.append("## 📜 Archive Structure")
            tree.extend(structure)

        # Add a spacer for the next file
        self.buffer.append("\n".join(tree))
        self.buffer.append("\n")

    def execute(self):
        if not self.source_path.exists():
            self.log(f"ERROR: Source path '{self.source_path}' not found.")
            return

        if self.source_path.is_file():
            self.process_file(self.source_path)
        else:
            files = list(self.source_path.glob("*.md"))
            if not files:
                self.log("No markdown files found to transmute.")
                return

            self.log(f"Found {len(files)} artifacts.")

            for file in files:
                self.process_file(file)

        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.buffer))

        self.log(f"✅ SUCCESS. Mindmap seed generated at: {self.output_file}")
        self.log("Import this file directly into Nicemind.")


# ==========================================
# EXECUTION ENTRY POINT
# ==========================================
if __name__ == "__main__":
    import sys

    # Hardcoded for this task as requested, but flexible enough if args provided
    SOURCE = r"c:\Users\Chris\Synarche_Workspace\_governance\00_Codex\CORE-CODEX-001_ThePhoenixCodex_v13.1.md"
    OUTPUT = r"c:\Users\Chris\Synarche_Workspace\open-notebook\open_notebook\tools\Nicemind_Codex_Import.md"

    if len(sys.argv) > 1:
        SOURCE = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT = sys.argv[2]

    transmuter = ArtifactTransmuter(SOURCE, OUTPUT)
    transmuter.execute()
