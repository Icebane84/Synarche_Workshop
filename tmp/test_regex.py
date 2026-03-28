import re
content = """# GVRN.Taxonomy.Relationships.md

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                                                           | Description       |
| :---------------- | :-------------------------------------------------------------- | :---------------- |
| **Artifact ID**   | `GVRN.Taxonomy.Relationships`                                   | The Sovereign ID. |
| **Official Name** | `GVRN.Taxonomy.Relationships.md`                                | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**                                               | The Standard.     |
"""
m1 = re.search(r"## \*\*Block A: The Identification Lock \(UIP-V15\)\*\*", content)
m2 = re.search(r"\|\s*\*\*Version\*\*\s*\|\s*\*\*v15\.0 \[OMEGA\]\*\*", content)
print(f"M1: {m1}")
print(f"M2: {m2}")
