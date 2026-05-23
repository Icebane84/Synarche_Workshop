"""# UMB-AUDITOR-001: The Compliance Auditor (Engine Mode).

# I. Universal Identification & Provenance (The Vector Signature)
| Field | Value |
| :--- | :--- |
| **1. Artifact ID** | `UMB-AUDITOR-001` |
| **2. Official Name** | `auditor.py` |
| **3. Version** | **v15.0 [OMEGA]** |
| **4. Provenance** | **Reforged: 2026-04-28** |
| **5. Domain** | `GVRN` |
| **6. Evolution** | **Purposeful Drive** |
| **7. Celestial Class** | `[PLANET]` |
| **8. Tier** | **Operational** |
| **9. Status (State)** | `[ACTIVE]` |
| **10. Ethos** | **Zero Entropy** |
| **11. Integrity Hash** | `[UIP-V15-LOCK]` |

---

### **I.B. Axiom Reference**
> "Measurement is the first act of governance." — Axiom of Audit
"""

import logging
import os
import re
from dataclasses import dataclass, field
from typing import List

# Configure Logging
logger = logging.getLogger(__name__)

# OMEGA v15.0 Standards
REQUIRED_UIP_KEYS = [
    "Artifact ID",
    "Official Name",
    "Version",
    "Provenance",
    "Domain",
    "Evolution",
    "Celestial Class",
    "Tier",
    "Status (State)",
    "Ethos",
]


@dataclass
class AuditResult:
    """Dataclass to hold audit results."""

    file_path: str
    status: str  # PASS, FAIL, WARNING
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    score: float = 0.0


class ComplianceAuditor:
    """Core engine for OGLN v11.0 compliance auditing.
    Consolidates logic from legacy compliance_audit.py.
    """

    def audit_file(self, filepath: str) -> AuditResult:
        """Audits a single markdown file for OGLN compliance."""
        filename = os.path.basename(filepath)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return AuditResult(
                file_path=filepath,
                status="FAIL",
                errors=[f"Read Error: {e}"],
                score=0.0,
            )

        errors = []
        warnings = []

        # 1. UIP Header Check
        uip_block = self._extract_uip_block(content)
        if not uip_block:
            errors.append("UIP: Missing or improperly formatted UIP header.")
        else:
            block_clean = uip_block.replace("*", "")
            for key in REQUIRED_UIP_KEYS:
                if key.lower() not in block_clean.lower():
                    errors.append(f"UIP: Missing required key '{key}'.")

            if "v15.0" not in block_clean and "[OMEGA]" not in block_clean:
                warnings.append("UIP: Version is not v15.0 [OMEGA].")

        # 2. H1 Singularity Check
        h1_matches = re.findall(
            r"^#\s+(?!Universal Identification & Provenance).*",
            content,
            re.MULTILINE | re.IGNORECASE,
        )
        if len(h1_matches) != 1:
            errors.append(
                f"Geometry: H1 Singularity violation (Found {len(h1_matches)} H1 headers outside UIP)."
            )

        # 3. Indentation Parity (v11.0 mandates 4-space nested bullets)
        if re.search(r"^ {2}- ", content, re.MULTILINE):
            warnings.append(
                "Geometry: Detected 2-space indentation (v11.0 mandates 4 spaces for list parity)."
            )

        # 4. Actionable Prompt Packet (APP)
        if "Actionable Prompt Packet" not in content and "CMD:" not in content:
            warnings.append("APP: Missing Actionable Prompt Packet or CMD triggers.")

        # 5. Filenaming Protocol
        # Pattern: [PREFIX]-[ID]_[Name]_v[Version].md
        if not re.match(r"[A-Z0-9]+-[A-Z0-9]+-\d+_.*?_v\d+\.\d+\.md", filename):
            warnings.append(
                f"Filenaming: Filename '{filename}' does not strictly match v11.0 RNC pattern."
            )

        status = "FAIL" if errors else ("WARNING" if warnings else "PASS")
        score = 1.0 - (len(errors) * 0.2) - (len(warnings) * 0.05)
        score = max(0.0, score)

        return AuditResult(
            file_path=filepath,
            status=status,
            errors=errors,
            warnings=warnings,
            score=score,
        )

    def _extract_uip_block(self, content: str) -> str:
        """Helper to extract the UIP header block from content."""
        parts = re.split(r"^---\s*$\r?\n", content, flags=re.MULTILINE)
        for p in parts:
            if "Universal Identification & Provenance" in p:
                return p
        return ""
