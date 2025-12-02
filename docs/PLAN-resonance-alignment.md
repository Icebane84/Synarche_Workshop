# PLAN: Resonance Alignment (Registry Subsystem)

The goal of this plan is to align the `_governance\01_Registries` subsystem with the Phoenix Codex v15 standard, specifically enforcing the `DOMAIN.Subsystem.Descriptor` naming axiom and standardizing internal metadata to resolve logic drift (e.g., mismatched `REG` vs `Registry` identifiers).

## User Review Required

> [!IMPORTANT]
>
> - **Filename Simplification**: I am proposing to rename `GVRN.Registry.OmniLogSynergisticLinksMatrix.md` to `GVRN.Registry.OSLM.md` for better resonance and systemic clarity.
> - **Substrate Alignment**: I am proposing to rename `GVRN.Registry.Data.OSLM.md` to `GVRN.Registry.DataOSLM.md` to eliminate the multi-dot ambiguity in the Descriptor field.
> - **Metadata Elevation**: All registry artifacts will be elevated to `Version: v15.0 [OMEGA]` and `Status: [CANONIZED]`.
> - **Relations Recursion**: All internal `Relations` blocks (AIP Block A) will be updated to reflect the new `DOMAIN.Subsystem.Descriptor` addresses.

## Proposed Changes

### Governance Registries (`_governance\01_Registries`)

#### [MODIFY] [GVRN.Registry.Master.md](file:///c:/Users/Chris/Synarche_Workspace/_governance/01_Registries/GVRN.Registry.Master.md)

- Update Geode Macro-System table to reflect new filenames (OSLM).
- Update internal Artifact ID and Official Name in Block A.
- Set Status to `[CANONIZED]`.

#### [MODIFY] [GVRN.Registry.ArtifactInventory.md](file:///c:/Users/Chris/Synarche_Workspace/_governance/01_Registries/GVRN.Registry.ArtifactInventory.md)

- Update internal Artifact ID from `GVRN.REG.ArtifactInventory` to `GVRN.Registry.ArtifactInventory`.
- Ensure all internal references to other registries use the `Registry` subsystem prefix.

#### [DELETE] [GVRN.Registry.Data.OSLM.md](file:///c:/Users/Chris/Synarche_Workspace/_governance/01_Registries/GVRN.Registry.Data.OSLM.md)

#### [NEW] [GVRN.Registry.DataOSLM.md](file:///c:/Users/Chris/Synarche_Workspace/_governance/01_Registries/GVRN.Registry.DataOSLM.md)

- Migration of content from the multi-dot version.
- Update internal Artifact ID to `GVRN.Registry.DataOSLM`.

#### [DELETE] [GVRN.Registry.OmniLogSynergisticLinksMatrix.md](file:///c:/Users/Chris/Synarche_Workspace/_governance/01_Registries/GVRN.Registry.OmniLogSynergisticLinksMatrix.md)

#### [NEW] [GVRN.Registry.OSLM.md](file:///c:/Users/Chris/Synarche_Workspace/_governance/01_Registries/GVRN.Registry.OSLM.md)

- Migration of content to the shorthand descriptor.
- Update internal Artifact ID to `GVRN.Registry.OSLM`.

#### [MODIFY] All Other Registries

- Perform a "Registry Sweep" on `Ethos.md`, `Ascension.md`, `KPI.md`, `Entities.md`, `Lexicon.md`, `GenesisSeeds.md`, `PhoenixRosettaStone.md`.
- Ensure `Artifact ID` and `Official Name` are strictly `GVRN.Registry.Descriptor`.
- Set Version to `v15.0 [OMEGA]` and Status to `[CANONIZED]`.
- **Recursive Update**: Map all `Relations` and `Synergy` blocks to use the new `Registry` subsystem prefix instead of `REG`.

## Verification Plan

### Automated Checks

- Run `CMD: AUDIT_LINKS` (simulated via `grep` and link validation) to ensure all cross-references in `Master.md` and `ArtifactInventory.md` are functional.
- Run `CMD: AUDIT_COMPLIANCE` (simulated via file inspection) to verify Block A and Block G anchors match the filenames Exactly.

### Manual Verification

- Verify that the `_governance\01_Registries` directory contains exactly 11 files with the correct `GVRN.Registry.*` naming.
