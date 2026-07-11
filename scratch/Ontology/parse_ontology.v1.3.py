import argparse
import json
import sys
import re
import os
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Tuple, Set, Optional

import jsonschema
import yaml
import orjson
import graphviz


def load_governance_model(ontology_path: Path) -> Dict[str, Any]:
    """Parses the ontology file to extract governance laws."""
    if not ontology_path.exists():
        raise FileNotFoundError(f"Ontology file not found: {ontology_path}")

    content = ontology_path.read_text(encoding="utf-8")
    laws = {}
    # Regex to find LAW_XX and its description
    law_pattern = re.compile(r"`(LAW_\d+)` \*\*(.*?):\*\* (.*)")
    matches = law_pattern.finditer(content)

    for match in matches:
        law_id, _, description = match.groups()
        # NOTE: Type and Scope are not in this file, so we default them.
        # This could be enhanced by parsing the Governance Model file.
        laws[law_id] = {
            "type": "Guardrail", # Defaulting to Guardrail
            "scope": "Lifecycle", # Defaulting to Lifecycle
            "description": description.strip()
        }
    if not laws:
        raise ValueError("Could not parse any laws from the ontology file.")
    return laws

def load_artifact_schema(ontology_path: Path) -> Dict[str, Any]:
    """Parses the ontology file to extract the JSON schema for artifacts."""
    if not ontology_path.exists():
        raise FileNotFoundError(f"Ontology file not found: {ontology_path}")

    content = ontology_path.read_text(encoding="utf-8")
    # Find the JSON schema block within the markdown
    match = re.search(r"## 28.0\[MACHINE_READABLE_SCHEMAS\].*?```json\s*(\{.*?\})\s*```", content, re.DOTALL)
    if not match:
        raise ValueError("Could not find the JSON schema in the ontology file.")

    schema_str = match.group(1)
    # Clean up potential markdown escaping issues in the schema pattern
    schema_str = schema_str.replace(r"\\.", r"\.")
    return json.loads(schema_str)


class ArtifactValidator:
	"""
	A validator that checks a new artifact against the Phoenix Ontology and Governance Model.
	"""

	def __init__(self, governance_model: Dict, schema: Dict, known_artifact_ids: Set[str]):
		self.governance_model = governance_model
		self.schema = schema
		self.known_artifact_ids = known_artifact_ids
		self.errors: List[str] = []
		self.warnings: List[str] = []

	def _add_error(self, message: str):
		self.errors.append(f"[ERROR] {message}")

	def _add_warning(self, message: str):
		self.warnings.append(f"[WARNING] {message}")

	def parse_artifact(self, file_path: Path) -> Tuple[Dict[str, Any], str]:
		"""
		Parses a Markdown file with YAML frontmatter.
		Returns the metadata dictionary and the body content.
		"""
		try:
			content = file_path.read_text(encoding="utf-8")
			# Use regex to find the YAML frontmatter block
			match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
			if not match:
				self._add_error(f"File '{file_path.name}' is missing YAML frontmatter block.")
				return {}, ""

			metadata_str = match.group(1)
			body = content[match.end():]

			# The UIP-V15 standard uses a custom table-like format.
			# We'll parse it line by line instead of using a standard YAML parser.
			metadata = {}
			current_block = None

			lines = metadata_str.strip().split('\n')
			for line in lines:
				line = line.strip()
				if not line or line.startswith('#'):
					continue

				if line.startswith('### Block'):
					block_key_map = {
						'Block A: The Identification Lock (UIP-V15)': 'UIP_Block_A',
						'Block B: State Vector (AGP-001)': 'State_Vector_Block_B',
						'Block C: Risk & Mitigation (AGP-002)': 'Risk_Mitigation_Block_C',
						'Block D: Standardized Synergy Block (The Loom Signature)': 'Synergy_Block_D',
					}
					current_block_name = line.split(':', 1)[0].strip()
					current_block = block_key_map.get(current_block_name)
					if current_block:
						metadata[current_block] = {} if 'Synergy' not in current_block else []
					continue

				if current_block and '|' in line and '---' not in line and 'Key' not in line:
					parts = [p.strip() for p in line.split('|') if p.strip()]
					if len(parts) >= 2:
						key, value = parts[0], parts[1]
						if current_block == 'Synergy_Block_D':
							 # Handle multi-column synergy block
							if len(parts) == 3:
								metadata[current_block].append({
									"Target_ID": key,
									"Relation_Type": value,
									"Impact": parts[2]
								})
						else:
							metadata[current_block][key.replace('**', '')] = value


			return metadata, body
		except Exception as e:
			self._add_error(f"Failed to parse artifact '{file_path.name}': {e}")
			return {}, ""

	def validate_structure(self, metadata: Dict[str, Any], file_name: str):
		"""
		Validates the artifact's metadata against the JSON schema from the Ontology.
		This corresponds to Law 007: Presentation Mandate.
		"""
		try:
			jsonschema.validate(instance=metadata, schema=self.schema)
		except jsonschema.exceptions.ValidationError as e:
			self._add_error(f"Structural validation failed for '{file_name}': {e.message} in {list(e.path)}")
		except Exception as e:
			self._add_error(f"An unexpected error occurred during structural validation of '{file_name}': {e}")

	def validate_governance(self, metadata: Dict[str, Any], body: str, file_name: str):
		"""
		Validates the artifact against the Governance Model's rules.
		This is a simplified check focusing on key constraints.
		"""
		# Example Governance Check: Law 006 (Grounding)
		# If an artifact makes a factual claim, it must be grounded.
		# This is a heuristic check looking for un-cited claims.
		if "claim:" in body.lower() and "source:" not in body.lower():
			rule = self.governance_model.get("LAW_006")
			# Assuming LAW_006 is a Constraint as per original logic
			if rule:
				self._add_error(
					f"Governance validation failed for '{file_name}': "
					f"Potential violation of {rule['description']} (Law 006). "
					"Factual claims detected without a 'source:' citation."
				)

		# Example Governance Check: Law 002 (Naming)
		# Checks if the artifact's name follows the RNC.
		artifact_id = metadata.get("UIP_Block_A", {}).get("Artifact_ID", "")
		if not re.match(r"^[A-Z]+\.[A-Za-z0-9]+\.[A-Za-z0-9_]+$", artifact_id):
			 rule = self.governance_model.get("LAW_02")
			 if rule:
				self._add_warning(
					f"Governance validation for '{file_name}': "
					f"Artifact_ID '{artifact_id}' may not fully comply with RNC (Law 02)."
				)

	def validate_links(self, metadata: Dict[str, Any], file_name: str):
		"""Enforces LAW_004 (HKG Weaving) by checking Synergy Block links."""
		synergy_block = metadata.get("Synergy_Block_D", [])
		for item in synergy_block:
			target_id = item.get("Target_ID")
			if target_id and target_id not in self.known_artifact_ids:
				self._add_error(
					f"Link validation failed for '{file_name}': "
					f"Violation of LAW_004 (HKG Weaving). Target_ID '{target_id}' does not correspond to a known artifact."
				)

	def validate_loom_connectivity(self, metadata: Dict[str, Any], file_name: str, system_graph: Dict[str, Any]):
		"""Enforces LAW_021 (The Loom) by ensuring bidirectional connectivity."""
		artifact_id = metadata.get("UIP_Block_A", {}).get("Artifact_ID")
		if not artifact_id:
			return # Cannot validate if there is no ID

		# Check for at least one outgoing link
		if not metadata.get("Synergy_Block_D"):
			self._add_warning(f"Loom validation for '{file_name}': Artifact has no outgoing links, potentially violating LAW_021.")


	def validate(self, file_path: Path) -> bool:
		"""
		Runs the full validation suite on a given artifact file.
		"""
		print(f"--- Validating Artifact: {file_path.name} ---")
		self.errors = []
		self.warnings = []

		if not file_path.exists():
			self._add_error(f"File not found: {file_path}")
			return False

		metadata, body = self.parse_artifact(file_path)
		if not metadata:
			return False # Parsing failed

		print("1. Running Structural Validation (Ontology Check)...")
		self.validate_structure(metadata, file_path.name)

		print("2. Running Governance Validation (Governance Model Check)...")
		self.validate_governance(metadata, body, file_path.name)

		print("3. Running Link Validation (HKG Weaving Check)...")
		self.validate_links(metadata, file_path.name)

		return not self.errors

	def get_report(self, file_path: Path) -> Dict[str, Any]:
		"""Returns the validation results as a JSON-serializable dictionary."""
		status = "FAILED" if self.errors else "PASSED"

		report = {
			"artifact_path": str(file_path),
			"status": status,
			"errors": self.errors,
			"warnings": self.warnings,
		}
		return report


def build_system_graph(root_dir: Path) -> Tuple[Set[str], Dict[str, List[Dict[str, str]]]]:
    """
    Scans a directory to build a complete map of all artifact IDs and their synergy links.
    """
    ids = set()
    graph = {}
    id_pattern = re.compile(r"^\s*\|\s*\*\*Artifact_ID\*\*\s*\|\s*`?([A-Z]+\.[A-Za-z0-9]+\.[A-Za-z0-9_]+)`?\s*\|", re.MULTILINE)
    synergy_pattern = re.compile(r"\|\s*`?([A-Z]+\.[A-Za-z0-9]+\.[A-Za-z0-9_]+)`?\s*\|\s*`?([A-Z_]+)`?\s*\|", re.MULTILINE)

    for md_file in root_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            id_match = id_pattern.search(content)
            if id_match:
                artifact_id = id_match.group(1)
                ids.add(artifact_id)
                graph[artifact_id] = []

                # Find synergy block to extract edges
                synergy_block_match = re.search(r"### Block D:.*?(-{3,}\s*)$", content, re.MULTILINE | re.DOTALL)
                if synergy_block_match:
                    block_content = synergy_block_match.group(0)
                    for link_match in synergy_pattern.finditer(block_content):
                        target_id, relation_type = link_match.groups()
                        graph[artifact_id].append({"target": target_id, "relation": relation_type})

        except Exception:
            # Ignore files that can't be read or parsed
            continue
    return ids, graph

def generate_graph_visualization(
    system_graph: Dict[str, List[Dict[str, str]]],
    output_path: Path,
    validated_artifact: Optional[str] = None,
    errors: Optional[List[str]] = None
):
    """Creates a visual graph of the repository structure using Graphviz."""
    dot = graphviz.Digraph('PhoenixLoom', comment='The Cognitive Loom of the Synarche', node_attr={'fontname': 'Helvetica'})
    dot.attr(rankdir='LR', size='12,8', splines='true', overlap='false', nodesep='0.6', ranksep='1.2')

    # Define node styles based on artifact type
    shape_map = {
        'UMB': 'box',
        'AOP': 'oval',
        'GUCA': 'parallelogram',
        'SELT': 'note',
        'CSL': 'septagon',
        'GVRN': 'doubleoctagon',
        'CORE': 'tripleoctagon',
        'DEFAULT': 'box'
    }

    error_nodes = {re.search(r"'([^']*)'", e).group(1) for e in (errors or []) if "' does not correspond" in e}

    for node_id in system_graph.keys():
        node_type = node_id.split('.')[0]
        shape = shape_map.get(node_type, shape_map['DEFAULT'])

        color = 'lightblue'
        if node_type == 'GVRN': color = 'lightgreen'
        if node_type == 'CORE': color = 'gold'

        attrs = {
            'shape': shape,
            'style': 'rounded,filled',
            'fillcolor': color
        }

        if node_id == validated_artifact:
            attrs['style'] = 'bold,rounded,filled'
            attrs['color'] = 'blue'
        if node_id in error_nodes:
            attrs['color'] = 'red'
            attrs['style'] = 'bold,rounded,filled'

        dot.node(node_id, **attrs)

    for source_id, links in system_graph.items():
        for link in links:
            dot.edge(source_id, link['target'], label=link['relation'])

    dot.render(output_path, format='png', cleanup=True)
    print(f"✅ Graph visualization saved to {output_path}.png")


async def publish_to_nats(report: Dict[str, Any]):
    """Publishes the validation report to a NATS topic."""
    try:
        from nats.aio.client import Client as NATS
        nc = NATS()
        await nc.connect(servers=["nats://localhost:4222"])
        topic = f"synarche.validation.{report['status'].lower()}"
        await nc.publish(topic, orjson.dumps(report))
        await nc.flush()
        await nc.close()
        print(f"✅ Report published to NATS topic: {topic}")
    except ImportError:
        print("❌ NATS client not installed. Please run `pip install nats-py orjson`.")
    except Exception as e:
        print(f"❌ Failed to publish to NATS: {e}")

def main():
	"""Main function to run the validator from the command line."""
	parser = argparse.ArgumentParser(
		description="Phoenix Artifact Validator: Checks artifacts against Ontology and Governance models."
	)
	parser.add_argument(
		"target_path",
		type=str,
		help="The path to the artifact markdown file to validate."
	)
	parser.add_argument(
		"--ontology",
		type=str,
		default="c:/Users/Chris/Synarche_Workspace/scratch/Ontology/SYSTEMIC ONTOLOGY-Phoenix_Synarche_Framework.md",
		help="Path to the master ontology file."
	)
	parser.add_argument(
		"--graph-output",
		type=str,
		default=None,
		help="Optional path to save a PNG visualization of the repository graph."
	)
	parser.add_argument(
		"--publish-to-nats",
		action="store_true",
		help="Publish the JSON report to a NATS topic instead of printing to stdout."
	)
	args = parser.parse_args()

	target_file = Path(args.target_path)
	ontology_file = Path(args.ontology)

	governance_model = load_governance_model(ontology_file)
	artifact_schema = load_artifact_schema(ontology_file)
	known_ids, system_graph = build_system_graph(target_file.parent) # Scan the directory of the target file

	validator = ArtifactValidator(
		governance_model=governance_model,
		schema=artifact_schema,
		known_artifact_ids=known_ids
	)

	is_valid = validator.validate(target_file)

	# Instead of printing to console, generate a JSON report
	report = validator.get_report(target_file)

	if args.publish_to_nats:
		asyncio.run(publish_to_nats(report))
	else:
		print(json.dumps(report, indent=2))

	if args.graph_output:
		generate_graph_visualization(
			system_graph=system_graph,
			output_path=Path(args.graph_output),
			validated_artifact=validator.parse_artifact(target_file)[0].get("UIP_Block_A", {}).get("Artifact_ID"),
			errors=report['errors']
		)

	if not is_valid:
		sys.exit(1)
	else:
		sys.exit(0)


if __name__ == "__main__":
	# To run this script, save it as `validate_artifact.py` and then execute:
	# python validate_artifact.py path/to/your/artifact.md
	#
	# Example:
	# Create a dummy file `test_artifact.md` with content like:
	#
	# ---
	# ### Block A: The Identification Lock (UIP-V15)
	# | Key | Value |
	# | :--- | :--- |
	# | **Artifact_ID** | GVRN.Test.Example |
	# | **Domain** | GVRN |
	# | **Status** | [ACTIVE] |
	# ### Block D: Standardized Synergy Block (The Loom Signature)
	# | Target_ID | Relation_Type | Impact |
	# | :--- | :--- | :--- |
	# | CORE.Codex.Phoenix | GOVERNS | This artifact is governed by the codex. |
	# ---
	# This is the body. It makes a claim: the sky is blue.
	#
	# Then run: `python validate_artifact.py test_artifact.md`
	main()
