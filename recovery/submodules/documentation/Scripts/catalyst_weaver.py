import argparse
import datetime
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any

# Reference: DOC-STD-001 (Coding Standards)
# Context: Implements the "Reality Weaving" protocol for bundling context.


@dataclass
class CatalystBundle:
    """
    Data Class representing the 'Weaved Reality'.
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
    """
    The Weaver Engine.
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

    def add_command(self, name: str, logic: str) -> None:
        """
        Injects a specific rule or script (The Weft).
        """
        # Why: Commands must be named to allow the AI to reference them by handle.
        entry = {"name": name, "logic": logic}
        self.bundle.commands.append(entry)
        # print(f"[WEAVER] Command '{name}' integrated.")

    def add_blueprint(self, name: str, schema: dict[str, Any]) -> None:
        """
        Injects a structural template (The Warp).
        """
        # Why: Blueprints are stored as Dicts to preserve JSON structure.
        entry = {"name": name, "schema": schema}
        self.bundle.blueprints.append(entry)
        # print(f"[WEAVER] Blueprint '{name}' integrated.")

    def add_process(self, instruction: str) -> None:
        """
        Injects the narrative intent (The Pattern).
        """
        self.bundle.processes.append(instruction)
        # print("[WEAVER] Process instruction woven.")

    def weave_reality(self) -> str:
        """
        Serializes the bundle into a portable Synarche Artifact string.
        """
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


# --- CLI Implementation ---


def main():
    parser = argparse.ArgumentParser(description="Synarche Catalyst Weaver")
    parser.add_argument("name", help="Name of the Bundle")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument(
        "--command", "-c", action="append", nargs=2, metavar=("NAME", "LOGIC"), help="Add a Command (Name, Logic)"
    )
    parser.add_argument("--process", "-p", action="append", help="Add a Process instruction")

    args = parser.parse_args()

    # 1. Initialize
    weaver = CatalystWeaver(args.name)

    # 2. Add Commands
    if args.command:
        for name, logic in args.command:
            weaver.add_command(name, logic)

    # 3. Add Processes
    if args.process:
        for proc in args.process:
            weaver.add_process(proc)

    # 4. Weave
    artifact = weaver.weave_reality()

    # 5. Output
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(artifact)
            print(f"✅ Bundle '{args.name}' weaved to {args.output}")
        except Exception as e:
            print(f"❌ Failed to write output: {e}")
            sys.exit(1)
    else:
        print(artifact)


if __name__ == "__main__":
    main()
