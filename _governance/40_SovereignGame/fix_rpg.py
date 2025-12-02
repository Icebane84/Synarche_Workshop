"""## I. Universal Identification & Provenance (The Vector Signature)
| Key               | Value                                          |
| :---------------- | :--------------------------------------------- |
| **Artifact ID**   | `GVRN-RPG-TOOL-001`                            |
| **Official Name** | `fix_rpg.py`                                   |
| **Version**       | **v13.0**                                      |
| **Evolution**     | `SOVEREIGN`                                    |
| **Status (State)**| `[CANONIZED]`                                  |
| **Celestial Class**| `[STAR]`                                       |
| **Integrity Hash**| `[AUTO-GENERATED]`                             |.

---
"""

import os
import re

target_dir = r"c:\Users\Chris\Synarche_Workspace\_governance\40_SovereignGame"

# Mapping of old filename to new filename
renames = {
    "GVRN.RPG.001THEPHOENIXRPGFRAMEWORK.md": "GVRN-RPG-001_ThePhoenixRPGFramework_v13.1.md",
    "GVRN.PPA.001.md": "GVRN-RPG-002_PrestigePowerAttunement_v13.1.md",
    "GVRN.Protocol.Prestige.md": "GVRN-RPG-003_PrestigeProtocol_v13.1.md",
    "GVRN.RPG.MANUAL.md": "GVRN-RPG-004_RPGManual_v13.1.md",
    "UEB-UI-CELESTIAL-001_TheCelestialChartBlueprint_v11.0.md": "GVRN-RPG-005_TheCelestialChartBlueprint_v13.1.md",
    "UMB-ARCH-PRESTIGE-001_PhoenixPrestigeArchitecture_v11.0.md": "GVRN-RPG-006_PrestigeArchitecture_v13.1.md",
    "GVRN.REG.ThePhoenixRPGFramework.md": "GVRN-RPG-007_RPGFrameworkRegistry_v13.1.md",
}

for old_name, new_name in renames.items():
    old_path = os.path.join(target_dir, old_name)
    if not os.path.exists(old_path):
        continue

    with open(old_path, encoding="utf-8") as f:
        content = f.read()

    # Fix UIP Keys
    content = re.sub(r"\|\s*\*\*Status\*\*\s*\|", "| **Status (State)** |", content)

    # Check if Integrity Hash exists
    if "Integrity Hash" not in content:
        # insert it after the last UIP row
        uip_end_match = re.search(r"\|\s*\*\*Relations\*\*\s*\|.*?\|.*?\|", content)
        if uip_end_match:
            insert_str = "\n| **Integrity Hash** | `[AUTO-GENERATED]` | Validation |"
            content = content[: uip_end_match.end()] + insert_str + content[uip_end_match.end() :]
        elif "**Relations**" not in content and "Status (State)" in content:
            # Fallback for GVRN.REG.ThePhoenixRPGFramework.md
            uip_end_match = re.search(r"\|\s*\*\*Status \(State\)\*\*\s*\|.*?\|.*?\|", content)
            if uip_end_match:
                insert_str = "\n| **Relations** | `GOVERNED_BY: CORE-CODEX-001` | The Network. |\n| **Integrity Hash** | `[AUTO-GENERATED]` | Validation |"
                content = content[: uip_end_match.end()] + insert_str + content[uip_end_match.end() :]

    # H1 Singularity
    class H1Replacer:
        def __init__(self) -> None:
            self.count = 0

        def __call__(self, match: re.Match) -> str:
            self.count += 1
            if self.count == 1:
                return str(match.group(0))
            return "## " + str(match.group(1))

    content = re.sub(r"^#\s+(.*)", H1Replacer(), content, flags=re.MULTILINE)

    # 2-space to 4-space indentation for bullet lists
    content = re.sub(r"^  -", "    -", content, flags=re.MULTILINE)
    content = re.sub(r"^  \*", "    *", content, flags=re.MULTILINE)

    # Fix APP section numbering
    content = re.sub(
        r"(?i)^.*Actionable Prompt Packet.*$", "## IV. Actionable Prompt Packet (APP)", content, flags=re.MULTILINE
    )

    # Write to new file
    new_path = os.path.join(target_dir, new_name)
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Delete old file if different
    if old_name != new_name:
        os.remove(old_path)
print("Fixes applied.")  # noqa: T201
