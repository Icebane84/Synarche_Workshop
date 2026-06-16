"""
artifact_anchor:
  id: GVRN.VALIDATOR.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: GVRN
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_GOVERNANCE_COMPONENT
  relations: []
"""

# Phase 3 & 4: Validation and Semantic Analysis
# Checks metadata schemas and verifies bidirectional import consistency

import re
import datetime
import ast

try:
    import jsonschema
    from jsonschema import validate, FormatChecker
    from jsonschema.exceptions import ValidationError
except ImportError:
    jsonschema = None  # type: ignore
from .config import UIP_V15_SCHEMA, DOMAIN_PREFIXES, ARTIFACT_REGISTRY


class PythonImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()

    def visit_Import(self, node):
        for name in node.names:
            self.imports.add(name.name.split(".")[0])

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module.split(".")[0])


class ArtifactValidator:
    def scan_python_imports(self, content: str) -> set:
        """Collects all top-level imported module names in a Python file via AST."""
        try:
            tree = ast.parse(content)
            visitor = PythonImportVisitor()
            visitor.visit(tree)
            return visitor.imports
        except Exception:
            return set()

    def run_schema_validation(self, metadata: dict) -> list[str]:
        """Runs standard jsonschema validation against the UIP-V15 schema definition."""
        errors = []
        if jsonschema is None:
            errors.append(
                "Dependency Error: 'jsonschema' library not found. Validation skipped."
            )
            return errors

        try:
            validate(
                instance=metadata, schema=UIP_V15_SCHEMA, format_checker=FormatChecker()
            )
        except ValidationError as err:
            prop = (
                ".".join([str(p) for p in err.absolute_path])
                if err.absolute_path
                else "root"
            )
            errors.append(f"Schema violation in '{prop}': {err.message}")
        return errors

    def run_semantic_drift_analysis(
        self, file_path: str, content: str, relations: list
    ) -> list[str]:
        """Performs static analysis to verify declared dependencies align with code imports."""
        warnings = []
        if not file_path.endswith(".py"):
            return warnings

        actual_imports = self.scan_python_imports(content)
        declared_nodes = {
            rel.get("node", "").lower()
            for rel in relations
            if rel.get("type") == "DEPENDS_ON"
        }

        for imp in actual_imports:
            # Replaces fragile heuristics with declarative registry checks
            if imp in ARTIFACT_REGISTRY:
                registry_item = ARTIFACT_REGISTRY[imp]
                required_target = registry_item["provider_id"]
                if required_target.lower() not in declared_nodes:
                    warnings.append(
                        f"[SEMANTIC DRIFT] Code imports module '{imp}' which maps to logical dependency '{required_target}', "
                        f"but no matching relationship is declared."
                    )
        return warnings

    def propose_auto_corrections(self, metadata: dict) -> tuple[dict, list[str]]:
        """Scans anchor properties and suggests UIP-V15 compliance updates, avoiding silent writes."""
        corrections = []
        fixed = metadata.copy()

        # Domain map corrections
        if "domain" in fixed:
            domain_val = str(fixed["domain"]).upper()
            if domain_val == "TOOL":
                fixed["domain"] = "INFRA"
                corrections.append("Propose: Convert domain 'TOOL' to 'INFRA'")
            elif domain_val not in UIP_V15_SCHEMA["properties"]["domain"]["enum"]:
                fixed["domain"] = "CORE"
                corrections.append(
                    f"Propose: Reset non-standard domain '{domain_val}' to 'CORE'"
                )

        # Tier map corrections
        if "tier" in fixed:
            tier_val = str(fixed["tier"]).upper()
            if tier_val == "AXIOMATIC":
                fixed["tier"] = "COMPUTE"
                corrections.append("Propose: Convert tier 'AXIOMATIC' to 'COMPUTE'")
            elif tier_val not in UIP_V15_SCHEMA["properties"]["tier"]["enum"]:
                fixed["tier"] = "LOGIC"
                corrections.append(
                    f"Propose: Reset non-standard tier '{tier_val}' to 'LOGIC'"
                )

        # ID Alignment Check
        if "id" in fixed:
            id_val = str(fixed["id"])
            pattern = UIP_V15_SCHEMA["properties"]["id"]["pattern"]
            if not re.match(pattern, id_val):
                domain_val = fixed.get("domain", "CORE")
                prefix = DOMAIN_PREFIXES.get(domain_val, "CORE")
                clean_id = re.sub(r"[^A-Za-z0-9._-]", "_", id_val).upper()
                clean_id = re.sub(r"__+", "_", clean_id).strip("_.")
                parts = [p for p in clean_id.split(".") if p]
                mid = "_".join(parts[1:-1]) if len(parts) > 2 else clean_id
                mid = mid[:30].strip("_.")
                fixed["id"] = f"{prefix}.{mid}.001"
                corrections.append(
                    f"Propose: Align non-compliant ID '{id_val}' to '{fixed['id']}'"
                )

        # Version check
        if "version" in fixed:
            ver_val = str(fixed["version"])
            pattern = UIP_V15_SCHEMA["properties"]["version"]["pattern"]
            if not re.match(pattern, ver_val):
                fixed["version"] = "v15.0 [OMEGA]"
                corrections.append(
                    f"Propose: Update non-standard version '{ver_val}' to 'v15.0 [OMEGA]'"
                )

        # Celestial Class
        if (
            fixed.get("celestial_class")
            not in UIP_V15_SCHEMA["properties"]["celestial_class"]["enum"]
        ):
            fixed["celestial_class"] = "STAR"
            corrections.append("Propose: Default celestial_class to 'STAR'")

        # State
        if fixed.get("state") not in UIP_V15_SCHEMA["properties"]["state"]["enum"]:
            fixed["state"] = "ACTIVE"
            corrections.append("Propose: Default state to 'ACTIVE'")

        # Date Provenance check
        if "provenance" not in fixed or not isinstance(
            fixed["provenance"], (str, datetime.date)
        ):
            fixed["provenance"] = datetime.date.today().isoformat()
            corrections.append("Propose: Injected missing date provenance")
        elif isinstance(fixed["provenance"], datetime.date):
            fixed["provenance"] = fixed["provenance"].isoformat()

        # Remove illegal additional properties
        allowed_keys = set(UIP_V15_SCHEMA["properties"].keys())
        extra_keys = set(fixed.keys()) - allowed_keys
        for ek in extra_keys:
            del fixed[ek]
            corrections.append(f"Propose: Prune illegal additional property '{ek}'")

        # Relations type correction
        if "relations" in fixed and isinstance(fixed["relations"], list):
            valid_relations = []
            allowed_rel_types = UIP_V15_SCHEMA["properties"]["relations"]["items"][
                "properties"
            ]["type"]["enum"]
            for rel in fixed["relations"]:
                if isinstance(rel, dict) and "type" in rel and "node" in rel:
                    rel_type = str(rel["type"]).upper()
                    if rel_type in ("USES", "UTILIZES"):
                        rel["type"] = "DEPENDS_ON"
                        corrections.append(
                            f"Propose: Map relation type '{rel_type}' -> 'DEPENDS_ON'"
                        )
                    elif rel_type in ("SYNERGIZES_WITH", "BROADCASTS_TO"):
                        rel["type"] = "SYNERGIZES"
                        corrections.append(
                            f"Propose: Map relation type '{rel_type}' -> 'SYNERGIZES'"
                        )
                    elif rel_type == "GOVERNED_BY":
                        rel["type"] = "DEPENDS_ON"
                        corrections.append("Propose: Map 'GOVERNED_BY' -> 'DEPENDS_ON'")

                    if rel["type"] in allowed_rel_types:
                        valid_relations.append(rel)
                    else:
                        corrections.append(
                            f"Propose: Drop non-standard relation type '{rel_type}'"
                        )
            fixed["relations"] = valid_relations

        return fixed, corrections
