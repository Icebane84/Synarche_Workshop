import re
from pathlib import Path

target = Path("c:/Users/Chris/Synarche_Workspace/_governance/10_Governance/GVRN.Taxonomy.Relationships.md")
with open(target, "r", encoding="utf-8") as f:
    content = f.read()

MANDATORY_V15_SECTIONS = [
    r"## \*\*Block A: The Identification Lock \(UIP-V15\)\*\*",
    r"\|\s*\*\*Version\*\*\s*\|\s*\*\*v15\.0 \[OMEGA\]\*\*",
    r"\[ARTIFACT START\]",
    r"\[ARTIFACT END\]",
    r"### \*\*Block G: The Omni-Anchor",
]

for section in MANDATORY_V15_SECTIONS:
    match = re.search(section, content)
    print(f"Testing {section}: {'PASS' if match else 'FAIL'}")
