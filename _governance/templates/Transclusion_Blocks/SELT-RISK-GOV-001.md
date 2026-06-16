---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `SELT-RISK-GOV-001` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

### **Block {{ block_index|default('2') }}. The Risk Governance Block (RISK-GOV-BLOCK)**

This block provides the **Quantifiable Locus of Risk (QLOR)** signature, determining the _source_ and _severity_ of
system flaws.

| DTS Element | Metric/Field | Source | Purpose |
| :---------- | :----------- | :----- | :------ |

[ARTIFACT START] | **Risk Priority** | **RPN (Risk Priority Number)** | FMEA | The scalar value (S x O x D) for quick
triage and prioritization. | | **QLOR Signature** | **$\text{L}_{\text{Internal}}$ Score** | FMEA/UMB | Risk attributed
to **PPL Code/Config** (Your direct fix responsibility). | | **QLOR Signature** | **$\text{L}_{\text{External}}$ Score**
| Ecomap/DSL Map | Risk attributed to **External Dependencies** (Requires governance/fail-safes). | | **Governing
Policy** | **Salient Drift Index** | DSL Map | Prioritizes monitoring based on external vendor **Power/Urgency**. |

---

[ARTIFACT END]
