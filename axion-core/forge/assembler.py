"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-ASSEMBLER-001`                | The Sovereign ID. |
| **Official Name** | `assembler.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import argparse
import hashlib
import os
import sys
from datetime import datetime
from typing import Any, ClassVar

import yaml
from jinja2 import Environment, FileSystemLoader
from rich.console import Console

console = Console()


class Assembler:
    """The Forge Engine (v13.2) - Axion Standard."""

    BLOCK_MAP: ClassVar[list[tuple[str, str, bool | str]]] = [
        ("0", "SELT-HEADER-000.md", True),  # Block 0: UIP
        ("A", "SELT-HEADER-UIP-001.md", True),  # Block A: 13-Point Lock
        ("U", "SELT-HEADER-UMG-001.md", "include_umg"),  # UMG
        ("V", "SELT-VECTOR-STATE-001.md", "include_vstate"),  # V-STATE
        ("K", "SELT-RISK-GOV-001.md", "include_risk"),  # RISK-GOV
        ("L", "SELT-LINK-DECOHERENCE-001.md", "include_link"),  # LINK-DCO
        ("T", "SELT-CMD-TRANSITION-001.md", "include_trans"),  # CMD-TRANS
        ("C", "SELT-COMP-ARCH-001.md", "include_arch"),  # COMP-ARCH
        ("P", "SELT-APP-001.md", "include_app"),  # APP (Standard)
        ("I", "SELT-IMPACT-SIG-001.md", "include_impact"),  # IMPACT-SIG
        ("S", "SELT-SRS-001.md", "include_srs"),  # SRS()
        ("D", "SELT-ANALYSIS-PRED-001.md", "include_pred"),  # PRED
        ("N", "SELT-CSL-NOVA-001.md", "include_nova"),  # CSL-NOVA
        ("F", "SELT-GOVERNANCE-FIN-001.md", "include_fin"),  # GOVERNANCE-FIN
        ("Y", "SELT-SYNERGY-VECTOR-001.md", "include_synergy"),  # SYNERGY-VECTOR
        ("g", "SELT-COGNITION-001.md", "include_cognition"),  # COGNITION
        ("Z", "SELT-ANCHOR-OMNI.md", True),
    ]

    SCAFFOLD_MAP: ClassVar[dict[str, list[str]]] = {
        "AOP": [
            "include_vstate",
            "include_risk",
            "include_trans",
            "include_synergy",
            "include_app",
            "include_umg",
        ],
        "UMB": [
            "include_arch",
            "include_srs",
            "include_impact",
            "include_synergy",
            "include_app",
            "include_umg",
        ],
        "CSL": ["include_nova", "include_link", "include_umg"],
        "SELT": ["include_umg"],
        "KNOWLEDGE": [
            "include_pred",
            "include_start_stop",
            "include_umg",
        ],  # Future proofing
    }

    def __init__(self, template_dir: str, strict: bool = False) -> None:
        self.template_dir = template_dir
        self.strict = strict
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir), autoescape=True
        )
        self.quarantine_dir = os.path.join(os.getcwd(), ".quarantine")

    def validate_metadata(self, metadata: dict[str, Any]) -> list[str]:
        """Verify mandatory OMEGA metadata fields."""
        required = ["artifact_id", "version", "status", "domain", "evolution"]
        return [f for f in required if not metadata.get(f)]

    def _should_include_block(
        self,
        condition: bool | str,
        metadata: dict[str, Any],
        # Feature Flags
        include_rpg: bool,
        include_fin: bool,
        include_vstate: bool = False,
        include_risk: bool = False,
        include_link: bool = False,
        include_trans: bool = False,
        include_arch: bool = False,
        include_impact: bool = False,
        include_srs: bool = False,
        include_pred: bool = False,
        include_nova: bool = False,
        include_app: bool = False,
        include_umg: bool = False,
        include_synergy: bool = False,
        include_cognition: bool = False,
    ) -> bool:
        """Helper to determine if a block should be included."""
        if isinstance(condition, bool):
            return condition
        if condition == "active_mask":
            return bool(metadata.get("active_mask"))

        # Dynamic Mapping
        flag_map = {
            "include_rpg": include_rpg,
            "include_fin": include_fin,
            "include_vstate": include_vstate,
            "include_risk": include_risk,
            "include_link": include_link,
            "include_trans": include_trans,
            "include_arch": include_arch,
            "include_impact": include_impact,
            "include_srs": include_srs,
            "include_pred": include_pred,
            "include_nova": include_nova,
            "include_app": include_app,
            "include_umg": include_umg,
            "include_synergy": include_synergy,
            "include_cognition": include_cognition,
        }

        return flag_map.get(condition, False)

    def generate_integrity_hash(self, metadata: dict[str, Any]) -> str:
        """Generates a SHA-256 hash based on core identity fields."""
        raw_string = f"{metadata.get('artifact_id')}-{metadata.get('version')}-{metadata.get('domain')}"
        return hashlib.sha256(raw_string.encode()).hexdigest()[:16].upper()

    def assemble(
        self,
        metadata: dict[str, Any],
        include_rpg: bool = False,
        include_fin: bool = True,
        # DTS Flags
        include_vstate: bool = False,
        include_risk: bool = False,
        include_link: bool = False,
        include_trans: bool = False,
        include_arch: bool = False,
        include_impact: bool = False,
        include_srs: bool = False,
        include_pred: bool = False,
        include_nova: bool = False,
        include_app: bool = False,
        include_umg: bool = False,
        include_synergy: bool = False,
        include_cognition: bool = False,
    ) -> str:
        """Assembles the SELT blocks using the structured BLOCK_MAP."""
        # Auto-Populate Timestamps and Derived Fields
        now_iso = datetime.now().astimezone().isoformat()
        metadata.setdefault("created_iso", now_iso)
        metadata.setdefault("updated_iso", now_iso)
        metadata.setdefault("RNC_ID", metadata.get("artifact_id"))

        # Identity Logic
        active_mask = metadata.get("active_mask")
        if not active_mask:
            active_mask = "SHARD_ARCHITECT_VOID"
        metadata["TAROT_SHARD"] = active_mask

        # Integrity Logic
        integrity_hash = self.generate_integrity_hash(metadata)
        metadata["SHA256_HASH"] = integrity_hash
        metadata["integrity_hash"] = integrity_hash

        metadata.setdefault("GENESIS_STAMP", now_iso)
        metadata.setdefault("ORIGIN_EVENT", "Manual Creation via Forge")
        metadata.setdefault("PRIMARY_LINK", "GOVERNED_BY: CORE-CODEX-001")
        metadata.setdefault("AUDIT_VERDICT", "PASS")
        metadata.setdefault("SIGNAL", "OMEGA")
        metadata.setdefault("CLASS", "[PLANET]")
        metadata.setdefault(
            "ALIGNMENT", metadata.get("evolution", "Cognitive Ascension")
        )
        metadata.setdefault("STATUS", metadata.get("status", "ACTIVE"))
        metadata.setdefault("DOMAIN", metadata.get("domain", "GVRN"))

        # Omni-Anchor v3.0 Logic
        metadata.setdefault("causal_link", "CMD: FORGE_ARTIFACT")
        metadata.setdefault(
            "state_vector",
            f"{metadata['SHA256_HASH'][:8]} : LOGIC_GATE_OPEN : {metadata['SIGNAL']}",
        )

        # Chronos Lock Timestamp (YYYY-MM-DD | HH:MM)
        ts = datetime.now()
        metadata["timestamp_anchor"] = ts.strftime("%Y-%m-%d | %H:%M")

        missing_meta = self.validate_metadata(metadata)
        if missing_meta:
            error_msg = f"Missing mandatory metadata: {', '.join(missing_meta)}"
            if self.strict:
                self.quarantine(metadata, "", [error_msg])
                raise ValueError(error_msg)
            console.print(f"[bold yellow]Warning:[/bold yellow] {error_msg}")

        full_markdown = ""
        errors = []

        for code, block_name, condition in self.BLOCK_MAP:
            if not self._should_include_block(
                condition,
                metadata,
                include_rpg,
                include_fin,
                include_vstate,
                include_risk,
                include_link,
                include_trans,
                include_arch,
                include_impact,
                include_srs,
                include_pred,
                include_nova,
                include_app,
                include_umg,
                include_synergy,
                include_cognition,
            ):
                continue

            try:
                template = self.env.get_template(block_name)
                rendered = template.render(**metadata)
                full_markdown += rendered.strip() + "\n\n---\n\n"
            except Exception as e:
                err = f"Block {code} ({block_name}) failed: {e}"
                errors.append(err)
                if self.strict:
                    self.quarantine(metadata, full_markdown, errors)
                    raise RuntimeError(f"Strict Mode Violation: {err}") from e
                console.print(f"[bold red]Error rendering {block_name}:[/bold red] {e}")

        return full_markdown

    def quarantine(
        self, metadata: dict[str, Any], partial_content: str, errors: list[str]
    ) -> None:
        """Safely divert failed artifacts to quarantine."""
        if not os.path.exists(self.quarantine_dir):
            os.makedirs(self.quarantine_dir)

        artifact_id = metadata.get("artifact_id", "unknown")
        filename = f"QUARANTINE_{artifact_id}.md"
        path = os.path.join(self.quarantine_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write("# !!! QUARANTINED ARTIFACT !!!\n")
            f.write("## Errors Encountered:\n")
            for err in errors:
                f.write(f"- {err}\n")
            f.write("\n---\n\n")
            f.write(partial_content)

        console.print(f"[bold red]Artifact Quarantined:[/bold red] {path}")


def discover_skills(mask: str, skills_dir: str) -> list[str]:
    """Discover skills matching the mask archetype."""
    found = []
    if os.path.exists(skills_dir):
        for skill in os.listdir(skills_dir):
            if mask.lower() in skill.lower():
                found.append(skill)
    return found


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Synarche Forge: Artifact Assembler (v13.2)"
    )
    parser.add_argument("--id", required=True, help="Target Artifact ID")
    parser.add_argument(
        "--type",
        choices=["AOP", "UMB", "CSL", "SELT"],
        help="Artifact Archetype Preset",
    )
    parser.add_argument("--mask", help="Active Tarot Mask")
    parser.add_argument("--abilities", help="Extra abilities")
    parser.add_argument("--rpg", action="store_true", help="Include RPG Integration")
    parser.add_argument("--strict", action="store_true", help="Enable Strict Mode")
    parser.add_argument("--out", help="Output file path")
    parser.add_argument("--meta", help="Path to YAML metadata file")

    # DTS Expansion Flags
    parser.add_argument(
        "--vstate", action="store_true", help="Include Vector State Block"
    )
    parser.add_argument(
        "--risk", action="store_true", help="Include Risk Governance Block"
    )
    parser.add_argument(
        "--link", action="store_true", help="Include Linkage/Decoherence Block"
    )
    parser.add_argument(
        "--trans", action="store_true", help="Include Command Transition Block"
    )
    parser.add_argument(
        "--arch", action="store_true", help="Include Component Architecture"
    )
    parser.add_argument(
        "--impact", action="store_true", help="Include Impact Signature"
    )
    parser.add_argument(
        "--srs", action="store_true", help="Include Systemic Relationship Standard"
    )
    parser.add_argument(
        "--pred", action="store_true", help="Include Predictive Analysis"
    )
    parser.add_argument("--nova", action="store_true", help="Include CSL Nova Spark")
    parser.add_argument(
        "--app", action="store_true", help="Include Actionable Prompt Packet"
    )
    parser.add_argument(
        "--umg", action="store_true", help="Include Universal Metadata & Governance"
    )
    parser.add_argument(
        "--synergy",
        action="store_true",
        help="Include Synergy Vector (Relational Dynamics)",
    )
    parser.add_argument(
        "--cognition", action="store_true", help="Include Cognitive Resonance Block"
    )

    args = parser.parse_args()

    # Default Metadata
    metadata = {
        "artifact_id": args.id,
        "official_name": f"{args.id}_Artifact.md",
        "version": "v13.2",
        "status": "DRAFT",
        "ethos": "Operational Coherence",
        "evolution": "Omega Ascension",
        "domain": args.id.split(".")[0] if "." in args.id else "GVRN",
        "active_mask": args.mask,
        "enabled_abilities": args.abilities if args.abilities else "None",
    }

    # Enhanced Skill Discovery
    if args.mask:
        skills_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", ".agent", "skills"
        )
        found_skills = discover_skills(args.mask, skills_dir)
        if found_skills:
            metadata["enabled_abilities"] = (
                f"{metadata['enabled_abilities']}, {', '.join(found_skills)}"
                if metadata["enabled_abilities"] != "None"
                else ", ".join(found_skills)
            )

    # Load from file if provided
    if args.meta and os.path.exists(args.meta):
        with open(args.meta, encoding="utf-8") as f:
            meta_data = yaml.safe_load(f)
            if meta_data:
                metadata.update(meta_data)

    template_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "_governance",
        "templates",
        "Transclusion_Blocks",
    )
    assembler = Assembler(template_path, strict=args.strict)

    # Scaffolding Logic
    flags = {
        "include_rpg": args.rpg,
        "include_vstate": args.vstate,
        "include_risk": args.risk,
        "include_link": args.link,
        "include_trans": args.trans,
        "include_arch": args.arch,
        "include_impact": args.impact,
        "include_srs": args.srs,
        "include_pred": args.pred,
        "include_nova": args.nova,
        "include_app": args.app,
        "include_umg": args.umg,
        "include_synergy": args.synergy,
        "include_cognition": args.cognition,
        "include_fin": True,  # Always include finalization by default
    }

    if args.type:
        scaffold_flags = Assembler.SCAFFOLD_MAP.get(args.type, [])
        for flag in scaffold_flags:
            flags[flag] = True
        metadata["artifact_type"] = args.type
        console.print(f"[bold cyan]Applying Scaffold: {args.type}[/bold cyan]")

    try:
        with console.status(f"[bold green]Forging {args.id}..."):
            result = assembler.assemble(metadata, **flags)

        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[bold green]Success![/bold green] [cyan]{args.out}[/cyan]")
        else:
            console.print(result)
    except Exception as e:
        console.print(f"[bold red]FORGE FAILED:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
