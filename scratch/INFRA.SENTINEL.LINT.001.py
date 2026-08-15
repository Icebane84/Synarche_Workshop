"""
artifact_anchor:
  id: "INFRA.SENTINEL.LINT.001"
  version: "v15.0 [OMEGA]"
  provenance: "2026-05-19"
  domain: "INFRA"
  celestial_class: "PLANET"
  tier: "COMPUTE"
  state: "ACTIVE"
  ethos: "ENFORCING_DETERMINISTIC_GOVERNANCE_VIA_STATIC_ANALYSIS"
  relations:
    - type: "IMPLEMENTS"
      node: "GVRN.Core.StarChart.PATH"
"""

import os
import yaml
import json
from pathlib import Path
from jsonschema import validate, ValidationError

# --- CONFIGURATION ---
SCHEMA_DEFINITION = {
    "type": "object",
    "required": ["id", "version", "domain", "state", "ethos"],
    "properties": {
        "id": {"type": "string", "pattern": r"^[A-Z]{3,4}\.[A-Z0-9_-]{3,30}\.[0-9]{3}$"},
        "domain": {"type": "string", "enum": ["CORE", "FABRIC", "INFRA", "GVRN", "TEST", "LORE", "COMPUTE"]},
        "state": {"type": "string", "enum": ["PROPOSED", "DRAFT", "ACTIVE", "CANONIZED"]},
        "version": {"type": "string"}
    }
}

class PhoenixSentinel:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.stats = {"scanned": 0, "valid": 0, "dissonant": 0}

    def extract_anchor(self, content):
        """Extracts YAML from MD tables, Python docstrings, or JS comments."""
        # Strategy: Look for the 'artifact_anchor:' marker
        if "artifact_anchor:" in content:
            try:
                # Basic extraction logic for YAML blocks
                yaml_part = content.split("artifact_anchor:")[1].split("*/")[0].split('"""')[0]
                return yaml.safe_load("artifact_anchor:" + yaml_part)["artifact_anchor"]
            except Exception:
                return None
        return None

    def audit(self):
        print(f"--- PHOENIX SENTINEL AUDIT: {self.root_dir} ---")
        for path in self.root_dir.rglob("*"):
            if path.suffix in [".md", ".py", ".js", ".ts"] and "node_modules" not in str(path):
                self.stats["scanned"] += 1
                content = path.read_text(errors="ignore")
                anchor = self.extract_anchor(content)

                if not anchor:
                    print(f"[DISSONANT] Missing Anchor: {path}")
                    self.stats["dissonant"] += 1
                    continue

                try:
                    validate(instance=anchor, schema=SCHEMA_DEFINITION)
                    self.stats["valid"] += 1
                except ValidationError as e:
                    print(f"[DISSONANT] Invalid Metadata in {path}: {e.message}")
                    self.stats["dissonant"] += 1

        self.report()

    def report(self):
        print("\n--- AUDIT SUMMARY ---")
        print(f"Files Scanned: {self.stats['scanned']}")
        print(f"Sovereign (Valid): {self.stats['valid']}")
        print(f"Dissonant (Failed): {self.stats['dissonant']}")
        
        if self.stats["dissonant"] > 0:
            print("\nRESULT: RED (Systemic Entropy Detected)")
            # In CI, we would sys.exit(1) here
        else:
            print("\nRESULT: GREEN (Resonant Coherence Maintained)")

if __name__ == "__main__":
    Sentinel = PhoenixSentinel()
    Sentinel.audit()