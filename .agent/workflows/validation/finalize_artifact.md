---
description: finalize_artifact.md - The Seven Gates of Ingestion (v15.0)
---

// turbo-all

This workflow is the mandatory finalization pathway for all artifacts. No artifact is considered "Canon" until it has passed all Seven Gates.

## 🏁 The Seven Gates Workflow

### 1. Gate 1: Verification (Truth Validation)

1. Verify all factual claims against primary sources or `GVRN.Registry.Master`.
2. Ensure no hallucinated references exist.
3. **Constraint**: Cite at least one primary source or verified context item in the reasoning.

### 2. Gate 2: Formatting (PGPS Compliance)

1. Audit the markdown for structural integrity (h1-h6 hierarchy).
2. Ensure use of standard OMEGA v15.0 UIP blocks.
3. **Constraint**: Document must be under 12,000 characters.

### 3. Gate 3: Naming (RNC Enforcement)

1. Validate filename follows `DOMAIN.Subsystem.Descriptor.md`.
2. **Constraint**: Ensure `Artifact ID` in UIP exactly matches the physical filename.
3. **Constraint**: Every artifact MUST belong to a Subsystem that has a `DOMAIN.Subsystem.Index.md`.

### 4. Gate 4: Indexing (Global Registration)

1. Create/Update entry in `_governance/01_Registries/GVRN.Registry.Master.md`.
2. Verify inclusion in `_governance/10_Governance/GVRN.HUD.Map.md`.

### 5. Gate 5: Linkage (Synergy Requirements)

1. Connect to at least **two** existing synergy nodes using standard relational syntax:
   `Relations | SYNERGIZES_WITH: [ID] | LINKED_TO: [ID]`
2. **Constraint**: Establish bidirectional links where possible.

### 6. Gate 6: Risk & Ethos (Guardian Check)

1. Populate the AGP block with at least one critical **Risk** and a corresponding **Mitigation**.
2. **Constraint**: Cite one Law from `CORE.Codex.Phoenix` that governs this artifact.

### 7. Gate 7: Canonization (The Seal)

1. Apply the terminal anchor:
   `[OMNI-ARTIFACT-ANCHOR] ID: [ID] VER: v15.0 [OMEGA] STATUS: CANONIZED TS: [TIMESTAMP]`
2. Run final `entropy_auditor.py` over the directory.

---

`[WORKFLOW-ID] GVRN.WF.Finalization VER: v15.0 [OMEGA] STATUS: ACTIVE`
