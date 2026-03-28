import datetime
import json
from dataclasses import asdict, dataclass
from typing import Any

# Reference: DOC-STD-001 (Coding Standards)
# Context: Implements the "Reality Weaving" protocol for bundling context.


@dataclass
class CatalystBundle:
    """Data Class representing the 'Weaved Reality'.
    Acts as the immutable state container for transfer.
    """

    name: str
    version: str
    timestamp: str
    commands: list[dict[str, str]]  # Scripts/Rules
    blueprints: list[dict[str, Any]]  # Templates/Schemas
    processes: list[str]  # Narrative Prompts/Instructions
    meta_tags: list[str]


class CatalystWeaver:
    """The Weaver Engine.
    Aggregates disparate conceptual elements into a single portable artifact.
    """

    def __init__(self, bundle_name: str, version: str = "1.0.0"):
        # Why: Initialize the empty state to ensure strict typing of the bundle.
        self.bundle = CatalystBundle(
            name=bundle_name,
            version=version,
            timestamp=datetime.datetime.now().isoformat(),
            commands=[],
            blueprints=[],
            processes=[],
            meta_tags=[],
        )

        # Integrate Cognitive Engine (if available)
        try:
            import os
            import sys

            sys.path.append(
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "axion-core")
                )
            )
            from src.logic.nlp.nlp_engine import AxionCognition

            self.cognition = AxionCognition()
        except ImportError:
            self.cognition = None

    def extract_meta_tags(self, content: str) -> None:
        """Uses the cognitive engine to extract resonance tags from content."""
        if self.cognition:
            analysis = self.cognition.process(content)
            entities = [ent[0] for ent in analysis.get("entities", [])]
            intent = analysis.get("user_intent_goal", "unknown")
            self.bundle.meta_tags.extend(list(set(entities + [intent])))
            print(f"[WEAVER] Extracted cognitive tags: {self.bundle.meta_tags}")

    def add_command(self, name: str, logic: str) -> None:
        """Injects a specific rule or script (The Weft)."""
        # Why: Commands must be named to allow the AI to reference them by handle.
        entry = {"name": name, "logic": logic}
        self.bundle.commands.append(entry)
        print(f"[WEAVER] Command '{name}' integrated.")

    def add_blueprint(self, name: str, schema: dict[str, Any]) -> None:
        """Injects a structural template (The Warp)."""
        # Why: Blueprints are stored as Dicts to preserve JSON structure.
        entry = {"name": name, "schema": schema}
        self.bundle.blueprints.append(entry)
        print(f"[WEAVER] Blueprint '{name}' integrated.")

    def add_process(self, instruction: str) -> None:
        """Injects the narrative intent (The Pattern)."""
        self.bundle.processes.append(instruction)
        print("[WEAVER] Process instruction woven.")

    def weave_reality(self) -> str:
        """Serializes the bundle into a portable Synarche Artifact string."""
        # Why: We use ensure_ascii=False to allow special characters in prompt text.
        raw_json = json.dumps(asdict(self.bundle), indent=4, ensure_ascii=False)

        # Why: Wrapping in Markdown makes it "Human Readable" and "AI Parseable".
        artifact = (
            f"# Synarche Catalyst Bundle: {self.bundle.name}\n"
            f"**Version:** {self.bundle.version}\n"
            f"**Generated:** {self.bundle.timestamp}\n"
            f"---\n"
            f"```json\n"
            f"{raw_json}\n"
            f"```\n"
            f"---\n"
            f"**[INSTRUCTION TO AI]**: Ingest this JSON block. "
            f"Map 'commands' to your constraints, 'blueprints' to your output formats, "
            f"and execute the 'processes' immediately."
        )
        return artifact


# --- Usage Example (Simulation) ---

if __name__ == "__main__":
    # 1. Initialize the Weaver
    weaver = CatalystWeaver("Project_Genesis_Initiative")

    # 2. Add a Command (Script/Rule)
    weaver.add_command(
        name="Rule_of_Precision",
        logic="All outputs must follow the What/How/Why framework.",
    )

    # 3. Add a Blueprint (Container)
    weaver.add_blueprint(
        name="UMB_Template_Simple",
        schema={
            "field_1": "Artifact ID",
            "field_2": "Description",
            "field_3": "Next Steps",
        },
    )

    # 4. Add a Process (Prompt Packet)
    weaver.add_process(
        "Analyze the current user sentiment and generate a report using the UMB Template."
    )

    # 5. Weave
    final_artifact = weaver.weave_reality()

    # Outputting to console (or file in real usage)
    print("\n--- FINAL WEAVED ARTIFACT ---\n")
    print(final_artifact)
