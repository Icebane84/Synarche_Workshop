"""
# CODE-REF-004: The Omega Reforger (Reforger Module)

# I. Universal Identification & Provenance (The Vector Signature)
| Field | Value |
| :--- | :--- |
| **1. Artifact ID** | `CODE-REF-004` |
| **2. Official Name** | `reforger.py` |
| **3. Version** | **v15.0 [OMEGA]** |
| **4. Provenance** | **Reforged: 2026-04-28** |
| **5. Domain** | `ARCH` |
| **6. Evolution** | **Omega Ascension** |
| **7. Celestial Class** | `[STAR]` |
| **8. Tier** | **Strategic** |
| **9. Status (State)** | `[ACTIVE]` |
| **10. Ethos** | **Total System Coherence** |
| **11. Integrity Hash** | `[UIP-V15-LOCK]` |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, ENFORCES, The Reforger executes the legislative will of the Codex.
GVRN-SYNERGY-001, IMPLEMENTS, The Reforger is the codified arm of the Refinement Protocol.
"""

import datetime
import logging
import os
from pathlib import Path

# Configure Logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("OmegaReforger")

# --- v15.0 OMEGA CONSTANTS ---
UIP_HEADER_TEMPLATE = """# {official_name}
> **Domain**: {domain}
> **Evolution**: {evolution}

# **Genesis Stamp: {date}** **Domain: {domain}** **State: {status}** **Tags:** `UIP-V15, {domain}, Reforged` **Criticality: {criticality}**

---

### **Block A: The Identification Lock (UIP-V15)**

| Key | Value | Description |
| :--- | :--- | :--- |
| **Artifact ID** | `{artifact_id}` | The Sovereign ID. |
| **Official Name** | `{official_name}` | The Filename. |
| **Version** | **v15.0 [OMEGA]** | The Standard. |
| **Provenance** | **Reforged: {date}** | The Birth. |
| **Domain** | `{domain}` | The Subject. |
| **Celestial Class** | `{celestial_class}` | The Weight. |
| **Evolution** | `{evolution}` | The Maturity. |
| **Status** | `{status}` | The Lifecycle. |
| **Ethos** | `{ethos}` | The Soul. |
| **Relations** | `{relations}` | The Network. |
"""

SYNERGY_BLOCK_TEMPLATE = """
---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN-REGISTRY-MASTER, INDEXES, This artifact is indexed in the Master Registry.
"""

DOMAIN_MAP = {
    "governance": "GVRN",
    "protocols": "GVRN",
    "documentation": "ARCH",
    "axion": "ARCH",
    "sentinel": "GVRN",
    "philosophy": "PHIL",
    "code": "CODE",
    "tools": "CODE",
    "modules": "CODE",
    "agents": "ARCH",
}

EVOLUTION_TRACKS = ["Omega Ascension", "Cognitive Ascension", "Purposeful Drive", "Crystalline Coherence"]


class BlockScanner:
    """Validates the existence and integrity of standard blocks."""

    @staticmethod
    def identify_blocks(content: str) -> dict[str, bool]:
        return {
            "A": "Block A: The Identification Lock" in content,
            "B": "Block B: The Ethos Field" in content,
            "C": "Block C: The Cognitive Spine" in content,
            "D": "Block D: Standardized Synergy Block" in content,
            "E": "Block E: The Integrity Gate" in content,
            "F": "Block F: The Omni-Anchor" in content,
        }


class OmegaReforger:
    """
    The v13.1 Omega Reforger.
    Enforces Codex Law across the Synarche System.
    """

    def __init__(self, target_path: str) -> None:
        self.target_path = Path(target_path)
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    def infer_domain(self, file_path: Path) -> str:
        """Infers domain from path."""
        for part in file_path.parts:
            key = part.lower().replace("_", "")
            if key in DOMAIN_MAP:
                return DOMAIN_MAP[key]
        return "GVRN"  # Default fallback

    def generate_artifact_id(self, file_path: Path, domain: str) -> str:
        """Generates a canonical Artifact ID if missing."""
        name = file_path.stem.upper().replace(" ", "-").replace("_", "-")
        return f"{domain}-{name}-001"

    def reforge_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """
        Transmutes a single file to v13.1 Standard.
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            blocks = BlockScanner.identify_blocks(content)

            # 1. Header Injection (Block A)
            if not blocks["A"]:
                logger.info(f"[+] Injecting Block A -> {file_path.name}")
                domain = self.infer_domain(file_path)
                aid = self.generate_artifact_id(file_path, domain)

                header = UIP_HEADER_TEMPLATE.format(
                    artifact_id=aid,
                    official_name=file_path.name,
                    version="v13.1 [OMEGA]",
                    domain=domain,
                    celestial_class="[PLANET]",
                    evolution="Omega Ascension",
                    status="[ACTIVE]",
                    signal="OMEGA",
                    date=self.timestamp,
                    criticality="Operational",
                    relations="GOVERNED_BY: CORE-CODEX-001",
                )

                # Prepend header, removing old YAML or H1 if redundant
                content = header + "\n" + content.lstrip()

            # 2. Synergy Injection (Block D)
            if not blocks["D"]:
                logger.info(f"[+] Injecting Block D -> {file_path.name}")
                content += SYNERGY_BLOCK_TEMPLATE

            if dry_run:
                logger.info(f"[DRY RUN] Would write {len(content)} bytes to {file_path.name}")
                return True

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True

        except Exception:
            logger.exception(f"[!] Failed to reforge {file_path.name}")
            return False

    def execute_scan(self) -> None:
        """Recursively scans and reforges the target directory."""
        logger.info(f"[*] Initiating Omega Reforger Scan on: {self.target_path}")

        count = 0
        for root, _, files in os.walk(self.target_path):
            for file in files:
                if file.endswith(".md") and not file.startswith("CORE-CODEX"):  # Don't touch the Law
                    full_path = Path(root) / file
                    if self.reforge_file(full_path):
                        count += 1

        logger.info(f"[*] Reforge Complete. Transmuted {count} artifacts.")


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    reforger = OmegaReforger(target)
    reforger.execute_scan()
