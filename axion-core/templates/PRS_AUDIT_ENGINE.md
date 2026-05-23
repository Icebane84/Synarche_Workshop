# UMB-PRS-001.SNT: The Sentinel PRS Audit Engine

- **System ID:** UMB-PRS-001.SNT
- **Official Name:** The Sentinel Phoenix Rosetta Stone Audit Engine
- **Sovereign Personality:** @sentinel (The Watcher)
- **Primary Function:** To execute automated, system-wide compliance scans against the PRS-001 architectural standard.

---

### **Provenance & Dependencies**

| Aspect                 | Specification                                                |
| :--------------------- | :----------------------------------------------------------- |
| **Source Statute**     | `GVRN.STATUTE.PRS-001`                                       |
| **Input Source**       | The Master Star-Chart (`tsconfig.json`)                      |
| **Output Target**      | `@archive/audits/`                                           |
| **Required Layers**    | `@sentinel`, `@atlas`, `@archive`                            |
| **Activation Trigger** | CI/CD Pipeline hook (`sentinel-prs-check`), Manual Directive |

---

### **Operational Parameters**

- **Mode 1 (Passive):** Executes on every pull request. Returns a binary pass/fail state.
- **Mode 2 (Active):** Executes on direct command. Generates a full Compliance Delta Report (CDR) detailing all violations.
