"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-DEBUG-REGEX-001`                | The Sovereign ID. |
| **Official Name** | `debug_regex.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import re

line = "| **Artifact ID** | `GVRN.RD.001` |"
line2 = "| **Artifact ID** | GVRN.RD.001 |"
lines = [line, line2]

id_pattern = r"(\|\s*\**Artifact ID\**\s*\|\s*`?)([^`|\n]+)(`?\s*\|)"

for l in lines:
    print(f"Testing line: '{l}'")
    match = re.search(id_pattern, l)
    if match:
        print("MATCH FOUND!")
        print(f"Group 1: '{match.group(1)}'")
        print(f"Group 2: '{match.group(2)}'")
        print(f"Group 3: '{match.group(3)}'")

        expected_id = "NEW_ID"
        new_line = re.sub(id_pattern, f"\\1{expected_id}\\3", l)
        print(f"Replaced: '{new_line}'")
    else:
        print("NO MATCH")
    print("-" * 20)
