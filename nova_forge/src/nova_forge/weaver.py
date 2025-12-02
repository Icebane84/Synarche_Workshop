"""
Artifact ID: CODE-REF-003
Module: Catalyst Weaver
Context: Nova Forge > Backend > Prompt Engineering
Description: Generates structured prompt bundles for AI ingestion.
"""

import datetime


class CatalystWeaver:
    """
    Constructs a standardized 'Catalyst Bundle' (prompt context).
    """

    def __init__(self, bundle_name: str):
        self.bundle_name = bundle_name
        self.timestamp = datetime.datetime.now().isoformat()
        self.processes: list[str] = []
        self.context_files: list[str] = []

    def add_process(self, instruction: str) -> None:
        """Adds a core instruction step."""
        self.processes.append(instruction)

    def add_context(self, file_path: str) -> None:
        """
        Reads a file and adds its content to the context.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.context_files.append(f"--- FILE: {file_path} ---\n{content}\n")
        except Exception as e:
            self.context_files.append(
                f"--- FILE: {file_path} ---\n[ERROR] Could not read file: {e}\n"
            )

    def generate(self) -> str:
        """Compiles the bundle into a formatted string."""
        header = f"""
# CATALYST BUNDLE: {self.bundle_name}
# Generated: {self.timestamp}
# Context: Synarche Workspace
--------------------------------------------------
"""
        body = "\n## DIRECTIVES\n"
        for i, proc in enumerate(self.processes, 1):
            body += f"{i}. {proc}\n"

        if self.context_files:
            body += "\n## ATTACHED CONTEXT\n"
            for context_item in self.context_files:
                body += f"{context_item}\n"

        footer = "\n--------------------------------------------------\nEnd of Bundle"

        return header + body + footer
