---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `GVRN.PROMPY.SYMPHONICSYNC` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

# GVRN.PROMPY.SymphonicSync [OMEGA v15.0]

> **Objective**: Maintain cross-language mathematical resonance between TypeScript (Axion Core) and Python (Axion Forge)
> environments. **Ground Truth**:
> [`GVRN.Standards.json`](file:///c:/Users/Chris/Synarche_Workspace/_governance/13_Standardization/GVRN.Standards.json)

---

## 🏛️ THE OPERATIONAL MANDATE

All agents and system processes MUST adhere to the **Symphonic Sync Protocol**. Hardcoding shared constants (Regex,
Enums, Schemas) is a **Sovereignty Violation**.

### 1. The Single Source of Truth

All architectural constants reside in the `GVRN.Standards.json` registry.

- **Path**: `_governance/13_Standardization/GVRN.Standards.json`
- **Contents**: `SOVEREIGN_ID_REGEX`, `Domain`, `ArtifactType`, `SubSystem`, `CelestialClass`.

### 2. Implementation Patterns

#### TypeScript (Axion Core)

- **Method**: Static JSON Import (bundled at build-time).
- **Import Syntax**:

    ```typescript
    import * as standards from '../../../_governance/13_Standardization/GVRN.Standards.json';
    export const SOVEREIGN_ID_REGEX = new RegExp(standards.regex.SOVEREIGN_ID);
    ```

- **Rule**: If constants change, you MUST run the `compile` task to propagate the static changes to the `out/`
  directory.

#### Python (Axion Forge)

- **Method**: Dynamic standard loader.
- **Import Syntax**:

    ```python
    from enums import STANDARDS, SOVEREIGN_ID_REGEX
    # Internally uses load_standards() to ingest the JSON
    ```

- **Rule**: If constants change, the Python layer will pick them up on the next execution (no re-compile needed).

### 3. Change Management Ritual

To modify a shared constant:

1. **Modify the JSON**: Edit `GVRN.Standards.json` in the governance layer.
2. **Sync TypeScript**: Run `npm run compile` (or the `tsc` debug equivalent) in `axion-core`.
3. **Verify Resonance**: Run `verify_dist.js` (TS) and `check_standards.py` (Python) to ensure zero entropy.

---

## 🛡️ SOVEREIGN GUARDRAILS

- **NEVER** modify `schemas.ts` or `enums.py` constants directly without updating the JSON first.
- **ALWAYS** verify that the `SOVEREIGN_ID_REGEX` supports legacy IDs (`PRS-001`) during refactors.
- **ISOMORPHIC LOGGING**: Record all sync adjustments in the `GVRN.Maintenance.Log.md`.

`[PROMPY-ANCHOR] ID: PROMPY.SYMPHONY.SYNC VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-16`
