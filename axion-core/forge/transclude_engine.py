"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-TRANSCLUDE-001`          | The Sovereign ID. |
| **Official Name** | `transclude_engine.py`         | The Filename.     |
| **Version**       | **v14.0**                      | The Standard.     |
| **Domain**        | `AXION`                        | The Subject.      |
| **Evolution**     | **Logic Hardening [23.5]**     | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |.

## Sovereign Ethos
This tool is the Primary Forge of the Synarche. Every byte of forged wisdom must pass through
the fires of integrity validation. It is not enough for a document to exist; it must be
correct, secure, and traceable.

"A flawed forge produces only brittle swords."
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from typing import Any

import yaml
from jinja2 import Environment, StrictUndefined
from rich.console import Console

console = Console()

# --- Sovereign Exceptions ---


class ForgeError(Exception):
    """Base exception for all Forge Toolkit errors."""

    pass


class SovereigntyViolationError(ForgeError):
    """Raised when a path resolution attempts to leave the Workspace Sanctuary."""

    pass


class RecursionDepthError(ForgeError):
    """Raised when transclusion exceeds the safe depth limit."""

    pass


class IntegrityError(ForgeError):
    """Raised when metadata or rendering integrity is compromised."""

    pass


class TranscludeEngine:
    """The Transclusion Pipeline (v14.0) - Hardened OMEGA Standard."""

    # Regex to find tags like {{ TRANSCLUDE: block_name.md }}
    TRANSCLUDE_PATTERN = re.compile(r"\{\{\s*TRANSCLUDE:\s*(.*?)\s*\}\}", re.IGNORECASE)
    MAX_DEPTH = 10

    def __init__(self, workspace_root: str, strict: bool = False) -> None:
        self.workspace = os.path.abspath(workspace_root)
        self.strict = strict
        self.shells_dir = os.path.join(self.workspace, "_governance", "templates", "Master_Shells")
        self.blocks_dir = os.path.join(self.workspace, "_governance", "templates", "Transclusion_Blocks")
        self.audit_log: list[dict[str, Any]] = []

        # Validate environment integrity
        for path in [self.shells_dir, self.blocks_dir]:
            if not os.path.exists(path):
                raise ForgeError(f"Critical Vault Missing: {path}. System integrity compromised.")

    def _safe_path_resolve(self, base_dir: str, filename: str) -> str:
        """Ensures the resolved path stays within the designated vault (Vault Jail)."""
        target_path = os.path.abspath(os.path.join(base_dir, filename))

        # Check for Symlinks (Sovereign Guard)
        if os.path.islink(target_path):
            raise SovereigntyViolationError(f"Symlink detected: {filename}. External links are forbidden in the Vault.")

        # Check for Path Traversal
        if os.path.commonpath([os.path.abspath(base_dir), target_path]) != os.path.abspath(base_dir):
            raise SovereigntyViolationError(
                f"Path Traversal Attempt: {filename}. The Forge remains within the Sanctuary."
            )

        return target_path

    def resolve_transclusions(self, content: str, depth: int = 0, transclusion_stack: list[str] | None = None) -> str:
        """Recursively resolves all TRANSCLUDE tags with stack-based cycle detection and security guards."""
        if transclusion_stack is None:
            transclusion_stack = []

        if depth > self.MAX_DEPTH:
            raise RecursionDepthError(
                f"Transclusion limit reached ({self.MAX_DEPTH}). Circular dependency or excessive nesting suspected."
            )

        def replacer(match: re.Match) -> str:
            block_filename = match.group(1).strip()

            try:
                block_path = self._safe_path_resolve(self.blocks_dir, block_filename)
            except SovereigntyViolationError as e:
                if self.strict:
                    raise
                return f"<!-- {e} -->"

            if not os.path.exists(block_path):
                error_msg = f"TRANSCLUDE ERROR: Block '{block_filename}' not found in vault."
                if self.strict:
                    raise FileNotFoundError(error_msg)
                console.print(f"[bold yellow]Warning:[/bold yellow] {error_msg}")
                return f"<!-- {error_msg} -->"

            # Cycle Detection (Ancestry Check)
            if block_path in transclusion_stack:
                raise RecursionDepthError(
                    f"Circular Transclusion Detected: {block_filename}. Stack: {' -> '.join(transclusion_stack)}"
                )

            # Log for Audit
            self.audit_log.append(
                {
                    "type": "block_ingestion",
                    "filename": block_filename,
                    "depth": depth,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            with open(block_path, encoding="utf-8") as f:
                block_content = f.read()

            # Recursive expansion - add current block to stack
            return self.resolve_transclusions(block_content, depth + 1, [*transclusion_stack, block_path])

        return self.TRANSCLUDE_PATTERN.sub(replacer, content)

    def generate_integrity_hash(self, metadata: dict[str, Any]) -> str:
        """Generates a SHA-256 hash based on core identity fields."""
        raw_string = f"{metadata.get('artifact_id')}-{metadata.get('version')}-{metadata.get('domain')}"
        return hashlib.sha256(raw_string.encode()).hexdigest()[:16].upper()

    def _auto_populate_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """Automatically injects standard OMEGA markers if missing."""
        now_iso = datetime.now().astimezone().isoformat()
        metadata.setdefault("created_iso", now_iso)
        metadata.setdefault("updated_iso", now_iso)

        # Identity Logic
        integrity_hash = self.generate_integrity_hash(metadata)
        metadata["SHA256_HASH"] = integrity_hash
        metadata["integrity_hash"] = integrity_hash

        metadata.setdefault("CLASS", "[PLANET]")
        metadata.setdefault("STATUS", metadata.get("status", "ACTIVE"))
        metadata.setdefault("DOMAIN", metadata.get("domain", "GVRN"))

        # Omnilog Closing Anchor
        ts = datetime.now()
        metadata["timestamp_anchor"] = ts.strftime("%Y-%m-%d | %H:%M")
        metadata.setdefault("causal_link", "CMD: TRANSCLUDE_ARTIFACT")
        return metadata

    def forge(self, shell_filename: str, metadata: dict[str, Any]) -> str:
        """Loads a shell, resolves transclusions, and renders variables with strictness."""
        try:
            shell_path = self._safe_path_resolve(self.shells_dir, shell_filename)
        except SovereigntyViolationError:
            # Attempt fuzzy matching but stay within shells_dir
            available = [f for f in os.listdir(self.shells_dir) if f.endswith(".md")]
            matches = [f for f in available if shell_filename.lower() in f.lower()]
            if matches:
                shell_path = os.path.join(self.shells_dir, matches[0])
                console.print(f"[cyan]Fuzzy matched shell:[/cyan] {matches[0]}")
            else:
                raise FileNotFoundError(f"Master Shell '{shell_filename}' not found.")

        if not os.path.exists(shell_path):
            raise FileNotFoundError(f"Master Shell '{shell_filename}' not found at {shell_path}.")

        self.audit_log.append(
            {
                "type": "shell_loading",
                "filename": shell_filename,
                "path": shell_path,
                "timestamp": datetime.now().isoformat(),
            }
        )

        with open(shell_path, encoding="utf-8") as f:
            raw_shell = f.read()

        # Step 1: Transclude blocks (Recursive & Guarded)
        composed_md = self.resolve_transclusions(raw_shell)

        # Step 2: Enrich Metadata
        full_metadata = self._auto_populate_metadata(metadata)

        # Step 3: Render via Jinja2 (Strict Mode)
        try:
            # Use a strict environment to catch missing metadata
            env = Environment(undefined=StrictUndefined)
            template = env.from_string(composed_md)
            rendered = template.render(**full_metadata)

            # Record Success
            self.audit_log.append({"type": "forge_success", "artifact_id": metadata.get("artifact_id")})
            return rendered
        except Exception as e:
            error_msg = f"Forging Failure: {e}"
            self.audit_log.append({"type": "forge_failure", "error": str(e)})
            console.print(f"[bold red]Jinja Rendering Error:[/bold red] {e}")
            raise IntegrityError(error_msg) from e

    def save_audit_log(self, output_path: str | None = None) -> None:
        """Writes the process trace to a machine-readable JSON log."""
        log_dir = os.path.join(self.workspace, "_governance", "50_Logs", "Forge_Audit")
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"transclude_{timestamp}.json")

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.audit_log, f, indent=4)

        console.print(f"[dim]Audit trace saved to: {log_file}[/dim]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Living Template Protocol Engine (v14.0) - Sovereign Hardened")
    parser.add_argument("--id", required=True, help="Target Artifact ID (e.g., SYNG.Doc.001)")
    parser.add_argument("--shell", required=True, help="Master Shell filename or substring (e.g., UMB, AOP, CSL)")
    parser.add_argument("--meta", help="Path to YAML metadata file")
    parser.add_argument("--out", help="Output file path (optional, prints to stdout if not provided)")
    parser.add_argument("--strict", action="store_true", help="Fail strictly on missing transclusions or variables")

    args = parser.parse_args()

    # Base Metadata
    metadata = {
        "artifact_id": args.id,
        "official_name": f"{args.id}.md",
        "version": "v14.0",
        "domain": args.id.split(".")[0] if "." in args.id else "UNKNOWN",
    }

    # Calculate Workspace Root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

    engine = TranscludeEngine(workspace_root=workspace_root, strict=args.strict)

    # Load Context YAML if provided (Hardened)
    if args.meta:
        try:
            meta_path = os.path.abspath(args.meta)
            # Vault Jail: Metadata must be inside the workspace
            if os.path.commonpath([workspace_root, meta_path]) != workspace_root:
                raise SovereigntyViolationError(f"Metadata traversal attempt: {args.meta}")

            if os.path.exists(meta_path):
                with open(meta_path, encoding="utf-8") as f:
                    yaml_meta = yaml.safe_load(f)
                    if yaml_meta:
                        metadata.update(yaml_meta)
                        engine.audit_log.append({"type": "meta_loaded", "path": meta_path})
        except Exception as e:
            console.print(f"[bold red]Metadata Error:[/bold red] {e}")
            if args.strict:
                sys.exit(1)

    try:
        with console.status(f"[bold green]Forging {args.id} from [cyan]{args.shell}[/cyan]..."):
            result = engine.forge(args.shell, metadata)

        if args.out:
            out_abs = os.path.abspath(args.out)
            # Integrity check for output path
            if os.path.commonpath([workspace_root, out_abs]) != workspace_root:
                raise SovereigntyViolationError(f"Output path outside sanctuary: {args.out}")

            os.makedirs(os.path.dirname(out_abs), exist_ok=True)
            with open(out_abs, "w", encoding="utf-8") as f:
                f.write(result)
            console.print(f"[bold green]Successfully Forged:[/bold green] {args.out}")
        else:
            console.print("\n" + result)

    except Exception as e:
        console.print(f"[bold red]FORGE FAILED:[/bold red] {e}")
        sys.exit(1)
    finally:
        engine.save_audit_log()


if __name__ == "__main__":
    main()
