import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import jsonschema
import yaml

# --- Constants representing the core architectural definitions ---

# This JSON Schema is extracted directly from Section 28.0 of your
# SYSTEMIC ONTOLOGY-Phoenix_Synarche_Framework.md document.
ARTIFACT_JSON_SCHEMA = {
	"$schema": "http://json-schema.org/draft-07/schema#",
	"title": "Phoenix_Sovereign_Artifact",
	"type": "object",
	"required": ["UIP_Block_A", "Synergy_Block_D"],
	"properties": {
		"UIP_Block_A": {
			"type": "object",
			"properties": {
				"Artifact_ID": {"type": "string", "pattern": r"^[A-Z]+\.[A-Za-z0-9]+\.[A-Za-z0-9_]+$"},
				"Version": {"type": "string"},
				"Domain": {"type": "string"},
				"Status": {"type": "string", "enum": ["[ACTIVE]", "[CANONIZED]", "[ARCHIVED]", "[DEPRECATED]"]},
			},
			"required": ["Artifact_ID", "Domain", "Status"]
		},
		"State_Vector_Block_B": {
			"type": "object",
			"properties": {
				"Coherence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
				"Resonance": {"type": "number", "minimum": 0.0, "maximum": 1.0},
				"Stability": {"type": "string"}
			}
		},
		"Synergy_Block_D": {
			"type": "array",
			"items": {
				"type": "object",
				"properties": {
					"Target_ID": {"type": "string"},
					"Relation_Type": {"type": "string", "enum": ["GOVERNS", "IMPLEMENTS", "TRIGGERS", "SYNERGY", "EXTENDS", "REFERENCES", "IS_A_COMPONENT_OF", "UPGRADES", "IS_GOVERNED_BY", "MONITORS", "REMEDIATES", "ENABLES", "CONSUMES_DATA_FROM", "FEEDS_DATA_TO", "ENHANCES", "RESOLVES_DISSONANCE_OF", "RESONATES_WITH", "BIRTHED_BY"]},
					"Impact": {"type": "string"}
				},
				"required": ["Target_ID", "Relation_Type"]
			}
		}
	}
}

# This data structure is a programmatic representation of your
# core_codex_phoenix_governance_model.md document.
# In a real system, this would be loaded from a config file or database.
GOVERNANCE_MODEL = {
	"LAW_006": {"type": "Constraint", "scope": "Runtime", "description": "RAG strict grounding"},
	"LAW_007": {"type": "Constraint", "scope": "Lifecycle", "description": "Strict schema validation (pre-commit lint)"},
	"LAW_015": {"type": "Constraint", "scope": "Lifecycle", "description": "Policy-as-Code (OPA/.rego)"},
	"LAW_017": {"type": "Constraint", "scope": "Architecture", "description": "DB normalization + FK constraints"},
	"LAW_028": {"type": "Constraint", "scope": "Organization", "description": "AI changes as proposals"},
	"LAW_004": {"type": "Guardrail", "scope": "Lifecycle", "description": "Graph DB topology / CI link-check hook"},
	"LAW_014": {"type": "Guardrail", "scope": "Architecture", "description": "API versioning / AOP lifecycle hooks"},
	"LAW_018": {"type": "Guardrail", "scope": "Architecture", "description": "DDD / Ubiquitous Language"},
	"LAW_022": {"type": "Guardrail", "scope": "Lifecycle", "description": "2PC state-machine promotion (dual sign-off)"},
	"LAW_026": {"type": "Guardrail", "scope": "Lifecycle", "description": "Fuzz testing / property-based testing"},
	# Add all other laws here...
}

class ArtifactValidator:
	"""
	A validator that checks a new artifact against the Phoenix Ontology and Governance Model.
	"""

	def __init__(self, governance_model: Dict, schema: Dict):
		self.governance_model = governance_model
		self.schema = schema
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
			if rule and rule["type"] == "Constraint":
				self._add_error(
					f"Governance validation failed for '{file_name}': "
					f"Potential violation of {rule['description']} (Law 006). "
					"Factual claims detected without a 'source:' citation."
				)

		# Example Governance Check: Law 018 (Synergistic Writing)
		# Checks if the artifact's name follows the RNC.
		artifact_id = metadata.get("UIP_Block_A", {}).get("Artifact_ID", "")
		if not re.match(r"^[A-Z]{3,4}\..+\..+$", artifact_id):
			 rule = self.governance_model.get("LAW_018") # Assuming Law 18 relates to naming
			 if rule and rule["type"] == "Guardrail":
				self._add_warning(
					f"Governance validation for '{file_name}': "
					f"Artifact_ID '{artifact_id}' may not fully comply with RNC (Law 002/018)."
				)


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

		print("\n--- Validation Summary ---")
		if self.errors:
			print(f"\n🔴 Validation FAILED with {len(self.errors)} error(s):")
			for error in self.errors:
				print(error)

		if self.warnings:
			print(f"\n🟡 Validation PASSED with {len(self.warnings)} warning(s):")
			for warning in self.warnings:
				print(warning)

		if not self.errors and not self.warnings:
			print("\n🟢 Validation PASSED. Artifact is compliant.")

		print("-" * 26)
		return not self.errors


def main():
	"""Main function to run the validator from the command line."""
	parser = argparse.ArgumentParser(
		description="Phoenix Artifact Validator: Checks artifacts against Ontology and Governance models."
	)
	parser.add_argument(
		"artifact_path",
		type=str,
		help="The path to the artifact markdown file to validate."
	)
	args = parser.parse_args()

	artifact_file = Path(args.artifact_path)

	validator = ArtifactValidator(
		governance_model=GOVERNANCE_MODEL,
		schema=ARTIFACT_JSON_SCHEMA
	)

	is_valid = validator.validate(artifact_file)

	if not is_valid:
		exit(1)
	else:
		exit(0)


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
