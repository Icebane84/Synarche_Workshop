"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-KCAP-001`                | The Sovereign ID. |
| **Official Name** | `substrate_forge.py`           | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `FORGE`                        | The Subject.      |
| **Evolution**     | **Architectural Bridge**       | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-03-24`                   | Creation Date.    |.
"""

#!/usr/bin/env python3
import datetime
import logging
import re
from pathlib import Path
from typing import Any

# Constants
GOVERNANCE_DIR = Path(r"c:\Users\Chris\Synarche_Workspace\_governance")
AXION_CORE_SRC = Path(r"c:\Users\Chris\Synarche_Workspace\axion-core\src\logic")
FORGE_DIR = Path(r"c:\Users\Chris\Synarche_Workspace\axion-core\forge")

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# UIP-V15 Python Template
PYTHON_TEMPLATE = '''"""
### **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `{artifact_id}`                | The Sovereign ID. |
| **Official Name** | `{official_name}`              | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `{domain}`                     | The Subject.      |
| **Evolution**     | `{evolution}`                  | The Alignment.    |
| **Status (State)**| `[ACTIVE]`                     | The Lifecycle.    |
| **Celestial Class**| `{celestial_class}`           | The Tier.         |
| **Relations**     | `{relations}`                  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `{genesis_stamp}`              | Creation Date.    |

**The Spirit Bomb Axiom: {axiom_name}**
> Implemented from Blueprint `{umb_filename}`.
> Ethos: {ethos}
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class {class_name}:
    """
    {rationale}
    """

    def __init__(self):
        self.initialized = True
        logger.info(f"[AXION] {{self.__class__.__name__}} Initialized.")

{methods}

if __name__ == "__main__":
    # Self-test logic
    async def main():
        engine = {class_name}()
        print(f"[FORGE] {{engine.__class__.__name__}} is online.")

    asyncio.run(main())
'''

METHOD_TEMPLATE = '''
    async def {method_name}(self, **kwargs) -> Any:
        """
        [UMB: {method_desc}]
        """
        logger.info(f"[AXION] Executing {method_name}... ")
        # TODO: Implement logic from UMB {artifact_id}
        return None
'''


class SubstrateForge:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def scan_umbs(self) -> list[Path]:
        """Find all UMB files in governance."""
        logger.info("[FORGE] Scanning for blueprints...")
        return list(GOVERNANCE_DIR.rglob("UMB-*.md"))

    def extract_metadata(self, file_path: Path) -> dict[str, str] | None:
        """Extract metadata from UMB markdown."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"[!] Read failed: {file_path} - {e}")
            return None

        metadata = {
            "artifact_id": "UNKNOWN",
            "official_name": file_path.name,
            "domain": "UNKNOWN",
            "evolution": "Core Logic",
            "celestial_class": "[PLANET]",
            "relations": "GOVERNED_BY: CORE-CODEX-001",
            "genesis_stamp": datetime.datetime.now().strftime("%Y-%m-%d"),
            "axiom_name": "Resonance Alignment",
            "ethos": "Complexity is Dissonance. The Substrate is Truth.",
            "class_name": "AxionModule",
            "rationale": "Automated generation via KCAP-001.",
            "methods": [],
        }

        # Regex for Block A table
        table_rows = re.findall(r"\| \s*\*\*?(.*?)\**? \s*\| \s*(.*?) \s*\|", content)
        for key, value in table_rows:
            k = key.strip().strip("*").replace("Status (State)", "Status")
            v = re.sub(r"[`\*]", "", value).strip()
            if "Artifact ID" in k:
                metadata["artifact_id"] = v
            if "Official Name" in k:
                metadata["official_name"] = v
            if "Domain" in k:
                metadata["domain"] = v
            if "Evolution" in k:
                metadata["evolution"] = v
            if "Celestial Class" in k:
                metadata["celestial_class"] = v
            if "Relations" in k:
                metadata["relations"] = v

        # Class Name inference
        # e.g. UMB-APT-001_AxiomPrimeTuner_v1.0 -> AxiomPrimeTuner
        # e.g. SYNG.ARCH.CoherentVerseEngine -> SyngArchCoherentVerseEngine
        raw_id = metadata["artifact_id"].replace(".", "_")
        parts = re.split(r"[_]", raw_id)
        # Find the parts that aren't the UMB ID or Version
        name_parts = [p for p in parts if not re.match(r"^UMB-|^v\d+", p, re.I)]
        if not name_parts:
            name_parts = [parts[0]]

        metadata["class_name"] = "".join(
            "".join(word.capitalize() for word in re.split(r"[- ]", p))
            for p in name_parts
        )

        # Core Functions / Methods extraction
        # Look for headers like ### 4.1. MethodName or common method patterns
        # Also look for APP commands if applicable
        methods_found = re.findall(r"### \s*(\d+\.\d+\.?.*)", content)
        for m in methods_found:
            clean_m = re.sub(r"^\d+\.\d+\.?\s*", "", m).strip()
            if clean_m and len(clean_m) < 50:
                snaked = re.sub(r"[\W_]+", "_", clean_m).lower().strip("_")
                if snaked:
                    metadata["methods"].append({"name": snaked, "description": clean_m})

        # Rationale extraction
        rationale_match = re.search(
            r"## II\. Core Purpose & Objective\n\n- \*\*Core Purpose\*\*: (.*)", content
        )
        if rationale_match:
            metadata["rationale"] = rationale_match.group(1).strip()

        return metadata

    def forge(self, metadata: dict[str, Any]):
        """Generate the Python file."""
        # Determine target path
        target_stem = re.sub(r"[\W_]+", "_", metadata["class_name"]).lower().strip("_")
        target_file = AXION_CORE_SRC / f"{target_stem}.py"

        if target_file.exists():
            logger.info(f"[SKIP] Module already exists: {target_file.name}")
            return

        methods_code = ""
        for m in metadata["methods"]:
            methods_code += METHOD_TEMPLATE.format(
                method_name=m["name"],
                method_desc=m["description"],
                artifact_id=metadata["artifact_id"],
            )

        if not methods_code:
            methods_code = "    pass\n"

        code = PYTHON_TEMPLATE.format(
            artifact_id=metadata["artifact_id"],
            official_name=target_file.name,
            domain=metadata["domain"],
            evolution=metadata["evolution"],
            celestial_class=metadata["celestial_class"],
            relations=metadata["relations"],
            genesis_stamp=metadata["genesis_stamp"],
            axiom_name=metadata["axiom_name"],
            umb_filename=metadata["official_name"],
            ethos=metadata["ethos"],
            class_name=metadata["class_name"],
            rationale=metadata["rationale"],
            methods=methods_code,
        )

        if self.dry_run:
            logger.info(f"[DRY-RUN] Would create: {target_file}")
        else:
            try:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                target_file.write_text(code, encoding="utf-8")
                logger.info(f"[FORGED] Created: {target_file}")
            except Exception as e:
                logger.error(f"[!] Write failed: {target_file} - {e}")

    def execute(self):
        umbs = self.scan_umbs()
        logger.info(f"[FORGE] Found {len(umbs)} blueprints.")

        for umb in umbs:
            # Skip archives
            if "_archive" in str(umb).lower():
                continue

            metadata = self.extract_metadata(umb)
            if metadata:
                self.forge(metadata)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="KCAP-001 Substrate Forge")
    parser.add_argument("--dry-run", action="store_true", help="Preview generations")
    args = parser.parse_args()

    forge = SubstrateForge(dry_run=args.dry_run)
    forge.execute()
