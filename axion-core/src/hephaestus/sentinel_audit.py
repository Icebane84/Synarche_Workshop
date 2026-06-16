import json
import re
from pathlib import Path
from typing import Any


class SentinelAuditor:
    """
    Enforces the Umbral Sentinel Protocol (AOP-SENTINEL-002) and UIP-V15 rules.
    Acts as the Active Immune System of the Synarche.
    """

    def __init__(self, target_path: str):
        self.target_path = Path(target_path)

    def audit_file(self, file_path: Path) -> dict[str, Any]:
        """Executes the 4-Point Hardening Matrix on a target Markdown file."""
        content = file_path.read_text(encoding="utf-8")
        violations: list[dict[str, str]] = []
        score = 100

        # 3.1. Vector Check (UIP Integrity) - Weight: 30%
        uip_valid = self._check_uip(content, violations)
        if not uip_valid:
            score -= 30

        # 3.2. Structural Geometry (The 4-Space Law) - Weight: 30%
        geometry_valid = self._check_geometry(content, violations)
        if not geometry_valid:
            score -= 30

        # 3.3. Actionable Prompt Packet (APP) - Weight: 20%
        app_valid = self._check_app(content, violations)
        if not app_valid:
            score -= 20

        # 3.4. The Umbral Signature - Weight: 20%
        umbral_valid = self._check_umbral(content, violations)
        if not umbral_valid:
            score -= 20

        return {
            "artifact_id": file_path.name,
            "health_score": max(0, score),
            "status": "PASS" if score == 100 else "NEEDS_REFINEMENT",
            "violations": violations,
            "v2_validation": {
                "uip_valid": uip_valid,
                "geometry_valid": geometry_valid,
                "app_present": app_valid,
                "umbral_signature": umbral_valid,
            },
        }

    def _check_uip(self, content: str, violations: list[dict[str, str]]) -> bool:
        """Validates presence of UIP/YAML Frontmatter with mandatory fields."""
        has_uip = "Artifact ID" in content or "artifact_anchor" in content
        has_version = "Version" in content or "version:" in content
        has_domain = "Domain" in content or "domain:" in content

        if not (has_uip and has_version and has_domain):
            violations.append({"type": "VECTOR", "message": "Missing Artifact ID, Version, or Domain in UIP."})
            return False
        return True

    def _check_geometry(self, content: str, violations: list[dict[str, str]]) -> bool:
        """Validates Markdown structural geometry (e.g., Single H1)."""
        h1_matches = re.findall(r"^#\s+.+$", content, re.MULTILINE)
        if len(h1_matches) != 1:
            violations.append({"type": "GEOMETRY", "message": f"Expected exactly 1 H1 tag. Found {len(h1_matches)}."})
            return False
        return True

    def _check_app(self, content: str, violations: list[dict[str, str]]) -> bool:
        """Validates presence of Actionable Prompt Packet."""
        if "Actionable Prompt Packet" not in content and "APP" not in content:
            violations.append({"type": "OPERATIONAL", "message": "Missing Actionable Prompt Packet (APP)."})
            return False
        return True

    def _check_umbral(self, content: str, violations: list[dict[str, str]]) -> bool:
        """Validates the End Marker (Zero Entropy)."""
        if "[ARTIFACT END]" not in content:
            violations.append({"type": "UMBRAL", "message": "Missing [ARTIFACT END] marker."})
            return False
        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.is_file():
            auditor = SentinelAuditor(str(target.parent))
            result = auditor.audit_file(target)
            print(json.dumps(result, indent=2))
            if result["health_score"] < 100:
                sys.exit(1)
