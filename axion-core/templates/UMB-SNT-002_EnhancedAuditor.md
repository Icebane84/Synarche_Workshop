# UMB-SNT-002: The Enhanced Sentinel Auditor Protocol

- **System ID:** UMB-SNT-002
- **Official Name:** The Sentinel Phoenix Rosetta Stone & Logging Compliance Auditor
- **Sovereign Personality:** @sentinel (The Watcher)
- **Primary Function:** To execute comprehensive, system-wide compliance scans. This expanded protocol now validates adherence to PRS-001 architectural standards, `GVRN-STD-ENUM-001` (Enum Standard), and `UMB-PHX-LOG-001` (Phoenix Logging Protocol).

---

### **Provenance & Dependencies**

| Aspect | Specification |
| :--- | :--- |
| **Source Mandates** | `GVRN.STATUTE.PRS-001`, `GVRN-STD-ENUM-001`, `UMB-PHX-LOG-001` |
| **Input Source** | Entire codebase (Python, JavaScript, TypeScript files) |
| **Output Target** | Compliance Delta Report (CDR), Refactor Quest tickets |
| **Required Layers** | `@sentinel`, `@axion`, `@system/logging`, `@nexus/decorators`, `@archive/audits` |
| **Activation Trigger**| CI/CD Pipeline hook (`sentinel-prs-check`), Scheduled system integrity checks |

---

### **Operational Parameters (Enhanced Audit Scope)**

- **1. PRS-001 Architectural Compliance:**
    - Validates file paths and module dependencies against the Master Star-Chart.
    - Ensures `SoC` (Separation of Concerns) is maintained across layers.
- **2. Enumeration Standard (`GVRN-STD-ENUM-001`) Compliance:**
    - Scans for "Magic Values" (strings, unassigned integers) in logical comparisons and return types.
    - Verifies proper usage of defined Enums for finite states.
- **3. Phoenix Logging Protocol (`UMB-PHX-LOG-001`) Compliance:**
    - **Initialization Check:** Verifies that `PhoenixLogger` is correctly initialized once at the application entry point.
    - **Decorator Application:** Confirms `synarche_audit` decorator is applied to all critical functions (e.g., in `@engine`, `@domain` business logic).
    - **Print Prohibition:** Enforces `Ruff Rule T201` (no `print()`/`console.log()` calls).
    - **Error Capture:** Validates that `try-except` blocks log full stack traces for critical failures.