import os

src_path = r"c:\Users\Chris\Synarche_Workspace\incoming\Registry of Origin .md"
dest_path = r"c:\Users\Chris\Synarche_Workspace\_governance\10_Governance\GVRN.Registry.Origins.md"

header = """\"\"\"
artifact_anchor:
  id: GVRN.Registry.Origins
  version: v15.0 [OMEGA]
  provenance: '2026-05-28'
  domain: GVRN
  celestial_class: PLANET
  tier: GOVERNANCE
  state: CANONIZED
  ethos: SOVEREIGN_GOVERNANCE_LEDGER
  relations: []
\"\"\"

\"\"\"### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                                | Description       |
| :------------------ | :----------------------------------- | :---------------- |
| **Artifact ID**     | `GVRN.Registry.Origins`              | The Sovereign ID. |
| **Official Name**   | `GVRN.Registry.Origins.md`           | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**                    | The Standard.     |
| **Domain**          | `GVRN`                               | The Subject.      |
| **Celestial Class** | `[PLANET]`                           | The Weight.       |
| **Evolution**       | `Operational`                        | The Maturity.     |
| **Status**          | `[CANONIZED]`                        | The Lifecycle.    |
| **Relations**       | `GOVERNED_BY: CORE.Codex.Phoenix`    | The Network.      |

**The Origins Axiom: Origin Mapping (Law 1)**
> Ethos: The Registry of Origin maps convergence and lineage across the workspace.
\"\"\"

"""

footer = """

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: GVRN.Registry.Origins VER: v15.0 [OMEGA] DOMAIN: GVRN STATUS: [CANONIZED] TS: 2026-05-28 HASH: REGISTRY-ORIGINS-V15`
"""

if not os.path.exists(src_path):
    print(f"Error: source file not found at {src_path}")
else:
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = header + content + footer

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Relocation completed successfully!")
