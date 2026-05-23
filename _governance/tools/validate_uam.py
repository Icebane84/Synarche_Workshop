import os
import re
import sys
import textwrap

import jsonschema
import yaml

# Reconfigure stdout/stderr to UTF-8 for cross-platform unicode safety
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Canonical UIP-V15 Sovereign JSON Schema (Draft-07 compliant)
UIP_V15_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "SovereignArtifactAnchor",
    "description": "Validation schema for UIP-V15 / UAM Artifact Anchor metadata blocks.",
    "type": "object",
    "required": [
        "id",
        "version",
        "provenance",
        "domain",
        "celestial_class",
        "tier",
        "state",
        "ethos",
    ],
    "additionalProperties": False,
    "properties": {
        "id": {
            "type": "string",
            "description": "The unique sovereign identifier of the artifact.",
            "pattern": "^[A-Z]{3,4}\\.[A-Z0-9._-]{3,30}\\.[0-9]{3}$",
        },
        "version": {
            "type": "string",
            "description": "Semantic versioning with optional architectural ring details.",
            "pattern": "^v[0-9]+\\.[0-9]+(?:\\.[0-9]+)?(?:\\s+\\[[A-Z]+\\])?$",
        },
        "provenance": {
            "type": "string",
            "format": "date",
            "description": "The ISO date of creation or canonization (YYYY-MM-DD).",
        },
        "domain": {
            "type": "string",
            "description": "Architectural partition defining the artifact's scope.",
            "enum": ["CORE", "FABRIC", "INFRA", "GVRN", "TEST", "LORE", "COMPUTE"],
        },
        "celestial_class": {
            "type": "string",
            "description": "Hierarchy ranking within the Synarchy network.",
            "enum": ["STAR", "PLANET", "MOON"],
        },
        "tier": {
            "type": "string",
            "description": "Functional layer of execution.",
            "enum": ["PRESENTATION", "LOGIC", "DATA", "COMPUTE", "GOVERNANCE"],
        },
        "state": {
            "type": "string",
            "description": "The governance lifecycle stage of the asset.",
            "enum": ["PROPOSED", "DRAFT", "ACTIVE", "CANONIZED"],
        },
        "ethos": {
            "type": "string",
            "description": "The singular, fundamental reason for this file's existence.",
            "maxLength": 120,
        },
        "relations": {
            "type": "array",
            "description": "Graph edges linking this artifact to the rest of the workspace.",
            "items": {
                "type": "object",
                "required": ["type", "node"],
                "additionalProperties": False,
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": [
                            "GOVERNS",
                            "SYNERGIZES",
                            "DEPENDS_ON",
                            "CONTROLS",
                            "IMPLEMENTS",
                            "UPDATES",
                        ],
                    },
                    "node": {
                        "type": "string",
                        "description": "Target Artifact ID or file path.",
                    },
                },
            },
        },
    },
}


def validate_uam_anchors(directory_path: str, require_all: bool = False) -> bool:
    """Scans a directory for active source files containing the artifact_anchor block
    and validates them against the UIP-V15 JSON Schema using PyYAML and jsonschema.
    """
    # Exclude standard/archival/cache/environment directories
    ignored_dirs = {
        ".git",
        "__pycache__",
        "node_modules",
        "venv",
        "env",
        ".agent",
        "_archive",
        ".archives",
        "_logs",
        "logs",
        ".mypy_cache",
        ".ruff_cache",
        "recovery",
        "incoming",
        ".trunk",
        ".vscode",
        "scratch",
        "artifacts",
        ".pytest_cache",
    }

    # Match block following 'artifact_anchor:' and stop at typical comment/YAML frontmatter closers.
    # We optionally match a single newline after the colon to preserve the first line's indentation.
    anchor_pattern = re.compile(
        r"artifact_anchor:(?:[ \t]*\n)?(.*?)(?:-->|\"\"\"|'''|\*/|---|\Z)", re.DOTALL
    )

    missing_anchor_files = []
    invalid_anchor_files = []
    valid_anchor_files = []

    print(f"Scanning Nexus directory: {os.path.abspath(directory_path)}...\n")

    for root, dirs, files in os.walk(directory_path):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for file in files:
            # Target relevant source files and skip the validator itself
            if (
                not file.endswith((".py", ".html", ".md", ".ts", ".js"))
                or file == "validate_uam.py"
            ):
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                match = anchor_pattern.search(content)

                if not match:
                    if require_all:
                        missing_anchor_files.append(file_path)
                    continue

                anchor_text = match.group(1)

                # Safe-dedent the YAML block to prevent indentation alignment parsing failures
                dedented_yaml = textwrap.dedent(anchor_text)

                try:
                    anchor_data = yaml.safe_load(dedented_yaml)
                except Exception as yaml_err:
                    invalid_anchor_files.append(
                        (file_path, f"YAML Parse Failure: {yaml_err}")
                    )
                    continue

                if not isinstance(anchor_data, dict):
                    invalid_anchor_files.append(
                        (file_path, "Metadata is not a key-value dictionary")
                    )
                    continue

                # Run jsonschema validation with Date format checker
                try:
                    jsonschema.validate(
                        instance=anchor_data,
                        schema=UIP_V15_SCHEMA,
                        format_checker=jsonschema.FormatChecker(),
                    )
                    valid_anchor_files.append(
                        (file_path, anchor_data.get("id"), anchor_data.get("version"))
                    )
                except jsonschema.exceptions.ValidationError as schema_err:
                    prop_path = (
                        ".".join([str(p) for p in schema_err.absolute_path])
                        if schema_err.absolute_path
                        else "root"
                    )
                    error_msg = f"Property '{prop_path}': {schema_err.message}"
                    invalid_anchor_files.append((file_path, error_msg))

            except Exception as e:
                invalid_anchor_files.append(
                    (file_path, f"Critical Validation Error: {e}")
                )

    # Reporting
    print("==================================================")
    print("             UIP-V15 VALIDATION REPORT            ")
    print("==================================================")

    if valid_anchor_files:
        print(
            f"\n[PASS] Validated {len(valid_anchor_files)} Sovereign Artifact Anchors:"
        )
        for path, aid, aver in sorted(valid_anchor_files):
            print(f"  - {os.path.basename(path)} | ID: {aid} | Ver: {aver}")

    if missing_anchor_files:
        print(
            f"\n[CRITICAL] Missing 'artifact_anchor' block ({len(missing_anchor_files)} files):"
        )
        for mf in sorted(missing_anchor_files):
            print(f"  - {mf}")

    if invalid_anchor_files:
        print(
            f"\n[FAIL] Malformed 'artifact_anchor' block ({len(invalid_anchor_files)} files):"
        )
        for inv_f, error in sorted(invalid_anchor_files):
            print(f"  - {inv_f}")
            print(f"    Issue: {error}")

    total_issues = len(missing_anchor_files) + len(invalid_anchor_files)
    if total_issues == 0:
        print(
            "\nALL CLEAR: All active artifacts adhere perfectly to the UIP-V15 Sovereign YAML Schema."
        )
        return True
    else:
        print(f"\nVALIDATION FAILED: {total_issues} issues identified.")
        return False


if __name__ == "__main__":
    # Check for target directory argument and optional --strict flag
    target_dir = os.getcwd()
    strict_mode = False

    args = sys.argv[1:]
    if "--strict" in args:
        strict_mode = True
        args.remove("--strict")

    if args:
        target_dir = args[0]

    is_valid = validate_uam_anchors(target_dir, require_all=strict_mode)
    sys.exit(0 if is_valid else 1)
